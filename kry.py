## Documentation ##
# Oordra - Simple file transfer between computers
# Filename: kry.py
# Author: Harrison H. Jones
# Grabs files from FTP servers using temporary codes

## Header / Initialization ##
import ftplib, sys, os, ConfigParser, argparse

# Initalization of Variables
localFilename = None
downloadingFile = None
downloadPercentState = 0
totalSize = None
sizeWritten = 0.0
config = ConfigParser.ConfigParser()
details = ConfigParser.ConfigParser()

## Helper Functions ##
# FTP Callback. Displays current progress of FTP file download
def handle(block):
    global sizeWritten, downloadPercentState, downloadingFile
    downloadingFile.write(block);
    sizeWritten += sys.getsizeof(block)
    if(totalSize != None):
        percentComplete = sizeWritten / totalSize
        if(downloadPercentState == int(percentComplete*100)):
            downloadPercentState += 10
            print(str(round((percentComplete)*100)) + "% downloaded (" + str(round(sizeWritten / 1024 / 1024 ,1)) + "Mb of " + str(round(totalSize / 1024 / 1024 ,1)) + "Mb)")

# Downloads a remote file from the FTP server and saves it with a local filename. Uses the FTP callback to display progress of the download and also delets the remote file if desired
def downloadFile(localFilename,remoteFilename,callback,deleteRemote):
    global sizeWritten, downloadingFile, downloadingFile
    # Reset the global sizeWritten variable to 0.0 so sequential calls to download file "start" with the correct size written
    sizeWritten = 0.0
    # Connect to the server
    ftp = ftplib.FTP(config.get('FTPConfig','ftpHostname'))
    ftp.login(config.get('FTPConfig','ftpUsername'), config.get('FTPConfig','ftpPassword'))
    # Change to the correct directory
    ftp.cwd(config.get('FTPConfig','ftpFolder'))
    #print('Connected to server')
    #print('Downloading file');
    downloadingFile = open(localFilename,'wb+')
    try:
        # Retreive the remote binary file and download it
        ftp.retrbinary('RETR %s' % remoteFilename, callback, 262144)
        if(deleteRemote == True):
            ftp.delete(remoteFilename)
    except Exception, e:
        print "FTP error %s" % str(e)
        return False
    else:
        pass
    finally:
        # Clean up by closing the file. If not done it cannot be removed with os.remove()
        downloadingFile.close()
    ftp.quit()
    return True

## Program Start ##
# Grab the command line arguments
parser = argparse.ArgumentParser(description='Download a file using a temporary code.');
parser.add_argument('code',nargs=1,help='a file\'s temporary code')
parser.add_argument('-d', dest='deleteRemote', action='store_const',const=True,default=False,help='Delete the remote file (default: leave the remote file on the server)')
args = parser.parse_args()
remoteCode = args.code[0]

# Load the config
config.readfp(open('config.ini'))

# Download and extract the details file
if(downloadFile('%s.details.ini' % remoteCode,'%s.details.ini' % remoteCode,handle,args.deleteRemote)):

    #print 'Unpacking details file'
    details.readfp(open('%s.details.ini' % remoteCode))
    localFilename = str(details.get('FileInfo','filename'))
    totalSize = float(details.get('FileInfo','filesize'))
    #print 'Local Filename: ' + localFilename
    #print 'Total Filesize: ' + str(totalSize)

    # Download the actual file now
    print 'Downloading "' + localFilename + '"'
    if(downloadFile(localFilename,remoteCode,handle,args.deleteRemote)):
        print ''
        print 'Done'
    else:
        print ''
        print 'Failed to download file' 
else:
    print ''
    print 'Failed to download file details'

os.remove('%s.details.ini' % remoteCode)