import numpy as np
import itertools
import cv2 as cv

def criar_indices(min_i, max_i, min_j, max_j):
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx

def run():
    cap = cv.VideoCapture(0)

    width = 320
    height = 240
    ang = 0

    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Não consegui capturar frame!")
            break

        frame = cv.resize(frame, (width,height), interpolation =cv.INTER_AREA)
        image = np.array(frame).astype(float)/255

        image_ = np.zeros_like(image.shape)
        X = criar_indices(0,width,0,height)
        rotate = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
        Xd = rotate @ X
        filter = (Xd[0,:] >= 0) & (Xd[0,:] <= image_.shape[0]) & (Xd[1,:] >= 0) & (Xd[1,:] <= image_.shape[1])
        Xd, X = Xd[:,filter], X[:,filter]
        image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]
        ang += 1

        cv.imshow('Minha Imagem!', image_)
        
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

run()