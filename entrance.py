__author__ = 'zcq'
#coding:utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import os
import sqlite3
import downloadall


try:

    browser = webdriver.Firefox()  # Get local session of firefox
    conn = sqlite3.connect("/home/zcq/PycharmProjects/PyTest/building.db")
    downloadall.download(conn, browser)

except TimeoutException:
    print 'timeout'
except Exception as ex:
    print ex.message
