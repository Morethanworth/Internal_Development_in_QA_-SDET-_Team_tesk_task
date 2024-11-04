import argparse
import os
import shutil
import filecmp
import time
import logging


def setup_logger(log_file):
    # if desired the file could be cleared first
    # open(log_file, 'w').close()

    logger = logging.getLogger("FolderSyncLogger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # logging format
    formatter = logging.Formatter('%(asctime)s -- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def sync_folders(source, replica, logger):
    # ensure all files and folders in the source are in the replica
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, relative_path)

        # make sure current path in replica
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)
            # logger.info(f"Directory created: {replica_root}")

        # copy files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)

            if not os.path.exists(replica_file) or not filecmp.cmp(source_file, replica_file, shallow=False):
                shutil.copy2(source_file, replica_file)
                logger.info(f"File copied: {source_file} to {replica_file}")

    # remove files and directories not in source
    for root, dirs, files in os.walk(replica, topdown=False):
        relative_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, relative_path)

        # remove directories
        for dir in dirs:
            replica_dir = os.path.join(root, dir)
            source_dir = os.path.join(source_root, dir)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                # logger.info(f"Directory removed: {replica_dir}")

        # remove files
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_root, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logger.info(f"File removed: {replica_file}")


def main():
    parser = argparse.ArgumentParser(description="Program that synchronizes two folders")
    parser.add_argument("-s", "--source", help="Path to the source folder")
    parser.add_argument("-r", "--replica", help="Path to the replica folder")
    parser.add_argument("-i", "--interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("-l", "--log_file", help="Path to the log file")

    args = parser.parse_args()
    # check if the source folder exists
    if not os.path.exists(args.source):
        print(f"Error: Source folder '{args.source}' does not exist.")
        return

    # check if the replica folder exists
    if not os.path.exists(args.replica):
        print(f"Error: Source replica '{args.replica}' does not exist.")
        return

    if not os.path.exists(args.log_file) or not args.log_file:
        print(f"Error: Logging file doesnt exist or not provided.")
        return

    # setup logger
    logger = setup_logger(args.log_file)
    while True:
        logger.info("Starting synchronization")
        sync_folders(args.source, args.replica, logger)
        logger.info("Synchronization complete")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
