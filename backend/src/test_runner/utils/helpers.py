import os
import pkgutil

from sqlalchemy import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute


class Module:
    def __init__(self, name, loader, ispkg):
        self.name = name
        self.ispkg = ispkg
        self.loader = loader


def load_modules(package_path, target_module_name=None):
    modules = [Module(name, loader, ispkg) for loader, name, ispkg in pkgutil.iter_modules([package_path])]

    for mod in modules:
        full_module_name = "{}.{}".format(target_module_name, mod.name)

        if not mod.ispkg:
            list_ = [target_module_name] if target_module_name is not None else None
            __import__(full_module_name, fromlist=list_)
        else:
            load_modules(os.path.join(package_path, mod.name), full_module_name)


def is_relationship_loaded(entity, attr):
    # type:(any, (str|InstrumentedAttribute))-> bool
    ins = inspect(entity)
    key = attr if isinstance(attr, str) else attr.key
    return key not in ins.unloaded
