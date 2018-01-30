import os

from toapi.cache import MemoryCache
from toapi.settings import Settings


class MySettings(Settings):
    """
    Create custom configuration
    http://www.toapi.org/topics/settings/
    """

    cache = {
        'cache_class': MemoryCache,
        'cache_config': {},
        'serializer': None,
        'ttl': 10,
    }
    storage = {
        "PATH": os.getcwd(),
        # 使用sqlite作为存储介质
        "DB_URL": 'sqlite:///data.sqlite',
    }
    web = {
        "with_ajax": False,
        "request_config": {},
        "headers": None
    }
