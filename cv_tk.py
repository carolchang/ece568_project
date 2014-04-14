import numpy as np
from multiprocessing import Process, Queue
from Queue import Empty
import cv2
import cv2.cv as cv
from PIL import Image, ImageTk
import time
import Tkinter as tk
from apiclient.discovery import build
import time
import os
import sys
import tkSimpleDialog

cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')

#tkinter GUI functions----------------------------------------------------------
def quit_(root, processes):
	for process in processes:
		process.terminate()
	root.destroy()

def update_vedio_frame(root, image_label, queue):
	frame = queue.get()
	im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	a = Image.fromarray(im)
	b = ImageTk.PhotoImage(image=a)
	vedio_label.configure(image=b)
	vedio_label._image_cache = b  # avoid garbage collection
	root.update()
	root.after(0, func=lambda: update_vedio_frame(root, image_label, queue))

#multiprocessing vedio processing function
def image_capture(queue):
	while True:
		try:
			flag, frame=cam.read()
			if flag==0:
				break
			frame = cv2.resize(frame,(frame.shape[1]/2,frame.shape[0]/2))
			queue.put(frame)
			cv2.waitKey(20)
			time.sleep(0.25)
		except:
			continue
	

#capture a frame
def capture(root):
    frame = queue.get()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4,4))
    clear_grey = clahe.apply(gray)

    faces = face_cascade.detectMultiScale(clear_grey, 1.3, 5)
    if faces is not []:
		for x,y,w,h in faces:
			#print x,y,w,h
			x,y,w,h = wider_area(x,y,w,h)
			#print x,y,w,h
			frame = frame[y:y+h,x:x+w]
			clear_grey = clear_grey[y:y+h,x:x+w]
			im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			a = Image.fromarray(im)
			b = ImageTk.PhotoImage(image=a)
			image_label.configure(image=b)
			image_label._image_cache = b  # avoid garbage collection
			root.update()

			cv2.imwrite('temp.jpg',frame)
			#save_image_process.terminate
			#save_image_process.start()
			save_image(root)
			
def save_image(root):
	frame = cv2.imread('temp.jpg')
	name = tkSimpleDialog.askstring("String", "Enter a String")
	#name = getText('Whos is this guy?')
	#cv2.imshow('clear grey image', clear_grey)
	#cv2.waitKey(0)
	dir_path = 'database/'+name

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
		print 'batabase for %s created'%name

	path, dirs, files = os.walk(dir_path).next()
	num_of_image_exits = len(files)
	print '%i images for %s'%(num_of_image_exits,name)

	cv2.imwrite('%s/%s_%i.jpg'%(dir_path,name,num_of_image_exits), frame)
	os.remove('temp.jpg')

def wider_area(x,y,w,h):
	wider = 25
	if x > wider : new_x = x - wider
	else: new_x = 0

	if y > wider : new_y = y - wider
	else : new_y = 0

	if x+w < 240-wider: new_w = w + 2*wider
	else: new_w = 239-new_x
	if y+h < 320-wider: new_h = h + 2*wider
	else: new_h = 319-new_y

	return [new_x,new_y,new_w,new_h]

def print_foo(queue):
	frame = queue.get
	print frame
	time.sleep(5)
	print_foo(queue)

	
if __name__ == '__main__':
	queue = Queue()
	root = tk.Tk()
	#vedio_label
	vedio_label = tk.Label(master=root)# label for the video frame
	vedio_label.pack()
	
	capture_process = Process(target=image_capture, args=(queue,))
	capture_process.start()
	
	# quit button
	quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,[capture_process]))
	quit_button.pack()
	# capture button
	capture_button = tk.Button(master=root, text='Capture',command=lambda: capture(root)).pack()
	# image label
	image_label = tk.Label(master = root)
	image_label.pack()
	
	save_image_process = Process(target = save_image,args=(root, ))
	
	root.after(0, func=lambda: update_vedio_frame(root, vedio_label, queue))
	
	root.mainloop()
	capture_process.join()

