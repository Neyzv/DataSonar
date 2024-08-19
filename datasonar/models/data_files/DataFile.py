from os import makedirs
from os.path import join
from dask.delayed import Delayed
import dask.dataframe as dd

from ...enums.FileFormat import FileFormat


class DataFile:
    """
    Class that represent datas of a file
    """
    __reader: list[Delayed]

    def __init__(self, reader: list[Delayed]) -> None:
        self.__reader = reader

    @property
    def reader(self) -> list[Delayed]:
        """
        The reader of the file
        """
        return self.__reader
    
    def __get_output_path(file_format: FileFormat, output_dir: str, file_name: str) -> str:
        """
        Create the output path if it doesn't exists and return the full path of the result file

        Args:
            file_format (FileFormat): The file format of the result
            output_dir (str): The path of the output folder
            file_name (str): The name of the result file

        Returns:
            str: The full path of the result file
        """
        makedirs(output_dir, exist_ok=True)

        return join(output_dir, f"{file_name}.{file_format}")
    
    def export_csv(self, output_dir: str, result_file_name: str, sep: str = ";") -> None:
        """
        Export the data file in it's current state as a CSV file

        Args:
            output_dir (str): The path of the output dir, and will be created if it doesn't exists
            result_file_name (str): The name of the result file without it's extension
            sep (str, optional): The data separator of the result file. Defaults to ";".
        """
        dd.from_delayed(self.__reader).to_csv(DataFile.__get_output_path(FileFormat.CSV, output_dir, result_file_name), index=False, sep=sep, single_file=True)