# @Time    : 2021-12-17 15:48
# @Author  : 老赵
# @File    : config.py
from functools import lru_cache
from typing import Dict, Type
from app.core.settings.app import AppSettings
from app.core.settings.base import BaseAppSettings, AppEnvTypes
from app.core.settings.dev import DevAppSettings
from app.core.settings.prod import ProdAppSettings
from app.core.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache(maxsize=128)
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
