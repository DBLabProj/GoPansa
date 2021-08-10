'''
21.08.05

'''
import cv2
import numpy as np

def stayPork(imagename, savedir):
    src = cv2.imread(imagename, cv2.IMREAD_COLOR)
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    dst2= dst.copy()
    size = ( 300, 600 )

    # thr = cv2.resize( dst2, size )
    # cv2.imshow("dst", dst2)
    # cv2.waitKey(0)

    ret, thr = cv2.threshold(dst, 100, 255, cv2.THRESH_BINARY) 

    # thr2 = thr.copy()
    # thr2 = cv2.resize( thr2, size )
    # cv2.imshow("threshold", thr2)
    # cv2.waitKey(0)

    ksize = 4
    kernel = np.ones((ksize, ksize),np.uint8)
    erosion = cv2.erode(thr, kernel,iterations = 2)

    # erosion2 = erosion.copy()
    # erosion2 = cv2.resize( erosion2, size )
    # cv2.imshow("erosion", erosion2)
    # cv2.waitKey(0)

    ero = cv2.cvtColor(erosion, cv2.COLOR_GRAY2BGR) // 255
    new = cv2.multiply( src , ero)

    new = cv2.resize( new, size )
    cv2.imshow("new", new)
    cv2.waitKey(0)

    return 0


if __name__ == "__main__":
    impath = "./sample/pig/croppedd/"
    imname = "QC_pig_segmentation_1_000010_crop"  + ".jpg"
    savedd = "./sample/pig/stay/"

    # checkSegShow(impath, imname, jpath, jname)
    stayPork(impath + imname, savedd )
