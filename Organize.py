import os 
import shutil
import datetime

#--------------------------------------------------------------------------------------------------------------------

"""Source , Destination , Extension to perform action ,  and date Format for folder name"""

#src= "C:\\Users\\Ps_Sarvna\\Desktop\\Src" 
#des = "C:\\Users\\Ps_Sarvna\\Desktop\\Des"
Datetime = "%Y"
Inc_sub = True
Ext_Sort = True
Ext_Spec  = True
folder_names = []
Images = ["Images" , ".jpg" , ".png" , ".gif" , "jpeg"]
Videos = ["Videos" , ".mp4" , ".mpeg" , ".avi" , ".mkv"]
Audio = ["Audio" , ".mp3" , ".wma" , ".amr" ]
Softwares = ["Softwares" , ".exe"]

Ext = [Images , Videos , Audio, Softwares ]

#--------------------------------------------------------------------------------------------------------------------

def Sort_files_mtime(src, des, Datetime , Inc_sub, Ext_Sort ,Ext_Spec ): 
	
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
			dtime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(src , file)))
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
				fname = dtime.strftime(Datetime)

			if fname not in folder_names:
				folder_names.append(fname)
				if fname not in os.listdir(des):
					os.mkdir(os.path.join(des , fname))

			try :
				shutil.move(os.path.join(src , file) , os.path.join(des , fname))
			except:
				Xfname = "Conflicts"
				Xdes = "C:\\Users\\Ps_Sarvna\\Desktop\\Des\\Conflicts"
				if Xfname not in os.listdir(des):
					os.mkdir(os.path.join(des , Xfname))
				if fname not in os.listdir(Xdes):
					os.mkdir(os.path.join(Xdes , fname))
					
				shutil.move(os.path.join(src , file) , os.path.join(Xdes , fname))
		
		else:
			if Inc_sub:
				if os.path.isdir(os.path.join(src , file)):
					Sort_files_mtime(os.path.join(src , file),des, Datetime , Inc_sub, Ext_Sort ,Ext_Spec )

#--------------------------------------------------------------------------------------------------------------------

Sort_files_mtime(src ,des, Datetime , Inc_sub, Ext_Sort ,Ext_Spec)