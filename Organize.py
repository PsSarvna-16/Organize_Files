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
window.iconbitmap(r'C:\Users\Ps_Sarvna\Desktop\ico2.ico')

#--------------------------------------------------------------------------------------------------------------------
class Count:
	def __init__(self,name):
		self.name = name
		self.value = 0
	def increase(self):
		self.value+=1
	def reset(self):
		self.value = 0

#--------------------------------------------------------------------------------------------------------------------
Moved  = Count("Moved")
Copied  = Count("Copied")
Skipped  = Count("Skipped")
OverWrited  = Count("OverWrited")

obj = [Moved, Copied, Skipped, OverWrited]

Inc_check = tk.BooleanVar()
Over_check = tk.BooleanVar()
copy = tk.BooleanVar()

Images = ["Images" , ".jpg" , ".png" , ".gif" , "jpeg" , ".ico" , ".tiff"]
Videos = ["Videos" , ".mp4" , ".mpeg" , ".avi" , ".mkv" , ".flv" , ".vob" , ".wmv" , ".3gp"]
Audios = ["Audios" , ".mp3" , ".wma" , ".amr" ,".wav"]
Softwares = ["Softwares" , ".exe", ".msi" , ",apk"]
Documents = ["Documets" , ".pdf" , ".txt" , ".docx" , ".doc" , ".ppt" , ".pptx" , ".xls" , ".zip", ".rar" ]

Ext = [Images , Videos , Audios, Softwares,Documents ]
#--------------------------------------------------------------------------------------------------------------------

def get_src_direct():
	src = filedialog.askdirectory()
	Src_entry.delete(0, tk.END)
	Src_entry.insert(0 , src)

def get_des_direct():
	des = filedialog.askdirectory()
	Des_entry.delete(0, tk.END)
	Des_entry.insert(0 , des)

def Combo_sort():
	Combo_Unsort.set('')

def Combo_Unsort():
	Combo_sort.set('')

def Reset_Variables():
	Des_entry.delete(0, tk.END)
	Src_entry.delete(0, tk.END)
	Combo_sort.set('')
	Combo_Unsort.set('')
	Inc_check.set(False)
	Over_check.set(False)
	copy.set(False)


def sort_files_button():

	src = Src_entry.get()
	des = Des_entry.get()
	Sort_type = Combo_sort.get()
	Unsort_type = Combo_Unsort.get()
	Copy  = copy.get()
	Inc_sub = Inc_check.get()
	OverWrite = Over_check.get()

	sort_type = ["FileType" , "Extensions" , "Year" , "Mon_Year"]
	unsort_type = ['All' ,'Images' , 'Videos' , 'Audios', 'Documents', 'Softwares']

	if len(Sort_type) < 2 and len(Unsort_type) < 2:
		tk.messagebox.showerror("Error!", "Select any one type.")
		return

	if not os.path.isdir(src):
		tk.messagebox.showerror("Error!", "Select Valid Source Directory")
		return
	if not os.path.isdir(des):
		tk.messagebox.showerror("Error!", "Select Valid Destination Directory")
		return

	if len(Unsort_type) < 2 :
		if Sort_type not in sort_type:
			tk.messagebox.showerror("Error!", "Select Valid Sort Type")
			return

		Sort_files(src, des, Inc_sub,Sort_type ,OverWrite ,Copy  )
		Result = "\nCompleted Succesfully \n\n"
		for objects in obj:
			if objects.value !=0 :
				Result = Result + "{}: {} files\n".format(objects.name , objects.value) 
		Status_entry.delete(0, tk.END)
		Status_entry.insert(0 , Result)
		tk.messagebox.showinfo(title="File Organizer", message=Result)
		Moved.reset()
		Copied.reset()
		Skipped.reset()
		OverWrited.reset()

	if len(Sort_type) < 2 :
		if Unsort_type not in unsort_type:
			tk.messagebox.showerror("Error!", "Select Valid UnSort Type")
			return
		if "Unsorted" not in os.listdir(des):
			os.mkdir(os.path.join(des,"Unsorted"))
		des = os.path.join(des,"Unsorted")
		Unsort_files( src , des,Unsort_type, Inc_sub , OverWrite,Copy)


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
					Moved.increase()
				else:
					try:
						shutil.copy2(os.path.join(src , file) ,os.path.join(os.path.join(des , fname),file))
						Copied.increase()
					except:
						Skipped.increase()
						pass
			except:
				if OverWrite:
					try:
						shutil.move(os.path.join(src , file) , os.path.join(os.path.join(des , fname),file))
						OverWrited.increase()
					except:
						Skipped.increase()
						pass
				else:
					Skipped.increase()
		else:
			if Inc_sub:
				if os.path.isdir(os.path.join(src , file)):
					Sort_files(os.path.join(src , file),des, Inc_sub,Sort_type, OverWrite ,Copy  )
					try:
						os.rmdir(os.path.join(src , file))
					except:
						pass


def Unsort_files( src , des,Unsort_type, Inc_sub , OverWrite,Copy):

	fname = "UnSorted"
	files = os.listdir(src)
	for file in files:
		extension = os.path.splitext(file)[1]
		if os.path.basename(file) == fname:
			continue
		
		if os.path.isfile(os.path.join(src , file)):
			if Unsort_type == "All":
				pass
			elif Unsort_type == "Images":
				if extension not in Images:
					continue
			elif Unsort_type == "Videos":
				if extension not in Videos:
					continue
			elif Unsort_type == "Audios":
				if extension not in Audios:
					continue
			elif Unsort_type == "Documents":
				if extension not in Documents:
					continue
			elif Unsort_type == "Softwares":
				if extension not in Softwares:
					continue
			try :
				if not Copy:
					shutil.move(os.path.join(src , file) , os.path.join(des))
				else:
					try:
						shutil.copy2(os.path.join(src , file) ,os.path.join(os.path.join(des),file))
					except:
						pass
			except:
				if OverWrite:
					try:
						shutil.move(os.path.join(src , file) , os.path.join(os.path.join(des ),file))
					except:
						pass

		else:
			if Inc_sub:
				print(file)
				Unsort_files(os.path.join(src , file), des,Unsort_type, Inc_sub , OverWrite,Copy)
				try:
					os.rmdir(os.path.join(src , file))
				except:
					pass


#--------------------------------------------------------------------------------------------------------------------

gui_title = tk.Label(text = "File Organizer" , fg = "black", font= ("Segoe Script",24) )
gui_title.place(x =180 , y = 25)


step1_lb = tk.Label(text = "Step 1: Select the Type" , fg = "black", font= ("Fixedsys") )
step1_lb.place(x =35 , y = 100)
step2_lb = tk.Label(text = "Step 2: Select Preferred Option" , fg = "black", font= ("Fixedsys") )
step2_lb.place(x =300 , y = 100)
step3_lb = tk.Label(text = "Step 3: Select Directories" , fg = "black", font= ("Fixedsys") )
step3_lb.place(x = 35 , y = 280)
step4_lb = tk.Label(text = "Step 4: Submit/Reset" , fg = "black", font= ("Fixedsys") )
step4_lb.place(x = 380 , y = 280)

sort_lb = tk.Label(text = "Sorting Types : " , fg = "black" )
sort_lb.place(x = 50 , y = 135)
Unsort_lb = tk.Label(text = "UnSorting Types :" , fg = "black" )
Unsort_lb.place(x = 50 , y = 200)

Src_lb = tk.Label(text = "Source Directory" , fg = "black")
Src_lb.place(x = 50 , y = 305)
Des_lb = tk.Label(text = "Destination Directory" , fg = "black" )
Des_lb.place(x = 50 , y = 355)
Status_lb = tk.Label(text = "Status Panel" , fg = "black" ,font= ("Fixedsys") )
Status_lb.place(x = 35 , y = 415)

linev = tk.Canvas(window,width = 1 , height = 175 , bg = "#DCDCDC")
linev.place(x =280, y = 100)
linev = tk.Canvas(window,width = 1 , height = 135 , bg = "#DCDCDC")
linev.place(x = 360, y = 270)
lineh = tk.Canvas(window,width = 500 , height = 1 , bg = "#DCDCDC")
lineh.place(x =35, y = 270)
lineh = tk.Canvas(window,width = 500 , height = 1 , bg = "#DCDCDC")
lineh.place(x =35, y = 405)

Combo_sort = ttk.Combobox(window, values = ('Year' , 'Mon_Year' , 'FileType' , 'Extensions'),width = 15,postcommand = Combo_sort)
Combo_sort.place(x = 150, y = 160)

Combo_Unsort = ttk.Combobox(window, values = ('All' ,'Images' , 'Videos' , 'Audios', 'Documents', 'Softwares'),width = 15, postcommand = Combo_Unsort)
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