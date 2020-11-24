import numpy as np
import cv2


class ImageList:
    images = []


    def addImages(self, imagesList ):
        for i in imagesList:
            self.images.append(i)

    def concat(self):
        black = np.full(self.images[0].shape, 0, dtype=np.uint8)
        count = len(self.images)
        if(count>=4):
            vis1 = np.concatenate((self.images[0], self.images[1]), axis=1)
            vis2 = np.concatenate((self.images[2], self.images[3]), axis=1)
            vis1 = cv2.resize(vis1,None,fx=0.25,fy=0.25)
            vis2 = cv2.resize(vis2,None,fx=0.25,fy=0.25)
            vis3 = np.concatenate((vis1, vis2), axis=1)
            self.images=self.images[4:]
        else:
            for i in range(0, 4-count):
                self.images.append(black)
        while( len(self.images)>=4 ):

            vis1 = np.concatenate((self.images[0], self.images[1]), axis=1)
            vis2 = np.concatenate((self.images[2], self.images[3]), axis=1)
            vis1 = cv2.resize(vis1,None,fx=0.25,fy=0.25)
            vis2 = cv2.resize(vis2,None,fx=0.25,fy=0.25)
            vis4 = np.concatenate((vis1, vis2), axis=1)
            self.images=self.images[4:]
            vis3 = np.concatenate((vis3, vis4), axis=0)
            if( len(self.images)<4 and len(self.images)>=1 ):
                for i in range(0, 4-len(self.images)):
                    self.images.append(black)
        cv2.imwrite('out2.png', vis3)
