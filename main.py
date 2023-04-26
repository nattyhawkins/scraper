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
import pandas as pd

import sendgrid
import os
from sendgrid.helpers.mail import Mail

"""This page details the main program chain of events, leveraging methods defined on other files"""

class PoolsuiteTracker():    
      def __init__(self, csvpath='db/db.txt'):
          opts = Options()
          opts.add_argument('--headless')
          assert '--headless' in opts.arguments
          self.driver = webdriver.Chrome(options=opts)
          self.driver.get('https://poolsuite.net/')
          self.mainPage = pages.MainPage(self.driver)
          self.database = []
          self.database_path = csvpath

      def start(self):
          self.mainPage.skip_intro()
          self.start_db()
          self.mainPage.welcome()   
          self.mainPage.get_channels()
          self.mainPage.menu()
          self.nav()
          self.tearDown()

      def start_db(self):
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
          while self.mainPage._is_playing:
              self.mainPage.update_current_track() #update current track attribute every 2 mins to account for naturally changing songs
              for x in range(6):
                self._update_db()
                sleep(20)          # Check every 20 seconds

      def _update_db(self):
          """ updates the database array attribute """
          try:
              check = (self.mainPage._current_track_record is not None
                      and (len(self.database) == 0
                            or self.database[-1].title != self.mainPage._current_track_record.title)
                      and self.mainPage._is_playing)
              if check:
                  self.database.append(self.mainPage._current_track_record)
                  self.save_db()
          except Exception as e:
              print('error while updating the db: {}'.format(e))

      def save_db(self):
          """ saves db array to file """
          with open(self.database_path,'w',newline='') as dbfile:
              dbwriter = csv.writer(dbfile)
              dbwriter.writerow(list(TrackRecord._fields)) # write the 1st row of field names using named tuple base helper _fields
              for entry in self.database:
                  dbwriter.writerow(list(entry))

      def send_email_db(self):
          address = self.mainPage._user_address

          if address:
            print('Your session history will be sent to -->', address)
          else:        
            address = 'nhk.development@gmail.com'

          if '@' in address and '.' in address:
            email = pd.read_csv(self.database_path)
            print(f"""Here is your track history to date: 

{email}

Your track history will be emailed to you if a valid address was provided.
            """)

            message = Mail(
              from_email='nhk.development@gmail.com',
              to_emails=address,
              subject='Your latest Poolsuite session is here!',
              html_content=email.to_html(),
              plain_text_content="Something missing? The track history is updated every 20s, so if the listening duration was less than that it may have been missed."
            )

            try:
              sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
              response = sg.send(message)
              return response
            except Exception as e:
              print(e)    

      def nav(self):
          try:    
            choice = input('Enter option: ').lower()
            if choice == 'q':
                return self.send_email_db()
            elif choice.startswith('c') and int(choice[1]) in range(0, 7):
                self.mainPage.select_channel(int(choice[1]))
            elif choice in ['-2', '-1', '0', '1']:
                self.mainPage.track_change(int(choice))
            else: raise Exception('Oops! Invalid input')
          except Exception as e:
              print(e)
          
          self.nav()

      def tearDown(self):
          # ? pkill -f "(chrome)?(--headless)" // Run in CLI to terminate any rogue headless browser instances
          print('Bye!')
          self.driver.close()



