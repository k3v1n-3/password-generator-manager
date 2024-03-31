# password-generator-manager
Will generate and securely store passwords.

Passwords will not have repeating character types, will be a minimum of 10 characters, with a random addition of 0-5 characters. Takes input for service name (i.e. website) and username, as well as flags -g for "get" to retrieve a stored password, -l for "length" so you can dictate the base length of the password before the random addition of 0-5 characters, and -d for "delete". Stores the encoded passwords. A master password is need for access to the manager, which is hashed to be more secure. 

Currently, it works best when interacted with in a CLI but I am trying to get a webapp or GUI, something where I can use it no matter where or what machine I am on. 
