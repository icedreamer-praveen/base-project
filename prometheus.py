import os


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
    """
    The function `replace_prometheus_apps` inserts the string `"django_prometheus"` into a Python
    settings file at the location where `THIRD_PARTY_APPS` is defined.
    
    :param settings_path: The `replace_prometheus_apps` function reads the content of a settings file
    located at the `settings_path`, finds the index of the line containing "THIRD_PARTY_APPS", and
    inserts `"django_prometheus"` in the list of third-party apps if the line is found
    """
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
    """
    The function `replace_prometheus_middleware` inserts Prometheus middleware classes into a Django
    settings file.
    
    :param settings_path: The `settings_path` parameter in the `replace_prometheus_middleware` function
    is the file path to the Django settings file (usually named `settings.py`) where you want to add the
    Prometheus middleware. This function reads the content of the settings file, locates the
    `MIDDLEWARE` setting
    """
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
    """
    The `append_prometheus_views` function appends Prometheus monitoring views code to a specified file
    path in Python.
    
    :param utilis_views_path: The `utilis_views_path` parameter in the `append_prometheus_views`
    function is the file path where you want to append the Prometheus views code. This code snippet
    defines Prometheus metrics and a health check endpoint for monitoring and health checking purposes
    in a Django application
    """
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
    """
    The function `update_prometheus_urls` appends code to a Django urls file for adding Prometheus
    monitoring endpoints.
    
    :param utilis_urls_path: The `utilis_urls_path` parameter in the `update_prometheus_urls` function
    is the file path where you want to append the Prometheus URLs code snippet. This function appends
    the code snippet for defining Django URLs related to health checks and Prometheus metrics to the
    specified file
    """
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