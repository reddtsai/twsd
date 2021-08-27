from selenium import webdriver

class Chrome_Browser:
    def __init__(self):
        # Chrome Options
        self.__option = webdriver.ChromeOptions()
        self.__option.add_argument('--headless') 
    
    def new_chrome_browser(self):
        # Chrome
        self.Browser = webdriver.Chrome(executable_path='./drivers/chromedriver', options=self.__option)

    def close(self):
        self.Browser.quit()
