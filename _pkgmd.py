"""Package metadata."""


__all__: tuple[str, ...] = (
    "__authors__",
    "__description__",
    "__autsrepo__",
    "__repository__",
    "__copyright__",
    "__license__",
    "__version__",
    "__maintainers__",
    "__email__",
    "__status__",
)

try:
    from typing_extensions import Final
except ImportError:
    from typing import Final


__authors__: Final[tuple[str, str]] = "Backist", "TheWisker"
__description__: Final[str] = ""
__repository__: Final[str] = "https://github.com/Backist/BoardToe"
__autsrepo__: Final[tuple[str, str]] = "https://github.com/Backist", "https://github.com/TheWisker"
__copyright__: Final[str] = "Copyright 2022-Present Backtist-TheWisker"
__license__: Final[str] = ""
__version__: Final[str] = "0.1.1"
__maintainers__: Final[str] = __authors__
__email__: Final[str] = "alvarodrumer54@gmail.com"
__status__: Final[str] = "Pre-Alpha Release -- Not stable"
