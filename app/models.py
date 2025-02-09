from django.db import models


class Files(models.Model):
    file = models.FileField(upload_to="files")

    def __str__(self):
        return self.file.name
