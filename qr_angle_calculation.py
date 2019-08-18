"""
Script to calculate qrCode angle in images

INPUT:

--folder           // Path to folder containing images
--output           // Path to file that will have calculated angles

if not given script will use default values

OUTPUT: 
File containing image names and angles ex. image1, 156
"""

import cv2
import math
import sys
from pyzbar import pyzbar
from glob import glob
from absl import app
from absl import flags

RESIZED_IMAGE_SIZE = 416

DEFAULT_IMAGES_DIRECTORY = ""
DEFAULT_FILE_NAME = "angles.txt"

FLAGS = flags.FLAGS
flags.DEFINE_string("folder", DEFAULT_IMAGES_DIRECTORY, "Folder path for images")
flags.DEFINE_string("output", DEFAULT_FILE_NAME, "Txt file name")

def calculate_slope(p1, p2):
    if p2.x - p1.x == 0 or p2.y - p1.y == 0:
	    slope = 0
    else: 
        slope = -1 * (p2.y - p1.y)/(p2.x - p1.x)
    return slope

def main(argv):
    k = len(FLAGS.folder) + 1 
    f = open(FLAGS.output, "w")
    img_names = glob(FLAGS.folder + '\*')
    print(img_names)
    for img in img_names:
        image = cv2.imread(img)
        image = cv2.resize(image, (RESIZED_IMAGE_SIZE, RESIZED_IMAGE_SIZE))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        barcodes = pyzbar.decode(blur)
        
        if not barcodes:
            print("Not Detected")
        else:
            cv2.imshow("a",blur)
            cv2.waitKey(0)
            vertices = barcodes[0].polygon
            maxY_vertex = vertices[0]
            maxX_vertex = vertices[0]

            for p in vertices[1:]:
                if maxY_vertex.y < p.y:
                    maxY_vertex = p
                if maxX_vertex.x < p.x: 
                    maxX_vertex = p 

            slope = calculate_slope(maxY_vertex, maxX_vertex)
            degree = round(math.atan(slope) * 180/math.pi)
            if degree == 90:
                degree = 0
            print(degree)
            f.write(img[k:len(img)-4] + ", " + str(degree) + '\n')

    f.close()

if __name__ == '__main__':
  app.run(main)