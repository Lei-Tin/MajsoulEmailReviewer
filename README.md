# Majsoul Email Akochan Reviewer v1.0

A automatic script that receives email input, and sends Akochan's review back to the sender.

# How do I use this thing?

- Option 1: 
  - Clone the whole repository and modify settings in both config.py and webpageReviewWindows.py so that it can be ran in your local machine. 
  - Then, you can send your email anytime to any email you desire
- Option 2:
  - Use the public email address and my machine to test out this project.
  - Send an email to "xxxxleitinxxxx@163.com", with the subject of the email being:
  - **"{Link to majsoul log} {Player index} \<Optional PT distribution\>"**
  - Player index takes the following format: **{0: 东, 1: 南, 2: 西, 3: 北}**, where the index correspond to the initial location the player is
  - If provided, Akochan will be called with the pt distribution you specified. By default, it uses **"95,45,-5,-95"**, which corresponds to [雀杰1](https://www.zhihu.com/question/474080670) in 金之间, 南风场, with regular 马点
  - Pt distribution has to be specified in the format of 
  - "{1st place pt gain},{2nd place pt gain},{3rd place pt gain},{4th place pt gain}"
  - Example usage of option 2 (Analysis of the game with the player starting at 东, with default PT distribution): 
  - https://game.maj-soul.net/1/?paipu=220619-59f4a3b6-2a44-48f9-a30c-11fcdd24b8eb_a90583244 0

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
