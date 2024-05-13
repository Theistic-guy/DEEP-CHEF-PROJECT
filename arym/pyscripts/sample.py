import recipe_utils as ru
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json
import os
import pickle

with open(ru.path_encoding_names,"rb") as f:
    data = pickle.load(f,encoding='utf-8')
    # print(data[:5])
    count = 1
    index = 0
    for i in range(1,len(data)):
        if data[i] == data[i-1]:
            count += 1
        else:
            if count %10 != 0:
                if count < 10:
                    print("hello")
            count = 1