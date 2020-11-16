import os
import sys
import time

for i in range(0,10):
    blankBubble = 'osascript -e \'tell application "Messages" \n send \".\" to buddy "{}" of service "E:{}" \n end tell\''.format(sys.argv[1],sys.argv[2])
    os.system(blankBubble)
    time.sleep(0.001)

exit()
