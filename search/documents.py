from django_elasticsearch_dsl import Document ,fields
from django_elasticsearch_dsl.registries import registry
from user.models import *


# keep in the index of an object 

@registry.register_document
class ExpertsDocument(Document):
    categories = fields.ObjectField(
        properties = {
            "name":fields.TextField(),
            "parent":fields.ObjectField(
                properties={
                    "name":fields.TextField()
                }
            )
        }
    )
    keywords = fields.ObjectField(
        properties = {
            "name":fields.TextField()
        }
    )
    description = fields.TextField()

    class Index:
        name = "experts"
        settings = {
        'number_of_shards': 1,
        'number_of_replicas': 1
    }

    class Django:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "is_online",
            "title",
            "education",
            "experience"
        ]
        related_models = [Category,Keywords]

@registry.register_document
class ServiceDocument(Document):
    category = fields.ObjectField(
        properties = {
            'name':fields.TextField(),
            'parent':fields.ObjectField(
                properties={
                    'name':fields.TextField()
                }
            )
        }
    )
    description = fields.TextField()
    class Index:
        name = 'services'
        settings = {
        'number_of_shards': 1,
        'number_of_replicas': 1
    }

    class Django:
        model = Services
        fields = [
            'service_id',
            'service_type',
            'service_name',
            'price'
        ]
        related_models = [Category]

    