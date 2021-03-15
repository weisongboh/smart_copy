import sys,os
import subprocess
from shutil import copyfile, copy2

#For recursive copying of directories containing intra-directory symlinks
#Updates symlink to new location

cp_src_dir = "Source" #input("Source Directory: ")
cp_dest_dir = "Destination" #input("Destination: ")

print("Copying directory %s to %s" % (cp_src_dir,cp_dest_dir))
missing_links = []

def check_dir_exist(dir_path):
    
    parent_dir = os.path.dirname(dir_path)
    #print(dir_path, file_parent, grandparent)
    if dir_path == "":
        return None
    if not os.path.exists(dir_path):
        check_dir_exist(parent_dir)
        os.mkdir(dir_path)
        print('Directory is missing, making directory: ', dir_path)
    return None
    
check_dir_exist(cp_dest_dir)

for root, dirs, files in os.walk(cp_src_dir):
    for filename in files:
        #Check file existence at destination
        new_root = root.replace(cp_src_dir, cp_dest_dir)
        path_dst = os.path.join(new_root,filename) 
        check_dir_exist(new_root)

        if os.path.exists(path_dst):
            print('File exists at destination: ', path_dst)
            continue
        check_dir_exist(new_root)

        path = os.path.join(root,filename) #src absolute path
        if os.path.islink(path):
            #path is a symlink
            target_path = os.readlink(path) #get symlink target
            if not os.path.isabs(target_path): #if target path is relative, get absolute path
                target_path = os.path.abspath(target_path)
                print('Target path: ', target_path)
            if not os.path.exists(target_path):
                #Target do not exist
                missing_links.append((path, target_path))
            
            target_dir = os.path.dirname(target_path) #get target file root
            #Start updating symlink
            new_src_path = os.path.join(new_root, filename)
            target_filename = target_path.replace((target_dir+'/'),"") #symlink target filename
            new_target_path = os.path.join(new_root, target_filename) #updated symlink target filepath
            print('Making symlink from %s to %s' % (new_target_path, path_dst))
            os.symlink(new_target_path, path_dst)
        
        else:
            #Not symlink, just copy file to new directory
            print('Copying %s to %s' % (path,path_dst))
            copyfile(path,path_dst)
print(missing_links)