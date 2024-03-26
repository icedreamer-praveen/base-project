import os
import shutil

# Constants
IGNORE_DIRS = ['.git', 'venv', 'mediafiles', 'staticfiles', 'config']
IGNORE_FILES = ['project_init.py', 'README.md']


# Replacement patterns
REPLACE_PATTERNS = {
    'asgi': ["os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')", "ASGI config for backend project."],
    'wsgi': ["os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')", "WSGI config for backend project."],
    'manage': ["os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')"],
    'settings': [
        "ROOT_URLCONF = 'backend.urls'",
        "WSGI_APPLICATION = 'backend.wsgi.application'",
    ]
}

def create_project_dir(project_location, project_name):
    project_path = os.path.join(project_location, project_name)

    # Check if the directory exists and is not empty; prompt for a new name if it is
    while os.path.exists(project_path) and os.listdir(project_path):
        print("Directory is not empty.")
        project_name = input("Enter a different project name: ")
        project_path = os.path.join(project_location, project_name)

    os.makedirs(project_path, exist_ok=True)
    return project_path

def copy_project_files(source, dest, project_name=None):
    for filename in os.listdir(source):
        if filename in IGNORE_FILES:
            continue
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest)
        elif os.path.isdir(file_path) and filename not in IGNORE_DIRS:
            if filename == 'backend':
                shutil.copytree(file_path, os.path.join(dest, project_name))
            else:
                shutil.copytree(file_path, os.path.join(dest, filename))

def replace_strings_in_file(filepath, replace_strings):
    with open(filepath, 'r') as f:
        file_lines = f.readlines()

    for i, line in enumerate(file_lines):
        for original, replacement in replace_strings.items():
            if original in line:
                file_lines[i] = line.replace('backend', replacement)
    with open(filepath, 'w') as f:
        f.writelines(file_lines)

def initialize_project(project_location, project_name):
    project_path = create_project_dir(project_location, project_name)
    copy_project_files('.', project_path, project_name=project_name)

    file_paths = get_file_paths(project_path, project_name)

    # Replace strings in files
    for key, replacement_strings in REPLACE_PATTERNS.items():
        replace_strings_in_file(file_paths[key], {original: project_name for original in replacement_strings})

    return file_paths

    # Define file paths for replacements and removals
def get_file_paths(project_path, project_name):
    return {
        'asgi': os.path.join(project_path, project_name, 'asgi.py'),
        'wsgi': os.path.join(project_path, project_name, 'wsgi.py'),
        'settings': os.path.join(project_path, project_name, 'settings.py'),
        'manage': os.path.join(project_path, 'manage.py'),
        'root_urls': os.path.join(project_path, project_name, 'urls.py'),
        'utilis_models': os.path.join(project_path, 'utilis', 'models.py'),
        'utilis_serializers': os.path.join(project_path, 'utilis', 'serializers.py'),
        'utilis_views': os.path.join(project_path, 'utilis', 'views.py'),
        'utilis_admin': os.path.join(project_path, 'utilis', 'admin.py'),
    }

def main():
    project_location = input("Enter project location: ")
    project_name = input("Enter project name: ")

    initialize_project(project_location, project_name)

    print(f"Project {project_name} created at {project_location}")

if __name__ == "__main__":
    main()