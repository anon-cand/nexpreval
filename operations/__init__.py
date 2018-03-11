import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

from .operation import Operation
from .constant import Constant
from .addition import Addition
from .subtraction import Subtraction
from .multiplication import Multiplication
from .division import Division

def catalogue():
    """
    Loads operations and constructs a mapping out of them
    :return: Mapping of operation tag and Operation class
    """
    catalog = {sc.TAG: sc for sc in Operation.__subclasses__()}
    return catalog

__all__ = ['catalogue']



