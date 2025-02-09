from rest_framework import serializers


class FilesSerializer(serializers.Serializer):
    file_id = serializers.CharField()
    chunk_index = serializers.IntegerField()
    total_chunk = serializers.IntegerField()
    file = serializers.FileField()
    file_name = serializers.CharField()
