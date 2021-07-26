import numpy as np
import cv2

from multimethod import multimethod


class Debugging:
    """
    Class that image checks the code for normal operation.
    """
    def __init__(self, color: tuple = (255, 0, 0), path: str = None, images: list = None):
        """
        Initialize member fields
        :param color: Color drawn in the image
        :param path: Image's path
        :param images: List of debugging images
        """

        # if images parameter is None, return empty list
        def initialize(_images: None) -> list:
            if _images is None:
                return list()

        self.__color = color
        self.__path = path
        self.__images = initialize(_images=images)

    # Debugging image for checking iterator
    def debug_iterator(self, bars: list):
        image = self.image
        for bar in bars:
            height, width, _ = image.shape
            cv2.line(image, (0, bar.begin), (width, bar.begin), self.color, 2)
            cv2.line(image, (0, bar.end), (width, bar.end), self.color, 2)
        self.image = image

    # Debugging image for checking inner components
    @multimethod
    def debug_components(self, components: list):
        image = self.image
        for component in components:
            cv2.rectangle(image, component.min, component.max, self.color, 3)
        self.image = image

    # Debugging image for checking outer components
    @multimethod
    def debug_components(self, components: list, positions: list):
        image = self.image
        for i in range(0, len(positions)):
            for component in components[i]:
                iterator = ((component.center[0], positions[i]), component.center)\
                    if positions[i] < component.center[1] else (component.center, (component.center[0], positions[i]))
                cv2.rectangle(image, component.min, component.max, self.color, 2)
                cv2.line(image, iterator[0], iterator[1], self.color, 2)
        self.image = image

    # Debugging image for checking actual lines
    def debug_actual_line(self, bars: list):
        image = self.image
        for line in [y for bar in bars for line in bar.lines.actual_lines for y in line]:
            height, width, _ = image.shape
            cv2.line(image, (0, line), (width, line), self.color, 2)
        self.image = image

    # Debugging image for checking virtual lines
    def debug_virtual_lines(self, bars: list):
        image = self.image

        # draw virtual lines
        for line in [line for bar in bars for line in bar.lines.virtual_lines]:
            height, width, _ = image.shape
            cv2.line(image, (0, line), (width, line), self.color, 2)

        # draw actual lines
        for line in [line for bar in bars for line in bar.lines.actual_lines]:
            height, width, _ = image.shape
            cv2.line(image, (0, line), (width, line), (0, 255, 0), 2)

        # draw another lines
        for line in [line for bar in bars for line in bar.lines.another_lines if bar.lines.another_lines is not None]:
            height, width, _ = image.shape
            cv2.line(image, (0, line), (width, line), (0, 255, 0), 2)

        self.image = image

    # Debugging image for checking connection
    def debug_connection(self, pairs: list):
        image = self.image
        for beam, component in pairs:
            iterator = (beam.center, component.center) if beam.center < component.center else (component.center,
                                                                                               beam.center)
            cv2.rectangle(image, component.min, component.max, self.color, 2)
            cv2.rectangle(image, beam.min, beam.max, self.color, 2)
            cv2.line(image, iterator[0], iterator[1], self.color, 2)
        self.image = image

    # getter property function
    @property
    def color(self) -> tuple:
        return self.__color

    # getter property function
    @property
    def path(self) -> str:
        return self.__path

    # getter property function
    @property
    def image(self) -> np.ndarray:
        return cv2.imread(self.path)

    # getter property function
    @property
    def images(self) -> list:
        return self.__images

    # setter property function
    @image.setter
    def image(self, _image: np.ndarray):
        self.__images.append(_image)
