"OS helper"

import os

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
