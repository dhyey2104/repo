from django.apps import AppConfig


class MyappsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapps'




# from django.apps import AppConfig
# from django.db import models
# import types
# import logging


# def custom_save(self, *args, **kwargs):
#     # Custom save logic here
#     print("Custom save method called")
#     super(models.Model, self).save(*args, **kwargs)

# def custom_delete(self, *args, **kwargs):
#     # Custom delete logic here
#     print("Custom delete method called")
#     super(models.Model, self).delete(*args, **kwargs)

# class MyappsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'myapps'

#     def ready(self):

#         models.Model.save = types.MethodType(custom_save, models.Model)
#         models.Model.delete = types.MethodType(custom_delete, models.Model)


#         # Import your custom model base class
#         # from .custom_models import CustomModel
#         print("hiiiiiiiiiiiiiiiiiiiiiii ")
#         # Prevent adding CustomModel if it's already a base
#         # if CustomModel not in models.Model.__bases__:
#         #     print("Trueeee")
#         #     print(CustomModel,";;;;;;;;")
#         #     models.Model.__bases__ 
#         #     models.Model.__bases__ = (CustomModel,) + models.Model.__bases__[1:]


            
#         print(models.Model.__bases__,"============")
#         #     # Dynamically add CustomModel to Model's base classes
#         #     models.Model.__bases__ = (CustomModel,) + models.Model.__bases__

#         print("CustomModel applied to Model basessss")