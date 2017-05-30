from tkinter import *
import tkinter.filedialog
import cv2
import glob
import os

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
    
window = Tk()
window.title("Imagel")

try:
  os.mkdir('gel')
  print('Création du dossier "gel" réussie !')
except OSError:
  print('Le dossier "gel" existe déjà, passage direct à l\'étape suivante.')
  pass

LF1 = LabelFrame(window, text='Par Dossier')
LF1.pack(fill='both', expand='yes', padx=10, pady=10)

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
