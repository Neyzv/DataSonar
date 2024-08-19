from pathlib import Path
from csv import Sniffer
import dask.dataframe as dd

from ...models.data_files.DataFile import DataFile

class DataFileService:
    """
    Service to create data file based on a file path
    """
    def create_from_csv(file_path: str, data_chunk_size: int = 250e6, sep: str | None = None,
                        delimiter_analyzer_size: int = 8192) -> DataFile:
        """
        Create a data file from a csv file

        Args:
            file_path (str): The path of the file
            data_chunk_size (int): The size of each chunk of the file. Defaults to 250Mo.
            sep (str | None, optional): The data separator str. Defaults to None.
            delimiter_analyzer_size (int, optional): If sep is None then an analyzer will determins the data separator automatically. Defaults to 8192.

        Raises:
            Exception: If the path is not a file
            Exception: If the delimiter analyzer size is not greater than zero

        Returns:
            DataFile: The data file of the file
        """
        file = Path(file_path)

        if not file.is_file():
            raise Exception(f"Can not find file at path '{file_path}'...")
        
        data_separator = sep

        if data_separator is None:
            if delimiter_analyzer_size <= 0:
                raise Exception("The delimiter analyzer buffer size must be greater than zero...")
            
            with open(file, 'r', encoding="utf-8") as f:
                data_separator = Sniffer().sniff(f.read(delimiter_analyzer_size)).delimiter
        
        return DataFile(dd.read_csv(file_path, sep=data_separator, blocksize=data_chunk_size, dtype=str).to_delayed())
    
    def create_from_parquet(file_path: str, data_chunk_size: int = 250e6) -> DataFile:
        """
        Create a data file from a parquet file

        Args:
            file_path (str): The path of the file
            data_chunk_size (int): The size of each chunk of the file. Defaults to 250Mo.

        Raises:
            Exception: If the path is not a file

        Returns:
            DataFile: The data file of the file
        """
        file = Path(file_path)

        if not file.is_file():
            raise Exception(f"Can not find file at path '{file_path}'...")
        
        return DataFile(dd.read_parquet(file_path, engine="pyarrow", blocksize=data_chunk_size).to_delayed())