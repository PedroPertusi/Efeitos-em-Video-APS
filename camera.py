import numpy as np
import math
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

    width = 300
    height = 300
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

        image_ = np.zeros_like(image)

        X = criar_indices(0,width,0,height)
        X = np.vstack((X,np.ones(X.shape[1])))

        # T = np.array([[1, 0, -height/2], [0, 1, -width/2], [0, 0,1]])
        # T2 = np.array([[1, 0, height/2], [0, 1, width/2], [0, 0,1]])
        T = np.array([[1, 0, -150], [0, 1, -150], [0, 0,1]])
        T2 = np.array([[1, 0, 150], [0, 1, 150], [0, 0,1]])

        R = np.array([[np.cos(math.radians(ang)), -np.sin(math.radians(ang)), 0], [np.sin(math.radians(ang)), np.cos(math.radians(ang)), 0], [0, 0, 1]])
        Xd = T2 @ R @ T @ X

        Xd = Xd.astype(int)
        X = X.astype(int)
        

        filter = (Xd[0,:] >= 0) & (Xd[0,:] < image.shape[0]) & (Xd[1,:] >= 0) & (Xd[1,:] < image.shape[1])

        Xd, X = Xd[:,filter], X[:,filter]

        fx = image.shape[0]
        fy = image.shape[1]

        image_[Xd[0,:], Xd[1,:], :] = image[X[0,:]-fx, X[1,:]-fy, :]
        ang += 1

        cv.imshow('Minha Imagem!', image_)
        
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

run()


"""
assigns values from the image array to the image_ array using the pixel coordinates specified in the X and Xd arrays.

Xd[0,:] and Xd[1,:] are two arrays of equal length that contain the x and y coordinates, respectively, of the transformed pixels. 

X[0,:] and X[1,:] are also two arrays of equal length that contain the x and y coordinates, respectively, of the original pixels.

The : at the end of each index means that we are selecting all values along the third axis, which represents the color channels of the image.

Thus, the line of code assigns to each pixel of the image_ array at the transformed pixel coordinates specified by Xd[0,:] and Xd[1,:] the color values 

from the corresponding pixel coordinates in the original image array specified by X[0,:] and X[1,:].

In other words, this line of code copies a rectangular region from the original image to the transformed image, and it's the key step for the image rotation effect in the code.

"""