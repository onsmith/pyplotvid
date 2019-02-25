##
# Various routines for creating and deleting files/directories from Python.
#


## Import
import os, shutil


##
# Attempts to delete a file or directory in an exception-safe way.
def remove(path):
  try:
    os.remove(path)
  except:
    try:
      shutil.rmtree(path)
    except:
      pass


##
# Calculates the size of a file in bytes
def size_of(path):
  return os.path.getsize(path)


##
# Recursively creates a directory if it does not already exist
def touch(path):
  os.makedirs(path, exist_ok=True)