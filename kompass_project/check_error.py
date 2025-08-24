#SELF CREATED MODULES
import Requests_Settings as set

#Function that check if the site returned a error page or other and removing the proxy that fail from list
def check_error_site(html,proxy)->bool:

    if "https://geo.captcha-delivery.com/interstitial" in html:
        set.proxies.remove(proxy)
        if not set.proxies:
            set.getting_proxies()
        return False

    if "δυνατή" in html:
        set.proxies.remove(proxy)
        if not set.proxies:
            set.getting_proxies()
        return False
    if "Please enable JS and disable any ad blocker" in html:
        set.proxies.remove(proxy)
        if not set.proxies:
            set.getting_proxies()
        return False
    
    if "Please contact your local Kompass or support.bip@kompass.com" in html:
        set.proxies.remove(proxy)
        if not set.proxies:
            set.getting_proxies()
        return False
    
    if "Η σύνδεσή σας δεν είναι ιδιωτική" in html:
        set.proxies.remove(proxy)
        if not set.proxies:
            set.getting_proxies()
        return False
    
    return True