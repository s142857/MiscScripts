"""
This is a script to fetch data about Math Seminars from the notice board and
 then create a ics file from it

"""


import time
import os
from selenium import webdriver
driver = webdriver.Chrome()

driver.get('https://www.math.uwaterloo.ca/~wnotice/notice_prgms/wreg/list_notices.pl?dept=all_depts&time_frame=year')

writepath = 'uwmathsems.ics'

with open(writepath, 'w') as f:
    f.write("BEGIN:VCALENDAR\n")
    f.write("PRODID:-//tzurl.org//NONSGML Olson 2016h//EN\n")
    f.write("VERSION:2.0\n")
    f.write("BEGIN:VTIMEZONE\n")
    f.write("TZID:America/Toronto\n")
    f.write("TZURL:http://tzurl.org/zoneinfo-outlook/America/Toronto\n")
    f.write("X-LIC-LOCATION:America/Toronto\n")
    f.write("BEGIN:DAYLIGHT\n")
    f.write("TZOFFSETFROM:-0500\n")
    f.write("TZOFFSETTO:-0400\n")
    f.write("TZNAME:EDT\n")
    f.write("DTSTART:19700308T020000\n")
    f.write("RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\n")
    f.write("END:DAYLIGHT\n")
    f.write("BEGIN:STANDARD\n")
    f.write("TZOFFSETFROM:-0400\n")
    f.write("TZOFFSETTO:-0500\n")
    f.write("TZNAME:EST\n")
    f.write("DTSTART:19701101T020000\n")
    f.write("RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\n")
    f.write("END:STANDARD\n")
    f.write("END:VTIMEZONE\n")

time.sleep(1)

Seminars = []

for i in range(1,4):
    Seminar = driver.find_element_by_xpath('//dl/dt[%d]/a' % i)
    Seminar.click()
    time.sleep(1)
    Type = driver.find_element_by_xpath('//h1').text
    Subject = driver.find_element_by_xpath('//h1[2]').text
    DT = driver.find_element_by_xpath('//h4').text
    Location = driver.find_element_by_xpath('//h4[2]').text
    Speaker = driver.find_element_by_xpath('//h4[3]').text
    Title = driver.find_element_by_xpath('//h2').text
    Abstract = driver.find_element_by_xpath('//blockquote').text
    
    con = time.strptime(DT, '%A, %d %B %Y at %I:%M%p')
    semdt = time.strftime("%Y%m%dT%H%M%S", con)
    hr = int(time.strftime("%H", con)) + 1
    enddt = time.strftime("%Y%m%dT", con) + str(hr) + time.strftime("%M%S", con)
    with open(writepath, 'a+') as f:
        f.write("BEGIN:VEVENT\n")
        f.write('DTSTART;TZID="America/Toronto":' + semdt + "\n")
        f.write('DTEND;TZID="America/Toronto":' + enddt + "\n")
        f.write("SUMMARY:"+ Title + " - " + Speaker +"\n")
        f.write("URL:"+ str(driver.current_url) + "\n")
        f.write("DESCRIPTION:" + Abstract + "\n")
        f.write("LOCATION:"+ Location + "\n")
        f.write("END:VEVENT\n")
    
    driver.back()

with open(writepath, 'a') as f:
    f.write("END:VCALENDAR\n")

driver.quit()
