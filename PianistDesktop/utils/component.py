class Component:
    """
    Class that stores information about music symbols
    """
    def __init__(self, name: str = None, max: tuple = None, min: tuple = None,
                 beams: int = 0, accuracy: float = None):
        """
        Initialize member fields
        :param name: Music symbol name
        :param max: Maximum coordinates of the bounding box
        :param min: Minimum coordinates of the bounding box
        :param beams: Variable determining if it is a note of less than 8 or less
        :param accuracy: Accuracy to determine musical symbols
        """
        self.__name = name
        self.__max = max
        self.__min = min
        self.__beams = beams
        self.__accuracy = accuracy

    # getter property function
    @property
    def name(self) -> str:
        return self.__name

    # setter property function
    @name.setter
    def name(self, name: str):
        self.__name = name

    # getter property function
    @property
    def max(self) -> tuple:
        return self.__max

    # getter property function
    @property
    def min(self) -> tuple:
        return self.__min

    # getter property function
    @property
    def width(self) -> int:
        """:return: Width of bounding box"""
        return self.__max[0] - self.__min[0]

    # getter property function
    @property
    def height(self) -> int:
        """:return: Height of bounding box"""
        return self.__max[1] - self.__min[1]

    # getter property function
    @property
    def center(self) -> tuple:
        """:return: Center coordinates of the bounding box"""
        def width(min_: tuple, max_: tuple) -> int:
            """:return: Width of the bounding box"""
            return int((max_[0] - min_[0]) / 2)

        def height(min_: tuple, max_: tuple) -> int:
            """:return: Height of the bounding box"""
            return int((max_[1] - min_[1]) / 2)

        return self.min[0] + width(self.min, self.max), self.min[1] + height(self.min, self.max)

    # getter property function
    @property
    def beams(self) -> int:
        return self.__beams

    # getter property function
    @beams.setter
    def beams(self, count):
        self.__beams += count

    # getter property function
    @property
    def length(self):
        def get_length(name_: str, beams_: int) -> int:
            """
            Returns the length of a note, rest by name
            :param name_: Note's or rest's name
            :param beams_: If it's an eighth or less note, a variable to shorten the length
            :return: Length of note, rest
            """
            switch = {'noteheadHalf': 8, 'noteheadWhole': 16, 'noteheadBlack': int(4 / (1 + beams_)), 'restWhole': 16,
                      'restHalf': 8, 'restQuarter': 4, 'rest8th': 2, 'rest16th': 1}

            return switch.get(name_)

        return get_length(self.name, self.beams)

    # getter property function
    @property
    def accuracy(self) -> float:
        return self.__accuracy

    # iterator function for sorting
    def __lt__(self, other) -> bool:
        return self.__min[1] < other.min[1]
