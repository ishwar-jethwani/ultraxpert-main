# from django_elasticsearch_dsl import Document ,fields
# from django_elasticsearch_dsl.registries import registry
# from user.models import *


# # keep in the index of an object 

# @registry.register_document
# class ExpertsDocument(Document):
#     description = fields.TextField()
#     profile = fields.ObjectField(properties={
#         "user_id":fields.KeywordField()
#     })

#     class Index:
#         name = "experts"
#         settings = {
#         'number_of_shards': 1,
#         'number_of_replicas': 1
#     }

#     class Django:
#         model = Profile
#         fields = [
#             "first_name",
#             "last_name",
#             "profile_img",
#             "gender",
#             "is_online",
#             "title",
#             "education",
#             "experience",
#             "country"
#         ]

# @registry.register_document
# class ServiceDocument(Document):
#     description = fields.TextField()
#     category = fields.ObjectField(properties={
#         "name":fields.KeywordField()
#     })
#     class Index:
#         name = 'services'
#         settings = {
#         'number_of_shards': 1,
#         'number_of_replicas': 1
#     }

#     class Django:
#         model = Services
#         fields = [
#             'service_id',
#             'service_type',
#             "service_img",
#             'service_name',
#             'price'
#         ]

    