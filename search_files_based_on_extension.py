import os
import sys
ans = []
path = input("enter the path: ")
if(os.path.exists(path)):
    if(os.path.isfile(path)):
        print("enter the directory path")
        sys.exit() # stop the interpetor to excute the python code
    else:
        if(len(os.listdir(path)))==0:
            print("Directory is empty")
            sys.exit()
        else:
            ext = input("enter the extension of the files to search: ")
            for r,d,files in os.walk(path):
                for file in files:
                    new_path = os.path.join(r,file)
                    if(new_path.endswith(ext)): #checking whether it end with extension or not
                        ans.append(new_path)
            if(len(ans)==0):
                print("No such file in the given directory")
                sys.exit() 
            else:                 
               print(f"These are the files end with {ext} extension. total of {len(ans)}") 
               print("=======********=========")      
               for path in ans:
                    print(path)      
else:
    print("Invalid path")
    sys.exit()            
