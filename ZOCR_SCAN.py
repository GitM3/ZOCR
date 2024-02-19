from imutils.perspective import four_point_transform
import pytesseract
import argparse
import imutils
import cv2
import re

def scanImage(image):
    original = image.copy()
    reducedImage = image.copy()
    reducedImage = imutils.resize(reducedImage,width=500)
    ratio = original.shape[1] / float(reducedImage.shape[1])
    gray  = cv2.cvtColor(reducedImage,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(5,5),0)
    edges  = cv2.Canny(blurred,75,200)
    contours = cv2.findContours(edges.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours,key=cv2.contourArea,reverse=True) # Largest contour first is receipt

    receiptContour = None
    for c in contours:
        perimeter = cv2.arcLength(c,True) # Lenght of closed contours
        approximated = cv2.approxPolyDP(c,0.02 * perimeter, True)
        if len(approximated) == 4: # four vertices to outline receipt
            receiptContour = approximated
            break
    if receiptContour is None:
        raise Exception("NO RECEIPT OUTLINE FOUND")
    
    receiptTransformed = four_point_transform(original,receiptContour.reshape(4,2) * ratio)
    receiptTransformed = cv2.cvtColor(receiptTransformed,cv2.COLOR_BGR2GRAY)
    receiptTransformed = cv2.GaussianBlur(receiptTransformed,(5,5),0)
    receiptTransformed = cv2.adaptiveThreshold(receiptTransformed,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,4)

    returnText = []
    options = "--psm 4"
    text = pytesseract.image_to_string(receiptTransformed,config=options)
    pricePattern = r'([0-9]+[\.,][0-9])'
    for row in text.split("\n"):
        if re.search(pricePattern,row) is not None:
            cleaned_row = re.sub(r'([\.,][0-9]{2}).*$', r'\1', row) # remove trailing characters
            cleaned_row = re.sub(r'[:|$%]','',cleaned_row) # remove special char (keep &)
            returnText.append(cleaned_row)
            if "TOTAL" in row.upper():
                break# row
    output = reducedImage.copy()
    cv2.drawContours(output, [receiptContour], -1, (0, 255, 0), 2)
    return returnText, output