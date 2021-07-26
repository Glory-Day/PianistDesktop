import numpy as np

from multimethod import multimethod


class Line:
    """
    Class that stores information about lines of score
    """

    def __init__(self, actual_lines: list = None, another_line: list = None, virtual_lines: list = None):
        """
        Initialize member fields
        :param actual_lines: Y-coordinate of actual lines
        :param another_line: Y-coordinate of virtual lines
        :param virtual_lines: Y-coordinate of virtual lines
        """
        self.__actual_lines = actual_lines
        self.__another_lines = another_line
        self.__virtual_lines = virtual_lines

    @staticmethod
    def detect_lines(segment: np.ndarray, position: int) -> list:
        """
        Detect the lines that really exist
        :param segment: Search segment
        :param position: Minimum y-coordinate of segment
        :return: Y-coordinate list of lines
        """

        def apply_position(verified_lines_: list, position_: int) -> list:
            """
            Convert to coordinates of segments before returning clear coordinates
            :param verified_lines_: Verified lines that have been tested for clarity
            :param position_: Beginning y-coordinates of segment
            :return: Coordinates of segments
            """
            lines_ = list()
            for coordinates_ in verified_lines_:
                lines_.append([_y + position_ for _y in coordinates_])
            return lines_

        def is_clear(coordinates_: list) -> list or None:
            """
            Check if the coordinates are clear and five
            :param coordinates_: Unclear and unconfirmed coordinates
            :return: If the lines are not clear, return None. Else Returns a clear set of lines
            """

            def coordinates_to_lines(coordinates__: list) -> list:
                """
                Translate unclear and unconfirmed coordinates clearly
                :param coordinates__: Unclear and unconfirmed coordinates
                :return: Clear coordinates
                """
                lines__ = list()
                index__, y__ = 0, coordinates__[0]

                # converts increasing elements by one into a set
                for i__, coordinate__ in enumerate(coordinates__[1:]):
                    different__ = coordinate__ - y__
                    if different__ != 1:
                        lines__.append(coordinates__[index__:i__ + 1])
                        index__ = i__ + 1
                    y__ = coordinate__
                lines__.append(coordinates__[index__:])

                return lines__

            lines_ = coordinates_to_lines(coordinates__=coordinates_)
            count_ = len(lines_)

            # check if there are five lines
            return lines_ if count_ == 5 else None

        _, width = segment.shape

        for i in range(width - 1, 0, -1):
            coordinates = list()

            # find a pixel whose color value is not 255.
            for j, pixel in enumerate(segment[:, i]):
                if pixel < 200:
                    coordinates.append(j)

            if coordinates:
                verified_lines = is_clear(coordinates_=coordinates)

                # if no definite coordinates have been returned,
                # clear the coordinate list and check the next vertical axis.
                if verified_lines is not None:
                    return apply_position(verified_lines_=verified_lines, position_=position)
                else:
                    coordinates.clear()

    def set_standard_lines(self):
        """
        If another lines is exist, set another lines else set actual lines
        """

        def get_middle(line_: list) -> int:
            """
            Return center y-coordinates of lines
            :param line_: line's coordinates
            :return: Center coordinates of lines
            """
            begin_, end_ = line_[0], line_[len(line_) - 1]
            return int((begin_ + end_) / 2)

        # if another lines is exist
        if self.another_lines is not None:
            another_lines = list()
            for line in self.another_lines:
                another_lines.append(get_middle(line))

            self.another_lines = sorted(another_lines)

        actual_lines = list()
        for line in self.actual_lines:
            actual_lines.append(get_middle(line))

        self.actual_lines = sorted(actual_lines)

    def get_virtual_lines(self) -> list:
        """
        Create virtual lines to determine pitch height
        :return: Virtual lines
        """

        def get_middle(begin_: int, end_: int) -> int:
            """
            Return center y-coordinates of lines
            :param begin_: Begin of iterator
            :param end_: End of iterator
            :return: Center coordinates of lines
            """
            return int((begin_ + end_) / 2)

        def get_upside_virtual_lines(actual_lines_: list) -> list:
            """
            Create virtual lines to determine upside area
            :param actual_lines_: Actual lines
            :return: Virtual lines of upside
            """
            virtual_lines_ = list()

            for i_ in range(0, len(actual_lines_) - 1):
                virtual_lines_.append(get_middle(actual_lines_[i_], actual_lines_[i_ + 1]))

            # set distance of line
            distance_ = virtual_lines_[0] - actual_lines_[0]

            for i_ in range(1, 5):
                virtual_lines_.append(actual_lines_[0] - (distance_ * i_))
            for i_ in range(1, 3):
                virtual_lines_.append(actual_lines_[4] + (distance_ * i_))

            return virtual_lines_

        def get_downside_virtual_lines(another_lines_: list) -> list:
            """
            Create virtual lines to determine downside area
            :param another_lines_: Another actual lines
            :return: Virtual lines of downside
            """
            virtual_lines_ = list()

            for i_ in range(0, len(another_lines_) - 1):
                virtual_lines_.append(get_middle(another_lines_[i_], another_lines_[i_ + 1]))

            # set distance of line
            distance_ = virtual_lines_[0] - another_lines_[0]

            for i_ in range(1, 2):
                virtual_lines_.append(another_lines_[0] - distance_ * i_)
            for i_ in range(1, 4):
                virtual_lines_.append(another_lines_[4] + distance_ * i_)

            return virtual_lines_

        virtual_lines = list()
        virtual_lines.extend(get_upside_virtual_lines(actual_lines_=self.actual_lines))
        # extend another line's virtual lines
        if self.another_lines is not None:
            virtual_lines.extend(get_downside_virtual_lines(another_lines_=self.another_lines))

        return sorted(virtual_lines)

    # set actual, virtual lines
    @multimethod
    def set_lines(self, segment: np.ndarray, begin: int):
        # set actual lines
        self.actual_lines = self.detect_lines(segment=segment, position=begin)

    @multimethod
    def set_lines(self):
        self.set_standard_lines()
        # set virtual lines
        self.virtual_lines = self.get_virtual_lines()

    # getter property function
    @property
    def actual_lines(self) -> list or None:
        return self.__actual_lines

    # getter property function
    @property
    def another_lines(self) -> list or None:
        return self.__another_lines

    # getter property function
    @property
    def virtual_lines(self) -> list or None:
        return self.__virtual_lines

    # getter property function
    @property
    def lines(self) -> list:
        lines = self.actual_lines + self.virtual_lines
        if self.another_lines is not None:
            lines.extend(self.another_lines)
        return sorted(lines)

    # getter property function
    @property
    def begin(self) -> int:
        return self.actual_lines[0][0]

    # getter property function
    @property
    def end(self) -> int:
        # end indexes of array
        first = len(self.actual_lines) - 1
        second = len(self.actual_lines[first]) - 1
        return self.actual_lines[first][second]

    # getter property function
    @property
    def center(self) -> int:
        def get_middle(begin_: int, end_: int) -> int:
            """:return: Center coordinates of iterator"""
            return int((end_ - begin_) / 2)

        return self.begin + get_middle(begin_=self.begin, end_=self.end)

    # setter property function
    @actual_lines.setter
    def actual_lines(self, lines: list):
        self.__actual_lines = lines

    # setter property function
    @another_lines.setter
    def another_lines(self, lines: list):
        self.__another_lines = lines

    # setter property function
    @virtual_lines.setter
    def virtual_lines(self, lines: list):
        self.__virtual_lines = lines
