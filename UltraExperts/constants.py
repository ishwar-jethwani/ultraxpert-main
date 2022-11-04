from requests_aws4auth import AWS4Auth
from decouple import config
DEBUG = config('DEBUG', default=False, cast=bool)
if DEBUG==False:
    RAZOR_KEY_ID = config("RAZOR_KEY_ID_LIVE_NEW")
    RAZOR_KEY_SECRET = config("RAZOR_KEY_SECRET_LIVE_NEW")
else:
    RAZOR_KEY_ID = config("RAZOR_KEY_ID_TEST")
    RAZOR_KEY_SECRET = config("RAZOR_KEY_SECRET_TEST")
    


SECRET_KEY = config("SECRET_KEY")
BASE_URL = config("BASE_URL")
ADMIN_SITE_HEADER = config("ADMIN_SITE_HEADER")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID_1")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY_1")
S3_BUCKET_NAME = config("S3_BUCKET_NAME_1")
REGION_NAME = config("REGION_NAME_1")
VIDEOSDK_API_KEY = config("VIDEOSDK_API_KEY")
PAYMANT_BASE_URL = config("PAYMANT_BASE_URL")
ES_REGION_NAME = config("ES_REGION_NAME")
SERVICE = config("SERVICE")
ELASTIC_SEARCH_URL = config("ELASTIC_SEARCH_URL_1")
MEDIA_BUCKET= config("MEDIA_BUCKET")
# AWS_AUTH = AWS4Auth(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,ES_REGION_NAME,SERVICE)
TWILIO_AUTH_ID = config("TWILIO_AUTH_ID")
TWILIO_SECRET_KEY = config("TWILIO_SECRET_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_FACEBOOK_KEY = config("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET  = config("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_LOGIN_REDIRECT_URL  = config("SOCIAL_AUTH_LOGIN_REDIRECT_URL")
SOCIAL_AUTH_FACEBOOK_SCOPE = config("SOCIAL_AUTH_FACEBOOK_SCOPE")
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = config("SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS")
SOCIAL_AUTH_USER_FIELDS = config("SOCIAL_AUTH_USER_FIELDS")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = config("SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE")
EMAIL_HOST_USER_NAME  = config("EMAIL_HOST_USER_NAME")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")
SERVER = config("SERVER")
REDIS_URL = config("REDIS_URL")
RDS_PRODUCTION_DB_NAME = config("RDS_PRODUCTION_DB_NAME")
RDS_PRODUCTION_DB_USERNAME = config("RDS_PRODUCTION_DB_USERNAME")
RDS_PRODUCTION_DB_PASSWORD = config("RDS_PRODUCTION_DB_PASSWORD")
RDS_PRODUCTION_DB_HOSTNAME = config("RDS_PRODUCTION_DB_HOSTNAME")
RDS_PRODUCTION_DB_PORT = config("RDS_PRODUCTION_DB_PORT")










