from .models import Customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('c_custkey', 'c_mktsegment','c_nationkey','c_name','c_address','c_phone','c_acctbal','c_comment')