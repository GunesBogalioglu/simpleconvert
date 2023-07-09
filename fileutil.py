import os
import shutil
import zlib


def zipfolder(file_name, folder):
    shutil.make_archive(file_name, "zip", folder)


def unzipfolder(filename, destination):
    shutil.unpack_archive(filename, destination)


def crc32(target, chunksize=65536):
    with open(target, "rb") as f:
        checksum = 0
        while chunk := f.read(chunksize):
            checksum = zlib.crc32(chunk, checksum)
        return checksum


def copy_dirtree(src, dst):
    src = os.path.abspath(src)
    src_prefix = len(src) + len(os.path.sep)
    try:
        for root, dirs, files in os.walk(src):
            for dirname in dirs:
                dirpath = os.path.join(dst, root[src_prefix:], dirname)
                os.mkdir(dirpath)
    except:
        # print("Copy_dirtree failed")
        pass


def get_filesize(file):
    try:
        size = os.path.getsize(file)
        if type(size) is type(None):  # Type None check
            return 0
        return size
    except Exception:  # Dosya bulunamaz yada okunamaz ise boyutu 0 al.
        return 0


def create_directory(dir):
    try:
        os.mkdir(dir)
    except:
        pass


def remove_file(file):
    try:
        os.remove(file)
    except:
        pass


def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
    except:
        pass


def get_filename(file):
    return os.path.basename(file)


def get_fileext(file):
    ext = os.path.splitext(os.path.basename(file))
    return ext[1].lower()


def move_file(src, dst):
    try:
        os.replace(src, dst)
    except:
        pass


def clear_folder(folder):
    try:
        shutil.rmtree(folder)
    except OSError:
        pass


def write_to_file(file, msg=None):
    try:
        with open(file, "a") as f:
            f.write("{}\n".format(msg))
    except Exception:
        open(file, "w").write(msg)


def check_file_exists(file):
    try:
        if os.path.exists(file):
            return True
        else:
            return False
    except OSError:
        pass
