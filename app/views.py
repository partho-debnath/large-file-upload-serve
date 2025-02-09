import os
from pathlib import Path
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .models import Files
from .serializers import FilesSerializer


class FileUploadView(APIView):

    serializer_class = FilesSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_serializer = self.serializer_class(data=request.data)
        upload_to = Files._meta.get_field("file").upload_to
        file_path = Path.joinpath(settings.MEDIA_ROOT, upload_to)
        if file_serializer.is_valid():
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_id = file_serializer.validated_data.get("file_id")
            chunk_index = file_serializer.validated_data.get("chunk_index")
            total_chunk = file_serializer.validated_data.get("total_chunk")
            chunk = request.FILES.get("file")

            temp_file_path = Path.joinpath(file_path, f"{file_id}.part")
            with open(temp_file_path, "ab") as file:
                for chunk_item in chunk.chunks():
                    file.write(chunk_item)
            if int(chunk_index) + 1 == int(total_chunk):
                file_name = file_serializer.validated_data.get("file_name")
                main_file_path = Path.joinpath(file_path, file_name)
                os.rename(temp_file_path, main_file_path)

                relative_file_path = os.path.relpath(
                    path=main_file_path, start=settings.MEDIA_ROOT
                )
                Files.objects.create(file=relative_file_path)
                return Response({"message": "File upload success."})
            else:
                return Response(file_serializer.data)
        else:
            return Response(file_serializer.errors)


class ServeFileAPiView(APIView):

    def get(self, request, *args, **kwargs):
        file_obj = get_object_or_404(Files, pk=kwargs.get("pk"))
        response = StreamingHttpResponse(self.get_file(file_obj.file.path))
        response["Content-Length"] = file_obj.file.size
        response["Content-Disposition"] = f"attachment; filename={file_obj.file.name}"
        return response

    def get_file(self, file_path):
        # 1MB = 1025KB; 1KB = 1024Bytes;  (1024 * 1024)Bytes == 1MB
        chunk_size = 1024 * 1024

        with open(file_path, "rb") as file:
            while chunk := file.read(chunk_size):
                yield chunk
