from PIL import Image
import time
import cv2
import numpy as np
import cv2

# import pygame
# pygame.init()
# screen = pygame.display.set_mode(1024,768) # Whatever resolution you want.
# image  = pygame.image.load("wake_up.png")
# screen.blit(image, (0,0))
# pygame.display.flip()

# im1 = Image.open("wake_up.png")
# im2 = Image.open("sleepy.png")
# im1.show()
# cv2.waitKey(1000)
# im2.show()
# cv2.waitKey(1000)
# im1.show()
# cv2.waitKey(1000)
# im2.show()
# im1.close()
# im2.close()
import cv2
from skimage import io
import numpy as np
from matplotlib import pyplot as plt

#cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
# im = cv2.imread("wake_up_2.png")                        # Read image
# cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
# cv2.imshow("window", im)
image1 = io.imread('~/Desktop/keyboard/1.jpg')
image2 = io.imread('~/Desktop/keyboard/5.jpg')
#print(image1)

f,(ax0,ax1) = plt.subplots(1,2,figsize=(10,8))
ax0.imshow(image1)
ax1.imshow(image2)
plt.imshow(image1)
# cv2.waitKey(1000)
# imS = cv2.resize(im, (1440, 900))                    # Resize image
#im1 = Image.open("wake_up_2.png")
# im1.show()
# #cv2.imshow("output", im1)                            # Show image
# cv2.waitKey(2000)
# im2.show()
# cv2.waitKey(2000)
# im1.show()