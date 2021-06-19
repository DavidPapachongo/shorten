from typing import Counter
from rest_framework import serializers
from shortURL.models import UrlModel, ClickModel
from rest_framework import serializers


class UrlSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    link = serializers.URLField()
    clicks_counter = serializers.ReadOnlyField()
    shorten_link = serializers.ReadOnlyField()
    
    def create(self, validated_data):
        return UrlModel.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance

class ClickSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    created = serializers.DateTimeField()
    url_id = serializers.ReadOnlyField()
    user_agent = serializers.ReadOnlyField()
    browser = serializers.ReadOnlyField()
    

        

    



