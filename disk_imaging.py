import subprocess
import os
from pathlib import Path
import matplotlib.pyplot as plt
import time
import threading

def list_devices():
    try:
        result = subprocess.run(['lsblk', '-dpo', 'NAME,SIZE,MODEL'], capture_output=True, text=True)
        devices = result.stdout.strip().split('\n')
        return devices
    except Exception as e:
        print(f"Error listing devices: {e}")
        return []

def select_device(devices):
    if not devices:
        print("No devices found.")
        return None

    print("Available devices:")
    for i, device in enumerate(devices):
        print(f"{i + 1}: {device}")

    try:
        choice = int(input("Select a device by number: "))
        if 1 <= choice <= len(devices):
            return devices[choice - 1].split()[0]  # Return the device name (e.g., /dev/sda)
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

def get_output_image_path():
    desktop_path = Path.home() / "Desktop"
    default_output_image = desktop_path / "disk_image.img"
    
    print(f"Default output image path: {default_output_image}")
    use_default = input("Do you want to use the default output path? (y/n): ").strip().lower()
    
    if use_default == 'y':
        output_image = default_output_image
    else:
        output_image = input("Enter the path for the output image file: ").strip()
        if not output_image:
            print("Error: Output image path cannot be empty.")
            return None
        output_image = Path(output_image)

    if output_image.exists():
        overwrite = input(f"{output_image} already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation aborted.")
            return None

    return str(output_image)

def create_disk_image_with_visualization(source_device, output_image):
    if not os.path.exists(source_device):
        print(f"Source device {source_device} does not exist.")
        return

    command = ['sudo', 'dd', f'if={source_device}', f'of={output_image}', 'status=progress', 'conv=noerror,sync', 'bs=4M']
    
    progress = []
    times = []

    def monitor_progress():
        nonlocal progress, times
        with subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True) as proc:
            for line in proc.stderr:
                if "bytes" in line:
                    try:
                        # Parse the progress output (e.g., "123456789 bytes (123 MB)")
                        bytes_copied = int(line.split()[0])
                        progress.append(bytes_copied)
                        times.append(time.time())
                        # Update visualization
                        plot_progress(progress, times)
                    except ValueError:
                        continue

    # Start the process in a separate thread
    thread = threading.Thread(target=monitor_progress)
    thread.start()
    thread.join()

    print(f"Disk image created: {output_image}")

def plot_progress(progress, times):
    plt.clf()
    elapsed_time = [t - times[0] for t in times]
    data_size_mb = [p / (1024 * 1024) for p in progress]  # Convert bytes to MB

    plt.plot(elapsed_time, data_size_mb, label="Data Copied (MB)")
    plt.xlabel("Time (s)")
    plt.ylabel("Data Copied (MB)")
    plt.title("Disk Cloning Progress")
    plt.legend()
    plt.pause(0.1)  # Allows real-time update of the plot

# Main execution flow
if __name__ == "__main__":
    devices = list_devices()
    source_device = select_device(devices)

    if source_device:
        output_image = get_output_image_path()
        if output_image:  # Proceed only if output_image is valid
            plt.ion()  # Interactive mode for live plotting
            plt.figure()
            create_disk_image_with_visualization(source_device, output_image)
            plt.ioff()  # Disable interactive mode
            plt.show()
