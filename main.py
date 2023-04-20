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
from sendgrid.helpers.mail import Mail, To, Content, Email



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
          
          # DB state
          self.database = []
          self.database_path = csvpath

          # Load db if possible
          # if isfile(self.database_path):
          #   with open(self.database_path, newline='') as dbfile: # open and read the csv plain text file
          #       dbreader = csv.reader(dbfile)
          #       next(dbreader)   # skip header line
          #       self.database = [TrackRecord._make(rec) for rec in dbreader]

          # The database maintenance thread
          self.thread = Thread(target=self._maintain, daemon=True) # set daemon flag > background process killed when the main process dies
          self.thread.start()

      def _maintain(self):
          print('miantaiin db')
          while self.is_playing:
              self.mainPage.update_current_track() #update current track attribute every 2 mins to account for naturally changing songs
              for x in range(6):
                self._update_db()
                sleep(20)          # Check every 20 seconds

      def _update_db(self):
          """ updates the database array attribute """
          print('update db')
          try:
              check = (self.mainPage._current_track_record is not None
                      and (len(self.database) == 0
                            or self.database[-1].title != self.mainPage._current_track_record.title)
                      and self.is_playing)
              print('updating... ', check)
              if check:
                  self.database.append(self.mainPage._current_track_record)
                  self.save_db()
          except Exception as e:
              print('error while updating the db: {}'.format(e))

      def save_db(self):
          """ saves db array to file """
          print('save db')
          with open(self.database_path,'w',newline='') as dbfile:
              dbwriter = csv.writer(dbfile)
              dbwriter.writerow(list(TrackRecord._fields)) # write the 1st row of field names using named tuple base helper _fields
              for entry in self.database:
                  dbwriter.writerow(list(entry))
          print('saveddd db')

      def send_email_db(self):
          address = self.mainPage._user_address
          if address == 'nhk':
              address = 'nhk.development@gmail.com'

          if address:
            print('Your session history will be sent to -->', address)

          if '@' in address and '.' in address:
            email = pd.read_csv(self.database_path)

            message = Mail(
              from_email='nhk.development@gmail.com',
              to_emails=address,
              subject='Your latest Poolsuite session is here!',
              html_content=email.to_html()
            )

            try:
              sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
              response = sg.send(message)
              # print(response.status_code)
              # print(response.body)
              # print(response.headers)
            except Exception as e:
              print(e)    


      def tearDown(self):
          # ? pkill -f "(chrome)?(--headless)"
          self.send_email_db()
          self.driver.close()

# run = PoolsuiteTracker('db/db.txt')

