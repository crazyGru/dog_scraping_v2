import requests
import os

# API URL for downloading the image
api_url = 'https://nawtavailableanimalsapi.mycharms.uk/api/Public/AnimalImage?id=4887&w=450&h=400&tblid=10976'

# Send a GET request to the API to download the image
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    # Specify the desired filename
    new_filename = 'new_image_filename!!!!!!!!.jpeg'

    # Save the downloaded image with the new filename
    with open(new_filename, 'wb') as file:
        file.write(response.content)

    # Print a success message
    print(f"Image saved as {new_filename}")
else:
    # Print an error message if the request was not successful
    print("Error downloading the image")