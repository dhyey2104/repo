import os
import django
import re


# Path to your Django project where models are located
project_path = os.path.expanduser('D:\vizzv\repo')

# BaseModel import line
base_model_import = 'from myapp.base_model import BaseModel'

for root, _, files in os.walk(project_path):
    print(root, _,files)
    for file in files:
        if file.endswith('models.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()

            updated_content = []
            base_model_found = False

            for line in content:
                # Check if BaseModel is already imported
                if base_model_import in line:
                    base_model_found = True

                # Replace `models.Model` with `BaseModel`
                if 'class ' in line and 'models.Model' in line:
                    line = line.replace('models.Model', 'BaseModel')

                updated_content.append(line)

            # Add the BaseModel import if it wasn't found
            if not base_model_found and any('class ' in line for line in content):
                updated_content.insert(0, base_model_import + '\n')

            # Write back the updated content if changes were made
            if updated_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(updated_content)

print("Model inheritance updated successfully.")
