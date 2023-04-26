# Poolsuite Track History
This project aims to allow the user to stream music, select a channel and skip songs programmatically, whilst keeping a record of the users track history. The radio will be controllable via CLI. 

⚒️ Work in progress ⚒️ 

## Technologies (So far)
- Python
- Selenium
- Unittest


## Code Installation
- Clone of download the repo
- `pipenv` to install python packages
- Run `source ./sendgrid.env`
- Can add / remove x from test names then run file to run tests. Full program not yet complete.
- If something goes wrong and the headless browser does not terminate when the program end, Mac users run: `pkill -f "(chrome)?(--headless)"`


## Instructions
Interact with the music station via CLI controls:
-2  Back
-1  Restart
0   Play/Pause
1   Next

CX  Change to channel X, X in [0, 6]
    Channel names will be displayed
    i.e. C3 --> Channel 3

## Focus
- Getting to grips with Selenium by following the docs
- Following the page object design pattern
- Implementing unit tests along side new functionality
- Learning about concurrency and incorporating a daemon thread to maintain the "database" in the background
- Parsing CSV files to save track history
- Send track history to email using SendGrid API at end of session
- Meaningful git commits


