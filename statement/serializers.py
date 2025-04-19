from rest_framework import serializers
from .models import Statement

class StatementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ['id', 'user', 'credit', 'debit', 'balance',
            'details', 'currency', 'created_at', 'updated_at', 'statement_uuid']
        read_only_fields = ['id', 'created_at', 'updated_at', 'statement_uuid']

class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__'