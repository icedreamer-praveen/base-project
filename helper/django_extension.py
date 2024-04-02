import os

def add_django_ext_config(project_path, project_name):
    """
    Adds Django django_extension configuration to the project.
    
    :param project_path: The path where the project is located.
    :param project_name: The name of the project.
    """
    # Add 'Werkzeug' and 'django-extensions' to requirements.txt
    requirements_path = os.path.join(project_path, 'requirements.txt')
    with open(requirements_path, 'a') as f:
        f.write('Werkzeug\ndjango-extensions\n')

    # Insert 'django_extensions' into THIRD_PARTY_APPS in settings.py
    settings_path = os.path.join(project_path, project_name, 'settings.py')
    replace_django_ext_apps(settings_path)


def replace_django_ext_apps(settings_path):
    """
    The function `replace_django_ext_apps` inserts the string `"django_extensions"` into a Python
    settings file at the location where `THIRD_PARTY_APPS` is defined.
    
    :param settings_path: The `replace_django_ext_apps` function reads the content of a settings file
    located at the `settings_path`, finds the index of the line containing "THIRD_PARTY_APPS", and
    inserts `"django_extensions"` in the list of third-party apps if the line is found
    """
    with open(settings_path, 'r') as file:
        settings_content = file.readlines()
    
    third_party_apps_index = next(
        (i for i, line in enumerate(settings_content) if "THIRD_PARTY_APPS" in line), None
    )
    
    if third_party_apps_index is not None:
        settings_content.insert(third_party_apps_index + 1, '    "django_extensions",\n')
    
    with open(settings_path, 'w') as file:
        file.writelines(settings_content)