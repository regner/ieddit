DEBUG = True

DATABASE = 'ieddit'
PG_USER = 'test'
PG_PASSWORD = 'test'
PG_HOST = 'localhost'


DB_TYPE = 'sqlite'

if DB_TYPE == 'sqlite':
	DATABASE_URI = 'sqlite:///{0}.db'.format(PG_USER)
	SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}.db'.format(PG_USER)

elif DB_TYPE == 'postgres':
	DATABASE_URI = 'postgres://{0}:{1}@{2}:5432/{3}'.format(PG_USER, PG_PASSWORD, PG_HOST, DATABASE)
	SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}:5432/{3}'.format(PG_USER, PG_PASSWORD, PG_HOST, DATABASE)

# This will be unique every time create_db.py is ran when testing
# to force clear sessions

SECRET_KEY = 'not-a-real-key-|r|hqLVmN0jv-|r|'

# Chhange this to your local URL. IE http://127.0.0.1
URL = 'http://dev.ieddit.com'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_COOKIE_SAMESITE='Lax'

CACHE_TYPE = 'simple'
RATE_LIMIT = False
RATE_LIMIT_TIME = 5
LIMITER_DEFAULTS = ['600 per minute']
CAPTCHA_ENABLE = False
CAPTCHA_NUMERIC_DIGITS = 8

SESSION_TYPE = 'filesystem'
USE_PROXIES = False

if USE_PROXIES:
	with open('proxies.txt', 'r') as p:
		proxy = p.read().strip()
		PROXIES = {'http':'http://' + proxy, 'https':'https://' + proxy}
else:
	PROXIES = None

PHEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
