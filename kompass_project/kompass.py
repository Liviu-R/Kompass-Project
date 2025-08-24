#IMPORT UNDETECTED DRIVER FROM SELENIUM CREATOR
import nodriver as uc


#NATIVE PYTHON MODULES
import time
import random as rnd
import pandas as pd
import re
import sys

#SELF CREATED MODULES
import Requests_Setting as set
import cleanup_temp_file as clean

#Class that is used to store information about sites and other information like proxy servers, and file name
class wsj:
    def __init__(self, file='dataset'):
        self.proxies={"http": None,"https":None}
        self.fine_name = file

        
        self.comp_phone = []
        self.comp_names = []
        self.comp_site = []
        self.comp_location = []
       

        self.comp_urls = []


    #Creating the csv file with the file name we input in class scrapper and store it in the program location 
    async def preparing_csv(self)->None:
        print('FINISH')
        path = sys.argv[0].replace('kompass.py', '') + self.fine_name + '.csv'
        info_dict = {'HOMESITE': self.comp_urls,'NAME': self.comp_names,'LOCATION': self.comp_location,'SITE': self.comp_site,'PHONE': self.comp_phone }
        df = pd.DataFrame(info_dict)
        df.to_csv(path, index = False)

    #Getting the data from each company url that was specified by the employer with nodriver(selenium)
    async def getting_info(self)->None:

        site_links=[]
        site_links.extend(self.comp_urls)
        
        print("START GETTING INFORMATION")
        while True:
            try:
                proxy=rnd.choice(set.proxies)

                driver =await uc.start(browser_args=[f"--proxy-server={proxy}","--start-maximized"])

                page =await driver.get(site_links[0])
                
                time.sleep(50)
                #CHECKING THE PAGE SOURCE CODE TO SEE IF IT RIGHT
                html=await page.query_selector(".headerCompany")
                if not html :
                    driver.stop()
                    time.sleep(5)
                    await clean.clean_up(driver)
                    set.removed_proxy.append(proxy)
                    set.proxies.remove(proxy)
                    if not set.proxies:
                        set.getting_proxies()
                    continue   
                
                #GETTING INFORMATION

                site_links.remove(site_links[0])

                #getting name

                name=await page.query_selector(".blockNameHead h1")
                if name:
                    self.comp_names.append(name.text.replace("\n","").replace("\t",""))
                else:
                    self.comp_names.append(None)

                #getting location

                location=await page.query_selector(".blockAddress .spRight")
                if location:
                    self.comp_location.append(location.text_all.replace("\n","").strip())
                else:
                    self.comp_location.append(None)

                #getting site 

                site=await page.query_selector(".tableCompanyRS .listWww a")
                if site:
                    self.comp_site.append(site.text.replace("\n","").strip())
                else:
                    self.comp_site.append(None)

                #getting phone

                phone=await page.query_selector(".contactButton")
                if phone:
                    await phone.click()
                    phone=await page.query_selector(".modal-content .freePhoneNumber")
                    self.comp_phone.append(phone.text.replace("+30","").strip())
                else:
                    self.comp_phone.append(None)

                driver.stop()
                time.sleep(5)
                await clean.clean_up(driver)

                if not site_links:
                    break
                
            except Exception as e:
                print(e)
                set.removed_proxy.append(proxy)
                set.proxies.remove(proxy)
                if not set.proxies:
                    set.getting_proxies()
                continue  
            finally:
                driver.stop()
                time.sleep(5)
                await clean.clean_up(driver)
                
    
        
            

async def main():

    fileName = input('enter file name : ')
    

    scrap = wsj(fileName)

    set.getting_proxies()
    index=1
    last_of_pagination=None
    
    
    #Getting the urls in html and moving on the pagination to storing all in wsj class in comp_urls porperty
    print("START GETTING COMPANIES URLS IN SITE AND PAGINATION")
    while True:
        try:
            proxy=rnd.choice(set.proxies)

            driver =await uc.start(browser_args=[f"--proxy-server={proxy}","--start-maximized"])

            page =await driver.get(f"https://us.kompass.com/businessplace/z/gr/page-{index}/")
            
            time.sleep(50)
            #CHECKING THE PAGE SOURCE CODE TO SEE IF IT RIGHT
            html=await page.query_selector("#classifSEO")
            
            if not html :
                driver.stop()
                time.sleep(5)
                await clean.clean_up(driver)
                set.removed_proxy.append(proxy)
                set.proxies.remove(proxy)
                if not set.proxies:
                    set.getting_proxies()
                continue  
            
            #GETTING COMPANIES URLS BY ITERATING THROUTH PAGINATION UNTLE WE GET LAST

            if last_of_pagination==None:
                last_of_pagination=await page.query_selector_all(".pagination .searchItemLi ")
                last_of_pagination=last_of_pagination[-2].text.replace("\n","").strip()
                last_of_pagination=int(last_of_pagination)
            
            comp_links = await page.query_selector_all(".prod_list .col-title a")
            for link in comp_links:
                scrap.comp_urls.append("https://us.kompass.com"+link["href"])

            index+=1
            
            driver.stop()
            time.sleep(5)
            await clean.clean_up(driver)

            if index > last_of_pagination:
                break
            
            
        except Exception as e:
            print(e)
            set.removed_proxy.append(proxy)
            set.proxies.remove(proxy)
            if not set.proxies:
                set.getting_proxies()
            continue  
        finally:
            driver.stop()
            time.sleep(5)
            await clean.clean_up(driver)
                


    await scrap.getting_info()
    await scrap.preparing_csv()

if __name__ == '__main__':
    uc.loop().run_until_complete(main())