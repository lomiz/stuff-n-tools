#!/usr/bin/env python

import json
import ast

"""
Reading a dictionary from json where tuple composed by 3 dimension coordinates is the key, but it was stored in string
format.
"""
json_file = "example_json/grid.json"


with open(json_file) as data_file:
    data = json.load(data_file)

data_file.close()

print "The data type for the json loaded file is %s" % type(data["grid"])
lista = data["grid"]

# Every single element in the grid list is a dictionary: i want to merge them in a super dictionary
print "Creating a super dictionary of all coordinates"
grid = {}
for space in lista:
    grid.update(space)


tuple_to_search = (1, 1, 1)
stringed_tuple_to_search = str(tuple_to_search)
print "The tuple to search is %s" % stringed_tuple_to_search


value_found_in_coordinates = grid.get(stringed_tuple_to_search)


print "Il valore trovato alle coordinate %s e' %s" % (stringed_tuple_to_search, value_found_in_coordinates)


print "\n\nOra inverto la tupla da tipo string a tipo tupla"
t = ast.literal_eval(stringed_tuple_to_search)
print "%s => %s\n%s => %s" % (stringed_tuple_to_search, type(stringed_tuple_to_search),
                              t, type(t))

