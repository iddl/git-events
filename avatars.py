import hashlib, requests, os
from config import config_provider

settings = config_provider.get()
print(settings)

class binary_cache:

    def __init__(self, cache_folder, size):
        self.cache_folder = cache_folder
        self.cache = dict()
        self.size  = size

        if not os.path.isdir(cache_folder):
            pass


    def encode_target(self, target):
        return hashlib.md5(target.encode('ascii')).hexdigest()[:10]

    def retrieve_content(self, content):
        content = requests.get(content)


    def get(self, content):
        encoded_target = self.encode_target(content)
        if encoded_target in self.cache:
            return self.cache[encoded_target]
        else:
            self.retrieve_content(content)

