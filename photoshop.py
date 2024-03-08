import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
import random as rd

def save(matPix, filename):
    Image.fromarray(matPix).save(filename)

def load(filename):
    return np.array(Image.open(filename))

create = True
nomImgCourante = ""
nomImgDebut = ""

def charger(widg):
    global create, photo, img, canvas, dessin, nomImgCourante, nomImgDebut
    filename = filedialog.askopenfilename(title='Choose a file')
    img = Image.open(filename)
    nomImgCourante = filename
    nomImgDebut = filename
    photo = ImageTk.PhotoImage(img)
    if create:
        canvas = tk.Canvas(widg, width=img.size[0], height=img.size[1])
        dessin = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.grid(row=0, column=1, rowspan=4, columnspan=2)
        create = False
    else:
        canvas.grid_forget()
        canvas = tk.Canvas(widg, width=img.size[0], height=img.size[1])
        dessin = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.grid(row=0, column=1, rowspan=4, columnspan=2)

def modify(matrice):
    global imgModif, nomImgCourante
    save(matrice, "modif.png")
    imgModif = ImageTk.PhotoImage(file="modif.png")
    canvas.itemconfigure(dessin, image=imgModif)
    canvas['width'] = imgModif.width()
    canvas['height'] = imgModif.height()
    nomImgCourante = "modif.png"

def reaffiche():
    global imgDebut, nomImgCourante
    if not create:
        imgDebut = ImageTk.PhotoImage(file=nomImgDebut)
        canvas.itemconfigure(dessin, image=imgDebut)
        canvas['width'] = imgDebut.width()
        canvas['height'] = imgDebut.height()
        nomImgCourante = nomImgDebut

def quit():
    fenetre.destroy()

def filtre_vert():
    mat = load(nomImgCourante)
    mat[:, :, 0] = 0 
    mat[:, :, 2] = 0
    modify(mat)

def gris():
    mat = load(nomImgCourante)
    # Convert the image to grayscale
    grayscale = np.dot(mat[..., :3], [0.299, 0.587, 0.114])
    mat = np.stack((grayscale,) * 3, axis=-1)
    modify(mat)

def negatif(): 
    mat =load(nomImgCourante)
    mat[:]= 255-mat[:]
    modify(mat)

def symetrique():
    mat =load(nomImgCourante) 
    mat[:] = mat[:,::-1]
    modify(mat)

def noirBlanc():
    mat=load(nomImgCourante)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            luminosite=0.2125*mat[i,j,0] + 0.0721*mat[i,j,2] + 0.7154*mat[i,j,1]
            
            if luminosite > 127:
                mat[i,j] = (255,255,255)
            else:
                mat[i,j]=(0,0,0)
            
    modify(mat)

def zoom():
    mat=load(nomImgCourante)
    #créer une matrice de largeur et hauteur deux fois plus grande
    matzoom=np.empty((2*mat.shape[0], 2*mat.shape[1], 3), dtype=np.uint8)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            matzoom[2*i,2*j]=mat[i,j]
            matzoom[2*i+1,2*j]=mat[i,j]
            matzoom[2*i,2*j+1]=mat[i,j]
            matzoom[2*i+1,2*j+1]=mat[i,j]
    modify(matzoom)

def gris():
    #On utilisera la conversion CIE709 qui permet de calculer la teinte de gris qui va être affichée dans le pixel
    #La teinte affichée est : gris=0,2125*rouge + 0,0721*bleu + 0,7154*vert
    mat=load(nomImgCourante)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            gris=0.2125*mat[i,j,0] + 0.0721*mat[i,j,2] + 0.7154*mat[i,j,1]
            mat[i,j] = (gris,gris,gris)
    modify(mat)

def shrink():
    mat=load(nomImgCourante)
    matshrink=np.empty((mat.shape[0]//2, mat.shape[1]//2, 3), dtype=np.uint8)
    for i in range(matshrink.shape[0]):
        for j in range(matshrink.shape[1]):
            rouge=(mat[2*i,2*j,0]//4+mat[2*i+1,2*j,0]//4+mat[2*i,2*j+1,0]//4+mat[2*i+1,2*j+1,0]//4)
            vert=(mat[2*i,2*j,1]//4+mat[2*i+1,2*j,1]//4+mat[2*i,2*j+1,1]//4+mat[2*i+1,2*j+1,1]//4)
            bleu=(mat[2*i,2*j,2]//4+mat[2*i+1,2*j,2]//4+mat[2*i,2*j+1,2]//4+mat[2*i+1,2*j+1,2]//4)
            matshrink[i,j]=(rouge,vert,bleu)
    modify(matshrink)

def poster():
    shrink()
    shrink()
    zoom()
    zoom()

def luminosite():
    v = molette_lum.get()
    mat=load(nomImgCourante)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            pourcentage = v/100
            if mat[i,j][0]*pourcentage<255:
                mat[i,j][0] =mat[i,j][0]*pourcentage
            else:
                mat[i,j][0] = 255

            if mat[i,j][1]*pourcentage<255:
                mat[i,j][1] =mat[i,j][1]*pourcentage
            else:
                mat[i,j][1] = 255

            if mat[i,j][2]*pourcentage<255:
                mat[i,j][2] =mat[i,j][2]*pourcentage
            else:
                mat[i,j][2] = 255
  
    modify(mat)

def bruitage():
    mat=load(nomImgCourante)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
           
                mat[i,j][0] = mat[i,j][0]+rd.randint(0,100)

                mat[i,j][1] = mat[i,j][1]+rd.randint(0,100)

                mat[i,j][2] = mat[i,j][2]+rd.randint(0,100)
    modify(mat)

def rotate():
    mat=load(nomImgCourante)
    matrotate=np.empty((mat.shape[1], mat.shape[0], 3), dtype=np.uint8)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            matrotate[j,mat.shape[0]-i-1]=mat[i,j]

    modify(matrotate)

fenetre = tk.Tk()
fenetre.title("Mon Petit Photoshop")

#Création des Widgets
label_img=ImageTk
boutton_quit=tk.Button(text="quitter",command=quit)
boutton_return=tk.Button(text="Retour", command=reaffiche)
boutton_charg=tk.Button(text="Charger", command=lambda :charger(fenetre))
boutton_filtre_vert=tk.Button(text="vert", command=filtre_vert)
boutton_negatif=tk.Button(text="negatif",command=negatif)
boutton_symetrique=tk.Button(text="symétrique",command=symetrique)
boutton_gris=tk.Button(text="gris",command=gris)
boutton_noir_blanc=tk.Button(text="Noir et Blanc", command=noirBlanc)
boutton_zoom=tk.Button(text="Zoom", command=zoom)
boutton_Dezoom=tk.Button(text="Dézoom", command=shrink)
boutton_flou=tk.Button(text="Poster", command=poster)
molette_lum =tk.Scale(from_=0, to=200, orient="horizontal")
btn_lum =tk.Button(text="Luminositer", command=luminosite)
btn_bruit=tk.Button(text="Bruitage", command=bruitage)
btn_rotate=tk.Button(text="Rotate", command=rotate)
#Positionnement des Widgets
btn_lum.grid(row=13,column=3)
boutton_return.grid(row=7,column=0)
boutton_charg.grid(row=11,column=0)
boutton_quit.grid(row=11,column=2)
boutton_filtre_vert.grid(row=0,column=0)
boutton_negatif.grid(row=1,column=0)
boutton_symetrique.grid(row=2,column=0)
boutton_gris.grid(row=3, column=0)
boutton_noir_blanc.grid(row=4,column=0)
boutton_zoom.grid(row=5,column=0)
boutton_Dezoom.grid(row=9,column=0)
boutton_flou.grid(row=10,column=0)
molette_lum.grid(row=11,column=3)
btn_bruit.grid(row=1,column=170)
btn_rotate.grid(row=15,column=0)

#Lancement de la boucle 
fenetre.mainloop()