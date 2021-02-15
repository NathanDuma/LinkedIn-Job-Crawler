# Linkedin Job Crawler
Automatically crawl linkedin and save job application links for later use. Skips easy apply jobs.

This bot is written in Python using Selenium.

## Setup 

To run the bot, open the command line in the cloned repo directory and install the requirements using pip with the following command:
```bash
pip install -r requirements.txt
```

Next, you need to fill out the config.yaml file. Most of this is self-explanatory but if you need explanations please see the end of this README.

```yaml
email: email@domain.com
password: yourpassword

disableAntiLock: False

remote: False

experienceLevel:
 internship: False
 entry: True
 associate: False
 mid-senior level: False
 director: False
 executive: False
 
jobTypes:
 full-time: True
 contract: False
 part-time: False
 temporary: False
 internship: False
 other: False
 volunteer: False
 
date:
 all time: True
 month: False
 week: False
 24 hours: False
 
positions:
 #- First position
 #- A second position
 #- A third position
 #- ...
locations:
 #- First location
 #- A second location
 #- A third location
 #- ...
distance: 25

outputFileDirectory: C:\Users\myDirectory\

companyBlacklist:
 #- company
 #- company2

titleBlacklist:
 #- word1
 #- word2
```


## Execute

To run the bot, run the following in the command line:
```
python3 main.py
```

Explanations for config.yaml:
Just fill in your email and password for linkedin.
```yaml
email: email@domain.com
password: yourpassword
```
This prevents your computer from going to sleep so teh bot can keep running when you are not using it. Set this to True if you want this disabled.
```yaml
disableAntiLock: False
```
Set this to True if you want to look for remote jobs only.
```yaml
remote: False
```
This is for what level of jobs you want the search to contain. You must choose at least one.
```yaml
experienceLevel:
 internship: False
 entry: True
 associate: False
 mid-senior level: False
 director: False
 executive: False
```
This is for what type of job you are looking for. You must choose at least one.
```yaml
jobTypes:
 full-time: True
 contract: False
 part-time: False
 temporary: False
 internship: False
 other: False
 volunteer: False
```
How far back you want to search. You must choose only one.
```yaml
date:
 all time: True
 month: False
 week: False
 24 hours: False
 ```
A list of positions you want to apply for. You must include at least one.
```yaml
positions:
 #- First position
 #- A second position
 #- A third position
 #- ...
 ```
A list of locations you are applying to. You must include at least one.
```yaml
locations:
 #- First location
 #- A second location
 #- A third location
 #- ...
 ```
How far out of the location you want your search to go. You can only input 0, 5, 10, 25, 50, 100 miles.
```yaml
distance: 25
 ```
This is the directory where all the job application stats will go to.
```yaml
outputFileDirectory: C:\Users\myDirectory\
 ```
A list of companies to not apply to.
```yaml
companyBlacklist:
 #- company
 #- company2
 ```
A list of words that will be used to skip over jobs with any of these words in there.
```yaml
titleBlacklist:
 #- word1
 #- word2
 ```
