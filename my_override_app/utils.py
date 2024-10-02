# model_overrides/utils.py

from django.apps import apps
from myapps.models import OperationQuery
  # Replace with the correct path to Model501

# Function to log changes to Model501
def log_model_change(instance, change_type):
    print(instance,change_type)
    # print(instance)
    OperationQuery.objects.create(
        sql_query = change_type
    )

def create_custom_save(original_save):
    
    def custom_save(self, *args, **kwargs):
        if self.pk is None:
            change_type = 'create'
        else:
            change_type = 'update'
        # Call the original save method
        original_save(self, *args, **kwargs)
        # Log the change in Model501
        log_model_change(self, change_type)
    return custom_save

# Create a delete method factory to handle closures properly
def create_custom_delete(original_delete):
    def custom_delete(self, *args, **kwargs):
        # Log the delete action
        log_model_change(self, 'delete')
        # Call the original delete method
        original_delete(self, *args, **kwargs)
    return custom_delete



# Function to globally override save and delete methods for all models
def override_methods_globally():
    for model in apps.get_models():
        print("modelllllllllllll",model)
        import types
        if model.__name__ != "OperationQuery":  # Skip Model501
            # Override save
            print(model.__name__)
            original_save = model.save
            print(original_save,"---------")
            print((model))
            custom_save = create_custom_save(original_save)
            # model.save = types.MethodType(custom_save, model)
            
            # Override delete method
            original_delete = model.delete
            custom_delete = create_custom_delete(original_delete)
            # model.delete = types.MethodType(custom_delete, model) 

            model.add_to_class('save', custom_save)
            model.add_to_class('delete', custom_delete)

        