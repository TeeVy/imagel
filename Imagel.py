from tkinter import *
import tkinter.filedialog
import cv2
import glob
import os

def ParDossier():
  directory = tkinter.filedialog.askdirectory(title="Choisir un dossier", initialdir=".")
  print(directory)
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
    
window = Tk()
window.title("Imagel")

try:
  os.mkdir('gel')
  print('Création du dossier "gel" réussie !')
except OSError:
  print('Le dossier "gel" existe déjà, passage direct à l\'étape suivante.')
  pass

LF1 = Label(window, text="Choisissez le dossier à examiner")
LF1.pack(padx=10, pady=10, side = LEFT)
Bouton1 = Button(window, text = 'Parcourir', command = ParDossier)
Bouton1.pack(padx=10, pady=10, side = RIGHT)

window.mainloop()
