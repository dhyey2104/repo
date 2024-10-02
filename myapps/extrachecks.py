# from django.db.models.signals import post_save, pre_delete
# from django.dispatch import receiver
# from django.db import connection

# # Define a function to execute raw SQL query to pass data to the MySQL trigger
# def execute_trigger_for_model(operation, model_name, instance):
#     with connection.cursor() as cursor:
#         # Construct an SQL query to simulate the operation for the trigger
#         sql_query = f"/* Operation: {operation} on Model: {model_name} */"
        
#         # Optionally, you can run any raw SQL query if needed, or just log it.
#         # In this case, we're simulating the action with a comment for debugging purposes.
#         cursor.execute(sql_query)

# # Trigger after saving (create or update) the instance
# @receiver(post_save)
# def handle_model_save(sender, instance, created, **kwargs):
#     if created:
#         operation = 'INSERT'
#     else:
#         operation = 'UPDATE'
    
#     # Extract the model name from the instance's metadata
#     model_name = instance._meta.model_name
#     # Call the function to execute SQL trigger and pass the necessary details
#     execute_trigger_for_model(operation, model_name, instance)

# # Trigger before deleting the instance
# @receiver(pre_delete)
# def handle_model_delete(sender, instance, **kwargs):
#     operation = 'DELETE'
#     # Extract the model name from the instance's metadata
#     model_name = instance._meta.model_name
#     # Call the function to execute SQL trigger and pass the necessary details
#     execute_trigger_for_model(operation, model_name, instance)



from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from django.apps import apps

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    # Get the model name dynamically
    model_name = instance._meta.db_table
    
    # Determine operation type
    operation_type = 'INSERT' if created else 'UPDATE'

    # Prepare the raw SQL query for INSERT or UPDATE
    if created:
        # For INSERT operation, construct an INSERT SQL query
        raw_sql_query = f"INSERT INTO {model_name} ({', '.join([field.name for field in instance._meta.fields])}) VALUES ({', '.join(['%s' for _ in instance._meta.fields])})"
    else:
        # For UPDATE operation, construct an UPDATE SQL query
        raw_sql_query = f"UPDATE {model_name} SET {', '.join([f'{field.name} = %s' for field in instance._meta.fields])} WHERE id = %s"

    # Call the stored procedure to log the operation with the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(f"CALL log_table_operations('{model_name}', '{operation_type}', '{raw_sql_query}');")

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    # Get the model name dynamically
    model_name = instance._meta.db_table
    
    # Prepare the raw SQL query for DELETE
    raw_sql_query = f"DELETE FROM {model_name} WHERE id = %s"

    # Call the stored procedure to log the operation with the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(f"CALL log_table_operations('{model_name}', 'DELETE', '{raw_sql_query}');")
