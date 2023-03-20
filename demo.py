import numpy as np
import math
import itertools
import cv2 as cv
import os.path

def criar_indices(min_i, max_i, min_j, max_j):
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx

def on_mouse(event, x, y, flags, param):
    global vel
    if event == cv.EVENT_LBUTTONUP:
        vel += 1
        print('Velocidade aumentada')
    if event == cv.EVENT_RBUTTONUP and vel > 1:
        vel -= 1
        print('Velocidade reduzida')

def run():
    global file_name
    global salvar
    global vel
    cap = cv.VideoCapture(0)

    width = 320
    height = 240
    ang = 0
    rodando_direita = False
    rodando_esquerda = False
    vel = 1
    zoom = 0
    salvar = False

    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()


    for i in range(999999):
        file_name = f"output{i}.mp4"
        if not os.path.isfile(file_name):
            break

    
    fps = cap.get(cv.CAP_PROP_FPS)
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(file_name, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Não consegui capturar frame!")
            break

        frame = cv.resize(frame, (width,height), interpolation =cv.INTER_AREA)
        image = np.array(frame).astype(float)/255

        image_ = np.zeros_like(image)

        Xd = criar_indices(0,height,0,width)
        Xd = np.vstack((Xd,np.ones(Xd.shape[1])))

        if zoom == 1:
            E = np.array([[1.5, 0, 0], [0, 1.5, 0], [0, 0, 1]])
        elif zoom == 2:
            E = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]]) 

        T = np.array([[1, 0, -height/2], [0, 1, -width/2], [0, 0, 1]])
        T2 = np.array([[1, 0, height/2], [0, 1, width/2], [0, 0, 1]])
        R = np.array([[np.cos(math.radians(ang)), -np.sin(math.radians(ang)), 0], [np.sin(math.radians(ang)), np.cos(math.radians(ang)), 0], [0, 0, 1]])

        if zoom == 1 or zoom == 2:
            A = T2 @ R @ E @ T 
        elif zoom == 0:
            A = T2 @ R @ T 
        X = np.linalg.inv(A) @ Xd

        Xd = Xd.astype(int)
        X = X.astype(int) 

        filter = (X[0,:] >= 0) & (X[0,:] < image.shape[0]) & (X[1,:] >= 0) & (X[1,:] < image.shape[1])

        Xd, X = Xd[:,filter], X[:,filter]

        fx = image.shape[0]
        fy = image.shape[1]

        image_[Xd[0,:], Xd[1,:], :] = image[X[0,:]-fx, X[1,:]-fy, :]


        if rodando_direita:
            ang -= 1 * vel
        elif rodando_esquerda:
            ang += 1 * vel


        out.write((image_ * 255).astype(np.uint8))
        cv.imshow('Minha Imagem!', image_)
        
        x = cv.waitKey(1)

        if x == ord('d'):
            if not rodando_direita:
                rodando_direita = True
            else:
                rodando_direita = False
            rodando_esquerda = False 
            print('Rotação a direita')


        if x == ord('a'):
            if not rodando_esquerda:
                rodando_esquerda = True
            else:
                rodando_esquerda = False
            rodando_direita = False
            print('Rotação a esquerda')

        if x == ord('z'):
            if zoom == 1:
                print('Zoom ampliado pra 2x')
                zoom = 2
            elif zoom == 0:
                zoom = 1
                print('Zoom ampliado para 1.5x')
            else:
                zoom = 0
                print('Zoom removido')
        if x == ord('q'):
            break

        if x == ord('s'):
            salvar = True
            print('Video is being saved')

        if x == ord('r'):
            ang = 0
            print('Angulo de rotação resetado')

        cv.setMouseCallback('Minha Imagem!', on_mouse)


    out.release()
    if salvar:
        print(f"Video saved to {file_name}")
    else:
        print("O video não foi salvo")
    cap.release()
    cv.destroyAllWindows()

run()

if not salvar:
    os.remove(file_name) 