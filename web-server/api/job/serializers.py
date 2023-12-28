from rest_framework import serializers
from api.models import Jobs

class JobsSerializer(serializers.ModelSerializer):
    # salesman_username = serializers.ReadOnlyField(source='salesman.username')
    publishtime = serializers.DateTimeField(required=False)
    class Meta:
        model = Jobs
        fields = '__all__'
class RecommendSerializer(serializers.Serializer):
    pagesize=serializers.IntegerField(max_value=50,min_value=20,default=20)
    page=serializers.IntegerField(max_value=10,min_value=1,default=1)
class CollectSerializer(serializers.Serializer):
    number=serializers.CharField()
class ClickSerializer(serializers.Serializer):
    number=serializers.CharField()
    