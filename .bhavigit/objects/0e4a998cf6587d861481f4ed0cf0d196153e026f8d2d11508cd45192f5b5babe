import os
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
directory_creation("ref/head/main")