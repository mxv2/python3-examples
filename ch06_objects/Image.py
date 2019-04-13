#!/usr/bin/env python3
import os
import pickle


class ImageError(Exception):
    pass


class CoordinateError(ImageError):
    pass


class NoFilenameError(ImageError):
    pass


class SaveError(ImageError):
    pass


class LoadError(ImageError):
    pass


class ExportError(ImageError):
    pass


class Image:
    def __init__(self, width, height, filename="",
                 background="#FFFFFF"):
        self.filename = filename
        self.__background = background
        self.__data = {}
        self.__height = height
        self.__width = width
        self.__colors = {self.__background}

    @property
    def background(self):
        return self.__background

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def colors(self):
        return set(self.__colors)

    def __getitem__(self, coordinate):
        assert len(coordinate) == 2, "coordinate should be 2-tuple"
        if (not 0 <= coordinate[0] <= self.__width or
                not 0 <= coordinate[1] <= self.__height):
            raise CoordinateError(str(coordinate))
        return self.__data.get(tuple(coordinate), self.__background)

    def __setitem__(self, coordinate, color):
        assert len(coordinate) == 2, "coordinate should be 2-tuple"
        if (not 0 <= coordinate[0] <= self.__width or
                not 0 <= coordinate[1] <= self.__height):
            raise CoordinateError(str(coordinate))
        if color == self.__background:
            self.__data.pop(tuple(coordinate), None)
        else:
            self.__data[tuple(coordinate)] = color
            self.__colors.add(color)

    def __delitem__(self, coordinate):
        assert len(coordinate) == 2, "coordinate should be 2-tuple"
        if (not 0 <= coordinate[0] <= self.__width or
                not 0 <= coordinate[1] <= self.__height):
            raise CoordinateError(str(coordinate))
        self.__data.pop(tuple(coordinate), None)

    def save(self, filename=None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            data = [self.width, self.height, self.__background, self.__data]
            fh = open(self.filename, "wb")
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(err)
        finally:
            if fh is not None:
                fh.close()

    def load(self, filename=None):
        if filename is not None:
            self.filename = filename
        if not self.filename:
            raise NoFilenameError()

        fh = None
        try:
            fh = open(self.filename, "rb")
            data = pickle.load(fh)
            (self.__width, self.__height, self.__background, self.__data) = data
            self.__colors = (set(self.__data.values()) | {self.__background})
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(err)
        finally:
            if fh is not None:
                fh.close()

    def export(self, filename):
        if filename.lower().endswith(".xpm"):
            self.__export_xpm(filename)
        else:
            raise ExportError("unsupported export format:" +
                              os.path.splitext(filename)[1])

    def __export_xpm(self, filename):
        raise NotImplementedError()
