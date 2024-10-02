# from .base_model import BaseModel
from django.db import models
import logging

class Bookss(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()



    # def save(self, *args, **kwargs):
    #     logging.info(f'Saving Book: {self.title}, Author: {self.author}')
    #     super().save(*args, **kwargs)
        

    # def delete(self, *args, **kwargs):
    #     logging.info(f'Deleting Book: {self.title}')
    #     super().delete(*args, **kwargs)

class OperationQuery(models.Model):
    sql_query = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)






# from django.db import models

# class CustomManager(models.Manager):
#     def save(self, instance, *args, **kwargs):
#          # Custom logic before saving
#         if not instance.pk:  # New instance
#             print(f"Creating a new object: {instance}")
#         else:  # Update existing instance
#             print(f"Updating object: {instance}")

#         # Call the model's save method directly
#         instance.save(*args, **kwargs)

#         # Custom logic after saving
#         print(f"Object {instance} saved successfully")

#     def delete(self, instance, *args, **kwargs):
#         # Custom logic before deleting
#         print(f"Object {instance} is about to be deleted")

#         # Call the default delete method
#         instance.delete(*args, **kwargs)

#         # Custom logic after deleting
#         print(f"Object {instance} has been deleted")
