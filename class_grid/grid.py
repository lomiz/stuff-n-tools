#!/usr/bin/env python
class CoordinatesError(Exception):
    def __init__(self, arg):
        self.msg = arg


class ElementsError(Exception):
    def __init__(self, arg):
        self.msg = arg


class ReplaceError(Exception):
    def __init__(self, arg):
        self.msg = arg


class Grid:
    """
    Description
        3d space rappresentation using Cartesian coordinate system composed by positive integers only (x,y and z >= 1).
        Every single space position is rappresented by a tuple composed by the three dimensions: (x,y,z) and can be
        filled by one element only. Void spaces are simply not defined to avoid resource comsuption.
        An element is rappresented by char (example 'a') that has to be defined in the "elements_table".

    Class Attributes:
        space -- a dictionary where the key is a tuple composed by x,y and z and the value is the object
                 in that point of the space. Void is not rappresented: if there is no key with that coordinates it means
                 there is no element in it.
                 Example of a 2x2x2 grid (5 elements, 3 voids):
                     {
                     (2,1,1):'a', (1,2,1):'a', (2,2,1):'c', (1,1,2):'b', (1,2,2):'a'
                     }
        elements --  an user defined dict with all the elements and theirs coordinates. If None was given all
                     types of object are permitted.
                     Example: {(1,1,1):'a', (1,2,5):'a', (67,2,123):'z'}
                     Default: None

        elements_table -- list of permitted Objects(elements) in the "space". If None, all is permitted.
                          Default: None

        grid_size -- the grid size rappresented by a tuple composed by x,y and z. Set z to 1 means a 2d grid.
                     Default: (10,10,10)

        position_overwriting -- if True permits the replace of elements in a position by new ones.
                                Void spaces are fillable also with False.
    Checks and Rules:
        You can't add an "element" to the "space" if:
            - it's out of bounds (its coordinates must be > 0,
            -


    DocTest
    >>> g = Grid()
    >>> g.is_empty((1,1,1))
    True
    >>> g.is_empty((1234, 1234, 1234))
    True
    >>> g.place({(1, 2, 3): 'a'})
    None
    >>> len(Grid.get_neighbours_coordinates((1, 1, 1), 3))
    7
    >>> len(Grid.get_neighbours_coordinates((2, 2, 2), 3))
    26
    >>> len(Grid.get_neighbours_coordinates((2, 1, 1), 3))
    11
    >>> len(Grid.get_neighbours_coordinates((3, 3, 3), 3))
    7
    >>> len(Grid.get_neighbours_coordinates((1, 1, 1), 5))
    26
    >>> len(Grid.get_neighbours_coordinates((3, 3, 3), 5))
    124
    >>> len(Grid.get_neighbours_coordinates((3, 1, 1), 5))
    44
    >>> len(Grid.get_neighbours_coordinates((1, 1, 1), 5))
    26
    """

    def __init__(self, elements=None, elements_table=None, grid_size=(10, 10, 10), position_overwriting=True):
        # Obtain only positive integer (natural) numbers for the grid size
        max_x = abs(int(tuple(grid_size)[0]))
        max_y = abs(int(tuple(grid_size)[1]))
        max_z = abs(int(tuple(grid_size)[2]))
        self.grid_size = (max_x, max_y, max_z)
        self.position_overwriting = bool(position_overwriting)
        self.elements_table = elements_table

        if elements is None:  # No {coordinates:elements} dictionary at Grid creation -> void dictionary
            self.space = {}
        else:  # They pass me a dictionary of {coordinates:elements} at Grid creation
            # checking out_of_bounds
            for coordinates in elements:
                try:
                    current_element = elements[coordinates]
                    current_coordinates = coordinates
                    Grid.ensure_integer_coordinates(current_coordinates)
                    if Grid.is_out_of_bounds(coordinates, grid_size):
                        raise CoordinatesError(["Coordinates {0} of the '{1}' element are out of bounds."
                                                .format(current_coordinates, current_element),
                                                {current_coordinates: current_element}])
                    # checking elements_table
                    elif not Grid.exist(current_element, self.elements_table):
                        raise ElementsError(["The element '{0}' does not exist in elements_table."
                                             .format(current_element),
                                             {current_coordinates: current_element}])
                except (CoordinatesError, ElementsError) as exc:
                    # For debug
                    # print exc.msg[0]
                    raise

            self.space = dict(elements)

    def __str__(self):
        r = "Grid size:" + \
            "\n\tMax x: " + str(self.grid_size[0]) + \
            "\n\tMax y: " + str(self.grid_size[1]) + \
            "\n\tMax z: " + str(self.grid_size[2]) + \
            "\n\nSpace: " + str(self.space) + "\n"
        return r

    def place(self, elements, ignore_invalid=True):
        """
        Add the given elements in the given coordinates. If replace is True any other element in that coordinates will
        be replaced.
        :param elements: dictionary of elements in the {(x,y,z):'myelement'} format
        :param ignore_invalid: if True, simply avoid to add invalid coordinates:element without re-raise Exceptions
                               Default: False
        """

        for coordinates in elements:
            current_element = elements[coordinates]
            current_coordinates = coordinates
            # For debug
            # print "\n\nCurrent: \t{0}->\t{1}".format(current_coordinates, current_element)
            try:
                Grid.ensure_integer_coordinates(current_coordinates)  # if not integers, CoordinatesError will be raised
                if Grid.is_out_of_bounds(coordinates, self.grid_size):  # avoid out_of_bounds elements
                    raise CoordinatesError(["Coordinates {0} of the '{1}' element are out of bounds."
                                            .format(current_coordinates, current_element),
                                            {current_coordinates: current_element}])
                elif not Grid.exist(current_element, self.elements_table):  # avoid elements not in
                    raise ElementsError(["The element '{0}' does not exist in elements_table."
                                         .format(current_element),
                                         {current_coordinates: current_element}])
                elif not self.is_empty and not self.position_overwriting:
                    raise ReplaceError(["Coordinates {0} are not empty and replacing/overwriting is not permitted"
                                        .format(current_coordinates),
                                        {current_coordinates: current_element}])
                else:  # Aggiungo il valore
                    self.space.update({current_coordinates: current_element})
            except (CoordinatesError, ElementsError, ReplaceError) as exc:
                # For debug
                # print exc.msg[0]
                if not ignore_invalid:
                    #print "Blocking the loop. Remaining elements will be not added."
                    raise
                else:
                    #print "Avoid adding last element at those coordinates. Going on.."
                    continue

        return True

    @staticmethod
    def ensure_integer_coordinates(coordinates):
        """
        Ensure that given coordinates are integer numbers
        :param coordinates: tuple with 3 coordinates in the (x,y,z) form
        CoordinatesError exception will be raised if any of given coordinates is not integer
        """
        if isinstance(coordinates[0], int) and isinstance(coordinates[1], int) and isinstance(coordinates[2], int):
            return True
        else:
            raise CoordinatesError(["Coordinates {0} MUST be integer numbers. They don't seem to be."
                                    .format(coordinates),
                                    coordinates])

    def is_empty(self, coordinates):
        """
        Check if there is an element at given coordinates (no element definition in space dictionary)
        :param coordinates: tuple of coordinates in the (x, y, z) style, or list of them.
        """
        if isinstance(coordinates, list):  # if they pass me a list of coordinates tuple
            for single_coordinates in coordinates:
                if tuple(single_coordinates) in self.space:  # searching in space dictionary for the coordinates. If we
                    return False                             # find one means it is occupy
                else:
                    return True
        else:  # they pass me a single coordinates tuple
            if tuple(coordinates) in self.space:
                return False
            else:
                return True

    @staticmethod
    def exist(element, elements_table=None):
        """
        Check the given element exist in the given elements_table. If not elements_table was given the method will try
        to use the one given at Grid creation. If none was given will be return True.
        """
        if elements_table is None:
            return True
        else:
            if element in elements_table:
                return True
            else:
                return False

    @staticmethod
    def is_out_of_bounds(coordinates, grid_size):
        """
        Check if given coordinates are out of grid bounds:
         - all coordinates must be positive because Grid use top-right part of a cartesian system
         - all coordinates must be inside the given grid_size
        :param coordinates: coordinates tuple to check or list of them.
                            If list, this method will return True just for a single tuple out of bounds.
        :param grid_size: tuple containing the grid size that rappresent top limits of the coordinates

        """
        x_limit = (tuple(grid_size))[0]
        y_limit = (tuple(grid_size))[1]
        z_limit = (tuple(grid_size))[2]

        if isinstance(coordinates, list):  # If user pass a list of tuple of coordinates i check everyone and return
                                           # True if only one of them is wrong
            for coordinates_tuple in coordinates:
                x = int((tuple(coordinates_tuple))[0])  # ensure that list elements are or can be coverted in tuple
                y = int((tuple(coordinates_tuple))[1])  # .. and convert the tuple elements in integers
                z = int((tuple(coordinates_tuple))[2])  #
                if (x <= 0 or y <= 0 or z <= 0) or (x > x_limit or y > y_limit or z > z_limit):
                    return True

        else:
            x = int((tuple(coordinates))[0])  # ensure tuple composed by integers
            y = int((tuple(coordinates))[1])  # .. same
            z = int((tuple(coordinates))[2])  # .. same
            if (x <= 0 or y <= 0 or z <= 0) or (x > x_limit or y > y_limit or z > z_limit):
                return True

        return False

    @staticmethod
    def get_neighbours_coordinates(coordinates, neighbours_cube_range=3):
        """
             ___ ___ ___  Image a 3x3 cube where the center is the coordinates parameter passed to the method.
           /___/___/___/| We choose the cube lenght (in this example 3) and we return all the coordinates of this cube
          /___/___/___/|| except the "coordinates" parameter itself
         /___/___/__ /|/| This method ignore if coordinates returned are invalid (like negative coordinates)
        |   |   |   | /|| If you want to get the element at the coordinates returned by this method look at the
        |___|___|___|/|/| "get_elements(coordinates)" function that is able to manage a single tuple or a list of
        |   |   |   | /|| coordinates and crop the wrong one (negatives).
        |___|___|___|/|/  Layers are the "depth" of the cube saw frontally.
        |   |   |   | /
        |___|___|___|/
        :param coordinates: a 3 element tuple like (x,y,z) rappresenting element coordinates (example: (5,3,2) )
        :param neighbours_cube_range: side lenght of an immaginary cube builded around "coordinates" element.
                                      this value MUST BE ODD POSITIVE NUMBER (otherwise there is not a perfect center)
                                      (default: 3)
        :return: a list of tuple where a single tuple rappresent the coordinates around the the element given
        """
        # If even number we dont return anything
        if neighbours_cube_range % 2 == 0:
            return None

        neighbours = []
        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]

        # Depth layer variation from center of the neighbours cube
        # 3 lenght side cube: -((3-1)/2) --> -1
        # 7 lenght side cube: -((7-1)/2) --> -3
        variator = -((abs(neighbours_cube_range)-1)/2)
        variator_limit = (abs(neighbours_cube_range)/2)+1
        # z variation
        layer_variator = variator

        #print "variator %s" % variator  ====================FOR DEBUGGING====================
        #print "variator_limit %s" % variator_limit  ====================FOR DEBUGGING====================

        # Image a 3x3 cube saw frontally where the element coordinates given are the center
        # Every while cicle we change layer:
        # - first cycle will be front layer of the "cube"
        # - second cycle will be the same layer of the element coordinates given
        # - third cycle will be the bottom layer
        while layer_variator < variator_limit:
            layer = z+layer_variator
            y_variator = variator

            while y_variator < variator_limit:
                row = y+y_variator
                x_variator = variator

                while x_variator < variator_limit:
                    column = x+x_variator
                    tmp_grid_size = neighbours_cube_range  # is_out_of_bounds() required a tuple (x,y,z) style for the
                                                           # grid_size parameter to know what are the grid limits

                    if not Grid.is_out_of_bounds((column, row, layer), (tmp_grid_size, tmp_grid_size, tmp_grid_size)):
                        # now i'm sure that current coordinates are not out of bounds. A coordinate is out_of_bounds if
                        # it's negative or if it's major than neighbours_cube_range.
                        # NB: As implemented there should not be coordinates major than neighbours_cube_range:
                        #    we use is_out_of_bounds() for preventing negative coordinates to be added.
                        if not (column == coordinates[0] and row == coordinates[1] and layer == coordinates[2]):
                            # ensure to return neighbours only (not coords themself)
                            neighbours.append((column, row, layer))
                        # else: ====================FOR DEBUGGING====================
                        #    print "%s are the same coordinates given to this method" % str((column, row, layer))
                    # else: ====================FOR DEBUGGING====================
                    #    print "%s is out of bounds" % str((column, row, layer))
                    x_variator += 1

                y_variator += 1

            layer_variator += 1

        return neighbours


if __name__ == "__main__":
    elementi = {(2, 1, 2): 'c', (1, 1, 1): 'a', (1, 1, 3): 'a', (3, 1, 1): 'a', (3, 1, 3): 'c'}
    dizionario_a = [1, 2, 3, 'a', 'b', 'c']
    dizionario_b = ['b']

    print "\n\n====TEST init()===="
    dimensioni = (3, 3, 3)
    print "Trying a Grid creation with these elements:\n\t{0}\nand these dimensions:\n\t{1}".format(elementi, dimensioni)
    try:
        g = Grid(elementi, dizionario_a, grid_size=dimensioni)
    except (CoordinatesError, ElementsError) as e:
        print "..."
        print "Grid creation failed. Details:\n{}".format(e.msg[0])
        # To get other variable in the exception CoordinatesError
        #print e.msg[1], e.msg[2]
    else:
        print "..."
        print "Grid successfully created: \n%s\n" % g

    print "\n\n====TEST get_neighbours_coordinates()===="
    c = Grid.get_neighbours_coordinates((1, 1, 1), 3)
    print c
    print len(c)

    print "\n\n====TEST is_out_of_bounds()===="
    cordlist = []
    for tupla in elementi:
        cordlist.append(tupla)

    print cordlist
    if Grid.is_out_of_bounds(cordlist, (3, 1, 3)):
        print "Not valid values"

    print "\n\n====TEST place()===="
    print g
    #Space: {(1, 1, 3): 'a', (1, 1, 1): 'a', (3, 1, 1): 'a', (2, 1, 2): 'c', (3, 1, 3): 'c'}
    g.place({(25, 1, 3): 'C', (3, 3, 2): 'z', (2.3, 3, 3): 'c'})
    print g