from django.db import models

class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Custom save logic
        print(f"Savingsssssssssssghjdkllllllllllllllllll {self.__class__.__name__}: {self}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Custom delete logic
        print(f"Deletingsgvbcnjjjn {self.__class__.__name__}: {self}")
        # super().delete(*args, **kwargs)