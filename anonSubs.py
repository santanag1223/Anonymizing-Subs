from math import trunc
import os
import argparse
import shutil
from   random import sample
from   tqdm   import tqdm

def get_args():
    """Parses command line and returns parser object."""

    parser = argparse.ArgumentParser()
    parser.add_argument("subs", help = "submissions to be anonymized and zipped")
    args   = parser.parse_args()
    return args

def is_path(pth: str) -> bool:
    """Checks if string is a path to a directory, returns True if '/' is present in the string."""

    return '/' in pth

def is_zip(file: str) -> bool:
    """Checks if string is a '.zip' file, returns True if '.zip' is present in the string."""

    return file.endswith('.zip')

def copy_from_path(sub_dir: str) -> str:
    """Copies a folder from given path and returns folder name."""

    start_dir = os.getcwd()                         # save our current dir
    scr_dir   = start_dir + '/' +os.path.basename(sub_dir)
    os.chdir("/")                                   # go to the root dir
    shutil.copytree(sub_dir, scr_dir, dirs_exist_ok=True)# copy over subs folder
    
    os.chdir(start_dir)                             # go back to working dir

    return os.path.basename(sub_dir)                # return new working folder

def unzip_folder(zipFile: str) -> str:
    """Unzips file and returns new folder name"""

    nozip = zipFile.replace(".zip" ,"")
    shutil.unpack_archive(zipFile, nozip)
    return nozip

def unzip_from_path(zip_path: str) -> str:
    """Copies '.zip' from another directory into current directory and unzips locally.\n
    deletes the '.zip' folder copied over after unzipping it\n
    returns new unzipped folder name """
    
    start_dir = os.getcwd()
    
    os.chdir('/')                                   # go to root dir
    print("copying file from path...")
    shutil.copy(zip_path,start_dir)                 # copy zipfile to our current dir
    os.chdir(start_dir)                             # return to working dir

    zipFolder = os.path.basename(zip_path)          # get our zipfolder name from path
    print("unzipping file...")
    zipFolder = unzip_folder(zipFolder)             # unzip folder and rename our zipFolder

    os.remove(zipFolder + '.zip')                   # delete the copied over zip

    return zipFolder                                # return working unzip file


def main():

    args = get_args()
    subs = args.subs

    dlt  = False

    if is_path(subs):
        dlt = True
        
        if is_zip(subs):
            try:                            subs = unzip_from_path(subs)
            except FileNotFoundError as e:  print(f"Directory '{subs}' could not be found.\n",e)
            except shutil.ReadError as e:   print(f"Directory '{subs}' could not be unzipped.\n",e)
        
        else:
            try:                            subs = copy_from_path(subs)
            except Exception as e:          print(f"Directory '{subs}' could not be found.\n",e)
    
    else:

        if is_zip(subs):
            dlt = True

            try:                            subs = unzip_folder(subs)
            except FileNotFoundError as e:  print(f"Directory '{subs}' could not be found.\n",e)
            except shutil.ReadError as e:   print(f"Directory '{subs}' could not be unzipped.\n",e)
        
        else:
            try:                            shutil.copytree(subs,subs+'_copy'); subs += '_copy'
            except Exception as e:          print(f"Directory '{subs}' could not be found.\n",e)
            
    os.chdir(subs)

    # list of numbers from 0 to size of dir, in random order
    size = len(os.listdir())
    possIDs = sample([i for i in range(size)], size)
    
    # for every student in subs dir / rename to vaild id
    for student in tqdm(os.listdir(), desc = "Folders Anonymized", unit = "Folders"):
        os.rename(student, "Student {:0>5}".format(possIDs.pop()))
    os.chdir("..")
    
    # zip working folder to 'subs_anonymized'
    print('creating new zip...')
    shutil.make_archive(subs + "-anonymized", "zip", subs)
    
    # delete subs
    shutil.rmtree(subs)

    
if __name__ == "__main__":
    main()