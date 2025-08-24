from requests import request,session
import random as rnd
import time

proxies=[]
removed_proxy=[]

#HTTP header used for custom requests
headers={"chrome":{
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8,el;q=0.7',
    'Cache-Control':'no-cache',
    'Cookie':'',
    'Pragma':'no-cache',
    'Priority':'u=0, i',
    'Sec-Ch-Device-Memory':'8',
    'Sec-Ch-Ua':'"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Arch':'"x86"',
    'Sec-Ch-Ua-Full-Version-List':'"Google Chrome";v="125.0.6422.142", "Chromium";v="125.0.6422.142", "Not.A/Brand";v="24.0.0.0"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Model':'""',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                   }
            }

#Getting free proxies for proxyscrape.com throught HTTP request and storing in a list
def getting_proxies()->None:

    global removed_proxy

    print("GETTING PROXIES")

    headings=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36']
    
    

    flag=True

    while flag:

        half_proxies=[]
        
        try:
            proxyscrape_s=session()
            proxyscrape_s.headers=headers_in_proxies={'User-Agent':rnd.choice(headings)}
            proxyscrape=proxyscrape_s.request(url="https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&anonymity=Elite&timeout=4016",headers=headers_in_proxies,method="GET").text
            proxyscrape_s.close()
        except ConnectionError as e:
            print(f"ConnectionError: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(15)
            continue

        new_proxies=proxyscrape.split("\r\n")
        for proxy in new_proxies:
            if proxy not in removed_proxy:
                half_proxies.append(proxy)

        if not half_proxies:
            removed_proxy=[]
            continue

        if '' in half_proxies:
            half_proxies.remove('')


        proxies.extend(half_proxies)
        break
