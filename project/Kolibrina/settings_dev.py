from Kolibrina.settings import *

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
DEBUG = True
REDIS_DB = 1

DOMAIN = 'dev.kolibrina.ru'
del STATIC_ROOT
STATICFILES_DIRS = [BASE_DIR / 'static/']

YANDEX_CHECKOUT_CONFIG = {'account_id': '742930',
                          'secret_key': 'test_4Yc8ayWUcMtNKy8RlHjKtgP4aDrcnIy9Xyiq_GYkOVI'}
