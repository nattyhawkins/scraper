from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pages
from track_record import TrackRecord
from locators import *
from element import *
from threading import Thread
from time import sleep
from os.path import isfile
import csv
import smtplib
from email.message import EmailMessage

"""This page details the main program chain of events, leveraging methods defined on other files"""

class PoolsuiteTracker():    

      def __init__(self, csvpath=None):
          opts = Options()
          opts.add_argument('--headless')
          assert '--headless' in opts.arguments
          self.driver = webdriver.Chrome(options=opts)
          self.driver.get('https://poolsuite.net/')
          self.mainPage = pages.MainPage(self.driver)
          self.is_playing = True

          self.mainPage.skip_intro()
          # self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
          # self.mainPage.get_channels()
          
          # DB state
          self.database_path=csvpath
          self.database = []

          # Load db if possible
          if isfile(self.database_path):
            with open(self.database_path, newline='') as dbfile: # open and read the csv plain text file
                dbreader = csv.reader(dbfile)
                next(dbreader)   # skip header line
                self.database = [TrackRecord._make(rec) for rec in dbreader]
          

          # The database maintenance thread
          self.thread = Thread(target=self._maintain, daemon=True) # set daemon flag > background process killed when the main process dies
          self.thread.start()

      def _maintain(self):
          while self.is_playing:
              self.mainPage.update_current_track() #update current track attribute every 2 mins to account for changing songs
              for x in range(6):
                print('Maintaining db')
                self._update_db()
                sleep(20)          # Check every 20 seconds

      def _update_db(self):
          try:
              check = (self.mainPage._current_track_record is not None
                      and (len(self.database) == 0
                            or self.database[-1] != self.mainPage._current_track_record)
                      and self.is_playing)
              if check:
                  self.database.append(self.mainPage._current_track_record)
                  self.save_db()

          except Exception as e:
              print('error while updating the db: {}'.format(e))

      def save_db(self):
          print('Saving db')
          with open(self.database_path,'w',newline='') as dbfile:
              dbwriter = csv.writer(dbfile)
              dbwriter.writerow(list(TrackRecord._fields)) # write the 1st row of field names using named tuple base helper _fields
              for entry in self.database:
                  dbwriter.writerow(list(entry))

      def send_email_db(self):
          print('sending email')
          with open(self.database_path) as fp:
              msg = EmailMessage()
              msg.set_content(fp.read())

          msg['Subject'] = f'Your latest Poolsuite session is here!'
          msg['From'] = msg['To'] = 'ne.hawkins4@gmail.com'

          # Set up own SMTP server
          s = smtplib.SMTP('localhost')
          s.send_message(msg)
          s.quit()      


      def tearDown(self):
          self.driver.close()

