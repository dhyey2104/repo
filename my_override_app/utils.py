# model_overrides/utils.py

from django.apps import apps
from myapps.models import OperationQuery
# Replace with the correct path to Model501

# Function to log changes to Model501
def log_model_change(instance, change_type):
    print(f"Primary Key: {instance.pk}")
    
    model_name = instance.__class__.__name__
    my_qry = ''
    
    # If creating a new record (INSERT)
    if change_type == 'create':
        field_dict = {}

        # Get all fields and values dynamically
        for field in instance._meta.fields:
            field_name = field.name
            field_value = getattr(instance, field_name)

            # Exclude the primary key field (like 'id') in INSERT
            if field_name != 'id':
                field_dict[field_name] = field_value  # Add field name and value to the dictionary

        # Constructing the dynamic insert query
        fields = ', '.join(field_dict.keys())
        values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in field_dict.values()])
        my_qry = f"INSERT INTO {model_name} ({fields}) VALUES ({values})"

    # If updating an existing record (UPDATE)
    elif change_type == 'update':
        field_dict = {}
        my_qry = f"UPDATE {model_name} SET "
        # Get all fields and values dynamically
        for field in instance._meta.fields:
            field_name = field.name
            field_value = getattr(instance, field_name)

            # Exclude the primary key field (like 'id') in INSERT
            if field_name != 'id':
                field_dict[field_name] = field_value  # Add field name and value to the dictionary

        for i in field_dict.keys():
            my_qry+=f"{i}='{field_dict[i]}',"
        
        my_qry = my_qry.rstrip(',')
        my_qry += f' WHERE id={instance.pk}'

    elif change_type == 'delete':
        my_qry = f"DELETE from {model_name} WHERE id={instance.pk}"

    print(my_qry)

    # Save the generated query to OperationQuery
    OperationQuery.objects.create(
        sql_query=my_qry
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
        if model.__name__ not in ["OperationQuery","LogEntry"]:
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
