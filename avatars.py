import hashlib, requests, os
from config import config_provider

settings = config_provider.get()

class binary_cache:

    def __init__(self):
        self.cache_folder = settings["Internal"]["cache_directory"]
        self.cache = dict()

        if not os.path.isdir(self.cache_folder):
            os.makedirs(self.cache_folder)

        self.warm_cache()

    def encode_target(self, target):
        return hashlib.md5(target.encode('ascii')).hexdigest()[:10]

    def warm_cache(self):
        for cached_file in os.listdir(self.cache_folder):
            self.cache[cached_file] = self.cache_folder + '/' + cached_file

    def get_content_filename(self, content):
        return self.cache_folder + '/' + self.encode_target(content)

    def download_content(self, content):
        downloaded_content = requests.get(content)
        filename = self.encode_target(content)
        binary_file = open(self.get_content_filename(content), 'wb')
        binary_file.write(downloaded_content.content)
        binary_file.close()
        self.cache[filename] = self.get_content_filename(content)

    def is_cached(self, target):
        encoded_target = self.encode_target(target)
        if encoded_target in self.cache:
            return True
        else:
            return False

    def retrieve_cached(self, target):
        encoded_target = self.encode_target(target)
        return self.cache[encoded_target]

    def get(self, content):
        if self.is_cached(content):
            return self.retrieve_cached(content)
        else:
            return self.download_content(content)


class AvatarProvider():

    def __init__(self):
        self.instance = None

    def get(self):
        if self.instance is None:
            self.instance = binary_cache()
        return self.instance

avatar_provider = AvatarProvider()