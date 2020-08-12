# Dependencies
from bs4 import BeautifulSoup as bs
import requests as req
from splinter import Browser
#from selenium import webdriver
import time
import os
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "driver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



