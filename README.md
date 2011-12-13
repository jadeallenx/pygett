pyGett
======

About
-----
This library provides a binding to the REST API for the file sharing service [Ge.tt](http://ge.tt). Please see
the [Ge.tt Developer's Documentation](http://ge.tt/developers) for information on how to get an API key.

Installation
------------
To install, use the standard `python setup.py install`

Quick Usage
-----------
The API initializaton requires the following parameters to be present:

- **apikey**: The API key assigned by Ge.tt for your application
- **email**: The email address linked to an API key
- **password**: The password linked to an API key

Example initialization:

    from pygett import Gett

    client = Gett(
            apikey = "apitest",
            email = "apitest@ge.tt",
            password = "secret"
    )

Getting a dict of all shares:

    shares = client.get_shares()
    for file in shares['4ddfds'].files
        print file.filename

Getting a list of all shares:

    shares = client.get_shares_list()
    for share in shares:
        for file in share.files:
            print share.sharename + "\t" + file.filename + "\t" + file.size

Getting a specific share:

    share = client.get_share("4ddfds")

Getting a specific file:

    file = client.get_file("4ddfds", 0)

Uploading a file:

    file = client.upload_file(
            filename = "test.rst",
            data = open("test.rst", "rb").read()
    )

        print "File '%s' is now available at %s" % (file.filename, file.getturl)

Downloading file content:

    file = client.get_file("4ddfds", 0)
    open("myCopy.txt", "wb").write(file.contents())

License
-------
Copyright (C) 2011 by Mark Allen.  You may use this library under the terms and conditions 
of the [MIT license](http://www.opensource.org/licenses/mit-license.php).  See the LICENSE 
file for full information.
