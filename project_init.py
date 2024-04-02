from helper.django_extension import add_django_ext_config
from helper.prometheus import add_prometheus_config
from initialize_helper import (REPLACE_PATTERNS, copy_project_files,
                               create_project_dir, get_file_paths,
                               replace_strings_in_file)


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
    promethues_features = input('Do you want to add prometheus? y/n: ')
    if promethues_features == "y":
        add_prometheus_config(project_path, project_name)
        
    ext_features = input('Do you want to add django_extension? y/n: ')
    if ext_features == "y":
        add_django_ext_config(project_path, project_name)

    return file_paths


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