# -*- coding: utf-8 -*-
"""Copy of Copy of CV2_Haar_16_04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C93Nev1Jclz6dy8RNHpZDnEJrYxQQxCU
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install pytesseract

!sudo apt update
!sudo apt install tesseract-ocr
!sudo apt install libtesseract-dev

# Commented out IPython magic to ensure Python compatibility.
import os
import cv2
import numpy as np
import pickle
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.transform import resize
from skimage.io import imshow
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import pytesseract
# %matplotlib inline

image_path1 = '/content/drive/My Drive/CarNumberPlate/009.jpg'
image_path2 = '/content/drive/My Drive/CarNumberPlate/003.jpg'
image_path3 = '/content/drive/My Drive/CarNumberPlate/004.jpg'
#image_path4 = '/content/drive/My Drive/CarNumberPlate/Damage Validation/training/01-whole/1009.png'
image_path5 = '/content/drive/My Drive/CarNumberPlate/002.jpg'
image_path6 = '/content/drive/My Drive/CarNumberPlate/001.jpg'
image_path7 = '/content/drive/My Drive/CarNumberPlate/HD/1.jpg'
image_path8 = '/content/drive/My Drive/CarNumberPlate/NHD/1.JPG'

img = cv2.imread(image_path8)

img.shape

if ((img.shape[0]!=510) and (img.shape[1]!=827)):
  dim =(827,510)
  img = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)

img.shape

temp = cv2.imread(image_path6, 0)

temp.shape

def display(img):
  fig = plt.figure(figsize=(10, 8))
  ax = fig.add_subplot(111)
  new_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  ax.imshow(new_img)

display(img)

plate_cascade = cv2.CascadeClassifier('/content/drive/My Drive/CarNumberPlate/haarcascade_russian_plate_number.xml')

plate_cascade.empty()

def detect_plate(img):
  plate_image = img.copy()
  
  plate_rects = plate_cascade.detectMultiScale(plate_image, scaleFactor=1.13, minNeighbors = 3)
  
  for (x,y,w,h) in plate_rects:
    cv2.rectangle(plate_image, (x,y), (x+w, y+h), (0,0,255), 4)
    
  return plate_image

result = detect_plate(img)

plate_image = img.copy()
plate_rects = plate_cascade.detectMultiScale(plate_image, scaleFactor=1.13, minNeighbors = 3)

plate_rects

x = plate_rects[0][0]
y = plate_rects[0][1]
w = plate_rects[0][2]
h = plate_rects[0][3]
print (x,y,w,h)
#x= x-20

display(result)

x1 = x + w
y1 = y + h

plate1 = img[y:y1, x:x1]

plate2=cv2.blur(plate1, (3, 3))

imshow(plate1)
imshow(plate2)

cv2.imwrite('/content/drive/My Drive/CarNumberPlate/plate.jpg', plate1)

img = cv2.cvtColor(plate1, cv2.COLOR_BGR2GRAY)

kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
img=cv2.blur(img, (5, 5))
#cv2.imwrite('/content/drive/My Drive/CarNumberPlate/plate1.jpg', plate)
imshow(img)

result = pytesseract.image_to_string(plate1)

result

result = pytesseract.image_to_string(plate2)

result

result = pytesseract.image_to_string(img)

result

import imutils
from skimage import measure
from skimage.measure import regionprops
from skimage.filters import threshold_otsu

labels = measure.label(plate, neighbors=8)
charCandidates = np.zeros(plate.shape, dtype="uint8")

imshow(labels)

len(regionprops(labels))

for label in np.unique(labels):
  if label == 0:
    continue
  labelMask = np.zeros(plate.shape, dtype="uint8")
  labelMask[labels == label] = 255
  cnts = cv2.findContours(labelMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if imutils.is_cv2() else cnts[1]

cv2.imwrite('/content/drive/My Drive/Car Insurance/License Plate/plate.jpg', plate)

plate2 = cv2.imread('/content/drive/My Drive/Car Insurance/License Plate/plate.jpg', 0)

plate2.shape

char_plate = resize(plate, (20, 20))

char_plate.shape

imshow(char_plate)

characters = []
characters.append(char_plate)

characters

# Gives first character
column_list = []
column_list.append(x)

letters = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
          ]

def read_training_data(training_directory):
  image_data = []
  target_data = []
  for each_letter in letters:
    for each in range(10):
      image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.jpg')
      # read each image of each character
      img_details = imread(image_path, as_grey=True)
      # converts each character image to binary image
      binary_image = img_details < threshold_otsu(img_details)
      # Flattening the 2D array of each image
      flat_bin_image = binary_image.reshape(-1)
      image_data.append(flat_bin_image)
      print(img_details.shape)
      target_data.append(each_letter)
      
  return (np.array(image_data), np.array(target_data))

def cross_validation(model, num_of_fold, train_data, train_label):
  accuracy_result = cross_val_score(model, train_data, train_label,
                                      cv=num_of_fold)
  print("Cross Validation Result for ", str(num_of_fold), "fold")

  print(accuracy_result * 100)

training_dataset_dir = '/content/drive/My Drive/Car Insurance/License Plate/train20X20'
image_data, target_data = read_training_data(training_dataset_dir)

svc_model = SVC(kernel='linear', probability=True)
cross_validation(svc_model, 4, image_data, target_data)

svm_model = SVC(kernel='linear', probability=True)
svm_model.fit(image_data, target_data)

#with open('/content/drive/My Drive/Car Insurance/License Plate/numberplate_SVM.pickle', 'wb') as model:
  #pickle.dump(svm_model, model)
with open('/content/drive/My Drive/Car Insurance/License Plate/numberplate_SVM.pickle', 'rb') as model:
  svm_model = pickle.load(model)

classification_result = []

for each_character in characters:
  each_character = each_character.reshape(1,-1)
  print(each_character.shape)

for each_character in characters:
  each_character = each_character.reshape(1,-1)
  result = svm_model.predict(each_character)
  classification_result.append(result)

classification_result

import imutils
from skimage import measure
from skimage.measure import regionprops
from skimage.filters import threshold_otsu
import matplotlib.patches as patches

grey_image = imread(image_path1, as_grey = True)

def threshold(grey_image):
  thresholdValue = threshold_otsu(grey_image)
  return grey_image > thresholdValue

binary_image = threshold(grey_image)

binary_image

def get_platelike_objects(binary_image, grey_image):
  count = 0
  label_image = measure.label(binary_image)
  plate_objects_cordinates = []
  threshold = binary_image
  plate_like_objects = []
  for region in regionprops(label_image):
    minimumRow, minimumCol, maximumRow, maximumCol = region.bbox
    regionHeight = maximumRow - minimumRow
    regionWidth = maximumCol - minimumCol
    if regionHeight <= h+50 and regionHeight >= h-50 and regionWidth <= w+50 and regionWidth >= w-50:
      count = count + 1
      plate_like_objects.append(binary_image[minimumRow:maximumRow, minimumCol:maximumCol])
      plate_objects_cordinates.append((minimumRow, minimumCol, maximumRow, maximumCol)) 
  rectBorder = patches.Rectangle((minimumCol, minimumRow), maximumCol - minimumCol, maximumRow - minimumRow, edgecolor="red",
                                  linewidth=2, fill=False)
  return plate_like_objects, rectBorder, count

def modify_threshold(grey_image):
  threshold_value = threshold_otsu(grey_image) - 0.05
  return grey_image < threshold_value

def more_plate_objects(plate_like_objects):
  for plate in plate_like_objects:
    height, width = plate.shape
    plate = modify_threshold(plate)
    number_plate = []
    highest_average = 0
    total_white_pixels = 0
    for column in range(width):
      total_white_pixels += sum(plate[:, column])
    average = float(total_white_pixels) / width
    if average >= highest_average:
      number_plate = plate
      
  return number_plate

def plot_image(grey_image):
  binary_image = threshold(grey_image)
  plate_like_objects, rectBorder, count = get_platelike_objects(binary_image, grey_image)
  if (len(plate_like_objects) == 0):
    print('No number plate detected')
  if (len(plate_like_objects) > 1):
    plate_like_objects = more_plate_objects(plate_like_objects)
    #plate_like_objects = plate_like_objects[0]
  else:
    plate_like_objects = plate_like_objects[0]
  fig, (ax1) = plt.subplots(1)
  print('count is', count)
  print(plate_like_objects)
  ax1.imshow(grey_image, cmap="gray")
  ax1.add_patch(rectBorder)
  plt.show()

plot_image(grey_image)

def get_characters(binary_image, grey_image):
  binary_image = threshold(grey_image)
  plate_like_objects, rectBorder, count = get_platelike_objects(binary_image, grey_image)
  if (len(plate_like_objects) == 0):
    print('No number plate detected')
  if (len(plate_like_objects) > 1):
    plate_like_objects = more_plate_objects(plate_like_objects)
    #plate_like_objects = plate_like_objects[0]
  else:
    plate_like_objects = plate_like_objects[0]
  print(len(plate_like_objects))
  license_plate = np.invert(plate_like_objects)
  roi = license_plate[y:y1, x:x1]
  resized_char = resize(roi, (20, 20))
  characters.append(resized_char)
  
  return characters, count

classification_result = []
def pred_characters(binary_image, grey_image):
  characters, count = get_characters(binary_image, grey_image)
  print(count)
  for each_character in characters:
    # converts it to a 1D array
    each_character = each_character.reshape(1, -1);
    result = svm_model.predict(each_character)
    classification_result.append(result)
  return classification_result

pred_characters(binary_image, grey_image)

