# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 23:02:42 2020

@author: dsikerid
Testing
"""





# import requests, bs4, re, time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")

# driver = webdriver.Chrome(options=options, executable_path=r"C:/Users/dsikerid/Desktop/chromedriver.exe")
# driver.get("https://vuejs.github.io/vue-hackernews/#!/news/1")
# print(driver.page_source)
# results = driver.find_elements_by_xpath("//h1")
# print('Number of results', len(results))

# driver.quit()




# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# def correct_url(url): 
#  if not url.startswith("http://") and not url.startswith("https://"):
#   url = "http://" + url
#  return url

# def scrollDown(browser, numberOfScrollDowns):
#  body = browser.find_element_by_tag_name("body")
#  while numberOfScrollDowns >=0:
#   body.send_keys(Keys.PAGE_DOWN)
#   numberOfScrollDowns -= 1
#  return browser

# def crawl_url(url, run_headless=True):


#  options = Options()
#  options.headless = True
#  options.add_argument("--window-size=1920,1200")
#  url = correct_url(url)
#  browser = webdriver.Chrome(options=options, executable_path=r"C:/Users/dsikerid/Desktop/chromedriver.exe")
#  browser.get(url)
#  browser = scrollDown(browser, 10)

#  all_hover_elements = browser.find_elements_by_class_name("hover-box")

#  for hover_element in all_hover_elements:
#      a_element = hover_element.find_element_by_tag_name("a")
#      product_title = a_element.get_attribute("title")
#      product_link = a_element.get_attribute("href")
#      print(product_title, product_link)

#  browser.quit()


# if __name__=='__main__':
#  url = "http://www.jabong.com/men/shoes/new-products/"
#  crawl_url(url)


from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Create a new instance of the Firefox driver
driver = webdriver.Chrome(options=options, executable_path=r"C:/Users/dsikerid/Desktop/chromedriver.exe")

# Go to the Google home page
driver.get('https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url')

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(
            request.url
        )
















