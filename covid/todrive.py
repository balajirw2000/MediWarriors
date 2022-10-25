from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# For using listdir()
import os

gauth = GoogleAuth()
drive = GoogleDrive(gauth)
def to_drive(uid):
    print("Current working directory: {0}".format(os.getcwd()))



    print("Current working directory: {0}".format(os.getcwd()))

    upload_file_list = 'media/'+str(uid)+'.pdf'

    gfile = drive.CreateFile({'parents': [{'id': '1bUYo4T_JIj5v4emc8uBpaoZMyK8YmuhF'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(upload_file_list)
    gfile.Upload()