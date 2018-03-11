import logging
from logging import NullHandler
from .operation import Operation as _Operation
from .constant import Constant as _Constant
from .addition import Addition as _Addition
from .subtraction import Subtraction as _Subtraction
from .multiplication import Multiplication as _Multiplication
from .division import Division as _Division

__all__ = ['catalogue']

logging.getLogger(__name__).addHandler(NullHandler())


def catalogue():
    """
    Loads operations and constructs a mapping out of them
    :return: Mapping of operation tag and Operation class
    """
    catalog = {sc.TAG: sc for sc in _Operation.__subclasses__()}
    return catalog








