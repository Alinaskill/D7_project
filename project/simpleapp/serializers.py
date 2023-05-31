from .models import *
from rest_framework import serializers


class NewSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = New
       fields = ['id', 'name', 'description', ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['id', 'name', ]


