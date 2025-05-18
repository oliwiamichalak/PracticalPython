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
  ".md": "MARKDOWMN",
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
  return 42

def get_stats(stats):
  # unknown_exts = set() # dict without values with unique keys
  langs = defaultdict(int)
  total_loc = 0

      # if lang in langs:
      #   langs[lang] += loc
      # else:
      #   langs[lang] = loc this is handled by defaultDict

  for path, dirs, files in os.walk(DIR_TO_SCAN):
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

      langs[lang] += loc
      
  # print(unknown_exts)
  stats["langs"] = langs
  stats["totalLoC"] = total_loc

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
   print(" done!")



if __name__ == "__main__":
  main()