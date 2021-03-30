
# extract_instadata

Application that extracts data from instagram given a username.


## How to install 
1. Clone this repository
2. Create a python virtual environment and activate it
3. Run >pip install requirements.txt
4. Start Django server


## How does it work

1. Type the instagran username that you want to scrape without @
2. After process, it shows if the account is private or if it's public
2.1 If it's public, it shows a link to get details. This show all posts.

Note: Even when the application has a web interface it's a scraper, for that reason, the process to get data may take several minuts, so ensure that the server doesn´t have time out issues.


## Why a Django web app for a Scraper

The approach of this project is apply knowledge related to extract information from internet, use of Django with its ORM and Testing.
