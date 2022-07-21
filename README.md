# TransferPassword

The class was created for the secure transmission of information, for example, passwords. It can be integrated into telegram bot, api, web, etc.

# requirements
- cryptography

Use command *pip3 install --upgrade cryptography* to install Python package

If pip3 are not installed: sudo apt-install python3-pip

Example

<code>

    storage = PasswordStorage()
    password = "Password1234"
    public_key, private_key = storage.save(password, 86400)
    original_password = storage.get(public_key, private_key)
    print(original_password)
   
</code>


