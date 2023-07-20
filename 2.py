import time
import json
import hashlib
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from setting import *
from functions import *
DOG_PAGE_URL="https://www.nawt.org.uk/rehoming/dogs/"
DOG_SITE_URL="https://www.nawt.org.uk"
DELAY_TIME=1
INFO_SAVE_FOLDER="C:/Dogs/"
DOWNLOAD_FOLDER="C:/Users/Administrator/Downloads/"
def click_button(driver, css_selector, delay_time, attempts, success_message, error_message):
    while attempts:
        time.sleep(delay_time)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            button = driver.find_element(By.CSS_SELECTOR, css_selector)
            button.click()
            print(success_message)
        except:
            print(error_message)
            break
        attempts=attempts-1
    if attempts: return False
    return True

def get_dog_urls(driver):
    js_script = '''dg_individual_urls=[]
        elements=document.querySelectorAll('[class*="page-cards__image"]');
        elements.forEach(element=>{
            dg_individual_urls.push(element.getAttribute("href"));
        });
        return dg_individual_urls;
        '''
    try:
        return driver.execute_script(js_script)
    except:
        print("Can't click Card")
        return []
    
def get_dog_reviews(driver):
    js_script = '''
        dg_individual_reviews=[]
        elements=document.querySelectorAll('[class*="page-cards__text"]');
        elements.forEach(element=>{
            dg_individual_reviews.push(element.textContent);
        });
        return dg_individual_reviews;
        '''
    try:
        return driver.execute_script(js_script)
    except:
        print("Can't get review")
        return []
    
def get_dog_info(driver, dog_unique_url):
    driver.get(dog_unique_url)
    dog_detail = driver.execute_script('return document.querySelector(".two-col-content").textContent;')
    return dog_detail

def save_dog_info(dog_detail, template_info, review, dog_unique_key):
    data = {
        "detail": dog_detail,
        "more": template_info,
        "status" : review + ".This shows this dog is available or reserved. If not include 'reserved', then it is available."
    }
    with open(INFO_SAVE_FOLDER + dog_unique_key, "w") as file:
        file.write(json.dumps(data))

def save_dog_image(driver, dog_unique_key):
    get_image_request=driver.execute_script('''return document.querySelector('[class*="content-image__image preview-image external-image rehoming-ratio"]').getAttribute("data-image");''')
    response = requests.get(get_image_request)

    if response.status_code == 200:
        image_name = f'{DOWNLOAD_FOLDER}{dog_unique_key}.jpeg'
        with open(image_name, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {image_name}")
    else:
        print("Error downloading the image")
    
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(DOG_PAGE_URL)
    click_button(driver, '[class*="ch2-btn ch2-allow-all-btn ch2-btn-primary"]', DELAY_TIME, 1, "Succeed", "Can't Click accept all button!")
     # Click Next Button
    time.sleep(1)
    dog_urls = []
    dog_reviews = []
    while True:
        time.sleep(1)
        dog_urls.extend(get_dog_urls(driver))
        dog_reviews.extend(get_dog_reviews(driver))
        if not click_button(driver, '[title="Next page"]', DELAY_TIME, 1, "Succeed", "Can't Click choose show more button!"):
            break

    print(dog_urls)
    template_info="This dog centered in National Animal Welfare Trust. This dog is microchipped and neatured."
    for url, review in zip(dog_urls, dog_reviews):
        dog_unique_url = f'{DOG_SITE_URL}{url}'
        md5_hash = hashlib.md5()
        md5_hash.update(dog_unique_url.encode())
        dog_unique_key = md5_hash.hexdigest()
        dog_detail = get_dog_info(driver, dog_unique_url)
        save_dog_info(dog_detail, template_info, review, dog_unique_key)
        save_dog_image(driver, dog_unique_key)