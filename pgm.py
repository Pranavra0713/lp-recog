import cv2, os, csv, imutils, pytesseract, tkinter as tk
from PIL import ImageTk, Image

output_csv_file = open('output.csv', 'w')
csv_writer = csv.writer(output_csv_file)
csv_writer.writerow(['Filename', 'License Plate'])
os.makedirs('out', exist_ok=True)

def process_images():
    for i in os.listdir('input'):
        image = cv2.imread('input/' + i)
        image = imutils.resize(image, width=500)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
        edged = cv2.Canny(gray_image, 30, 200)
        cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
                plate_filename = 'plate' + i
                cv2.imwrite(os.path.join('out', plate_filename), plate_img)
                break
        if screenCnt is not None:
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
        plate_text = pytesseract.image_to_string(plate_img)
        plate_text = ''.join([c for c in plate_text if c.isalnum()])
        csv_writer.writerow([i, plate_text])
    output_csv_file.close()
    display_results()

def display_results():
    results_window = tk.Toplevel()
    results_window.title("License Plate Recognition Results")
    w=60
    text_widget = tk.Text(results_window, height=30, width=w)
    text_widget.pack()
    photo_images = []  # List to store references to PhotoImage objects so that garbage collection of images will be avoided
    actual_images = []
    text_widget.tag_configure('center', justify='center')
    with open('output.csv', 'r') as file:
        csv_reader = csv.reader(file)
        rows = [row for row in csv_reader if any(field.strip() for field in row)]
    with open('output1.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
    with open('output1.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the first line (header row)
        for row in csv_reader:
            plate_image_filename = f"plate{row[0]}"
            plate_image =  Image.open(f"out/{plate_image_filename}")
            plate_image.thumbnail((400, 400))  # Resize the image
            plate_image = ImageTk.PhotoImage(plate_image)
            photo_images.append(plate_image)  # Store reference to PhotoImage object

            actual_image_filename = f"{row[0]}"
            actual_image = Image.open(f"input/{actual_image_filename}")
            actual_image.thumbnail((400, 400))  # Resize the image
            actual_image = ImageTk.PhotoImage(actual_image)
            actual_images.append(actual_image)
            text_widget.image_create(tk.END, image=actual_image)
            text_widget.insert(tk.END, "\n",'center')

            text_widget.insert(tk.END, f"Filename: {row[0]}\n",'center')

            text_widget.insert(tk.END, f"License Plate: {row[1]}\n",'center')

            text_widget.image_create(tk.END, image=plate_image)
            text_widget.insert(tk.END, "\n",'center')

            separator_line = "-" * w
            text_widget.insert(tk.END, f"{separator_line}\n\n")
    # Keep a reference to the PhotoImage objects to prevent them from being garbage collected
    text_widget.photo_images = photo_images
    text_widget.actual_images = actual_images
window = tk.Tk()
window.title("License Plate Recognition")
button = tk.Button(window, text="Start Recognition", command=process_images)
button.pack()
window.mainloop()
