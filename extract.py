import requests
import datetime
import os
import subprocess

def setWallpaper(file_path):
    full_path = os.path.abspath(file_path)
    print(full_path)
    subprocess.run([
        "gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{full_path}"
    ])
    subprocess.run([
        "gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", f"file://{full_path}"
    ])
    return

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
            if not os.path.exists('images'):
                os.makedirs('images')
            with open(f'images/{self.index}.jpg', 'wb') as file:
                file.write(response.content)
            print(f"Image {self.index} downloaded successfully.")
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
        self.curr_image = 0
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
        if not os.path.exists('images'):
            os.makedirs('images')
        image_path = f'images/{index}.jpg'
        if os.path.exists(image_path):
            self.delete_image(index)

        # Downloading images

        self.images[index].get_img()
        return 1

    def delete_image(self, index):
        if not os.path.exists('images'):
            print("No images directory to delete from.")
            return 1

        try:
            image = self.images[index]
            image_path = f'images/{image.index}.jpg'
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Image {image.index} deleted.")
            else:
                print(f"Image {image.index} not found.")
        except Exception as e:
            print(f"Failed to delete image {image.index}: {e}")
            return 1

        return

# Test Script:
if __name__ == "__main__":
    collection = BingCollection()
    collection.request_data()
    collection.extract_images()
    collection.download_image(0)
    collection.delete_image(0)
