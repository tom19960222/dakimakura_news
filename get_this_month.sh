#! /bin/bash

DATE=`date '+%Y%m'`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON3="/usr/bin/python3"

$PYTHON3 $DIR/dakimakura_news.py $DATE > $DIR/rss/$DATE.json

