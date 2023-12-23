from django.db import models
class FileUpload(models.Model):
    # uploaded_file = models.FileField(upload_to='uploads/') # can be removed
    resized_file = models.FileField(upload_to='uploads/resized/')
    thumbnail = models.FileField(upload_to='uploads/thumbnails/')
    zip_file = models.FileField(upload_to='uploads/zips/')
