import os
import shutil

IGNORE_DIRS = ['.git', 'venv', 'mediafiles', 'staticfiles', 'helper', '__pycache__']
IGNORE_FILES = ['project_init.py', 'README.md', 'initialize_helper.py']


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
    """
    The function `create_project_dir` creates a new directory at the specified location with the given
    project name, checking for existing directories with the same name and prompting for a new name if
    necessary.
    
    :param project_location: The `project_location` parameter in the `create_project_dir` function
    represents the location where the project directory will be created. This could be a path to a
    specific directory on your file system where you want the project folder to be located. For example,
    it could be something like "/Users/username
    :param project_name: The `project_name` parameter is a string that represents the name of the
    project you want to create. It will be used to create a directory with that name within the
    specified `project_location`
    :return: The function `create_project_dir` returns the path of the newly created project directory.
    """
    project_path = os.path.join(project_location, project_name)

    while os.path.exists(project_path) and os.listdir(project_path):
        print(f"Project with name {project_name} already exist.")
        project_name = input("Enter a different project name: ")
        project_path = os.path.join(project_location, project_name)

    os.makedirs(project_path, exist_ok=True)
    return project_path


def copy_project_files(source, dest, project_name=None):
    """
    The function `copy_project_files` copies files and directories from a source location to a
    destination, with the option to specify a project name for a specific directory.
    
    :param source: The `source` parameter in the `copy_project_files` function is the directory path
    where the project files are located and from where you want to copy the files
    :param dest: The `dest` parameter in the `copy_project_files` function represents the destination
    directory where the files from the source directory will be copied to
    :param project_name: The `project_name` parameter is an optional argument that specifies the name of
    the project being copied. It is used in the function `copy_project_files` to determine the
    destination path for the project files. If provided, the project files will be copied to a
    subdirectory with the specified project name within
    """
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
    """
    The function `replace_strings_in_file` reads a file, replaces specified strings in the file content,
    and writes the modified content back to the file.
    
    :param filepath: The `filepath` parameter in the `replace_strings_in_file` function is the path to
    the file that you want to modify. It should be a string representing the location of the file on
    your system
    :param replace_strings: The `replace_strings` parameter is a dictionary that contains the original
    strings to be replaced as keys and the replacement strings as values. For example, if you want to
    replace the string 'backend' with 'frontend' in the file, you would pass a dictionary like this:
    """
    with open(filepath, 'r') as f:
        file_lines = f.readlines()

    for i, line in enumerate(file_lines):
        for original, replacement in replace_strings.items():
            if original in line:
                file_lines[i] = line.replace('backend', replacement)
    with open(filepath, 'w') as f:
        f.writelines(file_lines)


def get_file_paths(project_path, project_name):
    """
    The function `get_file_paths` returns a dictionary containing file paths based on the provided
    project path and name.
    
    :param project_path: The `project_path` parameter in the `get_file_paths` function represents the
    base directory path where the project files are located. This function generates a dictionary
    containing paths to various files within a project directory structure based on the provided
    `project_path` and `project_name`
    :param project_name: The `project_name` parameter is a string representing the name of the project
    for which you want to generate file paths
    :return: The function `get_file_paths` returns a dictionary containing file paths for various files
    within a Django project. The keys in the dictionary represent different types of files (e.g.,
    'asgi', 'wsgi', 'settings'), and the values are the corresponding file paths based on the provided
    `project_path` and `project_name` parameters.
    """
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