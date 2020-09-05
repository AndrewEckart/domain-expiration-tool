## Domain Expiration Tool

This repository contains a Python script which can be used to find the 
expiration dates of domain name registrations.

### Requirements

To use this tool, you will need to have Python 3.7+ installed, as well as a 
whois client. 

On Ubuntu, you can install a whois client via `sudo apt install whois`.

On Windows, you can download a whois client from 
[Windows Sysinternals](https://docs.microsoft.com/en-us/sysinternals/downloads/whois)
and add it to your path.

The [python-dateutil](https://pypi.org/project/python-dateutil/) package is used
to parse dates into a standard format. 
This can be installed via `pip install -r requirements.txt`.


### Usage

To find the expiration dates of one or more domain names, pass them as 
command-line arguments like so:

```bash
$ python3 main.py google.com wikipedia.org
Registration for google.com expires at 2028-09-14 04:00:00.
Registration for wikipedia.org expires at 2023-01-13 00:00:00.
```
