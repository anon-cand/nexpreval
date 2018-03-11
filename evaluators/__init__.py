import logging
from logging import NullHandler

from .xml_file_evaluator import XMLFileEvaluator

__all__ = ['XMLFileEvaluator']

logging.getLogger(__name__).addHandler(NullHandler())