Qualys User List XML to CSV Converter
=========================================

Python script to download and convert the Qualys User List on a subscription to CSV

Usage
==========================================

Use the 'Download as ZIP' link on this page to download this package, and unzip/extract it to a directory of your choice

After the package has been extracted navigate to the directory via cli:

On windows assuming we extracted it to ```c:\Qualys-UserList-To-CSV-Converter```

``` cd c:\Qualys-UserList-To-CSV-Converter ```

then run the following command:

```python /path/to/converter.py --username=qualys-username --password=qualys-password```

If you dont want to put your credentials via the command line just simply run
``` python /path/to/converter.py ``` 
and the script will prompt your for username and password which will not be held in shell history
```
$ python converter.py
Qualys Username: someuser
Qualys Password: somepassword
```

Output
==========================================

The above will output a file named userlist.csv the directory where 'converter.py' is located

Requirements
==========================================

* Python 2.7+

If you are using windows, python 2.7 can be downloaded from this link - please choose 32bit or 64bit download:

``` https://www.python.org/downloads/release/python-2711/ ```
