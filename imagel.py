import cv2
import os
import glob

print('Bienvenue dans Imagel 0.1, commencez tout d\'abord par choisir le dossier contenant les vidéos.')
print('================================================')
directories = (next(os.walk('.'))[1])
print(str.join('\n', (directories)))
print('================================================')

directory = input("Dossier à explorer : ")
print('Si les vidéos se trouvent dans le même dossier que le script, appuyez simplement sur ENTER')

if directory == '':
    directory = '.'

try:
    os.mkdir('gel')
    print('Création du dossier "gel" réussie !')
except OSError:
    print('Le dossier "gel" existe déjà, passage direct à l\'étape suivante.')
    pass

print('================================================')

try:
    files = glob.glob(directory + '/*.mov') + glob.glob(directory + '/*.mp4')

    for filename in files:
        filename = filename.split('\\')
        del filename[0]
        filename = str.join('', (filename))
        print('opération en cours sur :', filename)
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
        print('================================================')

    input('Opérations réalisées avec succès ! Appuyez sur ENTER pour fermer le script')

##    print('\nSeconde boucle')
##    for filename in files:
##        filename = filename.split('\\')
##        del filename[0]
##        filename = str.join('', (filename))
##        print(filename)
except OSError:
    print('ERREUR : Dossier introuvable, relancez le programme pour recommencer.')
