import recipe_utils as ru
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json
import os
import pickle

# Aloo Gobi
# Chana (Chickpeas) Chaat
# Red Curry Pork With Peppers
# These 3 recipes have one less image
with open(ru.path_encoding_names,"rb") as f:
    data = pickle.load(f,encoding='utf-8')
    # print(data[:5])
    count = 1
    index = 0
    for i in range(1,len(data)):
        ind1 = data[i].split("->")[0]
        ind2 = data[i-1].split("->")[0]
        if ind1== ind2:
            count += 1
        else:
            if count %10 != 0:
                if count < 10:
                    print(data[i-1])
            count = 1
