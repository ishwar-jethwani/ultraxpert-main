from requests_aws4auth import AWS4Auth
from elasticsearch import RequestsHttpConnection

SECRET_KEY = 'django-insecure-4dxo_xznm7s#882^*pg0$885t=je!kh)(^qt+pg#kp!&%**wd)'
AWS_ACCESS_KEY_ID = "AKIA5DN3OIK4N4I7SMC3"
AWS_SECRET_ACCESS_KEY = "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"
S3_BUCKET_NAME = "videcontainer"
REGION_NAME = "ap-northeast-2"
RAZOR_KEY_ID = "rzp_test_8k0QagjXoofUTa"
RAZOR_KEY_SECRET = "gBFymE5aOESg7DnwpydhhPHd"
VIDEOSDK_API_KEY = "8a6405a4-3c2b-474b-acc0-c49367cfad89"
PAYMANT_BASE_URL = "https://api.razorpay.com/v1/"
SERVICE = "es"
awsauth = AWS4Auth(
                    AWS_ACCESS_KEY_ID,
                    AWS_SECRET_ACCESS_KEY,
                    REGION_NAME,
                    SERVICE ,
                )

ELASTICSEARCH_DSL = {
        "default":{
                    "hosts": "https://search-ultracreation-ujxyyd6ezbuiqexwslu5pe4b5m.ap-south-1.es.amazonaws.com/",
                    "http_auth": awsauth,
                    "use_ssl": True,
                    "verify_certs": True,
                    "connection_class": RequestsHttpConnection,
                    }
}