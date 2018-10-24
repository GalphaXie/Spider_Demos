# -*- coding: utf-8 -*-

# scrapy_plus/conf/settings
from .default_settings import *  # 全部导入默认配置文件的属性
from settings import *  # 由于程序在settings.py的同级目录下执行,所以会导入settings中的所有配置
