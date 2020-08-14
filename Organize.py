import os 
import shutil
import datetime
 
 """Source , Destination , Extension to perform action ,  and date Format for folder name"""

#src= "C:\\Users\\Ps_Sarvna\\Desktop\\Src" 
#des = "C:\\Users\\Ps_Sarvna\\Desktop\\Des"
#Ext = [".mp4" , ".jpg" , ".png" , ".amr"]
#Datetime = "%Y"
folder_names = []

#--------------------------------------------------------------------------------------------------------------------


def Sort_files_mtime(src, des, Ext, Datetime): 
	
	"""
	Function Process Step by step:
			1. get lis of files in Src folder
			2. Iterate through files
			3. Get extension of each file
			4. if the file is directory
					- call same function as recursive using foldername as source
			5. if it is file and extension is satisfied
			6. Get modified time and stip to given format (Datetime)
			7. check folder is present with mtime or Create folder
			8. Move files to destination
			9.If there is Conflicts:
				--Create Conflicts folder
				--create folder with mtime 
				--move to that folder
	"""
	
	files = os.listdir(src)
	for file in files:
		extension = os.path.splitext(file)[1]

		if os.path.isfile(os.path.join(src , file)) and extension in Ext:
			dtime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(src , file)))
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

			if os.path.isdir(os.path.join(src , file)):
				Sort_files_mtime(os.path.join(src , file), des, Ext, Datetime)


#--------------------------------------------------------------------------------------------------------------------


Sort_files_mtime(src, des, Ext, Datetime)