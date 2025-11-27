from . import main_url

from psutil import net_io_counters
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

def getTextFromG1(url):
    """
    * Extracts the text of a news article at the url provided. Optimized for articles from 'https:g1.globo.com'.
    * Parameters:
    * * url (string) - Web adrress of the news article
    """
    driver = Firefox()
    driver.get(url)
    textos = driver.find_elements(By.CLASS_NAME, "content-text__container")
    textos_trim = "".join([t.text for t in textos if len(t.text) > 0])
    textos_trim = "".join(textos_trim.split(" "))
    driver.quit()
    return textos_trim

def pickNewsPage():
    """
    * Searches for a random news article page from 'https://g1.globo.com' and returns its web address
    """
    net_read = net_io_counters()
    bytesOut, bytesIn = net_read.bytes_sent, net_read.bytes_recv
    driver = Firefox()
    driver.get(main_url)
    links = driver.find_elements(By.CLASS_NAME, "feed-post-link")
    link_idx = (bytesOut%1000)%len(links)
    chosen_link = links[link_idx]
    href = chosen_link.get_attribute('href')
    driver.quit()
    return href