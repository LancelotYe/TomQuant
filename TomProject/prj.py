import os, sys
project_dir = os.path.dirname(os.path.abspath(__NAME__));
print(os.path.basename(__file__))

def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        print(root) #当前目录路径  
        print(dirs) #当前路径下所有子目录  
        print(files) #当前路径下所有非目录子文件  
        
file_name('/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomProject')

print(os.listdir('/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomProject'))

def listdir(path, list_name):  
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        elif os.path.splitext(file_path)[1]=='.jpeg':  
            list_name.append(file_path)  
            
listdir()