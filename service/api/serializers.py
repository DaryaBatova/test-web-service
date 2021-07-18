from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    page_id = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('page_id', 'h1', 'h2', 'h3', 'a')

    def get_page_id(self, instance):
        return instance.id

    def to_representation(self, instance):
        """
        Modifies the representation style: convert 'a' to list of strings.

        :param instance: the object instance that requires serialization.
        :return: a representation of the object instance
        """
        ret = super().to_representation(instance)
        if instance.a == '':
            ret['a'] = []
        else:
            ret['a'] = [link for link in instance.a.split(', ')]
        return ret

