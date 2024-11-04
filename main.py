import argparse
import os
import shutil
import filecmp
import time

def sync_folders(source, replica, log_file):
    # Ensure all files and folders in the source are in the replica
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, relative_path)

        # make sure current path in replica
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)

        # copy files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)

            if not os.path.exists(replica_file) or not filecmp.cmp(source_file, replica_file, shallow=False):
                shutil.copy2(source_file, replica_file)
def main():
    parser = argparse.ArgumentParser(description="Program that synchronizes two folders")
    parser.add_argument("-s", "--source", help="Path to the source folder")
    parser.add_argument("-r", "--replica", help="Path to the replica folder")
    parser.add_argument("-i", "--interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("-l", "--log_file", help="Path to the log file")

    args = parser.parse_args()
    # Check if the source folder exists
    if not os.path.exists(args.source):
        print(f"Error: Source folder '{args.source}' does not exist.")
        return

    # Check if the replica folder exists
    if not os.path.exists(args.replica):
        print(f"Error: Source replica '{args.replica}' does not exist.")
        return

    while True:
        print("Synchronizing folders...")
        sync_folders(args.source, args.replica, args.log_file)
        print("Synchronization finished...")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
