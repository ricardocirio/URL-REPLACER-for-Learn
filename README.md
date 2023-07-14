# URL-REPLACER-for-Learn

Simple script to replace Link URLs from Blackboard Learn courses.

usage: learn-url-replacer.py [-h] -s SITE -f FILE -t TITLE -c CURRENT -r REPLACEMENT

options:
  -h,               --help                      Shows help message
  -s SITE,          --site SITE                 Base URL to process, eg test.blackboard.com
  -f FILE,          --file FILE                 File containing course ids, one per line
  -t TITLE,         --title TITLE               Title of Link content item that will be updated
  -c CURRENT,       --current CURRENT           Current URL
  -r REPLACEMENT,   --replacement REPLACEMENT   Replacement URL

Based on [BBDN-REST-DEMO_Python](https://github.com/blackboard/BBDN-REST-DEMO_Python).
