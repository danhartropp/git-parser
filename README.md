## This is a simple script to get headline activity stats for each contributor to a git repo

It is not intended to be used as a tool for measuring developer productivity. It will give you a sense of who has contributed the most changes to the repo over time - and where those changes have been made. It tells you nothing about the quality of those changes, or how many of them were bugfixes t solve problems caused by previous changes.

It could be useful as a **starting point** for understanding the output of developers on a team, relative to each other. If one set of numbers looks high or low to you, ask why.

## Usage

You'll need to have git installed and available on the command line in the target directory. You can test this with "git log".

The script only uses the standard library, so it should work with any version of Python 3, without the need for a virtual environment or installing and third-party libraries.

The script works in the directory it is run from ... so copy it into the repo directory, or call the script from that directory using its path. Typical usage is "python git_stats.py".

The script takes no parameters, but there are some config variables at the start of the script that can tweak how it works.

**IGNORE** : a list of .gitignore style regex patterns for files/folders that should be excluded from the analysis.

**WEIGHTINGS** : Git log reports the number of additions and the number of deletions for each file in each commit. Intuitively, it is easier to delete code than it is to write it, so a deletion should be "worth" less ... but deleting code is not a bad thing, so it should be worth something. By default, a deletion is worth half an addition.

**MONTHS_AGO** : How many months of commits to include in the analysis ... the default is 12.

## Outputs

An html file with headline stats is generated in the working folder, along with a csv of the weighted changes made in each file by each author. This is intended for further analysis using e.g. pivot tables or making pretty charts.

## TODO

1. The script needs testing on a bunch of repos
2. Tests - with test cases for all of the regex string stuff.

## Contributions

Feel free to make contributions if you'd like ... create a pull request and have at it!
