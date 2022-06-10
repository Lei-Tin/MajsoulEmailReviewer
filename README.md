# Majsoul Email Akochan Reviewer v1.0

A automatic script that receives email input, and sends Akochan's review back to the sender. 

# Features

- Usage of POP3 to receive and parse emails
- Usage of SMTP to send emails
- Usage of Selenium to imitate actual user logging in and downloading the majsoul log

# File Directory Structure

- webpageReviewWindows.py, the main file of this project, responsible for everything
- webpageReview.py, discontinued version of the webpageReview, because Akochan doesn't support MacOS. 
- config.py, file that is needed to configure multiple settings, such as the POP3, SMTP, Email address, etc. 
- demo.gif, a gif of an example running session
- README.md, the file you are reading at the moment
- downloadlogs.js, the file that has an unknown origin, the script used to download majsoul logs
- review.bat, the file responsible to execute Akochan's analysis
- sent, the file that records the current list of links and emails sent
- chromedriver.exe, the driver for Chrome in Windows
- /ChromeDriver, the driver files that were used to develop this script
- /Logs, a directory to store all the log files and HTML output files by Akochan
- /Akochan, fully adapted from [Akochan-reviewer](https://github.com/Equim-chan/mjai-reviewer), the analysis AI used for this project

# Picture while running

The GIF is a little bit large (40+ MB), so it might take a while to load :3

![Example running scene](https://github.com/Lei-Tin/majsoul-email-reviewer/blob/e8af5199e2bbc12f19a2a3bd2cf9e7ba6cde4061/demo.gif)

# Libraries Used

- time
- selenium
- typing
- subprocess
- os
- poplib
- email
- smtplib
