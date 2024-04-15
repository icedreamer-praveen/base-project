import os

import yaml


def load_config(base_dir):
    """
    Load YAML configuration from the first .yml file found inside the config or env_config directory.
    If no .yml file is found, load from a default file named 'env_config.yml'.
    """
    config_dirs = ['config', 'env_config']

    for config_dir in config_dirs:
        dir_path = os.path.join(base_dir, config_dir)
        config_file = os.path.join(dir_path, 'application-dev.yml')
        if not config_file:
            if os.path.exists(dir_path):
                if any(file.endswith('.yml') for file in os.listdir(dir_path)):
                    config_file = next(file for file in os.listdir(dir_path) if file.endswith('.yml'))
        with open(os.path.join(dir_path, config_file), 'r') as file:
            config = yaml.safe_load(file)
        return config
