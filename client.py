import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
import os
import ntpath #This is used to extract filename from path

from tkinter import filedialog
from pathlib import Path

import time
from playsound import playsound
import pygame
from pygame import mixer


PORT  = 8050
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096
song_counter = 0
listBox = None
infoLabel =""
filePathLabel = None
def play():
    global song_selected
    song_selected = listBox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()
    if(song_selected!=""):
        infoLabel.configure(text="Now Playing " +song_selected)
    else:
        infoLabel.configure(text="Nothing Playing")

def stop():
    global song_selected
    song_selected = listBox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.stop()
    infoLabel.configure(text="Nothing Playing")

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()

def resume():
    global song_selected 
    pygame   
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()   

def browseFiles():
    global textarea
    global filePathLabel

    try:
        fileName = filedialog.askopenfilename()
        filePathLabel.configure(text=fileName)
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd("shared_files")
        fname = ntpath.basename(fileName)
        with open(fileName,"rb") as file:
            ftp_server.storbinary(f"STOR {fname}",file)

        ftp_server.dir()    
        ftp_server.quit()
    except FileNotFoundError:
        print("Cancel button pressed")

def download():    
    song_to_download=listBox.get(ANCHOR)
    infoLabel.configure(text="Downloading "+ song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home())
    download_path=home+"/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary('RETR '+ song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text="Download Complete")
    time.sleep(1)
    if(song_selected != ""):
        infoLabel.configure(text="Now Playing: " +song_selected)
    else:
       infoLabel.configure(text="") 

def musicWindow():
    global listBox
    global song_counter
    global infoLabel
    global filePathLabel


    window = Tk()
    window.title("Music Window")
    window.geometry("330x490")
    window.configure(bg="LightSkyBlue")

    selectLabel = Label(window, text="Select Song", bg="LightSkyBlue" ,font=("Calibri",10))    
    selectLabel.place(x=5,y=3)

    listBox = Listbox(window,height=10,width=33,activestyle="dotbox",font=("Calibri",13),bd=1,bg="LightSkyBlue")
    listBox.place(x=10,y=24)
    
    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listBox.insert(song_counter,filename)
        song_counter+=1

    scrollbar1= Scrollbar(listBox)
    scrollbar1.place(relheight=1,relx=1.5)
    scrollbar1.config(command=listBox.yview)

    PlayButton = Button(window,text="Play",bd=1,font=("Calibri",11),bg="SkyBlue", width=10,command=play)
    PlayButton.place(x=30,y=270)

    Stop = Button(window,text="Stop",bd=1,font=("Calibri",11),bg="SkyBlue", width=10,command=stop)
    Stop.place(x=200,y=270)

    Upload = Button(window,text="Upload",bd=1,font=("Calibri",11),bg="SkyBlue", width=10,command=browseFiles)
    Upload.place(x=30,y=320)

    Download = Button(window,text="Download",bd=1,font=("Calibri",11),bg="SkyBlue", width=10,command=download)
    Download.place(x=200,y=320)

    Resume = Button(window,text="Resume",bd=1,font=("Calibri",11),bg="SkyBlue", width=10, command=resume)
    Resume.place(x=30,y=370)

    Pause = Button(window,text="Pause",bd=1,font=("Calibri",11),bg="SkyBlue", width=10,command=pause)
    Pause.place(x=200,y=370)

    infoLabel = Label(window, bg="SkyBlue" ,font=("Arial",11))    
    infoLabel.place(x=4,y=400)

    filePathLabel = Label(window, text= "",fg= "blue", font = ("Calibri",8))
    filePathLabel.place(x=5, y=450)

    window.mainloop()






def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    musicWindow()

setup()