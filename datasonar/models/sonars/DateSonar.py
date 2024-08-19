from re import search, compile
from dateutil.parser import parse
from dateutil.parser._parser import UnknownTimezoneWarning
from warnings import filterwarnings

from .abstractions.BaseSonar import BaseSonar


filterwarnings("ignore", category=UnknownTimezoneWarning)

class DateSonar(BaseSonar):
    """
    Sonar to clean dates
    """
    REGEX_CONTAINS_ONLY_NUMBERS = compile(r"^-?\d+(?:[\.,]\d+)?(?:e-?\d+)?$")

    __date_format: str
    __time_format: str

    def __init__(self, column_names: list[str] | None, date_format: str, time_format: str) -> None:
        super().__init__(column_names)
        self.__date_format = date_format
        self.__time_format = time_format

    def is_valid(self, value: object) -> bool:
        return not search(self.REGEX_CONTAINS_ONLY_NUMBERS, str(value))

    def treat(self, value: str) -> str:
        try:
            parsed_date = parse(value, tzinfos={})

            return parsed_date.strftime(self.__date_format if str(parsed_date.time()) == "00:00:00" and "00:" not in value else f"{self.__date_format} {self.__time_format}")
        except:
            return value