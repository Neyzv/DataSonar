from ..models.sonars.abstractions.BaseSonar import BaseSonar
from ..models.sonars.DateSonar import DateSonar
from ..models.sonars.ValueSubstitutionSonar import ValueSubstitutionSonar
from ..models.executors.SonarExecutor import SonarExecutor


class SonarExecutorBuilder:
    """
    Builder to create a SonarExecutor instance which allow to apply sonars on a data file
    """
    __sonars: list[BaseSonar]

    def __init__(self) -> None:
        self.__sonars = []

    def with_dates(self, column_names: list[str] | None = None,
                date_format: str = "%Y-%m-%d", time_format: str = "%H:%M:%S")-> "SonarExecutorBuilder":
        """
        Apply a date cleaner

        Args:
            column_names (list[str] | None, optional): Names of the columns that should be treated, if None all columns will be tested. Defaults to None.
            date_format (str, optional): Format of the outputed dates. Defaults to "%Y-%m-%d".
            time_format (_type_, optional): Format of the outputed time part of the dates. Defaults to "%H:%M:%S".

        Returns:
            SonarExecutorBuilder: self
        """
        self.__sonars.append(DateSonar(column_names, date_format, time_format))

        return self
    
    def with_substitution(self, matching_pattern: str, substitution_pattern: str,
                        column_names: list[str] | None = None) -> "SonarExecutorBuilder":
        """
        Apply a regex based substition mechanism

        Args:
            matching_pattern (str): Regex to match datas
            substitution_pattern (str): Regex of replacement
            column_names (list[str] | None, optional): Names of the columns that should be treated, if None all columns will be tested. Defaults to None.

        Returns:
            SonarExecutorBuilder: self
        """
        self.__sonars.append(ValueSubstitutionSonar(column_names, matching_pattern, substitution_pattern))

        return self
    
    def with_custom(self, sonar: BaseSonar) -> "SonarExecutorBuilder":
        """
        Add your custom sonar to the sonars collection

        Args:
            sonar (BaseSonar): Your custom sonar

        Returns:
            SonarExecutorBuilder: self
        """
        self.__sonars.append(sonar)

        return self

    def build(self) -> SonarExecutor:
        """
        Build all sonars to retreive an executor that will apply all specified sonars on a DataFile

        Returns:
            SonarExecutor: The executor that will run all sonars
        """
        result = SonarExecutor(self.__sonars)
        self.__sonars = []

        return result