# -*- coding: utf-8 -*-
import os

import yaml


class PluginConfig:
    def __init__(self, plugin_name: str, default_config):
        if not os.path.exists('./config'):
            os.mkdir('./config')
        if not os.path.exists(f'./config/{plugin_name}'):
            os.mkdir(f'./config/{plugin_name}')
            with open(f'./config/{plugin_name}/config.yaml', 'w', encoding='utf-8') as f:
                f.write(default_config.read())
        with open(f'./config/{plugin_name}/config.yaml', 'r', encoding='utf-8') as f:
            self.__config = yaml.load(f, Loader=yaml.FullLoader)

    @property
    def config(self):
        return self.__config
