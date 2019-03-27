import requests
import os
from datetime import datetime, timedelta
from class_token import BearerToken, JWEToken


class Process:
    """parent class for batch aggregation pulled from rational /CC API

    Attributes:
        :param created (datetime): time of call from api
        :param app_version (str)
        :param care_recipe (bool): unknown
        :param category (int): unknown
        :param chamber_id (int)
        :param device_family (str): families unknown
        :param device_name (str): SCC
        :param device_serialnumber (str): serial, consisting of country, store, branch. ex.: '699-124_SAT'
        :param finished (bool):
        :param group_id (int)
        :param group_name (str)
        :param process_id (int)
        :param recipe_id (int)
        :param recipe_name(str)
        :param start (datetime)
        :param temp_unit (str): C/F- default 'C'
    """
    def __init__(self,
                 created: datetime,
                 app_version: str,
                 care_recipe: bool,
                 category: int,
                 chamber_id: int,
                 device_family: str,
                 device_name: str,
                 device_serialnumber: str,
                 finished: bool,
                 group_id: int,
                 group_name: str,
                 process_id: int,
                 recipe_id: int,
                 recipe_name: str,
                 start: datetime,
                 temp_unit: str = 'C'):
        self.created = created
        self.app_version = app_version
        self.care_recipe = care_recipe
        self.category = category
        self.chamber_id = chamber_id
        self.device_family = device_family
        self.device_name = device_name
        self.device_serialnumber = device_serialnumber
        self.finished = finished
        self.group_id = group_id
        self.group_name = group_name
        self.process_id = process_id,
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.start = start
        self.temp_unit = temp_unit
        # :todo class method request
        # :todo class method send
        # :todo ORM


if __name__ == '__main__':
    test = Process(created=datetime.now(),
                   app_version='rand',
                   care_recipe=False,
                   category='blank',
                   chamber_id=1000,
                   device_family='blank',
                   device_name='699-124_SAT',
                   device_serialnumber='E11SH13022340226',
                   finished=False,
                   group_id=1,
                   group_name='03-Sattledt',
                   process_id=1,
                   recipe_id=195,
                   recipe_name='schnell',
                   start=datetime.now()-timedelta(hours=1, minutes=15))

    print(test)
    print(test.temp_unit)
    print(isinstance(test, Process))
    jwe = JWEToken()
    print(jwe.request())
    bearer = BearerToken()
    print(bearer.request(jwe=jwe.token))
