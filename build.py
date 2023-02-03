#!/usr/bin/python

import os
import subprocess
import shutil

ROOT_FS_PATH = "./initrd"
USERSPACE_NAME = "userspace"
CC = "clang"
CCFLAGS = "-static"
USERSPACE_SOURCE = "./userspace.c"
INITCPIO_NAME = "./initrd.cpio"


def make_rootfs_dirs(dirname):
    directory = os.path.join(ROOT_FS_PATH, dirname)
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    print("Building initrd")

    userspace_path = os.path.join(ROOT_FS_PATH, USERSPACE_NAME)

    if os.path.exists(userspace_path):
        print(f"Removing previous copy of userspace from '{userspace_path}'")
        os.unlink(userspace_path)

    cc_params = [CC, CCFLAGS, USERSPACE_SOURCE, "-o", userspace_path]
    print(f"Building userspace with '{cc_params}'")
    subprocess.call(cc_params)

    print("Copying init")
    init_path = os.path.join(ROOT_FS_PATH, "init")
    shutil.copy("init", init_path)

    print("Setting init permissions")
    subprocess.call(["chmod", "ugo+rx", init_path])

    make_rootfs_dirs("proc")
    make_rootfs_dirs("sys")

    print(f"Changing directory to {ROOT_FS_PATH}")
    os.chdir(ROOT_FS_PATH)

    print(f"Building cpio archive for `newc` format")

    find_process = subprocess.Popen(
        ["find", ".", "-print0"], stdout=subprocess.PIPE)
    output = subprocess.check_output(
        ["cpio", "--null", "--format=newc", "-o"], stdin=find_process.stdout)

    with open(INITCPIO_NAME, mode="wb") as file:
        file.write(output)

    os.chdir("..")

    os.rename(os.path.join(ROOT_FS_PATH, INITCPIO_NAME), INITCPIO_NAME)

    print("Build finished.")
    print("Starting kernel, qemu will look for `bzImage` kernel (or symlink) in the current directory")

    subprocess.Popen(["qemu-system-x86_64", "-kernel", "./bzImage",
                     "-initrd", INITCPIO_NAME], start_new_session=True)
