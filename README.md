# Stock-Analysis
# (c) Cobus H Smit 2021

# install with $ python3 -m pip install -r requirements.txt
# python3 -m venv env
# source env/bin/activate

https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
https://chromedriver.storage.googleapis.com/LATEST_RELEASE_
google-chrome --version |python3 -c \
  'import sys, re; s = sys.stdin.read(); s=re.compile("Google Chrome (\d+\.\d+\.\d+)\.\d+").match(s) ; print(f"wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{s.groups()[0]}");'
