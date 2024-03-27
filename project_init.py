import os
import shutil

# Constants
IGNORE_DIRS = ['.git', 'venv', 'mediafiles', 'staticfiles']
IGNORE_FILES = ['project_init.py', 'README.md', 'prometheus.py']


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

def initialize_project(project_location, project_name):
    """
    The `initialize_project` function creates a new project directory, copies project files, replaces
    strings in files, and returns the file paths.
    
    :param project_location: The `project_location` parameter in the `initialize_project` function
    refers to the location where the project will be created. This could be a directory path on your
    file system where the project files will be stored
    :param project_name: The `project_name` parameter is the name of the project that you are
    initializing. It is used to create a directory with this name and to replace certain strings in the
    project files with this name
    :return: The function `initialize_project` returns a dictionary `file_paths` containing the paths of
    the files in the project after performing string replacements.
    """
    project_path = create_project_dir(project_location, project_name)
    copy_project_files('.', project_path, project_name=project_name)

    file_paths = get_file_paths(project_path, project_name)

    for key, replacement_strings in REPLACE_PATTERNS.items():
        replace_strings_in_file(file_paths[key], {original: project_name for original in replacement_strings})

    # New feature implementation
    print('y/n: Prometheus')
    features = input('Do you want to add prometheus?: ')
    if features == "y":
        add_prometheus_config(project_path, project_name)

    return file_paths

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


def add_prometheus_config(project_path, project_name):
    """
    Adds Django Prometheus configuration to the project.
    
    :param project_path: The path where the project is located.
    :param project_name: The name of the project.
    """
    # Add 'django-prometheus' and 'prometheus_client' to requirements.txt
    requirements_path = os.path.join(project_path, 'requirements.txt')
    with open(requirements_path, 'a') as f:
        f.write('django-prometheus\nprometheus_client\n')

    # Insert 'django_prometheus' into THIRD_PARTY_APPS in settings.py
    settings_path = os.path.join(project_path, project_name, 'settings.py')
    replace_prometheus_apps(settings_path)

    # Add Prometheus middleware to MIDDLEWARE in settings.py
    replace_prometheus_middleware(settings_path)

    # Add Prometheus metrics view and health check view to utilis/views.py
    utilis_views_path = os.path.join(project_path, 'utilis', 'views.py')
    append_prometheus_views(utilis_views_path)

    # Update urls.py in utilis app
    utilis_urls_path = os.path.join(project_path, 'utilis', 'urls.py')
    update_prometheus_urls(utilis_urls_path)

def replace_prometheus_apps(settings_path):
    with open(settings_path, 'r') as file:
        settings_content = file.readlines()
    
    third_party_apps_index = next(
        (i for i, line in enumerate(settings_content) if "THIRD_PARTY_APPS" in line), None
    )
    
    if third_party_apps_index is not None:
        settings_content.insert(third_party_apps_index + 1, '    "django_prometheus",\n')
    
    with open(settings_path, 'w') as file:
        file.writelines(settings_content)

def replace_prometheus_middleware(settings_path):
    with open(settings_path, 'r') as file:
        settings_content = file.readlines()

    middleware_index = next(
        (i for i, line in enumerate(settings_content) if "MIDDLEWARE" in line), None
    )
    
    if middleware_index is not None:
        settings_content.insert(middleware_index + 1, '    "django_prometheus.middleware.PrometheusBeforeMiddleware",\n')
        for i, line in enumerate(settings_content[middleware_index:], start=middleware_index):
            if ']' in line:
                settings_content.insert(i, '    "django_prometheus.middleware.PrometheusAfterMiddleware",\n')
                break
    
    with open(settings_path, 'w') as file:
        file.writelines(settings_content)

def append_prometheus_views(utilis_views_path):
    prometheus_views_code = """
import re
import time

import psutil
from django.http import HttpResponse, JsonResponse
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest

from logger_helper_function.interceptor import log_functions

cpu_usage = Gauge('cpu_usage_percentage', 'CPU Usage Percentage')
memory_usage = Gauge('memory_usage_percentage', 'Memory Usage Percentage')
uptime_hours = Gauge('application_uptime_hours', 'Application Uptime in Hours')
warning_count = Gauge('log_warning_count', 'Total number of warning logs')
error_count = Gauge('log_error_count', 'Total number of error logs')
info_count = Gauge('log_info_count', 'Total number of info logs')

start_time = time.time()

def prometheus_metrics(request):
    log_file_path = "logs/backend.log"
    with open(log_file_path, 'r') as file:
        log_content = file.read()

    total_warnings = len(re.findall(r'\bWARNING\b', log_content))
    total_errors = len(re.findall(r'\bERROR\b', log_content))
    total_info = len(re.findall(r'\bINFO\b', log_content))

    warning_count.set(total_warnings)
    error_count.set(total_errors)
    info_count.set(total_info)

    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_usage.set(cpu_percent)

    memory_percent = psutil.virtual_memory().percent
    memory_usage.set(memory_percent)

    uptime_seconds = time.time() - start_time
    uptime_hours.set(uptime_seconds / 3600)  

    metrics = generate_latest()
    return HttpResponse(metrics, content_type=CONTENT_TYPE_LATEST)

@log_functions
def health_check(request):
    return JsonResponse(data={
        "status" : "UP"
    }, status=200)
"""
    with open(utilis_views_path, 'a') as file:
        file.write(prometheus_views_code)

def update_prometheus_urls(utilis_urls_path):
    prometheus_urls_code = """
from django.urls import path

from .views import health_check, prometheus_metrics

urlpatterns += [
    path("actuator/health/livenessState", health_check),
    path("actuator/prometheus", prometheus_metrics, name="prometheus_metrics"), 
]
"""
    with open(utilis_urls_path, 'a') as file:
        file.write(prometheus_urls_code)

def main():
    """
    The main function prompts the user to enter a project location and name, initializes the project
    using the provided information, and then prints a message confirming the creation of the project.
    """
    project_location = input("Enter project location: ")
    project_name = input("Enter project name: ")

    initialize_project(project_location, project_name)

    print(f"Project {project_name} created at {project_location}")

if __name__ == "__main__":
    main()