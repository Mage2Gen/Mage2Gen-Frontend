from apps.mage2gen.models import Module
from rest_framework import serializers


class GeneratorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Module
		fields = ('id', 'package_name', 'name', 'config')