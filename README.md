# Instructions
For Mac:  
    -Rename chromedriver_v80_macOS to just chromedriver  
    -move it to /usr/local/bin  
For Windows  
    -Rename your chromedriver executable to just chromedriver  
    -Run the chromedriver executable (according to your chrome's version) first *before* you run the script  
(Or download your version here https://chromedriver.chromium.org/downloads)

-Use pip to install selenium (if haven't already): pip install selenium
-Edit the Schedule file to fit your schedule, while KEEPING format and name (seel below)
-Change the email and pass in SID and user_pass variables to your credential in login_creds.py
-Run the main.py (python main.py)

To edit the schedule:
The days are separated by a comma (see line 19 of schedule.json)  
- The name are to be typed in full and first letter must be a cap  
The shifts are separated by a comma too (see line 90)  
- There are only three *shifts type*: VCS, VIT, and Labs. Type it as it is!  
The work study section contains the value "true" or "false", and it's to indicate whether you still have workstudy hours or not  
ALL words must be wrapped in double quotes

Tips: Copy the following SHIFT and paste it in a day (separate it by a comma if you have more than one shift), and edit it according to your schedule  

```
    "shift type":
      {
        "start":
          {
            "hour": "2",
            "min": "30",
            "period": "PM"
          },
        "end":
          {
            "hour": "5",
            "min": "00",
            "period": "PM"
          },
        "isWorkStudy": true
      }
```
