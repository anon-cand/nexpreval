import os
import logging
from pathlib import Path
from operations import catalogue
from parsers import XMLSpecParser


class ExpressionCalculator:
    """
    Processes all expression files with given extension in source directory
    Assumes that all files with given extension are expression files
    """

    __slots__ = ('source_dir', 'target_dir', 'extension', 'operations', 'spec_parser')

    def __init__(self, source: str, target: str, extension: str):
        """
        :param source: Path to source directory
        :param target: Path to target directory
        :param extension: extension of the files to be processed
        :return: None
        """
        self.operations = None
        self.spec_parser = None
        self.source_dir = None
        self.target_dir = None
        self.extension = extension
        self.validate(source, target)  # Validate the inputs
        self.operations = catalogue()  # Build the operations catalogues
        self.spec_parser = XMLSpecParser(self.operations, extension)  # Initialize the parser

    def process(self):
        """
        This function acts as a coordinator for actual execution
        """
        logger = logging.getLogger(__name__)
        logger.info('Collecting names of files that will be processed')
        entries = self.entries()
        logger.info('Found %d files to process', len(entries))
        for spec in entries:
            logger.info('Parsing spec: %s', spec)
            operations = self.spec_parser.parse(spec)
            logger.info('Evaluating operations found in the spec')
            results = self.evaluate(operations)
            logger.info('Persisting results for the spec')
            self.persist(spec, results)

    def entries(self) -> list:
        """
        Walk through the file system and find all suitable files
        :return: a list of files that have to be processed
        """
        entries = []
        logger = logging.getLogger(__name__)
        logger.debug('Traversing the source directory')
        for root, _, names in os.walk(self.source_dir):
            for name in names:
                if Path(name).suffix == self.extension:
                    full_path = os.path.join(root, name)
                    entries.append(full_path)
        return entries

    def evaluate(self, operations: dict) -> dict:
        """
        Execute operations.
        :param operations: a mapping of id and operations objects
        :return: a map of id and results
        """
        return {oid: obj() for oid, obj in operations.items()}

    def persist(self, spec: str, results: dict):
        """
        Transform the results using spec parser and save
        them to the target directory
        :param spec: name of the spec to be used for generating target file name
        :param results: mapping of top-level operation id and their results
        :return: information on the resultant file
        """
        logger = logging.getLogger(__name__)
        logger.debug('Preparing results for persistence')
        serialized_result = self.spec_parser.serialize(results, 'expressions', 'result')
        if serialized_result:
            logger.debug('Determining result file path')
            spec_path = Path(spec)
            file_name = spec_path.name[:-len(spec_path.suffix)]
            result_file_name = '%s_result%s' % (file_name, spec_path.suffix)
            result_file_path = self.target_dir.joinpath(result_file_name)
            with open(result_file_path, 'w') as rf:
                rf.write(serialized_result)
                logger.info('Results for spec %s have been saved to: %s', spec_path.name, result_file_path)
        else:
            logger.error("Failed to serialize results")

    def validate(self, source: str, target: str):
        """
        Validates inputs to the application
        :param source: path to source directory
        :param target: path to target directory
        :return:
        """
        logger = logging.getLogger(__name__)

        source_path = Path(source)  # Path to source directory
        target_path = Path(target)  # Path to destination directory

        logger.debug('Validating paths are valid and are directories')
        if not (source_path.exists() and source_path.is_dir()):
            raise ValueError('Path to source directory is not valid.')

        if not (target_path.exists() and target_path.is_dir()):
            raise ValueError('Path to target directory is not valid.')

        source = source_path.resolve()
        target = target_path.resolve()

        logger.debug('Checking if the directories are accessible to current user')
        if not (os.access(source, os.R_OK)):
            raise ValueError('Read permissions on source directory is missing.')

        if not (os.access(target, os.R_OK | os.W_OK)):
            raise ValueError('Read/write permissions on target directory are missing.')

        self.source_dir = source
        self.target_dir = target

