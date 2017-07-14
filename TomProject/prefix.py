import os, sys

'''
os.getcwd()
ha = os.curdir
os.pardir
os.chdir(os.pardir)
os.chdir(os.curdir)
os.listdir(os.getcwd())

os.stat(os.getcwd())
os.sep
os.chdir(os.sep)

os.pathsep
os.environ

print(sys.argv[0])
sys.argv[0]
sys.version
sys.path
def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        print(root) #当前目录路径  
        print(dirs) #当前路径下所有子目录  
        print(files) #当前路径下所有非目录子文件  
''' 
#file_name('/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomProject')    

my_projectName = 'TomProject'
#################################
data_name = 'TomData'
#################################
places = ['CN', 'UA']
#################################
cycles = ['Day','Week','Mouth','Season']


def getAbsPathByDirname(dirname):
  os.chdir(os.sep)
  pathList = []
  rootdir = os.getcwd()
  for (dirpath, dirnames, filenames) in os.walk(rootdir):
    if dirname in dirnames: 
      pathList.append((os.path.join(dirpath, dirname)))
  return pathList

def getAbsPathByFilename(filename):
  os.chdir(os.sep)
  pathList = []
  rootdir = os.getcwd()
  for (dirpath, dirnames, filenames) in os.walk(rootdir):
    if filename in filenames:  
      pathList.append((os.path.join(dirpath, filename)))
  return pathList

def getTomProjectDir():
  return(getAbsPathByDirname(my_projectName)[0])
      
#getTomProjectDir()
MYPROJECT_DIR = getTomProjectDir()

CHILD_DIRS = []
CHILD_DIRS_NAMES = []

CHILD_DIR_DICS = []
for place in places:
  for cycle in cycles:
    var = place+cycle
    #print(var)
    CHILD_DIRS_NAMES.append(var)
    path = os.path.join(MYPROJECT_DIR,data_name,place,cycle)
    #print(path)
    CHILD_DIRS.append(path)
    child_dir_dict = {var : path}
    #print(child_dir_dict)
    CHILD_DIR_DICS.append(child_dir_dict)
    
#print(CHILD_DIRS_NAMES)
print(CHILD_DIR_DICS)
#CNMouth




sys.argv[0]
#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
#打印结果
print (cur_file_dir())