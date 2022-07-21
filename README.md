# TransferPassword

The class was created for the secure transmission of information, for example, passwords. It can be integrated into telegram bot, api, web, etc.

<h2> Requirements </h2>

- cryptography

Use command *pip3 install --upgrade cryptography* to install Python package

If pip3 are not installed: sudo apt-install python3-pip

<h2> Example </h2>

<code>

    storage = Storage()
    password = "Password1234"
    public_key, private_key = storage.save(password, 86400)
    original_password = storage.get(public_key, private_key)
    print(original_password)
   
</code>


