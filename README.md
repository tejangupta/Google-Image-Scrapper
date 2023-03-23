# Google Image Scrapper
#### Description:
This is a Python script for scraping images from Google Images. It uses the Selenium and requests libraries to download images and can be run on a local machine with Google Chrome installed.

#### Modules and Packages Used:
- logging
- os
- time
- requests
- selenium

#### Installation
1. Clone the repository or download the source code.
2. Install the required libraries by running the following command in your terminal:
   `pip install -r requirements.txt`
3. Download the Chrome driver executable compatible with your version of Google Chrome from the following link: <br>
   `https://sites.google.com/a/chromium.org/chromedriver/downloads`
4. Move the Chrome driver executable to the root of the project directory.

#### Usage
To use this script, follow these steps:
1. Set the variable **search_term** in line 113 as whatever you would like the images of.
2. Run the following command in the terminal to start the image scraping process:<br>
   `python scrapper.py`
3. Wait for the script to complete. The downloaded images will be saved in the target directory.

#### Logging
The script logs each significant step using the Python logging module. The log file is named img_scrap.log and is located in the project directory. The log level is set to INFO and the log format includes the date, log level, and log message.
