'''

intiial steps:
(1) need to create
create ./bhavigit and put in it:
    /objects to store file snapshots
    /ref to store branches
    HEAD text file that points to the current branch
    index txt file for a staging area
'''

import os
import hashlib
import sys
import shutil
import time
import json
def init():

    if os.path.exists(".bhavigit"):
        print("bhavigit already exists")
        return
    
    try:
        os.makedirs(".bhavigit")
        print("Created bhavigit folder")
        os.makedirs(".bhavigit/objects", exist_ok=True)
        print("Created objects folder")
        os.makedirs(".bhavigit/refs", exist_ok=True)
        print("Created refs folder")
    except Exception as e:
        print("Error: ", e)

    HEAD  = '.bhavigit/HEAD.txt'
    index = '.bhavigit/index.txt'
    commit_order = '.bhavigit/commit_order.json'
    commit_order_dict = {}
    commit_order_dict['prev'] = None
    commit_order_dict['curr'] = None

    with open(HEAD, 'w') as file:
        file.write("ref: refs/head/main\n")
    with open(index, 'w') as file:
        file.write("")
    with open(commit_order, 'w') as file:
        json.dump(commit_order_dict, file, indent = 1)
    print("intialzied empty bhavi repo")

def copy_file_contents(fp1, fp2):
    print(f"Current working directoy: {os.getcwd()}")
    fp1 = os.path.abspath(fp1)
    fp2 = os.path.abspath(fp2)
    #print(f"source file: {fp1}\ndest file: {fp2}")

    
    try:
        if not (os.path.exists(fp2)):
            shutil.copyfile(fp1, fp2)
            print(f"Copied contents of {fp1} into {fp2}'")
    #except FileNotFoundError:
    #    print(f"Couldn't find source file: {fp1}")
    #except PermissionError:
    #    print(f"Permission denied acces to {fp1} or {fp2}")
    except Exception as e:
        print(f"Other error: {e}")
    

def add(filename):
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        print(filename, "===doesn't exist or its path doesn't exist")
        return
    hexdiges = None
    try:
        hashfunc = hashlib.new('sha256')
        with open(filename, 'rb') as file:
            chunk = file.read()
            hashfunc.update(chunk)
        filename_hash = hashfunc.hexdigest()

        print(f"The hash of {filename} is {filename_hash}")
        #print(f"Type of hexdiges is {type(hexdiges)}")

        snapshot_file = ".bhavigit/objects/" + filename_hash

        print(f"name of file for contents to be copied: {snapshot_file}")
        copy_file_contents(filename, snapshot_file)

        with open(".bhavigit/index.txt", 'r') as file:
            for line in file:
                if filename_hash in line:
                    print(f"file {filename} already staged. No need to stage again")
                    return
        with open(".bhavigit/index.txt", 'a') as file:
            
            '''
            TODO: update this are so that only the latest version of the add are staged. 
            That way we dont have mutliple hashes to the same file name
            '''   
            stageing_line = filename + "._." + filename_hash + "\n"
            file.write(stageing_line)
            print(f"staged ")


    except Exception as e:
        print("Erorr occured when trying to add and stage file: ", e)
        


def directory_creation(address):
    '''
    iteratively create directory and a file if one ore 
    more of the directories doesn't exist or if the file doesn't exist
    '''

    directories_and_files = address.split('/')
    directories = directories_and_files[:-1]
    #print(f'DIRECTORIES: ${directories}')
    path = os.getcwd()
    #print(f'WORKING DIRECT: {path}')
    for directory in directories:
        path += "\\" + directory
        #print("\n=========")
        #print(f'PATH TO CHECK IF IT EXSITS ${path}')
        if not os.path.exists(path):
            os.mkdir(path)
            

        else:
            print(f'path {path} alreay exsits')
            continue
    file = path + "\\" + directories_and_files[-1]
    if not os.path.exists(file):
        create_branch = open(file, 'x')
        create_branch.close()
    print(f'created branch file at ${path}')


def commit(message = "None"):
    '''
    notes
    how to get preiovus commit
    every commit has a hash

    '''
    
    if os.path.getsize(".bhavigit/index.txt") == 0:
        print("nothing to commit")
        return
    '''
    First we need to grab the previous commit hash if it exists
    if it doesn't exist then we set the current commit as the previous one 

    - then create commit object

    '''
    
    #first step
    commit_order = {}
    commit_string = ""
    files_to_commit = ""
    files_and_hashes = {}
    with open(".bhavigit/index.txt", 'r') as file:
        lines = file.readlines()
        files_and_hashes = {}
        for line in lines:
            file_and_hash = line.split("._.")
            files_and_hashes[file_and_hash[0]] = file_and_hash[1]
    print(f"Dict: {files_and_hashes}")


    with open(".bhavigit/commit_order.json", 'r') as file:
        commit_order = json.load(file)
        
    time_stamp = time.ctime(time.time())
    commit_string = "Parent: " + str(commit_order['prev']) + "\nTimestampe: " + time_stamp + "\nMessage: " + message + "\nFiles: \n"
    for file, hash in files_and_hashes.items():
        commit_string += file + "->" + hash + "\n"
    
    #hash commit_string
    hashfunc = hashlib.new("sha256")
    hashfunc.update(commit_string.encode())
    commit_hash = hashfunc.hexdigest()
    

    commit_filename = ".bhavigit/objects/" + commit_hash
    try:
        commit_file_create = open(commit_filename, 'x')
        commit_file_create.close()
    except FileExistsError:
        print(f"Commit for file {commit_filename} already exists")
    except Exception as e:
        print(f'UKNOWN error occured: {e}')
    
    with open(commit_filename, 'w') as file:
        file.write(commit_string)
        

    #update branch in HEAD to point to correct file and for that file to contain the current hash

    branch_file = ".bhavigit/"
    with open('.bhavigit/HEAD.txt') as file:
        line = file.readline().split(":")[1].strip()
        branch_file += line
    if not os.path.exists(branch_file):
        branch_file_create = directory_creation(branch_file)
    with open(branch_file, 'w') as file:
        file.write(commit_hash)

    commit_order['prev'] = commit_hash
    with open('.bhavigit/commit_order.json', 'w') as file:
        json.dump(commit_order, file, indent = 1)
        

    with open('.bhavigit/index.txt', 'w') as file:
        file.write('')
    print("+++++++++++++++++++++++++")
    print("=========================")
    print("+++++++++++++++++++++++++")
    print(f'Commited Changes with hash {commit_hash}')


def log():
    most_recent_ch = None
    prev_commit_hash = None
    commit_log = "====================\n====================\n"
    with open('.bhavigit/refs/head/main', 'r') as file:
        most_recent_ch = file.read().strip()
    
    prev_commit_hash = most_recent_ch
    while (prev_commit_hash != "None"):
        #print(f"Current previous commit hash is {prev_commit_hash}")
        commit_file = '.bhavigit/objects/' + prev_commit_hash
        
        with open(commit_file, 'r') as file:
            commit_obj = file.read()
            #print(f"Full Commit  \n{commit_obj}")
            prev_commit_hash = commit_obj.splitlines()[0].strip().replace(' ', '')
            prev_commit_hash = prev_commit_hash[prev_commit_hash.index("Parent:") + len("Parent:"):]
        commit_log = commit_log + commit_obj + "====================\n====================\n"

    
    print(commit_log)


#tread lightly
def purge():     
    shutil.rmtree(".bhavigit")
    print("Removed all objects, refs, files, etc from bhavigit")


if __name__ == "__main__":
    num_args = len(sys.argv) - 1

    if num_args == 0:
        print("no commands provided")
        sys.exit()

    command = sys.argv[1]
    if command == 'init':
        init()
    elif command == 'add':
        if num_args == 2:
            filename = sys.argv[2]
            add(filename)
            #print(f"Ur going to add {filename}")
        else:
            print('Did not enter filename')
            sys.exit()
    elif command == 'commit':
        if num_args == 2:
            message = sys.argv[2]

            commit(message)
    
    elif command == 'purge':
        ensure = input("are you sure you want to purge everything (y/n)")
        if ensure == 'y':
            purge()
        elif ensure == 'no':
            print('didn''t remove anything')
        else:
            print('please enter a valid input')
    elif command == 'log':
        log()

'''
skipping but still need to do:
add functionlaity for adding all files/more than 1
add functionality for commiting if more than 1 file is added

'''