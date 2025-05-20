import time
import os
import sys # sys.exit for debugging 
import json
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
BAR_WIDTH = 40

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

def show_stats_for(label, locs):
  max_loc = max(locs)
  i = 1
  while i < max_loc: 
    i *= 2
  
  print(f"\x1b[1;37m{label}\x1b[m") # coloured label white

  for j, loc in enumerate(locs):
    if len(locs) == 1:
      g = 255
    else:
      g = 55 + int(j / (len(locs) - 1)*255)
    
    color = f'\x1b[38;2;0;{g};0m'
    bar_size = int((loc / i) * BAR_WIDTH)
    bar = "\u2593" * bar_size
    print(f" \x1b[1;31m{loc:5} \x1b[m {color}{bar}\x1b") # coloured label red

  print()

def show_stats(stats_in_time):
  # pprint(stats) # pretty print
  print("\x1b[3J", end="") # clear all terminal screen, escape ASCI code

  for lang in ["BASH", "C/C++", "Python"]: 
    locs = []
    for stats in stats_in_time:
      locs.append(stats["langs"].get(lang, 0))
  show_stats_for(lang, locs)

  # show_stats_for("C/C++", stats["langs"].get("C/C++", 0)) example


def main():
  stats_in_time = []

  try:
    with open("stats.json") as f:
      stats_in_time = json.load(f)
  except FileNotFoundError:
    pass
  
  try:
    while True:
      stats = {
        "totalLoC": None,
        "langs": {
           # Python
       }
    }
      get_stats(stats)
      stats_in_time.append(stats)
      show_stats(stats_in_time[-6:]) # last 30 seconds = 6*5
      time.sleep(20) # Seconds
  except KeyboardInterrupt:
    print("\n done!")

  with open("stats.json", "w") as f:
    json.dump(stats_in_time, f)

if __name__ == "__main__":
  main()