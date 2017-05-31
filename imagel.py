from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import tkinter.filedialog
import cv2
import glob
import os
import webbrowser
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
gel = config['custom']['gel']
destination = config['custom']['destination']

if gel == '':
  gel = config['default']['gel']

if destination == '':
  destination = os.getcwd() + '/'
  destination = str.replace(destination, '\\', '/')
  config.set('default','destination',destination)
  config.set('custom','destination',destination)
  with open('config.ini', 'w') as configfile:
    config.write(configfile)

def Destination():
  destination = tkinter.filedialog.askdirectory(title='Choisir un dossier à traiter', initialdir='.')
  if destination != '': 
    config.set('custom','destination',destination + '/')
    with open('config.ini', 'w') as configfile:
      config.write(configfile)
    print('Destination de sortie modifiée : ' + destination)
  else:
    print('Changement de la destination de sortie annulée')

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
      frame_gel = filename[0:-4]
      cv2.imwrite(destination + gel + '/%s.jpg' % frame_gel, frame)
    print('\nOpérations terminées !')
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
      frame_gel = filename[0:-4]      
      cv2.imwrite(destination + gel + '/%s.jpg' % frame_gel, frame)
    print('\nOpération(s) terminée(s) !')
  else:
    print('\nAucun fichier sélectionné')

def Github():
  webbrowser.open("https://github.com/TeeVy/imagel")
    
try:
  os.mkdir(destination + gel)
  print('Création du dossier "'+ gel +'" réussie !')
  print('il a été placé dans ' + destination)
except OSError:
  print('Le dossier de sortie "'+ gel +'" existe déjà, passage direct à l\'étape suivante.')
  pass

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

#Par amètres
F_settings = LabelFrame(window, text='Nom & Destination du dossier de sortie')
F_settings.pack(fill='both', expand='yes', padx=10, pady=5)

F_info = Frame(F_settings)
F_info.pack(pady=5)

L_info_foldername = Label(F_info, text='Le dossier de sortie "' + gel + '" se trouve actuellement dans :', wraplength=286)
L_info_foldername.pack()

L_info_destination = Label(F_info, text=destination, wraplength=286)
L_info_destination.pack()

F_left_settings = Frame(F_settings)
F_left_settings.pack(padx=10, pady=5, side = LEFT)

L_foldername = Label(F_left_settings, text='Nom :', width=11)
L_foldername.pack(pady=5)

L_destination = Label(F_left_settings, text='Destination :', width=11)
L_destination.pack(pady=5)

F_right_settings = Frame(F_settings)
F_right_settings.pack(padx=10, pady=5, side = RIGHT)

foldername = StringVar()
foldername.set(gel)
E_foldername = Entry(F_right_settings, textvariable=foldername, width=11)
E_foldername.pack(pady=5)

B_destination = Button(F_right_settings, text = 'Parcourir...', width=11, command = Destination)
B_destination.pack(pady=5)

#Par dossier
LF1 = LabelFrame(window, text='Par dossier')
LF1.pack(fill='both', expand='yes', padx=10, pady=5)

L1 = Label(LF1, text='Choisissez le dossier à traiter')
L1.pack(padx=10, pady=10, side = LEFT)

Bouton1 = Button(LF1, text = 'Parcourir...', width=11, command = ParDossier)
Bouton1.pack(padx=10, pady=10, side = RIGHT)

#Par fichier(s)
LF2 = LabelFrame(window, text='Par fichier(s)')
LF2.pack(fill='both', expand='yes', padx=10, pady=5)

L2 = Label(LF2, text='Choisissez le(s) fichier(s) à traiter')
L2.pack(padx=10, pady=10, side = LEFT)

Bouton2 = Button(LF2, text = 'Parcourir...', width=11, command = ParFichiers)
Bouton2.pack(padx=10, pady=10, side = RIGHT)

#Fenêtre
window.mainloop()
