import codecs
import os

import numpy as np
import cv2
import copy

from PianistDesktop.utils.component import Component
from PianistDesktop.utils.line import Line
from PianistDesktop.utils.bar import Bar
from PianistDesktop.utils.debugging import Debugging
from collections import deque
from multimethod import multimethod


class Score:
    """
    Class to store objects stored in music score
    """

    def __init__(self, label_path: str, image_path: str):
        """
        Initialize member fields
        :param label_path: Path of detected objects
        :param image_path: Path of score images
        """

        def initialize(self_: Score) -> Debugging or None:
            return None if self_.image_path is None else Debugging(path=self_.image_path)

        self.__label_path = label_path
        self.__image_path = image_path
        # initialize debugging class's instance
        self.__debugging = initialize(self)
        # initialize score's bars
        self.__bars = self.get_bars()
        # initialize score's notes
        self.__notes = self.get_notes()

    def get_bars(self) -> list:
        """
        Returns score's bars and bar's components
        :return: List of score's bar
        """

        def read_image(path_: str) -> np.ndarray:
            """
            Read score's image file
            :param path_: Path of score's image
            :return: Image array
            """
            return cv2.imread(path_, cv2.IMREAD_GRAYSCALE)

        def deepcopy(image_: np.ndarray) -> np.ndarray:
            """
            Deep copy to avoid damaging the original
            :param image_: Image array
            :return: Deep copied image array
            """
            return copy.deepcopy(image_)

        def get_components(path_: str) -> list:
            """
            Returns score's entire components
            :param path_: Path of detected objects file
            :return: Entire components
            """

            def read_labels(path__: str) -> list:
                """
                Read score's component labels file
                :param path__: Path of detected objects file
                :return: Entire component's labels
                """
                labels__ = list()
                with codecs.open(path__, 'r') as file__:
                    for label__ in file__:
                        labels__.append(label__.rstrip())
                return labels__

            def get_component(label__: str) -> Component:
                """
                Create component class
                :param label__: Component's label
                :return: Component class
                """
                class_name__ = ['brace', 'fClef', 'flag128thDown', 'flag128thUp', 'flag16thDown', 'flag16thUp',
                                'flag64thDown', 'flag64thUp', 'flag8thDown', 'flag8thUp', 'gClef', 'noteheadBlack',
                                'noteheadHalf', 'noteheadWhole', 'rest16th', 'rest8th', 'restDoubleWhole',
                                'restHBar', 'restHNr', 'restHalf', 'restLonga', 'restQuarter', 'restWhole']
                elements__ = label__.split()

                # initialize component class
                component__ = Component(name=class_name__[int(elements__[0])],
                                        min=(int(elements__[1]), int(elements__[2])),
                                        max=(int(elements__[3]), int(elements__[4])),
                                        accuracy=float(elements__[5]))
                return component__

            components_ = list()
            labels_ = read_labels(path__=path_)

            # set components
            for label_ in labels_:
                components_.append(get_component(label__=label_))

            return components_

        def get_braces(components_: list) -> list:
            """
            If brace exist, return brace's components else return none
            :param components_: Entire components
            :return: List of brace
            """

            def is_brace(components__: list) -> bool:
                """
                Check brace exist
                :param components__: Entire components
                :return: Boolean
                """
                return 'brace' in [component__.name for component__ in components__]

            if is_brace(components__=components_) is True:
                braces__ = list(filter(lambda component__: component__.name == 'brace', components_))
                return sorted(braces__)
            else:
                return list()

        def get_clefs(components_: list) -> list:
            """
            Return clefs
            :param components_: Entire components
            :return: clefs
            """
            clefs_ = list(filter(
                lambda component_: component_.name == 'gClef' or component_.name == 'fClef', components_))
            return sorted(clefs_)

        def get_iterators(clefs_: list) -> tuple:
            """
            Clefs component's iterator initialize bar
            :param clefs_: clef components
            :return: iterator
            """
            centers_ = list()
            begin_, end_ = 0, 0
            for i_ in range(len(clefs_) - 1):
                height_ = int((clefs_[i_ + 1].center[1] - clefs_[i_].center[1]) / 2)
                center_ = clefs_[i_].center[1] + height_
                # set first bar's beginning iterator
                if i_ == 0:
                    begin_ = clefs_[i_].center[1] - height_
                # set last bar's ending iterator
                elif i_ == len(clefs_) - 2:
                    end_ = clefs_[i_ + 1].center[1] + height_
                # set bar's iterator
                centers_.append(center_)
            return begin_, end_, centers_

        def set_instances(bars_: list, count_: int):
            """
            Set instance of bar class
            :param bars_: Reference of bars list
            :param count_: Count of clefs
            :return: Set bars list
            """
            for i_ in range(0, count_):
                bars_.append(Bar())

        @multimethod
        def set_iterators(bars_: list, begin_: int, end_: int, centers_: list):
            """
            First set in setting up iterators
            :param bars_: List of bars
            :param begin_: Begin of bar iterator
            :param end_: End of bar iterator
            :param centers_: Center of bar iterator
            """
            for i_, center_ in enumerate(centers_):
                # set first bar's beginning iterator
                if i_ == 0:
                    bars_[i_].begin = begin_
                # set last bar's ending iterator
                elif i_ == len(centers_) - 1:
                    bars_[i_ + 1].end = end_
                # set middle bar's iterator
                bars_[i_].end = bars_[i_ + 1].begin = center_

            # debugging for image view
            self.debugging.debug_iterator(bars=bars_)

        @multimethod
        def set_line(bars_: list, image_: np.ndarray):
            """
            Detect actual lines and Set up bar
            :param bars_: List of bars
            :param image_: Score's image array
            """

            def set_segment(segments__: list, bars__: list, image__: np.ndarray):
                """
                Set segment of bar
                :param segments__: Segment of bar
                :param bars__: Bar
                :param image__: Score's image array
                :return: Segment of bar
                """

                def sort_image(segment___: np.ndarray) -> np.ndarray:
                    """
                    Sort segment of image to detect longest line(actual line)
                    :param segment___: Image segment of bar
                    :return: Sorted image segment of bar
                    """
                    return np.sort(segment___, axis=1)

                for bar__ in bars__:
                    segments__.append(sort_image(segment___=image__[bar__.begin:bar__.end, :]))

            segments_ = list()
            set_segment(segments__=segments_, bars__=bars_, image__=image_)

            for bar_, segment__ in zip(bars_, segments_):
                lines_ = Line()
                # set actual lines
                lines_.set_lines(segment__, bar_.begin)
                bar_.lines = lines_

            # debugging for image view
            self.debugging.debug_actual_line(bars=bars_)

        def detect_beams(bars_: list, components_: list, image_: np.ndarray) -> list:
            """
            Use Hough transform to detect rectangle objects
            :param bars_: List of bars
            :param components_: Entire component
            :param image_: Score's image array
            :return: List of rectangle objects
            """

            def remove_line(bars__: list, image__: np.ndarray):
                """
                Remove actual line to image
                :param bars__: List of bars
                :param image__: Score's image array
                """
                for y__ in [i__ for bar__ in bars__ for line__ in bar__.lines.actual_lines for i__ in line__]:
                    for i__, pixel__ in enumerate(image__[y__ - 1, :]):
                        if pixel__ > 100:
                            image__[y__, i__] = 255

            def remove_components(image__: np.ndarray, components__: list):
                """
                Remove components to image
                :param image__: Score's image array
                :param components__: Bar's components
                """
                for component__ in components__:
                    cv2.rectangle(image__, component__.min, component__.max, (255, 255, 255), -1)

            def detect_rectangle(image__: np.ndarray) -> list:
                """
                Use Hough transform
                :param image__: Score's image array
                :return: Detected rectangle objects
                """
                beams__ = list()
                ret__, threshold__ = cv2.threshold(image__, 50, 255, 1)

                # remove some small noise if any
                dilate__ = cv2.dilate(threshold__, None)
                erode__ = cv2.erode(dilate__, None)
                erode2__ = cv2.erode(erode__, None)

                # find contours with cv2.RETR_CCOMP
                contours__, hierarchy__ = cv2.findContours(erode2__, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

                for i__, contour__ in enumerate(contours__):
                    # Check if it is an external contour and its area is more than 100
                    if hierarchy__[0, i__, 3] == -1 and cv2.contourArea(contour__) > 100:
                        x__, y__, w__, h__ = cv2.boundingRect(contour__)
                        beam__ = Component(name='beam', min=(x__, y__), max=(x__ + w__, y__ + h__), accuracy=100)
                        beams__.append(beam__)

                return beams__

            def set_flags(beams__: list, components__: list):
                """
                Move flag component to beams
                :param beams__: Rectangle list
                :param components__: Bar's components
                """

                def _get_components(components___: list) -> list:
                    """
                    Select flag component and return
                    :param components___: Bar's components
                    :return: List of flag components
                    """
                    def check(component___):
                        """
                        Check bar's components have flag components
                        :param component___: Bar's components
                        :return: Boolean
                        """
                        return component___.name == 'flag128thDown' or component___.name == 'flag128thUp' \
                               or component___.name == 'flag64thDown' or component___.name == 'flag64thUp' \
                               or component___.name == 'flag16thDown' or component___.name == 'flag16thUp' \
                               or component___.name == 'flag8thDown' or component___.name == 'flag8thUp'

                    return list(filter(check, components___))

                # extend flag components
                return beams__.extend(_get_components(components___=components__))

            # remove actual lines
            remove_line(image__=image_, bars__=bars_)
            # remove bar's components
            remove_components(image__=image_, components__=components_)
            beams_ = detect_rectangle(image__=image_)
            # set flag components to beams list
            set_flags(beams__=beams_, components__=components_)

            # debugging for image view
            self.debugging.debug_components(beams_)

            return beams_

        @multimethod
        def set_iterators(bars_: list, braces_: list):
            """
            Reset iterator to detect inner and outer components
            :param bars_: List of bars
            :param braces_: List of braces
            """
            def get_iterator_in_brace(bars__: list, brace__: Component) -> list:
                """
                If brace components exist, return bars list in brace area
                :param bars__: List of bars
                :param brace__: List of braces
                :return: List of bar in brace
                """
                return [bar__ for bar__ in bars__ if brace__.min[1] <= bar__.lines.center <= brace__.max[1]]

            def delete_bars(bars__: list, targets__: list, index__: int):
                """
                Delete bar for including brace
                :param bars__: List of bars
                :param targets__: Bar in brace
                :param index__: Index of bar
                """
                for target__ in targets__:
                    if bars__[index__] is not target__:
                        bars__.remove(target__)

            # brace not exist
            if not braces_:
                for bar_ in bars_:
                    bar_.begin = bar_.lines.begin
                    bar_.end = bar_.lines.end
            # brace exist
            else:
                for brace_ in braces_:
                    bars_in_brace_ = get_iterator_in_brace(bars__=bars_, brace__=brace_)
                    index_ = bars_.index(bars_in_brace_[0])
                    bars_[index_].begin = bars_in_brace_[0].lines.begin
                    bars_[index_].end = bars_in_brace_[len(bars_in_brace_) - 1].lines.end
                    bars_[index_].lines.another_lines = bars_in_brace_[len(bars_in_brace_) - 1].lines.actual_lines
                    # delete bar for include brace
                    delete_bars(bars__=bars_, targets__=bars_in_brace_, index__=index_)

            # debugging for image view
            self.debugging.debug_iterator(bars=bars_)

        def set_components(bars_: list, components_: list, height_: int):
            """
            Set inner and outer components to bar
            :param bars_: List of bars
            :param components_: Entire components
            :param height_: Component's height
            """
            def _get_components(begin__: int, end__: int, components__: list) -> list:
                """
                Return components included bar
                :param begin__: Beginning iterator
                :param end__: Ending iterator
                :param components__: Entire component
                :return: Components in bar
                """
                return list(filter(lambda c__: begin__ <= c__.center[1] <= end__, components__))

            def _get_iterators(bars__: list, height__: int) -> list:
                """
                Return iterator for outer components
                :param bars__: List of bars
                :param height__: component's height
                :return: Iterator for outer components
                """
                iterators__ = list()
                # beginning iterator
                iterators__.append((0, bars__[0].begin))
                # middle iterator
                for i__ in range(0, len(bars__) - 1):
                    iterators__.append((bars__[i__].end, bars__[i__ + 1].begin))
                # ending iterator
                iterators__.append((bars__[len(bars__) - 1].end, height__))
                return iterators__

            def identify_component(begin__: int, end__: int, components__: list) -> tuple:
                """
                Find where the component belongs.
                :param begin__: Beginning iterator
                :param end__: Ending iterator
                :param components__: Components excluding external components
                :return: Distances of each iterator
                """
                upside__, downside__ = list(), list()
                for component__ in components__:
                    # set different upside iterator
                    distance_of_upside__ = component__.center[1] - begin__
                    # set different downside iterator
                    distance_of_downside__ = end__ - component__.center[1]
                    upside__.append(component__) \
                        if distance_of_upside__ < distance_of_downside__ else downside__.append(component__)
                return upside__, downside__

            # set the internal components to the bar they belong to
            for bar_ in bars_:
                bar_.components = _get_components(begin__=bar_.begin, end__=bar_.end, components__=components_)
                components_ = [component_ for component_ in components_ if component_ not in bar_.components]

            # debugging for image view
            self.debugging.debug_components([component_ for bar_ in bars_ for component_ in bar_.components])

            # set the external components to the bar they belong to
            pairs_ = list()
            iterators_ = _get_iterators(bars__=bars_, height__=height_)
            for i_, iterator_ in enumerate(iterators_):
                # external components in top
                if i_ == 0:
                    component_list_ = _get_components(iterator_[0], iterator_[1], components_)
                    pairs_.append((component_list_, bars_[0].begin))
                    bars_[0].components.extend(component_list_)
                # external components in bottom
                elif i_ == len(iterators_) - 1:
                    component_list_ = _get_components(iterator_[0], iterator_[1], components_)
                    pairs_.append((component_list_, bars_[len(bars_) - 1].end))
                    bars_[len(bars_) - 1].components.extend(component_list_)
                # external components in middle
                else:
                    upside_, downside_ = identify_component(
                        begin__=iterator_[0],
                        end__=iterator_[1],
                        components__=_get_components(
                            begin__=iterator_[0], end__=iterator_[1], components__=components_
                        )
                    )
                    pairs_.append((upside_, bars_[i_ - 1].end))
                    bars_[i_ - 1].components.extend(upside_)
                    pairs_.append((downside_, bars_[i_].begin))
                    bars_[i_].components.extend(downside_)

            # debugging for image view
            self.debugging.debug_components([pair_[0] for pair_ in pairs_], [pair_[1] for pair_ in pairs_])

        @multimethod
        def set_iterators(bars_: list):
            """
            Set Iterator to ensure bar boundaries
            :param bars_: List od bars
            """
            def sort(bar__: Bar):
                """
                Sort components in bar
                :param bar__: List of bars
                """
                sorted(bar__.components, key=lambda y__: y__.center[0])

            def get_iterator(bar__: Bar) -> tuple:
                """
                Return iterator to update
                :param bar__: List of bars
                :return: Iterator before change
                """
                begin__ = min(bar__.components, key=lambda y__: y__.center[1])
                end__ = max(bar__.components, key=lambda y__: y__.center[1])
                return begin__.min[1], end__.max[1]

            for bar_ in bars_:
                sort(bar__=bar_)
                begin_, end_ = get_iterator(bar__=bar_)
                # update iterator of bar
                bar_.begin = begin_ if begin_ < bar_.begin else bar_.begin
                bar_.end = end_ if end_ > bar_.end else bar_.end

            # debugging for image view
            self.debugging.debug_iterator(bars=bars_)

        def set_beams(bars_: list, beams_: list, image_: np.ndarray):
            def _get_components(components__: list) -> list:
                return [component__ for component__ in components__ if component__.name == 'noteheadBlack']

            def bfs(component__: Component, beam__: Component, image__: np.ndarray) -> bool:
                @multimethod
                def check(component___: Component, move___: tuple, image___: np.ndarray) -> bool:
                    return image___[move___[1]][move___[0]] < 255 and \
                           component___.min[0] <= move___[0] <= component___.max[0]

                @multimethod
                def check(current___: tuple, min___: tuple, max___: tuple) -> bool:
                    return min___[0] <= current___[0] <= max___[0] and min___[1] <= current___[1] <= max___[1]

                directions__ = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                visited__ = list()
                queue__ = deque()
                queue__.append(component__.center)

                while queue__:
                    current__ = queue__.popleft()

                    if check(current__, beam__.min, beam__.max) is True:
                        return True

                    for move__ in [(current__[0] + direction__[0],
                                    current__[1] + direction__[1]) for direction__ in directions__]:
                        if check(component__, move__, image__) and move__ not in visited__:
                            queue__.append(move__)
                            visited__.append(move__)

                return False

            def get_beams(beams__: list, begin__: int, end__: int, component__: Component) -> list:
                beam_in_segment__ = list()
                for beam__ in beams__:
                    x1__, y1__ = beam__.min
                    x2__, y2__ = beam__.max
                    x3__, y3__ = component__.min[0], begin__
                    x4__, y4__ = component__.max[0] + 100, end__

                    if x2__ < x3__ or x1__ > x4__ or y2__ < y3__ or y1__ > y4__:
                        continue

                    beam_in_segment__.append(beam__)

                return beam_in_segment__

            pairs_ = list()
            for i_ in range(0, len(bars_)):
                components_ = _get_components(components__=bars_[i_].components)

                if i_ == 0:
                    begin_, end_ = 0, bars_[i_ + 1].begin
                elif i_ == len(bars_) - 1:
                    begin_, end_ = bars_[i_ - 1].end, image_.shape[0]
                else:
                    begin_, end_ = bars_[i_ - 1].end, bars_[i_ + 1].begin

                for component_ in components_:
                    beams_in_segment_ = get_beams(beams__=beams_, begin__=begin_, end__=end_, component__=component_)
                    for beam_ in beams_in_segment_:
                        if bfs(component__=component_, beam__=beam_, image__=image_) is True:
                            pairs_.append((component_, beam_))
                            component_.beams = 1

            for _, beam_ in pairs_:
                if beam_ in beams_:
                    beams_.remove(beam_)

            # debugging for image view
            self.debugging.debug_connection(pairs=pairs_)

        @multimethod
        def set_line(bars_: list):
            for bar_ in bars_:
                bar_.lines.set_lines()

            self.debugging.debug_virtual_lines(bars=bars_)

        def set_rests(bars_: list, beams_: list, image_: np.ndarray):
            def get_beams(beams__: list, begin__: int, end__: int) -> list:
                beam_in_segment__ = list()
                for beam__ in beams__:
                    if begin__ + 5 <= beam__.min[1] <= end__ + 5 and begin__ + 5 <= beam__.max[1] <= end__ + 5:
                        beam_in_segment__.append(beam__)

                return beam_in_segment__

            def identify_beams(beam_in_segment__: list, begin__: int, end__: int) -> tuple:
                upside__, downside__ = list(), list()
                for beam__ in beam_in_segment__:
                    distance_of_upside__ = beam__.center[1] - begin__
                    distance_of_downside__ = end__ - beam__.center[1]
                    upside__.append(beam__) \
                        if distance_of_upside__ < distance_of_downside__ else downside__.append(beam__)
                return upside__, downside__

            def get_rest2(downside__: list, end__: int, image__: np.ndarray) -> list:
                def check(beam___: Component, end___: int, image___: np.ndarray) -> bool:
                    for i___ in range(beam___.min[0], beam___.max[0]):
                        for pixel___ in image___[beam___.min[1]:end___, i___]:
                            if pixel___ > 100:
                                return False
                    return True

                rests__ = list()

                for beam__ in downside__:
                    if check(beam___=beam__, end___=end__, image___=image__) is True:
                        beam__.name = 'restHalf'
                        rests__.append(beam__)

                return rests__

            def get_rest4(upside__: list, begin__: int, image__: np.ndarray) -> list:
                def check(beam___: Component, begin___: int, image___: np.ndarray) -> bool:
                    for i___ in range(beam___.min[0], beam___.max[0]):
                        for pixel___ in image___[begin___:beam___.max[1], i___]:
                            if pixel___ > 100:
                                return False
                    return True

                rests__ = list()

                for beam__ in upside__:
                    if check(beam___=beam__, begin___=begin__, image___=image__) is True:
                        beam__.name = 'restWhole'
                        rests__.append(beam__)

                return rests__

            components_ = list()
            for bar_ in bars_:
                begin_ = bar_.lines.actual_lines[1]
                end_ = bar_.lines.actual_lines[2]
                beam_in_segment_ = get_beams(beams__=beams_, begin__=begin_, end__=end_)
                upside_, downside_ = identify_beams(beam_in_segment__=beam_in_segment_, begin__=begin_, end__=end_)
                rests_ = get_rest2(downside__=downside_, end__=end_,
                                   image__=image_) + get_rest4(upside__=upside_, begin__=begin_, image__=image_)
                components_.extend(rests_)
                bar_.components.extend(rests_)

                if bar_.lines.another_lines is not None:
                    begin_ = bar_.lines.another_lines[1]
                    end_ = bar_.lines.another_lines[2]
                    beam_in_segment_ = get_beams(beams__=beams_, begin__=begin_, end__=end_)
                    upside_, downside_ = identify_beams(beam_in_segment__=beam_in_segment_, begin__=begin_, end__=end_)
                    rests_ = get_rest2(downside__=downside_, end__=end_,
                                       image__=image_) + get_rest4(upside__=upside_, begin__=begin_, image__=image_)
                    components_.extend(rests_)
                    bar_.components.extend(rests_)

            # debugging for image view
            self.debugging.debug_components(components_)

        bars = list()
        image = read_image(path_=self.image_path)
        components = get_components(path_=self.label_path)
        braces = get_braces(components_=components)
        clefs = get_clefs(components_=components)
        begin, end, centers = get_iterators(clefs_=clefs)

        set_instances(bars_=bars, count_=len(clefs))
        set_iterators(bars, begin, end, centers)
        set_line(bars, deepcopy(image_=image))
        beams = detect_beams(bars_=bars, components_=components, image_=deepcopy(image_=image))
        set_iterators(bars, braces)
        set_components(bars_=bars, components_=components, height_=image.shape[0])
        set_iterators(bars)
        set_beams(bars_=bars, beams_=beams, image_=deepcopy(image_=image))
        set_line(bars)
        set_rests(bars_=bars, beams_=beams, image_=deepcopy(image_=image))

        return bars

    def get_notes(self):
        """
        Return score's note
        :return: Note
        """

        @multimethod
        def get_components(components_: list, begin_: int, end_: int) -> list:
            def check(component__: Component) -> bool:
                """
                Check component is note or rest or something else
                :param component__: Component
                :return: Boolean
                """
                if component__.name in ['noteheadBlack', 'noteheadHalf', 'noteheadWhole', 'rest16th',
                                        'rest8th', 'restHalf', 'restQuarter', 'restWhole']:
                    return True
                else:
                    return False

            def check_in_segment(components__: list, begin__: int, end__: int) -> list:
                """
                Check notes and rests in segment
                :param components__: Checked components
                :param begin__: Beginning iterator
                :param end__: Ending iterator
                :return: Checked component in segment
                """
                components_in_segment__ = list()
                for component__ in components__:
                    if begin__ <= component__.center[1] <= end__:
                        components_in_segment__.append(component__)
                return components_in_segment__

            notes_ = list()
            for component_ in components_:
                if check(component__=component_) is True:
                    notes_.append(component_)

            return check_in_segment(notes_, begin__=begin_, end__=end_)

        def get_note(components_: list, begin_: int, end_: int) -> list:
            def sort(components__: list) -> list:
                return sorted(components__, key=lambda component__: component__.center[0])

            def get_chords(components__: list, begin__: int, end__: int) -> list:
                def is_empty(components___: list) -> bool:
                    return True if components___ else False

                def get_chord(component___: Component, components___: list, begin___: int, end___: int) -> list:
                    chord___ = list()
                    index___ = 0
                    for i___ in range(0, len(components___)):
                        x1___, y1___ = components___[index___ + i___].min
                        x2___, y2___ = components___[index___ + i___].max
                        x3___, y3___ = component___.min[0], begin___
                        x4___, y4___ = component___.max[0], end___

                        if x2___ < x3___ or x1___ > x4___ or y2___ < y3___ or y1___ > y4___:
                            continue

                        chord___.append(components___[index___ + i___])
                        components___.remove(components___[index___ + i___])
                        index___ -= 1
                    return chord___

                chords__ = list()
                while is_empty(components__):
                    chord__ = get_chord(component___=components__[0], components___=components__,
                                        begin___=begin__, end___=end__)
                    chords__.append(chord__)
                return chords__

            sorted_components_ = sort(components__=components_)
            notes_ = get_chords(components__=sorted_components_, begin__=begin_, end__=end_)

            return notes_

        def convert_text(notes_: list, lines_: list) -> str:
            @multimethod
            def get_token() -> str:
                return "/0000000000000000000000000000"

            @multimethod
            def get_token(token__: str) -> str:
                return token__[0:8] + '#' + token__[8:15] + '#' + token__[15:22] + '#' + token__[22:]

            def get_index(lines__: list, y__: int) -> int:
                indexes__ = [abs(y__ - line) for line in lines__]
                minimum__ = min(indexes__)
                return indexes__.index(minimum__)

            def replace(token__: str, indexes__: list, values__: list) -> str:
                token_list__ = list(token__)
                for index__, value__ in zip(indexes__, values__):
                    token_list__[index__] = str(value__)
                return ''.join(token_list__)

            text_ = ''
            note_list_ = list()
            note_list_.append(notes_)
            for chord_ in [chord_ for note_ in note_list_ for chord_ in note_]:
                token_ = get_token()
                if len(chord_) == 1 and chord_[0].name in ['rest16th', 'rest8th', 'restHalf',
                                                           'restQuarter', 'restWhole']:
                    tokens_ = chord_[0].length * get_token(get_token())
                else:
                    indexes_, values_ = list(), list()
                    for component_ in chord_:
                        indexes_.append(get_index(lines__=lines_, y__=component_.center[1]))
                        values_.append(component_.length if component_.length < 9 else 16)
                    maximum_ = max(values_) - 1
                    tokens_ = get_token(replace(token__=token_, indexes__=indexes_, values__=values_))
                    if maximum_ != 0:
                        tokens_ += get_token(get_token()) * maximum_
                text_ += tokens_

            return text_

        texts = ''
        for i, bar in enumerate(self.bars):
            lines = bar.lines.lines
            components = get_components(bar.components, lines[0], lines[len(lines) - 1])
            notes = get_note(components_=components, begin_=lines[0], end_=lines[len(lines) - 1])
            texts += convert_text(notes_=notes, lines_=lines)

        return texts

    # getter property function
    @property
    def label_path(self) -> str or None:
        return self.__label_path

    # getter property function
    @property
    def image_path(self) -> str or None:
        return self.__image_path

    # getter property function
    @property
    def bars(self) -> list:
        return self.__bars

    # getter property function
    @property
    def debugging(self) -> Debugging:
        return self.__debugging

    # getter property function
    @property
    def notes(self) -> str:
        return self.__notes


if __name__ == '__main__':
    # Please put the path of the converted images
    image_path = ""
    # Please put the path of the converted labels
    label_path = ""

    notes = ''

    image_names = os.listdir()
    label_names = os.listdir()

    score = list()

    for i in range(len(image_names)):
        scores.append(Score(
            image_path=image_path + '/' + image_names[i],
            label_path=label_path + '/' + label_names[i]
        ))

    for score in scores:
        notes += score.notes

    with open("../result", 'w') as file:
        file.write(notes)