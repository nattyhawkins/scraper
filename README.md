# Poolsuite Track History
This is a solo project I have been working on since completing the GA SEI course. It aims to allow the user to stream music, select a channel and skip songs programmatically, whilst keeping a record of the users track history.


## Technologies (So far)
- Python
- Selenium
- Unittest
- Sendgrid email API


## Code Installation
- Clone or download the repo
- `pipenv install` to install dependencies
- `source ./sendgrid.env`
- NOTE: In event of unterminated headless browser, Mac users run: `pkill -f "(chrome)?(--headless)"`


## Instructions
Run `python program.py` to begin! \
Interact with the music station via CLI controls: \
-2 --> Back \
-1 --> Restart \
0 --> Play/Pause \
1 --> Next \
\
CX --> Change to channel X, X in [0, 6] \
    Channel names will be displayed \
\
To run unit tests: add / remove x from start of test names and run `python test_main.py`


## Focus
- Getting to grips with Selenium by following the docs
- Following the page object design pattern
- Implementing unit tests along side new functionality
- Learning about concurrency and incorporating a daemon thread to maintain the "database" in the background
- Parsing CSV files to save track history
- Send track history to email using SendGrid API at end of session
- Meaningful git commits