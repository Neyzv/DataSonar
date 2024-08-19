# DataSonar 🌐
This is a simple lib to sanitize big datas in files by applying cleaners. It uses lazy loading and clustering loading to optimize performance with `dask` lib.

## Available file formats 📃
### Input ↩️

- CSV
- Parquet
> ⚠️ : CSV datas are loaded as string !

### Output ↪️

- CSV

## How to use 💯
### Creation of the executor 📈
```py
from datasonar import SonarExecutorBuilder

executor = SonarExecutorBuilder().with_dates(
    [
        "myDateField",
        "myDateTimeField"
    ],  # Field names that must be treated
    "%Y-%m-%d",  # New date format
    "%H:%M:%S",  # New time format
    ).build()  # Output a SonarExecutor instance that will execute sonars in the same order that they have been registered
```
> NB : You can add more sonars if it's needed.

### Load the DataFile 📄
```py
from datasonar import DataFileService

df = DataFileService.create_from_csv("./test.csv")  # If you don't specify the separator then an analyzer will determins it
df_parquet = DataFileService.create_from_parquet("./test.parquet")
```

### Execute the sonars 🎇
```py
executor.execute(df).export_csv("./", "result")
```

## Going further ⏩
You can also implement your own sonars with your custom logic.

### Create your sonar 👷
```py
from datasonar import BaseSonar
from re import search, compile


class PlusSonar(BaseSonar):
    """
    Sonar that increment integers by an amount
    """
    REGEX_IS_INT = compile(r"^-?\d+$")

    __amount: int

    def __init__(self, column_names: list[str] | None, amount: int) -> None:
        super().__init__(column_names)
        self.__amount = amount

    def is_valid(self, value: object) -> bool:
        return search(self.REGEX_IS_INT, str(value))

    def treat(self, value: object) -> object:
        return int(value) + self.__amount
```

### Add your sonar to the builder 🚀
```py
from datasonar import SonarExecutorBuilder

executor = SonarExecutorBuilder().with_custom(PlusSonar(None, 2)).build()
```
And now you can execute it on your loaded `DataFile`.