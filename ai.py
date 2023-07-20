import os
import openai
import mysql.connector
import json 
import base64, requests
class DogDataProcessor:
    def __init__(self):
        self.openai_api_key="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"
        self.db_config = {
            'host': "35.214.46.153",
            'user': "upbhfcibi1c6j",
            'password': "@7h35@1i5@@3",
            'database': "dbuabl3ljbq6px"
        }
        self.info_save_folder = "C:/DOGS/"
        self.sample_data_keys = [
            'name', 'status', 'city', 'county', 'country', 'sex', 'breed', 'center', 'min_age','max_age',
            'size', 'could_live_with_dogs', 'could_live_with_cats', 'could_live_with_young_child',
            'could_live_with_older_child', 'could_be_left_alone', 'microchipped', 'neutered'
        ]
    def get_dog_info(self, dog_data):
        try:
            prompt = f"{dog_data}This is dog description. Give me {', '.join(self.sample_data_keys)}. Provide the response in JSON format, with keys in lowercase without spaces or symbols. State and country should be filled from the location with the shortest public name. If 'yes',fill '1', 'no',fill'0',maybe, fill'2'. Age with only count of months."
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=500,
                temperature=0.8,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                n=1
            )
            return json.loads(response.choices[0].text.strip())
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return {"":""}
    def get_dog_summary(self, dog_data):
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f"{dog_data}Give me a summary not include age information about this dog with around 150 words with several paragraph.",
            max_tokens=300,
            temperature=0.8,
            top_p=0.9,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            n=1
        )
        return response.choices[0].text.strip()
    def insert_data_to_db(self, cursor, unique_key, json_data, summary):
        select_sql = "SELECT UID FROM `wp_dogs` WHERE `UID` = %s"
        cursor.execute(select_sql, (unique_key,))
        _ = cursor.fetchall()
        result=cursor.fetchone()
        if result:
            print("Data already exists. Skipping insert.")
            return False
        insert_sql = "INSERT INTO `wp_dogs`(`UID`, `name`, `status`, `location`, `county`, `country`, `min_age` ,`max_age`, `sex`, `breed`, `center`, `size`, `dog`, `cat`, `children`, `olderchildren`, `microchipped`, `neutered`, `alone`, `intro`, `src`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            unique_key, json_data['name'], json_data['status'], json_data['city'], json_data['county'],
            json_data['country'], json_data['min_age'], json_data['max_age'], json_data['sex'], json_data['breed'], json_data['center'], json_data['size'],
            json_data['could_live_with_dogs'], json_data['could_live_with_cats'],
            json_data['could_live_with_young_child'], json_data['could_live_with_older_child'],
            json_data['microchipped'], json_data['neutered'], json_data['could_be_left_alone'],
            summary, f"{unique_key}.webp"
        )
        try:
            cursor.execute(insert_sql, values)
            return True
        except Exception as e:
            return False
    def header(self, user, password):
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header_json = {'Authorization': 'Basic ' + token.decode('utf-8')}
        return header_json
    def upload_image_to_wordpress(self, file_path, url, header_json):
        media = {'file': open(file_path,"rb"),'caption': 'My great demo picture'}
        responce = requests.post(url + "wp-json/wp/v2/media", headers = header_json, files = media)
        print(responce)
    def process_unique_keys(self):
        hed = self.header("DEVGURU","ptJl zgJu T2a5 DaZ8 fcnC QOKg")
        with mysql.connector.connect(**self.db_config) as connection:
            cursor = connection.cursor()
            while len(os.listdir(self.info_save_folder)):
                for unique_key in os.listdir(self.info_save_folder):
                        print(unique_key)
                        with open(f"{self.info_save_folder}{unique_key}", 'r') as file:
                            dog_data = file.read()
                            print(dog_data)
                            json_data = self.get_dog_info(dog_data)
                            print(json_data)
                            if list(json_data.keys()) != self.sample_data_keys:
                                print(list(json_data.keys()))
                                print(self.sample_data_keys)
                                print("Keys mismatch")
                                continue
                            summary = self.get_dog_summary(dog_data)
                            print(summary)
                            file_path = "C:\\Users\\Administrator\\Downloads\\" + unique_key +".jpeg"
                            if self.insert_data_to_db(cursor, unique_key, json_data, summary):
                                connection.commit()
                                if os.path.exists(file_path):
                                    self.upload_image_to_wordpress(file_path, 'https://www.dogowner.co.uk/',hed)
                                    os.remove(file_path)
                            else:
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                        os.chmod(f"{self.info_save_folder}{unique_key}",0o777)
                        os.remove(f"{self.info_save_folder}{unique_key}")

if __name__ == "__main__":
    openai.api_key="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"
    processor = DogDataProcessor()
    processor.process_unique_keys()