from rest_framework import serializers
from api.models import company

class companySerializer(serializers.ModelSerializer):

    class Meta:
        model = company
        fields = '__all__'

    