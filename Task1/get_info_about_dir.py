import time
import os
from pprint import pprint
from collections import defaultdict

DIR_TO_SCAN = '/Users/oliwia/Documents/GitHub/PracticalPython/random-stuff'
EXT_TO_LANG = {
  ".c": "C/C++",
  ".cc": "C/C++",
  ".h": "C/C++",
  ".hpp": "C/C++",
  ".cpp": "C/C++",
  ".ino": "C/C++",
  ".py": "Python",
  ".pyw": "Python",
  ".md": "MARKDOWN",
  ".html": "HTML",
  ".htm": "HTML",
  ".css": "CSS",
  ".js": "JavaScript",
  ".bat": "Batch",
  ".pl": "PERL",
  ".php": "PHP",
  ".sh": "BASH"
}

def count_lines(fname):
  with open(fname, "rb") as f:  # open as binary due to bypass decoding error for simplicity
    return len(f.readlines()) 
  # alternatively f.read().split(b'\n') - more lines in split method as it counts empty lines on the end opf the files

def get_stats(stats):
  # unknown_exts = set() # dict without values with unique keys
  langs = defaultdict(int)
  total_loc = 0
  total_file_count = 0

      # if lang in langs:
      #   langs[lang] += loc
      # else:
      #   langs[lang] = loc this is handled by defaultDict

  for path, dirs, files in os.walk(DIR_TO_SCAN):

    path_elements = path.split(os.path.sep)
    if any([x.startswith(".") for x in path_elements]): # any([0,0,0]) => false, but any([0,1,0]) => true 
      print("EXCLUDED:", path)
      continue

    for file in files:
      full_fname = f"{path}/{file}" # don't use os.path.join as it deletes everything before /
      _, ext = os.path.splitext(file) # alternatively use .rsplit(".", 1) - split after right dot, once
      ext = ext.lower()

      lang = EXT_TO_LANG.get(ext) # get value for ext
      if lang is None:
        # unknown_exts.add(ext)
        continue
      
      loc = count_lines(full_fname)
      total_loc += loc
      total_file_count += 1

      langs[lang] += loc
      
  # print(unknown_exts)
  stats["langs"] = langs
  stats["totalLoC"] = total_loc
  stats["totalFiles"] = total_file_count

def show_stats(stats):
  pprint(stats)


def main():
  stats = {
    "totalLoC": None,
      "langs": {
        # Python
      }
  }

  try:
    while True:
      get_stats(stats)
      show_stats(stats)
      time.sleep(1.5) # Seconds
  except KeyboardInterrupt:
    print("\n done!")



if __name__ == "__main__":
  main()