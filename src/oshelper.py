"OS helper"

import os
import shutil

DEFAULT_FILE_NAME = ''
LOCK_FILE_NAME = 'LOCK'

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
        shutil.rmtree(path)
    if os.path.isfile(path):
        os.remove(path)

def join_paths(first, second):
    "Joins two paths into one"
    return os.path.join(first, second)
