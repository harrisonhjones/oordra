# Oordra
*Simple file transfer between computers*

## Purpose
Oordra (Afrikaans for "transfer") was created to make the tedious task of file transfer between computers easier and simpler. When you want to transfer a file simply:

* Find the file on the source computer
* *stuur* (Afrikaans for "send") the file and remember the shortcode
* Wait for the file to upload
* Navigate to a folder on the destination computer
* *kry* (Afrikaans for "get") the shortcode 
* Wait for the file to download
* Simple as that!

## Configuration
Edit config.example.ini to refelct your FTP server setup and rename to config.ini

## Usage
### Sending a File
To send files navigate to the file and run the following command 

    stuur.py filename

You will be given a 5 character code. Make note of this code

### Receiving a File
To receive a file navigate to the folder you wish to download the file to and type the following command

    kry.py shortCode

The file will begin downloading.

Use the 5 character code as the shortCode.

Add "-d" to the end of the command to automatically delete the file from the server when the download is complete