import os
import json
from cryptography.fernet import Fernet
from gen_sec_pass import gen_sec_pass

def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    return open('secret.key', 'rb').read()

if not os.path.exists('secret.key'):
    generate_key()

cipher = Fernet(load_key())

def encrypt_password(password):
    return cipher.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password).decode()

def save_credentials(service, username, password):
    try:
        with open('passwords.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:  
                data = {}
    except FileNotFoundError:
        data = {} 

    encrypted_password = cipher.encrypt(password.encode()).decode()
    if service not in data:
        data[service] = {}
    data[service][username] = encrypted_password

    with open('passwords.json', 'w') as file:
        json.dump(data, file)

def delete_credentials(service, username):
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
        
        if service not in data:
            print(f"The service '{service}' does not exist.")
            return False
        
        if username not in data[service]:
            print(f"No entry found for the username '{username}' in service '{service}'.")
            return False

        del data[service][username]
        
        if not data[service]:
            del data[service]

        with open('passwords.json', 'w') as file:
            json.dump(data, file)
        return True

    except FileNotFoundError:
        print("Error: passwords.json file not found.")
        return False
    except json.JSONDecodeError:
        print("Error: Unable to decode passwords.json file.")
        return False


def get_credentials(service, username=None):
    try:
        with open('passwords.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # The file is empty. Inform the user that no credentials are on record.
                print("No credentials on record.")
                return None
    except FileNotFoundError:
        print("No credentials on record.")
        return None
    
    if username:
        # If a specific username is requested, attempt to retrieve its password.
        try:
            encrypted_password = data[service][username]
            return {username: cipher.decrypt(encrypted_password.encode()).decode()}
        except KeyError:
            # The service or username does not exist in the data.
            print("No credentials on record.")
            return None
    else:
        # If no specific username is provided, return all credentials for the service.
        try:
            return {user: cipher.decrypt(pwd.encode()).decode() for user, pwd in data[service].items()}
        except KeyError:
            # The service does not exist in the data.
            print("No credentials on record.")
            return None


def main():
    operation = input("Select operation:\n1. Save password\n2. Retrieve password\n3. Delete password\n4. Update password\n")
    
    if operation == "1":
        service = input('Enter the service name: ')
        username = input('Enter the username: ')
        password = gen_sec_pass()
        save_credentials(service, username, password)
        print(f'Password for {username}@{service} saved!')
    elif operation == "2":
        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        retrieved_password = get_credentials(service, username)
        if retrieved_password:
            print(f'Retrieved password for {username}@{service}: {retrieved_password}')
        else:
            print(f"No credentials found for {username}@{service}.")
    elif operation == "3":
        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        delete_credentials(service, username)
    else:
        print("Invalid operation. Please select a valid operation.")

if __name__ == '__main__':
    main()