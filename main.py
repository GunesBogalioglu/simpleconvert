from config import *
import fileutil
import engine
import argparse
import concurrent.futures
import multiprocessing
import os


class File:
    output_size = 0
    method = "jxl"
    processed = False

    def __init__(self, location):
        self.name = fileutil.get_filename(location)
        self.location = location
        self.temp_location = None  # Change this to a temporary location so that apps that doesnt support unicode dir locations works
        self.destination = location.replace(location.split(".")[-1], self.method)
        self.input_size = fileutil.get_filesize(location)


"""
-i input (file or folder)
-o output (file or folder)
-m mode (which program to be used) def:jxl
-p parallel
-t thread (if parallel is True,cpu core count) def cpu core count
-r replace (remove old files)
-overwrite (if file exists, overwrite)

.....
"""


def ignite(file_list, thread_count):
    with concurrent.futures.ProcessPoolExecutor(max_workers=thread_count) as executor:
        futures = []
        for file in file_list:
            future = executor.submit(engine.process, file)
            futures.append(future)
        concurrent.futures.wait(futures)
        for idx, future in enumerate(futures):
            new_file = future.result()
            if new_file.processed:
                file_list[idx].processed = True
    return file_list


def process_folder(folder):
    file_list = []
    folder_list = []
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            folder_list.append(dir)
            # fileutil.create_directory(TEMP_DIR + "/" + folder_list[folder_list.index(dir)])
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(File(file_path))
    return file_list, folder_list


def main():
    file_list = []
    parser = argparse.ArgumentParser(description="File Processing Program")

    parser.add_argument("-i", "--input", help="Input file or folder", required=True)
    parser.add_argument(
        "-m", "--mode", default="jxl", help="Program mode (default: jxl)"
    )
    parser.add_argument(
        "-p", "--parallel", action="store_true", help="Enable parallel processing"
    )
    parser.add_argument(
        "-t",
        "--thread",
        type=int,
        default=multiprocessing.cpu_count(),
        help="Number of threads (default: CPU core count)",
    )
    parser.add_argument("-r", "--replace", action="store_true", help="Remove old files")
    parser.add_argument(
        "-ow",
        "--overwrite",
        action="store_true",
        default=False,
        help="Enable automatic overwriting of existing files during the conversion process if they already exist in the destination location",
    )

    args = parser.parse_args()

    if args.input:
        num_threads = 1
        if os.path.isfile(args.input):
            file_list.append(File(args.input))
        elif os.path.isdir(args.input):
            if args.parallel:
                num_threads = args.thread
            file_list, folder_list = process_folder(args.input)
        if args.overwrite:
            for file in file_list:
                if fileutil.check_file_exists(file.destination):
                    fileutil.remove_file(file.destination)
        processed_list = ignite(file_list, num_threads)
        if args.replace:
            for file in processed_list:
                if file.processed and file.location.split(".")[-1] != file.method:
                    if fileutil.check_file_exists(file.location):
                        fileutil.remove_file(file.location)


if __name__ == "__main__":
    main()
