## Documentation ##
# Oordra - Simple file transfer between computers
# Filename: stuur.py
# Author: Harrison H. Jones
# Sends a file and the file's details to a FTP server. A temporary code is generated and used as the remote filename

## Header / Initialization ##
import ftplib, os.path, sys, ConfigParser, random, string, argparse

# Initalization of Variables
sizeWritten = 0.0
totalSize = None
uploadPercentState = 0
config = ConfigParser.ConfigParser()


## Helper Functions ##
# Generates a short 5 character code for the remote filename
def generateCode():
    length = 5
    chars = string.ascii_lowercase + string.digits
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

## Helper Functions ##
# FTP Callback. Displays current progress of FTP file upload
def handle(block):
    global sizeWritten, uploadPercentState
    sizeWritten += 1024 
    percentComplete = sizeWritten / totalSize
    if(uploadPercentState == int(percentComplete*100)):
        uploadPercentState += 10
        print(str(round(sizeWritten / 1024 / 1024 ,1)) + " of " + str(round(totalSize / 1024 / 1024 ,1)) + " uploaded " + str(round((percentComplete)*100)) + "%)")

# Generates a config (*.ini) file containing original file details so they can be "restored" when downloaded
def generateDetailFile(code, localFilename, totalSize):
    detailsFile = open('%s.details.ini' % code,'w+')
    config = ConfigParser.ConfigParser()
    config.add_section('FileInfo')
    config.set('FileInfo','filename', localFilename)
    config.set('FileInfo','fileSize', totalSize)
    config.write(detailsFile)
    detailsFile.close()

# Downloads a local file to the FTP server and saves it as the temporary code. Uses the FTP callback to display progress of the upload
def uploadFile(localFilename,remoteFilename,callback, silent):
    global uploadPercentState
    uploadPercentState = 0
    totalSize = float(os.path.getsize(localFilename))
    #print('Total file size : ' + str(round(totalSize / 1024 / 1024 ,1)) + ' Mb (' + str(totalSize) + ' bytes)')
    # Connect to the server
    ftp = ftplib.FTP(config.get('FTPConfig','ftpHostname'))
    ftp.login(config.get('FTPConfig','ftpUsername'), config.get('FTPConfig','ftpPassword'))
    # Change to the correct directory
    ftp.cwd(config.get('FTPConfig','ftpFolder'))
    # Open the file and upload it
    #print('Uploading file');
    file = open(localFilename,'rb')                  # file to send
    if(silent == True):
        ftp.storbinary('STOR %s' % remoteFilename, file, 1024, None)     # send the file
    else:
        ftp.storbinary('STOR %s' % remoteFilename, file, 1024, callback)     # send the file
    #print('File upload successful')
    # Cleanup
    file.close()
    ftp.quit()

## Program Start ##
# Grab the command line arguments
parser = argparse.ArgumentParser(description='Upload a file & get a temporary download code.');
parser.add_argument('filename',nargs=1,help='the local file to upload')
args = parser.parse_args()
localFilename = args.filename[0]
totalSize = float(os.path.getsize(localFilename))

# Load the config
config.readfp(open('config.ini'))

print 'Sending "' + localFilename + '" to the server'

#print 'Generating temporary code'
remoteCode = generateCode()

#print 'Generating file details file'
generateDetailFile(remoteCode, localFilename, totalSize)

#print 'Uploading file detail file'
uploadFile('%s.details.ini' % remoteCode,'%s.details.ini' % remoteCode,handle,True)
os.remove('%s.details.ini' % remoteCode)

#print 'Uploading specified file'
uploadFile(localFilename,remoteCode,handle,False)

print ''
print 'Done. The temporary download code is ' + remoteCode



