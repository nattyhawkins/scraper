# Poolsuite Track History
This is a solo project I have been working on since completing the GA course. After It aims to allow the user to stream music from Poolsuite.net via a headless browser, controlling the music station programmatically, whilst keeping a record of the users track history which can then be shared via email. The key focus points were:

- Getting to grips with Selenium by following the docs
- Following the page object design pattern
- Implementing unit tests along side new functionality
- Learning about concurrency and incorporating a daemon thread to maintain the database in the background
- Parsing CSV files to save track history
- Send track history to email using SendGrid API at end of session
- Meaningful git commits

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
0  --> Play/Pause \
1  --> Next \
\
CX --> Change to channel X, X in [0, 6] \
sChannel names will be displayed \
\
To run unit tests: add / remove x from start of test names and run `python test_main.py`


ReadMe under construction.

## Build Process

### Planning, initial research, and set up
To begin with, I researched headless browsers and web scraping, whilst going through the Selenium docs to understand how it works. Although the documentation seems fairly comprehensive, there were some aspects of the example code that were not explained so well, particularly in the Page Objects section detailing the overal design pattern. Thanks to a YouTube tutorial that explained this chapter thoroughly, this did not remain an issue. Selenium had also undergone some updates since the example code had been written, so some of it was no longer applicable. This just required a little extra research to adjust.

After setting up a GitHub repo for the project and a virtual environment using pipenv, I created the main files and classes, following the reccomended structure in the documentation. These pages included: locators, pages, elements, tests and main.

Once the Chrome Driver was defined in the main class constructor, and the test file defined with setUp and tearDown methods, I could run a placeholder test, confirming the headless browser and test class ran properly.

For the locator page, I defined a list of the key elements I knew I would need to target, finding unique selectors of each by looking through the web page html in browser developer tools. 
![locators](/images/locators.png)

In Selenium, the web page elements are formed by inheriting base get/set functionality from a BasePageElement class, and its unique locator is defined as an attribute, referencing the locator page defined previously. The get and set methods needed some alterations to match the new Selenium release, and I changed the get method to retreive all elements matching the given locator rather than one. This made it easier for me to access all the channel names and return it in an array.
![element](/images/element.png)


### Methods and tests
With the main elements now defined and easily accessable, I wrote the first unit test corresponding to a mainPage method that simply skips the intro animation played upon loading Poolsuite. This involved waiting for various elements to be visible, performing an ActionChain to press spacebar, and ensuring the music is playing thereafter.

click_element was another key method, taking a locator as a paramater. Due to the dynamic nature of the website, I realised that using Waits at the start of methods added a margin for delay, preventing errors where the target element had not yet become visible. The Wait is set to a max of 10s though will end when the subsequent until() method resolves. This makes the program more efficient than using a predetermined time.sleep call as it will wait for only the required length of time. 

The idea behind select_channel is to accept an integer as argument corresponding to the desired channel, jumping to the subsequent channel by default if no argument is passed. This method works for looping the 7 channels, though could be improved by dynamically retreiving the number of channels as currently 7 is hardcoded. The locator is defined and if the target channel is above 3, an ActionChain performs a downward scroll to move the element into view before the click_element method is called. There was a bug on the website, where some songs would not play and the radio would remain paused. To fix this, I wrote the ensure_is_playing method which clicks the play button repeatedly until a playable track begins. 

![methods](/images/methods.png)

As an example, the test corresponding to this method calls the select_channel method on each channel, asserting that the correct channel is saved "in memory" followed by a 2s sleep for me to hear the channel playing. The final assertion confirms that the channel box has returned to its default state for future interactions.

![tests1](/images/tests1.png)

### Concurrency

I took this opportunity to do some research on concurrency, learning about pre-emptive vs cooperative multitasking (Threading and Asyncio) for input/output bound problems, in contrast to the truely parallel multiprocessing for CPU bound problems. 

The benefit of using a daemon thread to maintain the database is that the program will preemptively switch over when it is optimal, during pauses in the main program, and terminate with the main program. 

![db maintenance](/images/startdb.png)

### CSV Parsing
The start_db function loads the existing data from the csv file into memory, before beginning the maintenance thread. Here, the _current_track_record attribute is updated every 2 mins to account for naturally changing songs. The assumption is that all songs last at least 2 mins. Every 20 seconds, a named tuple record of the track is created and added to the database array attribute if it does not match the previously added record. Then, the updated database is saved to the csv, writing in each record.

![save db](/images/savedb.png)

### Email API: Sendgrid

### Command Line UI loop
