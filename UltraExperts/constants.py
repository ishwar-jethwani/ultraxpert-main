from requests_aws4auth import AWS4Auth


SECRET_KEY = "django-insecure-4dxo_xznm7s#882^*pg0$885t=je!kh)(^qt+pg#kp!&%**wd)"
AWS_ACCESS_KEY_ID = "AKIA5DN3OIK4N4I7SMC3"
AWS_SECRET_ACCESS_KEY = "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"
S3_BUCKET_NAME = "videcontainer"
REGION_NAME = "ap-northeast-2"
RAZOR_KEY_ID = "rzp_test_8k0QagjXoofUTa"
RAZOR_KEY_SECRET = "gBFymE5aOESg7DnwpydhhPHd"
VIDEOSDK_API_KEY = "8a6405a4-3c2b-474b-acc0-c49367cfad89"
PAYMANT_BASE_URL = "https://api.razorpay.com/v1/"
SERVICE = "es"
ELASTIC_SEARCH_ENDPOINT = "https://search-ultracreation-ujxyyd6ezbuiqexwslu5pe4b5m.ap-south-1.es.amazonaws.com/"
AWS_AUTH = AWS4Auth(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,REGION_NAME,SERVICE)
TWILIO_AUTH_ID = "ACd22bf4b8b61b6e2f7ca81bef207a8c7c"
TWILIO_SECRET_KEY = "30759284eac6beaa003544ce1a022cea"



