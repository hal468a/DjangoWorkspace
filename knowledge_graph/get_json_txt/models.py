from django.db import models

class JsonData(models.Model):
    data = models.JSONField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.create_at)
