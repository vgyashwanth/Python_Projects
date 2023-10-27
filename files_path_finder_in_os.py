import os
import platform as  pt
import  string
import sys
print(pt.system())
#sys.exit()
req_file = input("enter your file name: ")
if "Windows"==pt.system(): 
     drive = string.ascii_uppercase #return all characters in  upper case as string
     drive_list = [] #for storing the drivers
     for x in drive:
          if os.path.exists(x+":\\"):
               drive_list.append(x+":\\") #adding directroy if exists
     print(drive_list)   
     for each_driver in  drive_list: #searching path
          for path,dic,file in (os.walk(each_driver)):
               for each_file in file:
                    if(req_file==each_file): 
                         print(os.path.join(path,each_file)) #print path
else: #for linux operating system
     for path,dic,file in os.walk("/"):
          for each_file in file:
               if(req_file==each_file):
                    print(os.path.join(path,each_file))


                    
               
                         

