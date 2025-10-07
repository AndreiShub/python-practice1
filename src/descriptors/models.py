from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]

class Field:
    def __init__(self, path):
        self.path = path.split(".")
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        data = instance.payload
        try:
            for key in self.path:
                data = data[key]
            return data
        except (KeyError, TypeError):
            return None

    def __set__(self, instance, value):
        data = instance.payload
        try:
            for key in self.path[:-1]:
                data = data[key]
            data[self.path[-1]] = value
        except (KeyError, TypeError):
            pass

class Model:
    def __init__(self, payload: JSON):
        self.payload = payload

