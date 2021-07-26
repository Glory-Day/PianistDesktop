from PianistDesktop.utils.line import Line


class Bar:
    """
    Class that stores a single area in score
    """
    def __init__(self, type: str = None, lines: Line = None,
                 begin: int = None, end: int = None, components: list = None):
        """
        Initialize member fields
        :param type: Clef name of segment
        :param lines: Lines of segment
        :param begin: beginning iterator of segment
        :param end: ending iterator of segment
        :param components: Music symbols of segment
        """
        self.__type = type
        self.__lines = lines
        self.__begin = begin
        self.__end = end
        self.__components = components

    # getter property function
    @property
    def type(self) -> str:
        return self.__type

    # getter property function
    @property
    def lines(self) -> Line:
        return self.__lines

    # getter property function
    @property
    def begin(self) -> int:
        return self.__begin

    # getter property function
    @property
    def end(self) -> int:
        return self.__end

    # getter property function
    @property
    def components(self) -> list:
        return self.__components

    # getter property function
    @type.setter
    def type(self, _name: str):
        self.__type = _name

    # setter property function
    @lines.setter
    def lines(self, _lines: Line):
        self.__lines = _lines

    # setter property function
    @begin.setter
    def begin(self, _begin: int):
        self.__begin = _begin

    # setter property function
    @end.setter
    def end(self, _end: int):
        self.__end = _end

    # setter property function
    @components.setter
    def components(self, _components: list):
        self.__components = _components
