# iMessage-Server / Auto-Responder
Python program to process iMessages as they are sent to your computer, and send back responses.

Demonstration:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/_PM09SBeWTk/0.jpg)](https://www.youtube.com/watch?v=_PM09SBeWTk)

### Requirements:
- Your Computer [must be in "rootless" mode.](https://osxdaily.com/2015/10/05/disable-rootless-system-integrity-protection-mac-os-x/)

- for the pre-written song function you must have the youtube downloader downloaded

- to start: ```python3 start.py```

```brew install youtube-dl```

### Make sure you change credentials.py to your information

# HOW TO PRE-PROGRAM RESPONSES

in ```commandprocess.py```, responses can be written like so:

```   if (message = "hi"): ```

```           sendMessage.messageSend("Hey, how's it going!",sender)  ```
