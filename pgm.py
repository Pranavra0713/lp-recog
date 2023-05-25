import cv2,os,csv,imutils,pytesseract
output_csv_file = open('output.csv', 'w')
csv_writer = csv.writer(output_csv_file)
csv_writer.writerow(['Filename', 'License Plate'])
for i in os.listdir('input'):
    image = cv2.imread('input/' + i)
    image = imutils.resize(image, width=500)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    edged = cv2.Canny(gray_image, 30, 200)
    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, cnts, -1, (0, 255, 0), 3)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    screenCnt = None
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx
            x, y, w, h = cv2.boundingRect(c)
            plate_img = image[y:y + h, x:x + w]
            cv2.imwrite('plate.png', plate_img)
            break
    if screenCnt is not None:
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
    plate_text = pytesseract.image_to_string(plate_img)
    plate_text = ''.join([c for c in plate_text if c.isalnum()])
    csv_writer.writerow([i,plate_text])
output_csv_file.close()
