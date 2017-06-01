from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
import cv2
import glob
import os
import webbrowser
import configparser
import subprocess

config = configparser.ConfigParser()
config.read('config.ini')
destination = config['custom']['destination']

if destination == '':
  destination = os.getcwd() + '/'
  destination = str.replace(destination, '\\', '/')
  config.set('default','destination',destination)
  config.set('custom','destination',destination)
  with open('config.ini', 'w') as configfile:
    config.write(configfile)

print('Bienvenue dans Imagel, la destination de sortie se trouve actuellement dans :\n' + destination)

def Destination():
  global destination
  new_destination = tkinter.filedialog.askdirectory(title='Changer la destination de sortie', initialdir=destination)
  if new_destination != '':
    destination = new_destination + '/'
    config.set('custom','destination',destination)
    with open('config.ini', 'w') as configfile:
      config.write(configfile)
    print('\nDestination de sortie modifiée : \n' + destination)
    T_destination.config(state=NORMAL)
    T_destination.delete(1.0, END)
    T_destination.insert(END, destination)
    T_destination.config(state=DISABLED)
  else:
    print('\nChangement de la destination de sortie annulée')

def ParDossier():
  directory = tkinter.filedialog.askdirectory(title='Choisir un dossier à traiter', initialdir='.')
  if directory != '':
    print('\nDossier sélectionné :', directory)
    files = glob.glob(directory + '/*.mov') + glob.glob(directory + '/*.mp4')
    for filename in files:
      filename = filename.split('\\')
      del filename[0]
      filename = str.join('', (filename))
      print('\nOpération en cours sur :', filename)
      cap = cv2.VideoCapture(directory + '/' + filename)
      length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      print('Nombre de frames de la vidéo :', length)
      cap.set(1,length);
      ret, frame = cap.read()
      print ('Capture de l\'image', length, ':', ret)
      while ret==False:
        print('Échec de la capture, recul d\'une image...')
        length = length-1
        cap.set(1,length);
        ret, frame = cap.read()
        print ('Capture de l\'image', length, ':', ret)
      gel = filename[0:-4]
      cv2.imwrite(destination + gel + '.jpg', frame)
    print('\nOpérations terminées !')
    print('Dossier de sortie : ' + destination)
  else:
    print('\nAucun dossier sélectionné')

def ParFichiers():
  files = tkinter.filedialog.askopenfilenames(title='Choisir un ou des fichiers à traiter', filetypes=[('Vidéos','*.mov;*.mp4')], initialdir='.')
  if files !='':
    for filename in files:
      file = str.join('', (filename))
      filename = os.path.basename(file)
      print('\nOpération en cours sur :', filename)
      cap = cv2.VideoCapture(file)
      length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      print('Nombre de frames de la vidéo :', length)
      cap.set(1,length);
      ret, frame = cap.read()
      print ('Capture de l\'image', length, ':', ret)
      while ret==False:
        print('Échec de la capture, recul d\'une image...')
        length = length-1
        cap.set(1,length);
        ret, frame = cap.read()
        print ('Capture de l\'image', length, ':', ret)
      gel = filename[0:-4]
      print(destination + gel)
      cv2.imwrite(destination + gel + '.jpg', frame)
    print('\nOpération(s) terminée(s) !')
    print('Dossier de sortie : ' + destination)
  else:
    print('\nAucun fichier sélectionné')

def Github():
  webbrowser.open("https://github.com/TeeVy/imagel")

window = Tk()
window.title('Imagel')
window.resizable(width=False, height=False)
window.iconbitmap('img/imagel_icon.ico')

M = Menu(window)

MenuFichier = Menu(M,tearoff=0, activebackground='#91c9f7', activeforeground='black')
MenuFichier.add_command(label='Choisir un dossier à traiter',command=ParDossier)
MenuFichier.add_command(label='Choisir un ou des fichiers à traiter',command=ParFichiers)
MenuFichier.add_command(label='Quitter',command=window.destroy)
M.add_cascade(label='Fichier', menu=MenuFichier)

MenuApropos = Menu(M,tearoff=0, activebackground='#91c9f7', activeforeground='black')
MenuApropos.add_command(label="Github",command= Github)
M.add_cascade(label="À propos", menu=MenuApropos)

window.config(menu=M)

logo = PhotoImage(file="img/imagel_logo.png")

canvas = Canvas(window,width=317, height=98)
canvas.create_image(0, 0, anchor=NW, image=logo)
canvas.pack()

#Par amètres (la bonne blague)
LF_settings = LabelFrame(window, text='Paramètres')
LF_settings.pack(fill='both', expand='yes', padx=10, pady=5)

T_destination = Text(LF_settings, height=1, width=45, wrap='none', font='Arial, 8', relief = GROOVE, borderwidth=2)
T_destination.pack(pady=5, padx=10)
T_destination.insert(END, destination)
T_destination.config(state=DISABLED)

L_destination = Label(LF_settings, text='Destination de sortie :')
L_destination.pack(pady=5, padx=10, side = LEFT)

B_destination = Button(LF_settings, text = 'Parcourir...', command = Destination)
B_destination.pack(pady=5, padx=10, side = RIGHT)

#Par dossier
LF1 = LabelFrame(window, text='Par dossier')
LF1.pack(fill='both', expand='yes', padx=10, pady=5)

L1 = Label(LF1, text='Choisissez le dossier à traiter')
L1.pack(padx=10, pady=10, side = LEFT)

Bouton1 = Button(LF1, text = 'Parcourir...', command = ParDossier)
Bouton1.pack(padx=10, pady=10, side = RIGHT)

#Par fichier(s)
LF2 = LabelFrame(window, text='Par fichier(s)')
LF2.pack(fill='both', expand='yes', padx=10, pady=5)

L2 = Label(LF2, text='Choisissez le(s) fichier(s) à traiter')
L2.pack(padx=10, pady=10, side = LEFT)

Bouton2 = Button(LF2, text = 'Parcourir...', command = ParFichiers)
Bouton2.pack(padx=10, pady=10, side = RIGHT)

#Fenêtre
window.mainloop()
