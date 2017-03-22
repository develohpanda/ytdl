"OS helper"

import os
import logging
import errno
from shutil import rmtree, copy2

DEFAULT_FILE_NAME = ''
LOCK_FILE_NAME = 'CANT_TOUCH_THIS'

def absolute_files(path):
    "Returns the files at this directory as absolute filepaths"
    if os.path.isdir(path):
        files = [os.path.join(path, f) for f in os.listdir(path)]
        return [f for f in files if os.path.isfile(f)]
    return []

def absolute_dirs(path):
    "Returns the directories at this directory as absolute filepaths"
    if os.path.isdir(path):
        dirs = [os.path.join(path, f) for f in os.listdir(path)]
        return [f for f in dirs if os.path.isdir(f)]
    return []

def try_create_lock_file(path):
    "Creates a lock file at the specified path"
    lock_file_path = os.path.join(path, LOCK_FILE_NAME)
    if os.path.isdir(path) and not os.path.exists(lock_file_path):
        open(lock_file_path, 'w+')
        logging.getLogger(__name__).info('Created lockfile - %s', lock_file_path)

def lock_file_exists(path):
    "Determines whether or not a LOCK file exists to prevent any changes"
    if os.path.isdir(path):
        files = [f for f in os.listdir(path)]
        return LOCK_FILE_NAME in files
    return False

def try_delete_lock_file(path):
    "Deletes the lock file at the specified path"
    lock_file_path = os.path.join(path, LOCK_FILE_NAME)
    if os.path.exists(lock_file_path):
        remove(lock_file_path)
        logging.getLogger(__name__).info('Deleted lockfile - %s', lock_file_path)

def get_track_file(files):
    "Gets the mp3 file from this folder (*.mp3)"
    return next((f for f in files if f.endswith('.mp3')), DEFAULT_FILE_NAME)

def get_album_art_file(files):
    "Gets the album art file from this folder (*.jpg)"
    return next((f for f in files if f.endswith('.jpg')), DEFAULT_FILE_NAME)

def get_track_info_file(files):
    "Gets the track info file from this folder (*.info.json)"
    return next((f for f in files if f.endswith('.info.json')), DEFAULT_FILE_NAME)

def isdir(path):
    "Checks if path is a directory"
    return os.path.isdir(path)

def remove(path):
    "Delete file or directory as appropriate"
    if os.path.isdir(path):
        rmtree(path)
    if os.path.isfile(path):
        os.remove(path)

def join_paths(first, second):
    "Joins two paths into one"
    return os.path.join(first, second)

def copy(source_file, target_dir):
    "Copies the file to the directory"
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    copy2(source_file, target_dir)

def filename(path):
    "Gets the file name"
    return os.path.basename(path)

def filename_no_extension(path):
    "Gets the file name without the extension"
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

def dirname(path):
    "Gets the directory name"
    return os.path.dirname(path)

def mkdir(path):
    "Makes directory if it doesn't exist"
    if os.path.exists(path):
        return

    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
