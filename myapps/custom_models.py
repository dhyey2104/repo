# # myapp/models/custom_model.py
# from django.db import models

# class CustomModelBase(models.base.ModelBase):
#     def __new__(cls, name, bases, attrs):
#         # Add custom behavior to save() or other methods here
#         print(f"Custom model base class is applied to {name}")
#         return super().__new__(cls, name, bases, attrs)

# class CustomModel(models.Model, metaclass=CustomModelBase):
#     class Meta:
#         abstract = True

#     def save(self, *args, **kwargs):
#         print(f"Custom save method called in {self.__class__.__name__}")
#         return super().save(*args, **kwargs)



# from django.db import models

# class CustomManager(models.Manager):
#     def save(self, instance, *args, **kwargs):
#         # Custom logic before saving
#         if not instance.pk:  # New instance
#             print(f"New object {instance} is being created")
#         else:  # Update existing instance
#             print(f"Object {instance} is being updated")

#         # Call the default save method
#         super().save(*args, **kwargs)

#         # Custom logic after saving
#         print(f"Object {instance} saved successfully")

#     def delete(self, instance, *args, **kwargs):
#         # Custom logic before deleting
#         print(f"Object {instance} is about to be deleted")

#         # Call the default delete method
#         instance.delete(*args, **kwargs)

#         # Custom logic after deleting
#         print(f"Object {instance} has been deleted")



from django.db import models

class CustomModel:
    class Meta:
        abstract = True  # Ensure this is an abstract model



    def save(self, *args, **kwargs):
        print(f"Custom save method called for {self.__class__.__name__}")
        # Additional logic can be added here if needed
        super().save(*args, **kwargs)  # Call the original save method
