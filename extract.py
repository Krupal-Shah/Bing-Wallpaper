import requests
import datetime
import os
import subprocess

PATH = '//usr/share/Bing-Wallpaper/images'

def setWallpaper(filename):
    full_path = os.path.join(f'file:/{PATH}', filename)
    print(full_path)

    getCurrentImageDetailsLight = subprocess.run([
        "gsettings", "get", "org.gnome.desktop.background", "picture-uri"
    ], stdout=subprocess.PIPE, check=True)

    getCurrentImageDetailsDark = subprocess.run([
        "gsettings", "get", "org.gnome.desktop.background", "picture-uri-dark"
    ], stdout=subprocess.PIPE, check=True)

    output1 = getCurrentImageDetailsLight.stdout.decode().strip()
    output2 = getCurrentImageDetailsDark.stdout.decode().strip()
    print(output1, output2)

    # if getCurrentImageDetailsLight.stdout.decode().strip() != full_path:
    #     subprocess.run([
    #         "gsettings", "set", "org.gnome.desktop.background", "picture-uri", full_path
    #     ], stdout=subprocess.PIPE)

    # if getCurrentImageDetailsDark.stdout.decode().strip() != full_path:
    #     subprocess.run([
    #         "gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", full_path
    #     ], stdout=subprocess.PIPE)

    # return f"{output1} \n {output2} \n {full_path}"

class BingImage:
    def __init__(self):
        self.index = None
        self.startdate = None
        self.enddate = None
        self.imageurl = None
        self.title = None
        self.description = None
        self.descriptionlink = None

    def get_img(self):
        try:
            response = requests.get(self.imageurl)
            response.raise_for_status()  # Raise an exception for HTTP errors
            if not os.path.exists(PATH):
                os.makedirs(PATH)
            with open(f'{PATH}/{self.index}-{self.startdate}-{self.enddate}.jpg', 'wb') as file:
                file.write(response.content)
            print(f"Image {self.index}-{self.startdate}-{self.enddate} downloaded successfully.")
        except Exception as e:
            print(f"Failed to download image {self.index}: {e}")

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_description_link(self):
        return self.descriptionlink

class BingCollection:
    def __init__(self):
        self.data = None
        self.images = []
        self.api_endpoint = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&mkt=en-US"

    def request_data(self):
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.data = response.json()
            print("Data fetched successfully.")
        except Exception as e:
            print(f"Failed to fetch data: {e}")

    def extract_images(self):
        if not self.data or 'images' not in self.data:
            print("No image data available to extract.")
            return

        count = 0
        for image in self.data['images']:
            img = BingImage()
            img.index = count
            img.startdate = datetime.date(year=int(image['startdate'][:4]), month=int(image['startdate'][4:6]), day=int(image['startdate'][6:]))
            img.enddate = datetime.date(year=int(image['enddate'][:4]), month=int(image['enddate'][4:6]), day=int(image['enddate'][6:]))
            img.imageurl = "https://www.bing.com" + image['url']
            img.title = image['title']  # Fixed: should access image['title'] not img['title']
            img.description = image['copyright'].split('(')[0].rstrip()
            img.descriptionlink = "https://www.bing.com" + image['copyrightlink']
            self.images.append(img)
            count += 1
        print(f"Extracted {count} images.")
        return

    def download_image(self, index):
        # Data not extracted yet
        if not self.images:
            self.extract_images()

        # Images file is not empty.
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        
        file_count = len([f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))])
        if file_count > 10:
            self.delete_all_image()

        # Downloading images
        self.images[index].get_img()

    def delete_all_image(self):
        for f in os.listdir(PATH):
            os.remove(os.path.join(PATH, f))
    
# Test Script:
if __name__ == "__main__":
    collection = BingCollection()
    collection.request_data()
    collection.extract_images()
    collection.download_image(0)
    setWallpaper('0-2024-10-09-2024-10-10.jpg')
    # collection.delete_image(0)
