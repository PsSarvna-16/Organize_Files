import os 
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog

#--------------------------------------------------------------------------------------------------------------------
window = tk.Tk()
window.title("PsSarvna")
window.geometry("500x400")
window.minsize(width = "600" , height = "500")
window.maxsize(width = "600" , height = "500")


daterb = tk.StringVar()
Inc_check = tk.BooleanVar()

def get_src_direct():
	src = filedialog.askdirectory()
	Src_entry.delete(0, tk.END)
	Src_entry.insert(0 , src)

def get_des_direct():
	des = filedialog.askdirectory()
	Des_entry.delete(0, tk.END)
	Des_entry.insert(0 , des)

def Pre_unsort():
	Des_browse.configure(state = "disabled")
	Des_entry.configure(state = "disabled")

def sort_files_button():
	src = Src_entry.get()
	des = Des_entry.get()
	datetime = daterb.get()
	Inc_sub = Inc_check.get()
	if datetime == "ext":
		Ext_Sort = True
		Ext_Spec = False
	elif datetime == "extspec":
		Ext_Spec = True
		Ext_Sort = False
	else:
		Ext_Sort = False
		Ext_Spec = False
	Sort_files(src ,des, datetime , Inc_sub, Ext_Sort ,Ext_Spec)
	

	


#--------------------------------------------------------------------------------------------------------------------

Images = ["Images" , ".jpg" , ".png" , ".gif" , "jpeg"]
Videos = ["Videos" , ".mp4" , ".mpeg" , ".avi" , ".mkv"]
Audio = ["Audio" , ".mp3" , ".wma" , ".amr" ]
Softwares = ["Softwares" , ".exe"]

Ext = [Images , Videos , Audio, Softwares ]

#--------------------------------------------------------------------------------------------------------------------

def Sort_files(src, des, Datetime , Inc_sub, Ext_Sort ,Ext_Spec ): 
	
	"""
	Function Process Step by step:
			1. get lis of files in Src folder
			2. Iterate through files
			3. Get extension of each file
			4. if the file is directory (This Works if Inc_Sub is True)
					- call same function as recursive using foldername as source
			5. if it is file.
			6. Types of Sorting (According to Boolean inputs) - Determine Folder names
					a)  Ext_Spec = True
							- Sort files as (Audio ,Video , Images) by checking Predefined Ext list
					b) Ext_Sort  =True
							- Sort files as their extension of the file.
					c)  Else 
							- Sort with Modified time (month and year / year - determined by Datetime) 
			7. check folder is presen or Create folder
			8. Move files to destination
			9.If there is Conflicts:
				--Create Conflicts folder
				--create folder with mtime 
				--move to that folder
	"""
	
	files = os.listdir(src)
	for file in files:
		extension = os.path.splitext(file)[1]
		if os.path.isfile(os.path.join(src , file)):
			if Ext_Spec:
				find = False
				for lists in Ext:
					if extension in lists:
						fname = lists[0]
						find = True
				if not find:
					fname = "Others"
					find = False

			elif Ext_Sort:
				fname = os.path.splitext(file)[1].split(".")[1]
			else:
				dtime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(src , file)))
				fname = dtime.strftime(Datetime)

			if fname not in os.listdir(des):
					os.mkdir(os.path.join(des , fname))

			try :
				shutil.move(os.path.join(src , file) , os.path.join(des , fname))
			except:
				#Xfname = "Conflicts"
				#Xdes = "C:\\Users\\Ps_Sarvna\\Desktop\\Des\\Conflicts"
				#if Xfname not in os.listdir(des):
				#	os.mkdir(os.path.join(des , Xfname))
				#if fname not in os.listdir(Xdes):
				#	os.mkdir(os.path.join(Xdes , fname))
				#try:	
				#	shutil.move(os.path.join(src , file) , os.path.join(Xdes , fname))
				#except:
				pass
		
		else:
			if Inc_sub:
				if os.path.isdir(os.path.join(src , file)):
					Sort_files(os.path.join(src , file),des, Datetime , Inc_sub, Ext_Sort ,Ext_Spec )
					try:
						os.rmdir(os.path.join(src , file))
					except:
						pass
		

#--------------------------------------------------------------------------------------------------------------------

gui_title = tk.Label(text = "Organize files" , fg = "black", font= ("Fixedsys",24) )
gui_title.place(x =200 , y = 30)


Radio_btn1 = tk.Radiobutton(window,text="Sort - Month/Year" , value = "%b_%Y" , variable = daterb)
Radio_btn1.place(x =100 , y = 130)
Radio_btn2 = tk.Radiobutton(window,text="Sort - Year      ." , value = "%Y", variable = daterb)
Radio_btn2.place(x =100 , y = 170)
Radio_btn3 = tk.Radiobutton(window,text="Sort - Ext       ." , value = "ext", variable = daterb)
Radio_btn3.place(x =100 , y = 210)
Radio_btn4 = tk.Radiobutton(window,text="Sort - Ext-Spec  " , value = "extspec", variable = daterb)
Radio_btn4.place(x =100 , y = 250)

Src_entry = tk.Entry(window ,width = 40)
Src_entry.place(x =50 , y = 320)
Src_browse = tk.Button(window,text = "Browse" , command = get_src_direct)
Src_browse.place(x =300 , y = 315)
Submit = tk.Button(window,text = "Submit" , command = sort_files_button )
Submit.place(x =435 , y = 330)




Des_entry = tk.Entry(window,width = 40)
Des_entry.place(x =50 , y = 360)
Des_browse = tk.Button(window,text = "Browse" , command = get_des_direct)
Des_browse.place(x =300 , y = 355)

Inc_chec = tk.Checkbutton(text = "Include Folders" , onvalue = True , offvalue  = False , variable = Inc_check)
Inc_chec.place(x =375 , y = 235)

window.mainloop()


#--------------------------------------------------------------------------------------------------------------------
"""
Radio_btn5 = tk.Radiobutton(text="UnSort" , value = "Unsort", variable = un_sort , command = Pre_unsort)
Radio_btn5.pack()


Un_Ext = [".jpg"]


def Unsort_files(src):

	fname = "UnSorted"
	if Orig_src == src :
		if fname not in os.listdir(Orig_src):
			os.mkdir(os.path.join(Orig_src, fname))
	files = os.listdir(src)

	for file in files:
		extension = os.path.splitext(file)[1]
		if os.path.basename(file) == fname:
			continue
		
		if os.path.isfile(os.path.join(src , file)):
			if Ext_Unsort:
				if extension not in Un_Ext:
					continue
			shutil.move(os.path.join(src , file) , os.path.join(Orig_src, fname))
		else:
			Unsort_files(os.path.join(src , file))
			try:
				os.rmdir(os.path.join(src , file))
			except:
				pass

"""