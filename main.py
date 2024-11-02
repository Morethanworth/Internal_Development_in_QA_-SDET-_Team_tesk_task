import argparse


def main():
    parser = argparse.ArgumentParser(description="Program that synchronizes two folders")
    parser.add_argument("-s", "--source", help="Path to the source folder")
    parser.add_argument("-r", "--replica", help="Path to the replica folder")
    parser.add_argument("-i", "--interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("-l", "--log_file", help="Path to the log file")

    args = parser.parse_args()
    print(args.source)
    print(args.replica)
    print(args.interval)
    print(args.log_file)


if __name__ == "__main__":
    main()
