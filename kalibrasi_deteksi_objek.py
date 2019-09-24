import cv2.cv as cv     # import libarary openCV
import time
capture = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture,3,640)
cv.SetCaptureProperty(capture,4,480)
time.sleep(2)

while True:
    img = cv.QueryFrame(capture)
    cv.Smooth(img,img,cv.CV_BLUR,3)
    hue_img = cv.CreateImage(cv.GetSize(img),8,3)
    cv.CvtColor(img,hue_img,cv.CV_BGR2HSV)
    threshold_img=cv.CreateImage(cv.GetSize(hue_img),8,1)
    cv.InRangeS(hue_img,(0,150,0),(5,255,255),threshold_img)
    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(threshold_img,storage,cv.CV_RETR_CCOMP,cv.CV_CHAIN_APPROX_SIMPLE)
    points = []
    while contour:
        rect = cv.BoundingRect(list(contour))

        # konversi koordinat objek menjadi karakter yang dikirimkan ke arduino
        if rect[0]>426.67 and rect[0]<640.0 and rect[1]>0.0 and rect[1]<240.0:
            print ('BELOK KANAN SEDANG')

        if rect[0]>426.67 and rect[0]<640.0 and rect[1]>240.0 and rect[1]<480.0:
            print ('BELOK KANAN CURAM')

        if rect[0]>213.33 and rect[0]<426.67 and rect[1]>0.0 and rect[1]<240.0:
            print ('MAJU KEDEPAN')

        if rect[0]>213.33 and rect[0]<426.67 and rect[1]>240.0 and rect[1]<480.0:
            print ('DIAM')

        if rect[0]>0.0 and rect[0]<213.33 and rect[1]>0.0 and rect[1]<240.0:
            print ('BELOK KIRI SEDANG')

        if rect[0]>0.0 and rect[0]<213.33 and rect[1]>240.0 and rect[1]<480.0:
            print ('BELOK KIRI CURAM')
        
        contour = contour.h_next()
        size = (rect[2]*rect[3])
        if size > 100:
            pt1 = (rect[0],rect[1])
            pt2 = (rect[0]+rect[2],rect[1]+rect[3])
            cv.Rectangle(img,pt1,pt2,(38,160,60))

    cv.ShowImage("Colour Tracking",img)
    if cv.WaitKey(10)==27:
        break
