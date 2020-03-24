# -*- coding: utf-8 -*-
"""
"""
#import yaml
from pathlib import Path
from typing import Union, List, Tuple, Dict, Set, Any
import inspect
import importlib

import django.db.models


class classproperty(object):
    """
    This is woring as a decolator to treat a property in the class, when it's not instanced.

    Usage:
    --- as a method in the class ---
    >>> class Hoge:

    >>>     @classproperty  # add this decolator before defining the method
    >>>     def huga(*args, **kwargs):
    >>>         return 'any stuff you wanna return'

    >>> print(Hoge.huga)  # would be correctly working
    'any stuff you wanna return'
    """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class TableCreator:

    def __init__(self):
        pass

    def run(self, yaml_path: Union[str, Path]):
        pass

    def load_yaml(self, yaml_path: Union[str, Path]) -> Dict[str, str]:
        with open(str(yaml_path), 'r') as f:
            yaml_ = yaml.load(f)
        return yaml_

    def request(self):
        pass

    def parse(self):
        pass


class DRFAbstractInfo:

    @staticmethod
    def get_init_args(cls: Any, is_dict: bool = True) -> Union[Dict, inspect.ArgSpec]:
        args_obj = inspect.getfullargspec(getattr(cls, '__init__'))
        args, defaults = args_obj.args, args_obj.defaults
        if defaults is None:
            return {}
        args.remove('self')
        assert len(args) == len(defaults), f'The number of args and defaults are diffrent. {len(args)} {len(defaults)}'
        args = {arg: default for arg, default in zip(args, defaults)}
        return args if is_dict else args_obj

    @staticmethod
    def _get_recursive_subclasses(cls: Any) -> Set[object]:
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in DRFAbstractInfo._get_recursive_subclasses(c)]) | {cls}

    class Models:

        def __init__(self):
            raise NotImplementedError('This class is not implemented yet.')

    # TODO: This class could be abstracted
    # TODO: This class name should be singular or plural??
    # -> Since this class is basically operating multipul fields, it might be better to choose plural.
    class Fields:
        _module = django.db.models.Field
        required_definition = {  # TODO: look for the way how required definitions are automatically gathered.
            'django.db.models.fields.CharField': {
                'max_length': None
            },
            'django.db.models.fields.DecimalField': {
                'max_digits': None,
                'decimal_places': None
            },
        }

        # TODO: may be better to create a cache of this result as a class variable once this property would be called
        @classproperty
        def FIELD_TYPE(cls: object) -> Tuple[Tuple[str, str]]:
            _fields = cls.all()
            fields = tuple((field.__name__.replace('Field', '').lower(), field.__module__ + f'.{field.__name__}')
                           for field in _fields if field.__name__ != 'Field')
            return fields

        # THINK: classproperty or classmethod -> if cls object is needed, then choose classmethod
        # TODO: may be better to create a cache of this result as a class variable once this method would be called
        @classmethod
        def all(cls: object) -> List[object]:
            _fields = sorted(DRFAbstractInfo._get_recursive_subclasses(cls._module), key=lambda x: x.__name__)
            return _fields

        @classproperty
        def default_args(cls: object) -> Dict[str, Any]:
            return DRFAbstractInfo.get_init_args(cls._module, is_dict=True)

        @classproperty
        def all_args(cls: object) -> Dict[str, Dict[str, Any]]:
            x = dict(
                list(
                    map(
                        lambda f: (
                            f.__module__ + f'.{f.__name__}',
                            {
                                key: val for key, val in DRFAbstractInfo.get_init_args(
                                    getattr(importlib.import_module(f.__module__), f.__name__)
                                ).items() if key not in DRFAbstractInfo.Fields.default_args.keys()
                            }
                        ),
                        DRFAbstractInfo.Fields.all()
                    )
                )
            )
            return x

        @classmethod
        def args_(cls, field: str) -> Dict[str, Any]:
            # FIXME: idk it's a best practice or not to add an error key-val.
            return cls.all_args.get(field, {'error': f'"{field}" is not a kind of Field'})

    class Serializers:

        def __init__(self):
            raise NotImplementedError('This class is not implemented yet.')

    class Views:

        def __init__(self):
            raise NotImplementedError('This class is not implemented yet.')
