import os 
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

window = tk.Tk()
window.title("PsSarvna")
window.geometry("500x400")
window.minsize(width = "600" , height = "500")
window.maxsize(width = "600" , height = "500")

#--------------------------------------------------------------------------------------------------------------------

Inc_check = tk.BooleanVar()
Over_check = tk.BooleanVar()
copy = tk.BooleanVar()

Images = ["Images" , ".jpg" , ".png" , ".gif" , "jpeg"]
Videos = ["Videos" , ".mp4" , ".mpeg" , ".avi" , ".mkv"]
Audio = ["Audio" , ".mp3" , ".wma" , ".amr" ]
Softwares = ["Softwares" , ".exe"]


Ext = [Images , Videos , Audio, Softwares ]
#--------------------------------------------------------------------------------------------------------------------

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

def sort_pre():
	Des_browse.configure(state = "normal")
	Des_entry.configure(state = "normal")

def Reset_Variables():
	Des_entry.delete(0, tk.END)
	Src_entry.delete(0, tk.END)
	Combo_sort.set('')
	Inc_check.set(False)
	Over_check.set(False)
	copy.set(False)


def sort_files_button():
	src = Src_entry.get()
	des = Des_entry.get()
	Sort_type = Combo_sort.get()
	Copy  = copy.get()
	sort_type = ["FileType" , "Extensions" , "Year" , "Mon_Year"]

	if len(Sort_type) < 2:
		print(Sort_type)
		tk.messagebox.showerror("Error!", "Select any one type.")
		return
	if Sort_type not in sort_type:
		tk.messagebox.showerror("Error!", "Select Valid Type")

	if not os.path.isdir(src):
		tk.messagebox.showerror("Error!", "Select Valid Source Directory")
		return

	if not os.path.isdir(des):
		tk.messagebox.showerror("Error!", "Select Valid Destination Directory")
		return



	Inc_sub = Inc_check.get()
	OverWrite = Over_check.get()
	Orig_src = src
	if datetime == "unsort":
		fname = "UnSorted"
		if Orig_src == src :
			if fname not in os.listdir(src):
				os.mkdir(os.path.join(src, fname))
			Unsort_files(src , src, Inc_sub  , OverWrite, Copy )
			return

	Sort_files(src ,des, Inc_sub,Sort_type, OverWrite ,Copy)

#--------------------------------------------------------------------------------------------------------------------


def Sort_files(src, des,  Inc_sub,Sort_type ,OverWrite ,Copy  ): 
	
	files = os.listdir(src)
	for file in files:
		extension = os.path.splitext(file)[1]
		if os.path.isfile(os.path.join(src , file)):
			
			if Sort_type == "Extensions":
				fname = os.path.splitext(file)[1].split(".")[1]
			elif Sort_type == "FileType":
				find = False
				for lists in Ext:
					if extension in lists:
						fname = lists[0]
						find = True
				if not find:
					fname = "Others"
					find = False
			elif Sort_type == "Mon_Year":
				dtime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(src , file)))
				fname = dtime.strftime("%b_%Y")
			elif Sort_type == "Year":
				dtime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(src , file)))
				fname = dtime.strftime("%Y")
			else:
				return 


			if fname not in os.listdir(des):
					os.mkdir(os.path.join(des , fname))

			try :
				if not Copy:
					shutil.move(os.path.join(src , file) , os.path.join(des , fname))
				else:
					try:
						shutil.copy2(os.path.join(src , file) ,os.path.join(os.path.join(des , fname),file))
					except:
						pass
			except:
				if OverWrite:
					try:
						shutil.move(os.path.join(src , file) , os.path.join(os.path.join(des , fname),file))
					except:
						pass
		else:
			if Inc_sub:
				if os.path.isdir(os.path.join(src , file)):
					Sort_files(os.path.join(src , file),des, Inc_sub,Sort_type, OverWrite ,Copy  )
					try:
						os.rmdir(os.path.join(src , file))
					except:
						pass


def Unsort_files(Orig_src , src, Inc_sub , OverWrite,Copy):

	fname = "UnSorted"
	files = os.listdir(src)
	for file in files:
		extension = os.path.splitext(file)[1]
		if os.path.basename(file) == fname:
			continue
		
		if os.path.isfile(os.path.join(src , file)):
			#if Ext_Unsort:
			#	if extension not in Un_Ext:
			#		continue
			try :
				if not Copy:
					shutil.move(os.path.join(src , file) , os.path.join(Orig_src , fname))
				else:
					try:
						shutil.copy2(os.path.join(src , file) ,os.path.join(os.path.join(Orig_src , fname),file))
					except:
						pass
			except:
				if OverWrite:
					try:
						shutil.move(os.path.join(src , file) , os.path.join(os.path.join(Orig_src , fname),file))
					except:
						pass

		else:
			if Inc_sub:
				Unsort_files(Orig_src, os.path.join(src , file), Inc_sub , OverWrite,Copy )
				try:
					os.rmdir(os.path.join(src , file))
				except:
					pass


#--------------------------------------------------------------------------------------------------------------------

gui_title = tk.Label(text = "Organize files" , fg = "black", font= ("Fixedsys",24) )
gui_title.place(x =200 , y = 30)


step1_lb = tk.Label(text = "Step 1: Select the Type" , fg = "black", font= ("Fixedsys") )
step1_lb.place(x =35 , y = 100)
step2_lb = tk.Label(text = "Step 2: Select Preferred Option" , fg = "black", font= ("Fixedsys") )
step2_lb.place(x =300 , y = 100)
step3_lb = tk.Label(text = "Step 3: Select Directories" , fg = "black", font= ("Fixedsys") )
step3_lb.place(x = 35 , y = 280)
step4_lb = tk.Label(text = "Step 4: Submit/Reset" , fg = "black", font= ("Fixedsys") )
step4_lb.place(x = 380 , y = 280)

sort_lb = tk.Label(text = "Sorting Types : " , fg = "black", font= ("Fixedsys") )
sort_lb.place(x = 50 , y = 135)
Unsort_lb = tk.Label(text = "UnSorting Types :" , fg = "black", font= ("Fixedsys") )
Unsort_lb.place(x = 50 , y = 200)

Src_lb = tk.Label(text = "Source Directory" , fg = "black", font= ("Fixedsys") )
Src_lb.place(x = 50 , y = 305)
Des_lb = tk.Label(text = "Destination Directory" , fg = "black", font= ("Fixedsys") )
Des_lb.place(x = 50 , y = 355)
Status_lb = tk.Label(text = "Status Panel" , fg = "black", font= ("Fixedsys") )
Status_lb.place(x = 35 , y = 415)

linev = tk.Canvas(window,width = 1 , height = 175 , bg = "#DCDCDC")
linev.place(x =280, y = 100)
linev = tk.Canvas(window,width = 1 , height = 135 , bg = "#DCDCDC")
linev.place(x = 360, y = 270)
lineh = tk.Canvas(window,width = 500 , height = 1 , bg = "#DCDCDC")
lineh.place(x =35, y = 270)
lineh = tk.Canvas(window,width = 500 , height = 1 , bg = "#DCDCDC")
lineh.place(x =35, y = 405)

Combo_sort = ttk.Combobox(window, values = ('Year' , 'Mon_Year' , 'FileType' , 'Extensions'),width = 15)
Combo_sort.place(x = 150, y = 160)

Combo_Unsort = ttk.Combobox(window, values = ('Year' , 'Mon_Year' , 'FileType' , 'Extensions'),width = 15)
Combo_Unsort.place(x = 150, y = 225)

Move_chec = tk.Checkbutton(text = "Move" , onvalue = False , offvalue  = True , variable = copy)
Move_chec.place(x =370 , y = 135)
Copy_chec = tk.Checkbutton(text = "Copy" , onvalue = True , offvalue  = False , variable = copy)
Copy_chec.place(x =370 , y = 165)

Inc_chec = tk.Checkbutton(text = "Include Folders" , onvalue = True , offvalue  = False , variable = Inc_check)
Inc_chec.place(x =370 , y = 195)

Overwrite = tk.Checkbutton(text = "Overwrite Exist files" , onvalue = True , offvalue  = False , variable = Over_check)
Overwrite.place(x =370 , y = 225)

Src_entry = tk.Entry(window ,width = 40)
Src_entry.place(x =50 , y = 325)
Src_browse = tk.Button(window,text = "Browse" , command = get_src_direct)
Src_browse.place(x =300 , y = 320)

Des_entry = tk.Entry(window,width = 40)
Des_entry.place(x =50 , y = 375)
Des_browse = tk.Button(window,text = "Browse" , command = get_des_direct)
Des_browse.place(x =300 , y = 370)


Submit = tk.Button(window,text = "Submit" ,width = 8 , height = 1 , command = sort_files_button )
Submit.place(x =435 , y = 315)
Reset = tk.Button(window,text = "Reset " ,width = 4, command = Reset_Variables )
Reset.place(x =448 , y = 355)

Status_entry = tk.Entry(window ,width = 82,background= "#EBEBEB" , fg = "#39a75e")
Status_entry.place(x =40 , y = 435)

window.mainloop()  

#-------------------------------------------------------------------------------------------------------------------