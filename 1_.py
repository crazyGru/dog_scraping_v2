import time
import json
import hashlib
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from setting import *
from functions import *
DOG_PAGE_URL="https://www.dogstrust.org.uk/rehoming/dogs/"
DOG_SITE_URL="https://www.dogstrust.org.uk"
DELAY_TIME=1
INFO_SAVE_FOLDER="C:/Dogs/"
def click_button(driver, css_selector, delay_time, success_message, error_message):
    while True:
        time.sleep(delay_time)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            button = driver.find_element(By.CSS_SELECTOR, css_selector)
            button.click()
            print(success_message)
        except:
            print(error_message)
            break

def get_dog_urls(driver):
    js_script = '''eles = document.querySelectorAll("[class *= \\"SectionDogList-module--component\\"] a[href]");
        var i = 0;
        urls = [];
        for (i = 0; i < eles.length; i++) {
            urls.push(eles[i].getAttribute("href"));
        }
        return urls;
        '''
    try:
        return driver.execute_script(js_script)
    except:
        print("Can't click Card")
        return []

def get_dog_review_info(driver):
    js_script = '''eles = document.querySelectorAll("[class *= 'DogListingCard-module--dogcardcontainer--caada']");
        var i = 0;
        review_infos = [];
        for (i = 0; i < eles.length; i++) {
            review_infos.push(eles[i].textContent);
        }
        return review_infos;
    '''
    try:
        return driver.execute_script(js_script)
    except:
        print("Can't get review info.")
        return []
    
def get_dog_info(driver, dog_unique_url):
    driver.get(dog_unique_url)
    dog_detail = driver.execute_script('return document.querySelector(".SectionDogBio-module--dogbioinner--dee72").textContent;')
    dog_summary = driver.execute_script('''
        var summary_tags = document.querySelectorAll(".SectionTitleBody-module--textarea--4ca48 p");
        var i = 0;
        var summary = '';
        for (i = 0; i < summary_tags.length; i++) {
            summary+=summary_tags[i].textContent;
        }
        return summary;
    ''')
    return dog_detail, dog_summary

def save_dog_info(dog_detail, dog_summary, template_info, dog_review_info, dog_unique_key):
    data = {
        "detail": dog_detail,
        "summary": dog_summary,
        "more": template_info,
        "status" : dog_review_info + ".Get dog status here. check include 'reserved' or 'available'."
    }
    with open(INFO_SAVE_FOLDER + dog_unique_key, "w") as file:
        file.write(json.dumps(data))

def save_dog_image(driver, dog_unique_key):
    driver.execute_script('''
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
    ''' % dog_unique_key)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(DOG_PAGE_URL)
    click_button(driver, '[id *= "onetrust-accept-btn-handler"]', DELAY_TIME, "Succeed", "Can't Click choose accept all button!")
    click_button(driver, '[class *= "SectionDogList-module--showmorebutton"]', DELAY_TIME, "Succeed", "Can't Click choose show more button!")
    dog_urls = get_dog_urls(driver)
    dog_review_infos=get_dog_review_info(driver)
    template_info="This dog centered in DogsTrust. This dog is microchipped and neatured."
    for url, dog_review_info in zip( dog_urls, dog_review_infos):
        if '/rehoming/dogs/' not in url:
            continue
        dog_unique_url = f'{DOG_SITE_URL}{url}'
        md5_hash = hashlib.md5()
        md5_hash.update(dog_unique_url.encode())
        dog_unique_key = md5_hash.hexdigest()
        dog_detail, dog_summary = get_dog_info(driver, dog_unique_url)
        save_dog_info(dog_detail, dog_summary, template_info, dog_review_info, dog_unique_key)
        save_dog_image(driver, dog_unique_key)