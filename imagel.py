from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
import cv2
import glob
import os
import webbrowser

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
      cv2.imwrite('gel/%s.jpg' % gel, frame)
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
      gel = filename[0:-4]
      cv2.imwrite('gel/%s.jpg' % gel, frame)
    print('\nOpération(s) terminée(s) !')
  else:
    print('\nAucun fichier sélectionné')

def Apropos():
  webbrowser.open("https://github.com/TeeVy/imagel")
    
try:
  os.mkdir('gel')
  print('Création du dossier "gel" réussie !')
except OSError:
  print('Le dossier "gel" existe déjà, passage direct à l\'étape suivante.')
  pass

window = Tk()
window.title("Imagel")
window.resizable(width=False, height=False)
window.iconbitmap('img/imagel_icon.ico')

M = Menu(window)

MenuFichier = Menu(M,tearoff=0, activebackground='#91c9f7', activeforeground='black')
MenuFichier.add_command(label="Choisir un dossier à traiter",command=ParDossier)
MenuFichier.add_command(label="Choisir un ou des fichiers à traiter",command=ParFichiers)
MenuFichier.add_command(label="Quitter",command=window.destroy)
M.add_cascade(label="Fichier", menu=MenuFichier)

MenuAide = Menu(M,tearoff=0, activebackground='#91c9f7', activeforeground='black')
MenuAide.add_command(label="À propos",command= Apropos)
M.add_cascade(label="Aide", menu=MenuAide)

window.config(menu=M)

logo = PhotoImage(file="img/imagel_logo.png")

canvas = Canvas(window,width=317, height=98)
canvas.create_image(0, 0, anchor=NW, image=logo)
canvas.pack(pady=10)

LF1 = LabelFrame(window, text='Par Dossier')
LF1.pack(fill='both', expand='yes', padx=10)

L1 = Label(LF1, text='Choisissez le dossier à traiter')
L1.pack(padx=10, pady=10, side = LEFT)
Bouton1 = Button(LF1, text = 'Parcourir', command = ParDossier)
Bouton1.pack(padx=10, pady=10, side = RIGHT)

LF2 = LabelFrame(window, text='Par fichier(s)')
LF2.pack(fill='both', expand='yes', padx=10, pady=10)

L2 = Label(LF2, text='Choisissez le(s) fichier(s) à traiter')
L2.pack(padx=10, pady=10, side = LEFT)
Bouton2 = Button(LF2, text = 'Parcourir', command = ParFichiers)
Bouton2.pack(padx=10, pady=10, side = RIGHT)

window.mainloop()
