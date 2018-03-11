import logging
from logging import NullHandler

from .xml_spec_parser import XMLSpecParser

__all__ = ['XMLSpecParser']

logging.getLogger(__name__).addHandler(NullHandler())