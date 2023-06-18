Prerequisites:
the following must be installed
- sudo pacman -S tesseract  
- sudo pacman -S tesseract-data-eng   
- pip install opencv-python   
- pip install imutils   
- pytesertact
- pip install tk

This mini project showcases the application of digital image processing techniques to detect and read number plates from a collection of input images stored in the 'input' folder. 
  Each image will be processed individually, and the identified license plate will be extracted using Tesseract OCR. 
  The extracted plate information will be saved in a structured format within the 'output.csv' file. 
  Additionally, the recognized plates will be stored in the 'out' folder, enabling further processing if desired.

To enhance user experience, a user-friendly front-end interface has been developed. 
  The interface elegantly presents the extracted information, including the image filename, the recognized license plate, and the corresponding plate image. 
  The layout and design ensure readability and orderly presentation of the results, facilitating efficient analysis of the processed images.

With this project, you can explore the capabilities of digital image processing for number plate recognition while enjoying a user-friendly interface that provides clear and organized information for each processed image.
