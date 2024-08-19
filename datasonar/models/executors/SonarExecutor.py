from pandas import isna
import dask.dataframe as dd

from ..sonars.abstractions.BaseSonar import BaseSonar
from ..data_files.DataFile import DataFile


class SonarExecutor:
    """
    Class to execute sonars on a data file
    """
    __sonars: list[BaseSonar]

    def __init__(self, sonars: list[BaseSonar]) -> None:
        self.__sonars = sonars

    def execute(self, data_file: DataFile) -> DataFile:
        """
        Clean the data file with all sonars

        Args:
            data_file (DataFile): The data file that need to receive sonars actions

        Returns:
            DataFile: A new instance of data file wich have been modified
        """
        modified_partitions = []

        for partition in data_file.reader:
            pd_df = partition.compute()

            for col in pd_df.columns:
                for sonar in self.__sonars:
                    if sonar.should_treat_column(col):
                        pd_df[col] = pd_df[col].apply(lambda x: x if isna(x) else sonar.execute(x))

            modified_partitions.append(dd.from_pandas(pd_df, npartitions=1).to_delayed()[0])
        
        return DataFile(modified_partitions)