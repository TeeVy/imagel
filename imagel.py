from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from tkinter import messagebox
import cv2
import glob
import os
import webbrowser
import configparser
import clipboard
import subprocess

version ='1.0.0-release'

def Destination():
  global destination
  new_destination = tkinter.filedialog.askdirectory(title='Changer la destination de sortie', initialdir=destination)
  if new_destination != '':
    destination = new_destination + '/'
    config.set('default','destination',destination)
    with open('config.ini', 'w') as configfile:
      config.write(configfile)
    print('\nDestination de sortie modifiée : \n' + destination)
    T_destination.config(state=NORMAL)
    T_destination.delete(1.0, END)
    T_destination.insert(END, destination)
    T_destination.config(state=DISABLED)
  else:
    print('\nChangement de la destination de sortie annulée')

#Vérification de config.ini
config = configparser.ConfigParser()

def CreateIni():
  global destination
  destination = os.getcwd() + '/'
  destination = str.replace(destination, '\\', '/')
  config['default'] = {'destination': destination}
  with open('config.ini', 'w') as configfile:
    config.write(configfile)

try:
  with open('config.ini'):
    print('Le fichier "config.ini" a été chargé avec succès !')
except IOError:
  print('Le fichier "config.ini" est introuvable, Imagel va automatiquement en créer un...')
  CreateIni()
  print('Le fichier "config.ini" a été créé avec succès !')

config.read('config.ini')
destination = config['default']['destination']

#Vérification de l'existence du dossier de sortie
def DestinationCheck(destination):
  global destination_check
  destination_check = os.path.isdir(destination)
  if destination_check == False:
    print('\nErreur ! Le dossier de sortie est introuvable !')
    if 'window' in globals():
      messagebox.showerror('Imagel - Erreur', 'Le dossier de sortie est introuvable !\nVeuillez changer la destination de ce dernier')
      Destination()
    else:
      CreateIni()
      print('La destination du dossier de sortie a été rénitialisée')

DestinationCheck(destination)

#Vérifications terminées, on peut désormais lancer le script
print('\nBienvenue dans Imagel, la destination de sortie se trouve actuellement dans :\n' + destination)

def PopCopy(event):
  T_destination.focus_force()
  T_destination.tag_add('sel', '1.0', 'end')
  M_copy.post(event.x_root, event.y_root)

def Copy(destination):
  clipboard.copy(destination)
  print('\nChemin du dossier de sortie copié dans le presse-papier\n' + destination)

def OpenFolder():
  DestinationCheck(destination)
  if destination_check == True:
    open_destination = str.replace(destination, '/', '\\')
    subprocess.Popen('explorer ' + open_destination)
    
def ParDossier():
  DestinationCheck(destination)
  if destination_check == True:
    directory = tkinter.filedialog.askdirectory(title='Choisir un dossier à traiter', initialdir='.')
    if directory != '':
      script_path = os.getcwd()
      os.chdir(destination)
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
        gel = filename[0:-4] + '.jpg'
        cv2.imwrite(gel, frame)
      print('\nOpérations terminées !')
      Copy(destination)
      os.chdir(script_path)
    else:
      print('\nAucun dossier sélectionné')

def ParFichiers():
  DestinationCheck(destination)
  if destination_check == True:
    files = tkinter.filedialog.askopenfilenames(title='Choisir un ou des fichiers à traiter', filetypes=[('Vidéos','*.mov;*.mp4')], initialdir='.')
    if files !='':
      script_path = os.getcwd()
      os.chdir(destination)
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
        gel = filename[0:-4] + '.jpg'
        cv2.imwrite(gel, frame)
      print('\nOpération(s) terminée(s) !')
      Copy(destination)
      os.chdir(script_path)
    else:
      print('\nAucun fichier sélectionné')

def Github():
  webbrowser.open('https://github.com/TeeVy/imagel')

def Donate():
  webbrowser.open('https://www.paypal.me/RobinCarlo')

def Twitter():
  webbrowser.open('https://www.twitter.com/robinowned')

def Website():
  webbrowser.open('http://robincarlo.fr')

def About():
  W_about = Toplevel()
  W_about.iconbitmap('img/imagel_icon.ico')
  canvas = Canvas(W_about, width = 317, height = 126)
  canvas.pack()
  logo = PhotoImage(file = 'img/imagel_logo.png')
  canvas.create_image(0, 20, image = logo, anchor = NW)
  canvas.logo = logo
  L_version = Label(W_about, text='Version ' + version, font='Arial 9 bold')
  L_version.pack(pady=5)
  F_about = Frame(W_about)
  F_about.pack(pady=10)
  B_donate = Button(F_about, text='Faire un don', command = Donate)
  B_donate.pack(side = LEFT, padx=2)
  B_website = Button(F_about, text='Site Web', command = Website)
  B_website.pack(side = LEFT, padx=2)
  B_twitter = Button(F_about, text='Twitter', command = Twitter)
  B_twitter.pack(side = LEFT, padx=2)
  B_git = Button(F_about, text='Github', command = Github)
  B_git.pack(side = LEFT, padx=2)
  
#Fenêtre
window = Tk()
window.title('Imagel')
window.resizable(width=False, height=False)
window.iconbitmap('img/imagel_icon.ico')

#Menu
M = Menu(window)

MenuFichier = Menu(M,tearoff=0, activebackground='#91c9f7', activeforeground='black')
MenuFichier.add_command(label='Choisir un dossier à traiter',command=ParDossier)
MenuFichier.add_command(label='Choisir un ou des fichiers à traiter',command=ParFichiers)
MenuFichier.add_command(label='Copier le chemin du dossier de sortie',command=lambda: Copy(destination))
MenuFichier.add_separator()
MenuFichier.add_command(label='Quitter',command=window.destroy)
M.add_cascade(label='Fichier', menu=MenuFichier)

MenuApropos = Menu(M,tearoff=0, activebackground='#91c9f7', activeforeground='black')
MenuApropos.add_command(label='À propos', command = About)
MenuApropos.add_command(label='Faire un don', command = Donate)
MenuApropos.add_separator()
MenuApropos.add_command(label='Site Web', command = Website)
MenuApropos.add_command(label='Twitter', command = Twitter)
MenuApropos.add_command(label='Github', command = Github)
M.add_cascade(label='À propos', menu=MenuApropos)

window.config(menu=M)

#Logo
logo = PhotoImage(file='img/imagel_logo.png')

canvas = Canvas(window, width=317, height=126)
canvas.create_image(0, 20, anchor=NW, image=logo)
canvas.pack()

#Par amètres (la bonne blague)
LF_settings = LabelFrame(window, text='Paramètres')
LF_settings.pack(fill='both', expand='yes', padx=10, pady=10)

F_settings = Frame(LF_settings)
F_settings.pack(pady=5)

F_settings_L1 = Frame(F_settings, width = 277, height=24)
F_settings_L1.pack(pady=5)
F_settings_L1.pack_propagate(0)

F_settings_L2 = Frame(F_settings, width = 277, height=25)
F_settings_L2.pack(pady=5)
F_settings_L2.pack_propagate(0)

T_destination = Text(F_settings_L1, height=1, width=40, wrap='none', font='Arial, 8', relief = GROOVE, borderwidth=2)
T_destination.pack(padx=2, side = LEFT)
T_destination.insert(END, destination)
T_destination.config(state=DISABLED)

open_gif = PhotoImage(file = 'img/open.gif')

B_open = Button(F_settings_L1, image = open_gif, command = OpenFolder)
B_open.pack(side = RIGHT)

L_destination = Label(F_settings_L2, text='Destination de sortie')
L_destination.pack(side = LEFT)

B_destination = Button(F_settings_L2, text = 'Parcourir...', command = Destination)
B_destination.pack(side = RIGHT)

#Copy
M_copy = Menu(T_destination, tearoff=0)
M_copy.add_command(label='Copier', command = lambda: Copy(destination))
T_destination.bind("<Button-3>", PopCopy)

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

#Fenêtre loop
window.mainloop()
