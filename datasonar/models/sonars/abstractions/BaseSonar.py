from abc import abstractmethod


class BaseSonar:
    """
    Base class to create data sonars
    """
    __column_names: list[str] | None

    def __init__(self, column_names: list[str] | None) -> None:
        self.__column_names = column_names
    
    @abstractmethod
    def treat(self, value: object) -> object:
        """
        Apply the cleaning on the value

        Args:
            value (object): The value that need to be cleaned

        Returns:
            object: The cleaned value
        """
        pass

    def should_treat_column(self, column_name: str) -> bool:
        """
        Determine if the values of this column should be treated or not

        Args:
            column_name (str): The name of the column

        Returns:
            bool: True if the column should be treated otherwise False
        """
        return self.__column_names is None or column_name in self.__column_names

    def is_valid(self, value: object) -> bool:
        """
        [Can be overwritten]
        Check whenether the value is valid to be cleaned or not

        Args:
            value (object): The value of the dataframe we want to change

        Returns:
            bool: True if the value is valid to be cleaned otherwise False
        """
        return True

    def execute(self, value: object) -> object:
        """
        Clean the value if it should be

        Args:
            value (object): The value that may need to be cleaned

        Returns:
            object: The cleaned value or the initial value if it don't need to be cleaned
        """
        if self.is_valid(value):
            return self.treat(value)
        
        return value