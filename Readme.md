### Setup for minimal linux environment using Busybox

1. Run the `.\setup_busybox.py` command to download, configure, build and install the busybox 1.36.0 into the temporary `busybox` directory.
2. This should produce two folders, the `busybox` folder where the busybox archive was downloaded and built, and a `initrd` folder where the busybox directory is setup to behave as a minimal linux installation.
3. Then you can run `build.py` and that should build `userspace.c` file and copy the init script into the `initrd` folder and then make an `initrd.cpio` archive
4. It will then try to run `qemu-system-x86_64` emulator to run the kernel and the newly built init image

> Note: You will need a built linux kernel, you can do a `make defconfig && make -j $(nproc)` to build the kernel for testing. Then you will need to symlink the kernel as name `bzImage` in the root of the repo

Program dependencies:
* clang/gcc (Build the userspace.c file)
* find (Collecting files to build cpio archive)
* cpio (Building cpio archive)
* python (For running build scripts)
* qemu-system-x86_64 (For testing the built cpio)
