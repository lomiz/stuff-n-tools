#!/usr/bin/env python
class CoordinatesError(Exception):
    def __init__(self, arg):
        self.msg = arg


class ElementsError(Exception):
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
        elements_table -- list of permitted Objects(elements) in the "space". If None, all is permitted.
        grid_size -- the grid size rappresented by a tuple composed by x,y and z. Set z to 1 means a 2d grid.
    """

    def __init__(self, elements=None, elements_table=None, grid_size=(10, 10, 10)):
        # Obtain only positive integer (natural) numbers for the grid size
        self.max_x = abs(int(tuple(grid_size)[0]))
        self.max_y = abs(int(tuple(grid_size)[1]))
        self.max_z = abs(int(tuple(grid_size)[2]))
        self.elements_table = elements_table
        # Controllare correttezza di:
        #     - che i valori delle coordinate siano numberi naturali)
        #     - spazio (deve essere dentro le coordinate massime)
        #     - che gli elementi nel dizionario elements siano in elements_table

        # checking out_of_bounds
        for coordinates in elements:
            if Grid.is_out_of_bounds(coordinates, grid_size):
                raise CoordinatesError("Coordinates %s of the element %s are out of bounds." % (coordinates, elements[coordinates]))
                #raise CoordinatesError("prova")
        self.elements = dict(elements)
        self.space = self.elements
        self.grid_size = grid_size

    def __str__(self):
        r = "Grid size:" + \
            "\n\tMax x: " + str(self.max_x) + \
            "\n\tMax y: " + str(self.max_y) + \
            "\n\tMax z: " + str(self.max_z) + \
            "\n\nSpace: " + str(self.space) + "\n"
        return r

    def is_empty(self, coordinates):
        """
        Check if there is an element at given coordinates (no element definition in space dictionary)
        """
        if tuple(coordinates) in self.space:  # if in space dictionary there is not a definition "coordinates: elements"
            return False                      # means it must be an empty position (void filled)
        else:
            return True

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
                        #    print "%s sono le stesse coordinate passate" % str((column, row, layer))
                    # else: ====================FOR DEBUGGING====================
                    #    print "%s e' fuori dai limiti" % str((column, row, layer))
                    x_variator += 1

                y_variator += 1

            layer_variator += 1

        return neighbours


elementi = {(2, 1, 2): 'c', (1, 1, 1): 'a', (1, 1, 3): 'a', (3, 1, 1): 'a', (3, 1, 3): 'a'}
try:
    g = Grid(elementi, grid_size=(3, 3, 2))
except e as CoordinatesError:
    print e
    quit()
print g

c = g.get_neighbours_coordinates((1, 1, 1), 3)
print c
print len(c)




cordlist = []
for tupla in elementi:
    cordlist.append(tupla)

print cordlist
if g.is_out_of_bounds(cordlist, (3, 1, 3)):
    print "ci sono velori non validi"

# Prove per scartare le coordinate fuori piano cartesiano
"""d = []
for elem in c:
    if not (elem[0] <= 0 or elem[1] <= 0 or elem[2] <= 0):
        d.append(elem)


print d
print len(d)
"""