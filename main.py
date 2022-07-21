import csv
import os
import smtplib
import ssl
import time
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

gbConversion = 1073741824
mbConversion = 1048576
csvFields = ['File Name', 'Size', 'Modification Time']
csvFiles = ['Data_Log_Movies.csv', 'Data_Log_TV.csv', 'Data_Log_Music.csv']


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def DeleteOldFiles():
    for x in csvFiles:
        if os.path.exists(x):
            os.remove(x)
        else:
            print("The file does not exist")


def SendEmail():
    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")
    subject = "Data Log " + dt
    sender_email = ""
    receiver_email = ""
    password = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    for f in csvFiles:  # add files to the message
        file_path = os.path.join('C:/Users/Server-PC/Desktop/FileLogger/', f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        message.attach(attachment)

    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def SaveToCSV(_Dir, fileName, excludeSubtitles: bool):
    listOfFiles = getListOfFiles(_Dir)

    with open(fileName, 'a+', encoding="utf8", newline='') as csvfile:

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(csvFields)

        for i in listOfFiles:
            fileSizeBase = os.path.getsize(i)
            fileSizeConverted = str(round(os.path.getsize(i) / gbConversion, 2))
            modificationTime = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(os.path.getmtime(i)))
            sizeSuffix = 'GB'

            if int(float(fileSizeConverted)) < 1.0:
                fileSizeConverted = str(round(os.path.getsize(i) / mbConversion, 2))
                sizeSuffix = 'MB'

            if (i.__contains__('.srt') or i.__contains__('.idx') or i.__contains__('.sub')) and excludeSubtitles:
                print('Skipping File.')
            else:
                csvRows = [i, fileSizeConverted + sizeSuffix, modificationTime]
                csvwriter.writerow(csvRows)

def main():
    SaveToCSV('E:/Plex Librarys', 'Data_Log_Movies.csv', True)
	SaveToCSV('E:/Plex Librarys', 'Data_Log_TV.csv', True)
	SaveToCSV('E:/Plex Librarys', 'Data_Log_Music.csv', True)
    SendEmail()


if __name__ == '__main__':
    DeleteOldFiles()
    main()
