import subprocess
import os
from pathlib import Path

def mount_img(img_path, mount_point):
    """
    Mount a disk image to a specified mount point using loopback.
    """
    # Ensure the mount point exists
    mount_point = Path(mount_point)
    if not mount_point.exists():
        mount_point.mkdir(parents=True)
        print(f"Created mount point: {mount_point}")
    
    # Mount the image file
    try:
        subprocess.run(['sudo', 'mount', '-o', 'loop', img_path, str(mount_point)], check=True)
        print(f"Mounted {img_path} to {mount_point}")
    except subprocess.CalledProcessError as e:
        print(f"Error mounting image: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def unmount_img(mount_point):
    """
    Unmount the disk image from a specified mount point.
    """
    try:
        subprocess.run(['sudo', 'umount', mount_point], check=True)
        print(f"Unmounted {mount_point}")
    except subprocess.CalledProcessError as e:
        print(f"Error unmounting image: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    """
    Main function to provide an interactive interface for mounting/unmounting a disk image.
    """
    while True:
        print("\nDisk Image Utility")
        print("1. Mount a disk image")
        print("2. Unmount a disk image")
        print("3. Exit")
        
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            img_path = input("Enter the path to the disk image: ").strip()
            mount_point = input("Enter the mount point directory: ").strip()
            
            if not os.path.exists(img_path):
                print(f"Error: Disk image {img_path} does not exist.")
            else:
                mount_img(img_path, mount_point)
        
        elif choice == "2":
            mount_point = input("Enter the mount point directory: ").strip()
            if not os.path.exists(mount_point):
                print(f"Error: Mount point {mount_point} does not exist.")
            else:
                unmount_img(mount_point)
        
        elif choice == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
