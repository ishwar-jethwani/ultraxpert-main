from django.db import models
from django_elasticsearch_dsl import Document ,fields
from django_elasticsearch_dsl.registries import registry
from user.models import *


# keep in the index of an object 

@registry.register_document
class ExpertsDocument(Document):
    id = fields.IntegerField(attr='id')
    fielddata=True
    first_name = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
        }
    )
    last_name= fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
        }
    )
    title = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
        }
    )
    description = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
        }
    )


    class Index:
        name = "experts"
        settings = {
        'number_of_shards': 1,
        'number_of_replicas': 1
    }

    class Django:
        model = Profile