import time
import json


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from setting import *
from functions import *

import hashlib

DOG_PAGE_URL="https://www.dogstrust.org.uk/rehoming/dogs/"
DOG_SITE_URL="https://www.dogstrust.org.uk"
DELAY_TIME=0.1
INFO_SAVE_FOLDER="C:/Dogs/"


if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get(DOG_PAGE_URL)

    # Click accept all button
    ts = time.time()
    ACCPET_ALL_BUTTON = '[id *= "onetrust-accept-btn-handler"]'
    while time.time()-ts < 20 :
        time.sleep(DELAY_TIME)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ACCPET_ALL_BUTTON))
            )
            driver.find_element(By.CSS_SELECTOR, ACCPET_ALL_BUTTON).click()
            print ("Succeed")
            break
        except:
            print('Can\'t Click choose accept all button!')


    # Click Show More Button   
    SHOW_MORE_BOTTON = '[class *= "SectionDogList-module--showmorebutton"]'
    count_failed=1
    while count_failed < 1:
        time.sleep(DELAY_TIME)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SHOW_MORE_BOTTON))
            )
            driver.find_element(By.CSS_SELECTOR, SHOW_MORE_BOTTON).click()
            count_failed=0
        except:
            count_failed +=1
            print('Can\'t Click choose show more button!')

    #Click Dog Cards
    time.sleep(DELAY_TIME)
    dogURLs = []
    try:
        js_script = 'eles = document.querySelectorAll("[class *= \\"SectionDogList-module--component\\"] a[href]");\
            var i = 0;\
            urls = [];\
            for (i = 0; i < eles.length; i++) {\
                urls.push(eles[i].getAttribute("href"));\
            }\
            return urls;\
            '
        dogURLs = driver.execute_script(js_script)
        print(dogURLs)
    except:
        print("Can't click Card")
        pass

    template_info="This dog centered in DogsTrust. This dog is microchipped and neatured."
    for url in dogURLs:
        if '/rehoming/dogs/' not in url:
            continue
        
        dog_unique_url=f'{DOG_SITE_URL}{url}'
        md5_hash = hashlib.md5()
        md5_hash.update(dog_unique_url.encode())
        dog_unique_key = md5_hash.hexdigest()           #Create Dog Unique Key By Using MD5

        driver.get(dog_unique_url)                      #Open Individual Dog Page Url


        GET_DOG_DETAIL_JS_SCRIPT='''
            return document.querySelector(".SectionDogBio-module--dogbioinner--dee72").textContent;
        '''
        dog_detail=driver.execute_script(GET_DOG_DETAIL_JS_SCRIPT)  #Get Individual Dog Detail
        


        GET_DOG_SUMMARY_JS_SCRIPT='''
            var summary_tags = document.querySelectorAll(".SectionTitleBody-module--textarea--4ca48 p");
            var i = 0;
            var summary = '';
            for (i = 0; i < summary_tags.length; i++) {
                summary+=summary_tags[i].textContent;
            }
            return summary;
        '''
        dog_summary=driver.execute_script(GET_DOG_SUMMARY_JS_SCRIPT)    #Get Individual Dog Summary

        data={
            "detail":dog_detail,
            "summary":dog_summary,
            "more":template_info
        }

        with open(INFO_SAVE_FOLDER+dog_unique_key,"w") as file:
            file.write(json.dumps(data))


        
        SAVE_DOG_IMAGE_JS_SCRIPT = '''
            const imgUrlElement = document.querySelector('[class*="IntroDogBio-module--imagewrapper--094a3"] picture source');
            let imgUrl = "";

            if (imgUrlElement) {
                imgUrl = imgUrlElement.getAttribute("srcset").split(",")[0].trim().split(" ")[0];
            }

            if (imgUrl) {
                const xhr = new XMLHttpRequest();
                xhr.open("GET", imgUrl, true);
                xhr.responseType = "arraybuffer";
                xhr.onload = function () {
                    if (this.status === 200) {
                    const blob = new Blob([this.response], { type: "image/jpeg" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "%s.jpeg";
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    }
                };
                xhr.send();
            }
        ''' % dog_unique_key    
        driver.execute_script(SAVE_DOG_IMAGE_JS_SCRIPT)