# For people who are lazy to read this

Use your RSS reader to subscribe [http://rss.hsexpert.net/dakimakura_news?appendmonthes=1](http://rss.hsexpert.net/dakimakura_news?appendmonthes=1)

# Getting started

First, you need:

* Node.js (Tested on v4.3.1 LTS and 5.7.0 stable)
* Python3 (Tested on Python 3.4.3)

And then do `pip install -r requirements.txt` and `npm install` to install required packages.

After install, run `get_this_month.sh` to get the latest RSS, then run `node server.js` to start the server.

Open your RSS reader or browser and visit `http://localhost:3081` to get the RSS feed.

If everything is OK, setup a cron job to run `get_this_month.sh` daily (or whatever you like), keep server up. **And Enjoy It!**

## URL Parameter
### Get data more than this month
Add `?appendmonthes=N` to get N more monthes data. (The max of N is 12, the number over 12 will be treated as 12.)

Example: `http://localhost:3081/?appendmonthes=1` give you data of this month and previous month.

### Get data of specified month
Change your URL to `/date/YYYYMM` will give you the data of month you request.

Example `http://localhost:3081/date/201601` will give you data of Jan 2016.

## LICENSE

MIT license, do whatever you want, feel free to fork, pull request are welcome.

