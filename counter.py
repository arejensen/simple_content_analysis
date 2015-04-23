#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This code reads a file containing words you would like to count.
# The words must be on their own line. Left, or right-side whitespace is stripped (including newlines)
# Example format:
# Vice words:
# a
# b
# c
#
# Virtue words:
# x
# y
# z

# The lines "Vice words:" and "Virtue words:" would be ignored since they contain a : (our heading delimiter)
# The blank newline before the "Virtue words:" line will also be removed.


# Note that the code is /very/ verbose, and heavily commented. It's intentional so that non-computer savvy colleagues can
# hack at this with some understanding of what is going on.

DEBUG = True

import sys     # needed for command line arguments
import glob    # needed for gathering list of data_files
from collections import Counter # needed for easy counting of words. Not super efficient, but thats OK.
import pprint  # easier debug
import os      # access to portable path seperators and newline characters
import csv     # for export

# make sure we have enough arguments
if len(sys.argv) < 3:
    print("Usage - " + sys.argv[0] + " wordlist" + " directory_of_files")
    sys.exit()

pp = pprint.PrettyPrinter(indent=4)

# words will, assuming the first argument is a valid filename,
# contain all the lines of the document.
# we strip away lines with : in them. They designate word type.
# we also strip away new lines. We don't care about those.
words = [str.strip(s, " "+os.linesep).lower() for s in open(sys.argv[1]).readlines() if not ":" in s and not s == os.linesep]

if DEBUG: print("\nWord list:\n" + "\n".join(words))
# data_files will, assuming the sys.argv[2] directory exists, and there aren't any errors reading
# them, contain a list of all text files in the sys.argv[2] directory. Identity is determined by their file extension.
data_file_names = glob.glob(sys.argv[2] + os.sep + "*.txt")

if DEBUG: print("\nFile list:\n" + "\n".join(data_file_names))
# data_files_handles will, assuming there aren't any errors creating a handle for
# the files, contain handles for every file
data_file_handles = [open(file_name) for file_name in data_file_names]

# count all the words in every file
word_count_per_file = {}
for handle in data_file_handles:
    word_count_per_file[handle.name] = Counter(handle.read().split()) # reads the files into a list of words
    handle.close()

if DEBUG:
    print("\nPer file data structure")
    pp.pprint(word_count_per_file)

# count the global files in total
word_count_total = {}
for fil in word_count_per_file.keys():               # each file
    for word in word_count_per_file[fil].keys():     # each word in file
        if word not in words:     # not in our word list
           continue
        elif word in word_count_total:
            word_count_total[word] = word_count_total[word] + word_count_per_file[fil][word]
        else:
            word_count_total[word] = 1

if DEBUG:
    print("\nTotal sum data structure")
    pp.pprint(word_count_per_file)


# write everything to disk
writer_total = csv.writer(open('count_total.csv', 'wt'))
writer_total.writerow(["Word", "Count"])
for key, value in word_count_total.items():
    writer_total.writerow([key, value])

writer_each_file = csv.writer(open('count_each_file.csv', 'wt'))

sorted_fnames = sorted(data_file_names)

writer_each_file.writerow([""] + (words))
for fname in sorted_fnames:
    counts = [fname]
    for word in words:
        counts.append(word_count_per_file[fname].get(word, 0))
    writer_each_file.writerow(counts)


print("\nWe should be done. Inspect count_each_file.csv and count_total.csv.")
