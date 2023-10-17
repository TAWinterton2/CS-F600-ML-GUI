from zipfile import ZipFile
import os





def zip_unpack(zip_file_name):

    #Get current wording directory of server and save it as a string
    cwd = os.getcwd()
    zip_file_path = os.path.join(cwd, zip_file_name)

    temp_dir = "temp"
    temp_path = os.path.join(cwd, temp_dir)

    ext = ('.csv')



    #check if temp already exists
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)


    print("Zip FIle Path: ", zip_file_path)
    print("Current Working Directory", cwd)
    print("Temporary Directory", temp_dir)
    print("Temp Dir path", temp_path)

    with ZipFile(zip_file_path, 'r') as zObject:

    #Extract all files in the zip
    #into a specific location
        zObject.extractall(path=temp_path)
        zObject.close()

    temp_folder_name = os.path.splitext(zip_file_name)[0]
    temp_path = os.path.join(temp_path, temp_folder_name)

    names = []
    for files in os.listdir(temp_path):
        if files.endswith(ext):
            print(files)
            names.append(files)


        else:
           continue
    print(names)


zip_unpack("tmp_file.zip")
