from django.db import models

class Document(models.Model):
    doc_id = models.IntegerField(db_index=True)
    text = models.TextField()
    title = models.TextField()
    views_count = models.IntegerField(default=0)
