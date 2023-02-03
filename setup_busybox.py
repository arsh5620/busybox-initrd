#!/usr/bin/python
import urllib.request
import os
import shutil
import psutil
import subprocess
from distutils.dir_util import copy_tree

BUSYBOX_SRC = "https://busybox.net/downloads/busybox-1.36.0.tar.bz2"
BUSYBOX_TAR_FOLDER = "busybox-1.36.0"
BUSYBOX_TMP = "busybox"
INSTALL_FOLDER = "initrd"


def create_folder_anew(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        print(f"Folder `{folder_path}` already exists and might contain data.")
        print("This folder will be deleted if you continue.")
        response = input("Continue? y/n: ")
        if response.lower() != "y":
            print("Please move or rename the folder and try again.")
            exit(1)
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)


if __name__ == "__main__":
    create_folder_anew(BUSYBOX_TMP)
    create_folder_anew(INSTALL_FOLDER)

    tar_downloaded_path = os.path.join(BUSYBOX_TMP, "busybox.tar.bz2")
    print("Downloading busybox, please wait...")
    urllib.request.urlretrieve(BUSYBOX_SRC, tar_downloaded_path)

    print("Extracting archive")
    subprocess.call(["tar", "-xvf", tar_downloaded_path, "-C", BUSYBOX_TMP])

    print("Copying busybox configuration")
    busybox_build_directory = os.path.join(BUSYBOX_TMP, BUSYBOX_TAR_FOLDER)
    shutil.copy(".config", os.path.join(busybox_build_directory, ".config"))
    os.chdir(busybox_build_directory)

    print("Starting busybox build, this will take some time")
    subprocess.call(["make", "-j", f"{psutil.cpu_count()}"])
    subprocess.call(["make", "install"])

    os.chdir("../../")

    busybox_install_directory = os.path.join(
        busybox_build_directory, "_install")
    print(f"Copying the built busybox to `{INSTALL_FOLDER}`")
    copy_tree(busybox_install_directory,
              INSTALL_FOLDER, preserve_symlinks=True)

    print("Setting up busybox finished")