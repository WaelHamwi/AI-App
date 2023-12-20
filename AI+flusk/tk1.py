# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 13:12:18 2022

@author: WAEL
"""
#import lib
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import cv2
import tensorflow as tf
import numpy as np
from PIL import ImageTk, Image

#import model
print('_________________________________')
print('..........Start loading..........')

model = tf.keras.models.load_model('32x2x0CNN.model')

print('_________________________________')
print('...........Model Loaded..........')
print('_________________________________')

# dictionary to label all traffic signs class.
labels = ['Covid', 'Normal']

# initialise GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Covid-19_Normal Classification')
top.configure(background='#CDCDCD')
label = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)

#To classify an image
def classify(file_path):
    global label_packed
    image =cv2.imread(file_path,cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (500,500))
    image = image / 255.0
    image = image.reshape(-1,500,500,1)
    prediction = model.predict(image)
    x = round(prediction[0,0], 2)
    preds = np.array([x])
    sign = labels[np.argmax(preds)]
    if prediction <0.5:
      label.configure(fg='red', text="covid")
    else:
      label.configure(fg='green', text="Normal")     
    print(preds)
    print(sign)
    

#Button
def show_classify_button(file_path):
    classify_b = Button(top, text="Classify Image",
                        command=lambda: classify(file_path),
                        padx=10, pady=5)
    classify_b.configure(background='#364156', foreground='white',
                         font=('arial', 10, 'bold'))
    classify_b.place(relx=0.79, rely=0.46)

#Upload image
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),
                            (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass

upload = Button(top, text="Upload an image",
                command=upload_image, padx=10, pady=5)
upload.configure(background='#364156', foreground='white',
                 font=('arial', 10, 'bold'))
upload.pack(side=BOTTOM, pady=50)
sign_image.pack(side=BOTTOM, expand=True)
label.pack(side=BOTTOM, expand=True)
heading = Label(top, text="Image Classification",
                pady=20, font=('arial', 20, 'bold'))
heading.configure(background='#CDCDCD', foreground='#364156')
heading.pack()
top.mainloop()
