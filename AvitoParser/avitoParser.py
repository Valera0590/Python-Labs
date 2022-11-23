import re
from selenium import webdriver
from fileOperations import WriteToFile

# global variables
SITE = "https://www.avito.ru"
# options
options = webdriver.ChromeOptions()
# user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
# ignore-certificates
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-certificate-errors-spki-list")
options.add_argument("--ignore-ssl-errors")

driver = webdriver.Chrome(
    executable_path=r'C:\Users\Валерий\Desktop\Универ\10 трим\ОИС\Lab_7\chromedriver\chromedriver.exe',
    # service=Service(str=r'C:\Users\Валерий\Desktop\Универ\10 трим\ОИС\Lab_7\chromedriver\chromedriver.exe'),
    options=options)

def RemoveSubstring(sourceString, subString):
    result = ""
    i = sourceString.rfind(subString) + len(subString)
    lengthSourceString = len(sourceString)
    while (i < lengthSourceString):
        result += sourceString[i]
        i += 1
    return result

def ParsePriceAndDescriptionToFile(region, category, catchingObject, dirSaveFile):
    try:
        pageNum = 1
        link = SITE+"/"+region+"/"+category+"?p={pageNum}&q="+catchingObject
        driver.get(url=link)
        driver.implicitly_wait(5)
        try:
            pagesButton = driver.find_elements('xpath',"//div[@data-marker='pagination-button']/span")
            driver.implicitly_wait(5)
            pagesCount = int(pagesButton[-2].text)
        except Exception:
            print("This request find only one page.")
            pagesCount = 1
        finally:
            while (pageNum <= pagesCount):
                print(f"Current URL is: {driver.current_url}")
                try:
                    adsLinkList = driver.find_elements("xpath","//div[@data-marker='catalog-serp']//div[@data-marker='item-photo']")
                    driver.implicitly_wait(5)
                    if not adsLinkList:
                        pageNum = pagesCount + 1
                        continue
                except Exception:
                    print(f"This object wasn't find at your region{adsLinkList}")
                    pageNum = pagesCount + 1
                    continue
                finally:
                    descNum = 0
                    for item in adsLinkList:
                        item.click()
                        driver.implicitly_wait(5)
                        driver.switch_to.window(driver.window_handles[1])
                        driver.implicitly_wait(5)
                        urlItemString = str(driver.current_url)
                        print(f"Currently URL is: {urlItemString}")
                        try:
                            # title = driver.find_element('xpath',"//span[@data-marker='item-view/title-info'")
                            title = driver.find_element('class name','title-info-title-text').text
                            driver.implicitly_wait(5)
                            try:
                                description = driver.find_element('xpath',"//div[@data-marker='item-view/item-description']").text
                                driver.implicitly_wait(5)
                                price = driver.find_element('xpath',"//span[@itemprop='price']").get_attribute('content')
                                priceCurrency = driver.find_element('xpath',"//span[@itemprop='priceCurrency']").get_attribute('content')
                                driver.implicitly_wait(5)
                                infoItemString = "\n Title: "+title+"\n Price: "+price+" "+priceCurrency+"\n Link: "+urlItemString+"\n Description: "+description+str("\n\n"+"#"*50+"\n")
                                WriteToFile(dirSaveFile, infoItemString)
                            except Exception:
                                print(f"Description or price not found at page {urlItemString}")
                        except Exception:
                            print(f"Title not found at page {urlItemString}")
                        finally:
                            driver.implicitly_wait(5)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            driver.implicitly_wait(5)
                            descNum += 1
                    if (pageNum != pagesCount):
                        buttonNextPage = driver.find_element("xpath","//span[@data-marker='pagination-button/next']")
                        driver.implicitly_wait(5)
                        buttonNextPage.click()
                        driver.implicitly_wait(5)
                    pageNum += 1
            
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()



def ParseDiffFullAndShortDescriptionToFile(region, category, catchingObject, dirSaveFile):
    try:
        pageNum = 1
        link = SITE+"/"+region+"/"+category+"?p={pageNum}&q="+catchingObject
        driver.get(url=link)
        driver.implicitly_wait(5)
        try:
            pagesButton = driver.find_elements('xpath',"//div[@data-marker='pagination-button']/span")
            driver.implicitly_wait(5)
            pagesCount = int(pagesButton[-2].text)
        except Exception:
            print("This request find only one page.")
            pagesCount = 1
        finally:
            while (pageNum <= pagesCount):
                print(f"Currently URL is: {driver.current_url}")
                try:
                    adsLinkList = driver.find_elements("xpath","//div[@data-marker='catalog-serp']//div[@data-marker='item-photo']")
                    driver.implicitly_wait(5)
                    adsDescriptionList = driver.find_elements("xpath","//div[@data-marker='catalog-serp']//meta[@itemprop='description']")
                    driver.implicitly_wait(5)
                    if not adsLinkList:
                        pageNum = pagesCount + 1
                        continue
                except Exception:
                    print(f"This object wasn't find at your region{adsLinkList}")
                    pageNum = pagesCount + 1
                    continue
                finally:
                    descNum = 0
                    for item in adsLinkList:
                        descriptionShort = adsDescriptionList[descNum].get_attribute("content")
                        item.click()
                        driver.implicitly_wait(5)
                        driver.switch_to.window(driver.window_handles[1])
                        driver.implicitly_wait(5)
                        urlItemString = str(driver.current_url)
                        print(f"Currently URL is: {urlItemString}")
                        try:
                            # title = driver.find_element('xpath',"//span[@data-marker='item-view/title-info'")
                            title = driver.find_element('class name','title-info-title-text')
                            driver.implicitly_wait(5)
                            try:
                                description = driver.find_element('xpath',"//div[@data-marker='item-view/item-description']")
                                driver.implicitly_wait(5)
                                print(f"Short desc: {descriptionShort}\n")
                                print(f"Full desc: {description.text}\n")
                                descriptionFull = re.sub(r'[^\w !?`~\@\(\)\[\],\.\';:\{\}&$%№\*\|\/\–\—\-\+\=\\\n]', '', description.text)
                                if(descriptionShort[0].isalpha() and descriptionShort[0].lower() == descriptionFull[0].lower()):
                                    if(descriptionFull[0].islower()):
                                        descriptionShort = descriptionShort.replace(descriptionShort[0], descriptionShort[0].lower(), 1)
                                descriptionShort = descriptionShort.replace("\xa0—"," -")
                                if (descriptionFull[-1].isalnum()):
                                    descriptionShort = descriptionShort[:-1]
                                descriptionShort=descriptionShort.replace(".\n","\n")
                                descriptionFull=descriptionFull.replace(".\n","\n")
                                print(f"Short desc after changes: {descriptionShort}")
                                # print(f"Different part of desc: {descriptionFull.removeprefix(descriptionShort)}\n")
                                descriptionDiff = RemoveSubstring(descriptionFull, descriptionShort[-7:]) if len(descriptionFull) != len(descriptionShort) else ' '
                                print(f"Different part of desc: {descriptionDiff}\n")
                                # infoItemString = " Title: "+title.text+"\n Link: "+urlItemString+"\n Description: "+descriptionFull.removeprefix(descriptionShort)
                                infoItemString = " Title: "+title.text+"\n Link: "+urlItemString+"\n Description: "+descriptionDiff+str("\n\n"+"#"*50+"\n\n")
                                WriteToFile(dirSaveFile, infoItemString)
                            except Exception as excep:
                                print(f"Description not found at page {urlItemString}")
                        except Exception:
                            print(f"Title not found at page {urlItemString}")
                        finally:
                            driver.implicitly_wait(5)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            driver.implicitly_wait(5)
                            descNum += 1
                    if (pageNum != pagesCount):
                        buttonNextPage = driver.find_element("xpath","//span[@data-marker='pagination-button/next']")
                        driver.implicitly_wait(5)
                        buttonNextPage.click()
                        driver.implicitly_wait(5)
                    pageNum += 1
            
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
