import secrets
import string

def char_type(c):
    """Determines the character type of c."""
    if c in string.ascii_lowercase:
        return 'lowercase'
    elif c in string.ascii_uppercase:
        return 'uppercase'
    elif c in string.digits:
        return 'digit'
    elif c in '!@#$%&*':
        return 'special'
    else:
        return None

def gen_sec_pass(min_length=10):
    length = min_length + secrets.randbelow(6)  # Total password length
    char_sets = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        '!@#$%&*',
    ]
    
    password = [secrets.choice(secrets.choice(char_sets))]  # Start with a random character from a random set
    
    while len(password) < length:
        prev_char = password[-1]
        prev_char_type = char_type(prev_char)
        
        # Filter out the char set of the previous character type
        available_sets = [s for s in char_sets if char_type(secrets.choice(s)) != prev_char_type]
        
        # Randomly select the next character from the available sets
        next_char = secrets.choice(secrets.choice(available_sets))
        
        password.append(next_char)

    # The shuffle is removed to ensure the sequence avoids consecutive characters of the same type
    return ''.join(password)
