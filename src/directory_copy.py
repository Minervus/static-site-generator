import os
import shutil
from generate_page import *



# dir_list = os.listdir(dest_dir)

# # remove 
# shutil.rmtree(dest_dir)

# # add in new destination folder
# directory = "public"

# parent_dir = '../'

# path = os.path.join(parent_dir,directory)

# os.mkdir(path)

# copy files over recursively

def copy_files(source_path,destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    
    os.mkdir(destination_path)


    for item in os.listdir(source_path):
        current_source_path = os.path.join(source_path,item)
        current_destination_path = os.path.join(destination_path,item)

        print(f"Currently processing: {current_source_path}")

        if os.path.isfile(current_source_path):
            os.makedirs(os.path.dirname(current_destination_path), exist_ok=True)
            # if not os.path.exists(current_destination_path):
            #     os.mkdir(current_destination_path)
            #     print(f"Created directory: {current_destination_path}")
            
            # CURRENT BLOCKER
            # file_tup = os.path.splitext(current_source_path)
            # file_extension = file_tup[1]
            #print(f"This is the file extension: {file_extension}")

            try:
                shutil.copy(current_source_path,current_destination_path)
                print(f"Copied file: {current_source_path} to {current_destination_path}")
            except Exception as e:
                print(f"Failed to copy file {current_source_path} due to {e}")
        elif os.path.isdir(current_source_path): 
            if not os.path.exists(current_destination_path):
                try:
                    os.mkdir(current_destination_path)
                    print(f"Created directory: {current_destination_path}")
                except FileExistsError:
                    print(f"Directory already exists: {current_destination_path}")
                except Exception as e:
                    print(f"Failed to create directory: {current_destination_path} due to {e}")
            copy_files(current_source_path,current_destination_path)

    print(f"COPY FILES FUNCTION FINISHED")
            


