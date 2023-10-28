import os 
import sys
path = input("enter the path to search: ")
my_dir = []
my_file = []
if(os.path.exists(path)): 
    for dir_file in os.listdir(path):
        new_path = os.path.join(path,dir_file)
        if(os.path.isdir(new_path)):
            my_dir.append(new_path) #storing directories
        elif(os.path.isfile(new_path)): 
            my_file.append(new_path) #storing files
    print(f"Number of Directories are: {len(my_dir)} ") # return the number of directories
    for dir in my_dir:
        print(dir)
    print(f"Number of Files are: {len(my_file)} ") # return the number of files
    for file  in my_file:
        print(file)

else:
    print("Path not Exists enter the valid path")
    sys.exit()        # stop the interpreter to excute the python code
         
                
