from re import compile, Pattern, sub

from .abstractions.BaseSonar import BaseSonar


class ValueSubstitutionSonar(BaseSonar):
    """
    Sonar to substitute values
    """
    __matching_pattern: Pattern[str]
    __substitution_pattern: str

    def __init__(self, column_names: list[str] | None,
                matching_pattern: str, substitution_pattern: str) -> None:
        super().__init__(column_names)
        self.__matching_pattern = compile(matching_pattern)
        self.__substitution_pattern = substitution_pattern

    def is_valid(self, value: object) -> bool:
        return isinstance(value, str)

    def treat(self, value: object) -> object:
        return sub(self.__matching_pattern, self.__substitution_pattern, value)