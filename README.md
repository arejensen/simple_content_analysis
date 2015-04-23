# simple_content_analysis
A simple tool for counting a set of words across a single or multiple text files.

*Requirements:* Python 3

*Usage:* python counter.py [wordlist] [directory containing text (.txt) files]

**Assuming directory structure:**

counter.py
wordlist.txt
txt/text1.txt
txt/text2.txt
txt/text3.txt

*Invocation:*

python counter.py wordlist.txt txt

This will create two csv files. These can then be imported into a spreadsheet program (e.g. Calc, Excel, Numbers).
