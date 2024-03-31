import os
import argparse
from gen_sec_pass import gen_sec_pass
from mstr_pass import verify_master_password, set_master_password
from pass_man import save_credentials, get_credentials, delete_credentials

master_password_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'master_password.json')

def main():
    if not os.path.exists(master_password_file):
        set_master_password()
    else:
        if not verify_master_password():
            print("Access denied. Incorrect master password.")
            return

    parser = argparse.ArgumentParser(description="Manage and generate secure passwords.")
    parser.add_argument('-l', '--length', type=int, help='Set the base length of the password. The generated password will have up to 5 additional characters. Minimum base length is 10.')
    parser.add_argument('-g', '--get', action='store_true', help='Retrieve the username and password for a specified service.')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete the password for a specified service and username.')

    args = parser.parse_args()

    if args.get:
        service = input("Enter the service name: ")
        credentials = get_credentials(service)
        if credentials:
            for user, pwd in credentials.items():
                print(f"Username: {user}, Password: {pwd}")
    elif args.delete:
        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        if delete_credentials(service, username):
            print(f"Deleted entry for {username} @ {service}.")
        else:
            print(f"Failed to delete entry for {username} @ {service}.")
    else:
        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        if args.length and args.length < 10:
            print("The minimum base length is 10. Adjusting to 10.")
            args.length = 10
        password = gen_sec_pass(min_length=args.length) if args.length else gen_sec_pass()
        save_credentials(service, username, password)
        print(f"Generated and saved password: {password} for {username} @ {service}.")

if __name__ == '__main__':
    main()

