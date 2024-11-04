import requests
import datetime
import os
from os.path import join as join
import subprocess
import json

ICONPATH = "//usr/share/bingwallpaper/icons/"
PATH = join(os.getenv("HOME"), ".cache", "bingwallpaper")


def set_wallpaper(filename):
    full_path = join(f"file://{PATH}", filename)
    print(f"Setting wallpaper: {full_path}")

    # Detect the desktop session and session type
    desktop_session = os.getenv("DESKTOP_SESSION", "").lower()
    xdg_session_type = os.getenv("XDG_SESSION_TYPE", "").lower()

    # Define setter functions for KDE, Cinnamon, and GNOME
    def set_kde():
        script = f"""
        qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "
            var allDesktops = desktops();
            for (i=0;i<allDesktops.length;i++) {{
                d = allDesktops[i];
                d.wallpaperPlugin = 'org.kde.image';
                d.currentConfigGroup = Array('Wallpaper', 'org.kde.image', 'General');
                d.writeConfig('Image', '{full_path}');
            }}"
        """
        subprocess.run(script, shell=True, check=True)

    def set_cinnamon():
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.cinnamon.desktop.background",
                "picture-uri",
                full_path,
            ],
            check=True,
        )

    def set_gnome():
        getCurrentImageDetailsLight = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"],
            stdout=subprocess.PIPE,
            check=True,
        )

        getCurrentImageDetailsDark = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.background", "picture-uri-dark"],
            stdout=subprocess.PIPE,
            check=True,
        )

        if getCurrentImageDetailsLight.stdout.decode().strip() != full_path:
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    "picture-uri",
                    full_path,
                ],
                stdout=subprocess.PIPE,
            )

        if getCurrentImageDetailsDark.stdout.decode().strip() != full_path:
            subprocess.run(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    "picture-uri-dark",
                    full_path,
                ],
                stdout=subprocess.PIPE,
            )

    # Set the wallpaper based on the desktop environment
    if desktop_session in ["mate", "xfce"]:
        print(
            f"{desktop_session.capitalize()} desktop detected, you may need a specific handler."
        )
    elif desktop_session in ["cinnamon"]:
        set_cinnamon()
    elif desktop_session in ["plasma", "kde"]:
        set_kde()
    elif desktop_session in ["gnome", "ubuntu", "deepin", "zorin", "pop", "budgie"]:
        set_gnome()
    else:
        print("Unsupported session type")


class BingImage:
    def __init__(self):
        self.index = None
        self.startdate = None
        self.enddate = None
        self.imageurl = None
        self.title = None
        self.description = None
        self.descriptionlink = None
        self.favorite = False

    def get_img(self):
        try:
            response = requests.get(self.imageurl)
            response.raise_for_status()
            if not os.path.exists(PATH):
                os.makedirs(PATH)
            with open(f"{PATH}/{self.startdate}-{self.enddate}.jpg", "wb") as file:
                file.write(response.content)
            print(f"Image {self.startdate}-{self.enddate} downloaded successfully.")
        except Exception as e:
            print(f"Failed to download image {self.index}: {e}")

    def save_img(self, savepath):
        try:
            response = requests.get(self.imageurl)
            response.raise_for_status()
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            with open(f"{savepath}/{self.startdate}-{self.enddate}.jpg", "wb") as file:
                file.write(response.content)
            print(f"Image {self.startdate}-{self.enddate} saved successfully.")
        except Exception as e:
            print(f"Failed to save image {self.index}: {e}")

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
        self.api_endpoint = (
            "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&mkt=en-US"
        )

    def request_data(self):
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            self.data = response.json()
            print("Data fetched successfully.")
        except Exception as e:
            print(f"Failed to fetch data: {e}")

    def extract_images(self):
        if not self.data or "images" not in self.data:
            print("No image data available to extract.")
            return

        count = 0
        for image in self.data["images"]:
            img = BingImage()
            img.index = count
            img.startdate = datetime.date(
                year=int(image["startdate"][:4]),
                month=int(image["startdate"][4:6]),
                day=int(image["startdate"][6:]),
            )
            img.enddate = datetime.date(
                year=int(image["enddate"][:4]),
                month=int(image["enddate"][4:6]),
                day=int(image["enddate"][6:]),
            )
            img.imageurl = "https://www.bing.com" + image["url"]
            img.title = image["title"]
            img.description = image["copyright"].split("(")[0].rstrip()
            img.descriptionlink = "https://www.bing.com" + image["copyrightlink"]
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

        file_count = len([f for f in os.listdir(PATH) if os.path.isfile(join(PATH, f))])
        if file_count > 10:
            self.delete_all_images()

        # Downloading images
        self.images[index].get_img()
        return 1

    def delete_all_images(self):
        for f in os.listdir(PATH):
            file_path = join(PATH, f)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    print(f"Could not find the file {file_path}. File not deleted.")
                except PermissionError:
                    print(f"Permission denied for file {file_path}. File not deleted.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        return 1


class FavoriteCollection:
    def __init__(self):
        self.data = None
        self.folder_path = join(PATH, "favorites")
        self.file_path = join(self.folder_path, "data.json")
        self.images = []
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def extract_images(self):
        if os.listdir(self.folder_path) and os.path.exists(self.file_path):
            self.data = json.load(open(self.file_path))
            count = 0
            for image in self.data:
                img = BingImage()
                img.index = count
                img.startdate = datetime.date(
                    year=int(image["startdate"][:4]),
                    month=int(image["startdate"][4:6]),
                    day=int(image["startdate"][6:]),
                )
                img.enddate = datetime.date(
                    year=int(image["enddate"][:4]),
                    month=int(image["enddate"][4:6]),
                    day=int(image["enddate"][6:]),
                )
                img.title = image["title"]
                img.description = image["copyright"].split("(")[0].rstrip()
                img.favorite = True
                self.images.append(img)
                count += 1
            print(f"Extracted {count} images.")
            return 1
        else:
            print("No image data available to extract.")
            return 0

    def add_favorite(self, image: BingImage):
        if not self.data:
            self.data = []
        self.data.append(
            {
                "startdate": image.startdate.strftime("%Y%m%d"),
                "enddate": image.enddate.strftime("%Y%m%d"),
                "title": image.title,
                "copyright": image.description,
            }
        )
        json.dump(self.data, open(self.file_path, "w"))
        image.save_img(self.folder_path)
        self.images.append(image)
        print(f"Added image to favorites.")
        return 1

    def remove_favorite(self, image: BingImage):
        if not self.data:
            self.extract_images()

        # Find the index of the image in self.data by matching attributes
        data_entry = next(
            (
                entry
                for entry in self.data
                if entry["startdate"] == image.startdate.strftime("%Y%m%d")
                and entry["enddate"] == image.enddate.strftime("%Y%m%d")
            ),
            None,
        )

        if data_entry is not None:
            try:
                # Remove the image file from the filesystem
                os.remove(
                    join(self.folder_path, f"{image.startdate}-{image.enddate}.jpg")
                )

                # Remove the entry from data and images
                self.data.remove(data_entry)
                self.images = [
                    img
                    for img in self.images
                    if img.startdate != image.startdate or img.enddate != image.enddate
                ]

                # Update the JSON file
                with open(self.file_path, "w") as file:
                    json.dump(self.data, file)

                print("Deleted image from favorites.")
                return 1
            except Exception as e:
                print(f"Error deleting image: {e}")
                return 0
        else:
            print("Image not found in favorites.")
            return 0


# Test Script:
if __name__ == "__main__":
    collection = BingCollection()
    collection.request_data()
    collection.extract_images()
    collection.download_image(0)
    set_wallpaper("0-2024-10-12-2024-10-13.jpg")
    # collection.delete_image(0)
