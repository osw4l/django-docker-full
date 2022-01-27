import json
from django.conf import settings

class RedisClient:
    @staticmethod
    def get_client():
        return settings.REDIS

    def get(self, key: str):
        return self.get_client().get(key)

    def set(self, key: str, value: str):
        self.get_client().set(key, value)

    def get_json(self, key: str):
        bytes_data = self.get(key=key)
        json_data = bytes_data.decode('utf8').replace("'", '"')
        return json.loads(json_data)


client = RedisClient()
