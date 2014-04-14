from Tkinter import *
from ttk import  *
import cv2
from multiprocessing import Process, Queue
from PIL import Image, ImageTk

cam = cv2.VideoCapture(0)

class system(Frame):
	def initUI(self):
		self.parent.title("Windows")
		self.style = Style()
		self.style.theme_use("default")
		self.pack(fill=BOTH, expand=1)

		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=7)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(5, pad=7)

		self.image_label = Label(self, text="live stream")
		self.image_label.grid(sticky=W, pady=4, padx=5)

		self.update_database_button = Button(self, text="Update Database")
		self.update_database_button.grid(row=1, column=3)

		self.catch_button = Button(self, text="Catch", command = self.catch_image)
		self.catch_button.grid(row=5, column=0, padx=5)

		#self.obtn = Button(self, text="OK")
		#self.obtn.grid(row=5, column=3)


	def catch_image(self):
		ret,img = cam.read()
		cv2.imwrite("blabla.jpg",img)
		photo =PhotoImage(file='blabla.jpg')
		self.image_label.configure(image = photo).pack()

	def update_image(self):
		(flag, frame) = self.cam.read()
		im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		a = Image.fromarray(im)
		b = ImageTk.PhotoImage(image=a)
		self.image_label.configure(image=b)
		self.image_label._image_cache = b  # avoid garbage collection
		#Frame.after(0, func=lambda: self.update_image(self))

	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()
		#self.image_process = Process(target = self.update_image,args = ())
		#self.image_process.start()
		#self.image_process.join()

def main():

    root = Tk()
    root.geometry("400x300+300+300")
    app = system(root)
    root.mainloop()


if __name__ == '__main__':
    main()
