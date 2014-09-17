#!/usr/bin/env python
import shelve


class Turtle:
    """
    This is a turtle that will be saved in a proper files and cloned
    """

    def __init__(self, name=None, age=None, cry="..."):
        if not name:
            self.name = "UnnamedTurtle"
        else:
            self.name = str(name)
        if age:
            self.age = int(age)
        else:
            self.age = "Unknown"

        self.cry = cry

    def __str__(self):
        r = "Turtle:" + \
            "\n\tName:\t\t" + self.name + \
            "\n\tAge:\t\t" + str(self.age) + \
            "\n\tCry:\t\t" + self.cry
        return r

print "-------------------"
print "I'm creating a turtle...\n"
t1 = Turtle("Mr.Johnson")
print str(t1)
print "-------------------"
print "We found %s age!!" % t1.name
t1.age = 42
print "This is now %s" % t1.name
print str(t1)
print "-------------------"
print "%s in near to die. We need to save him!" % t1.name
s1 = shelve.open("example_shelve/myturtle.txt")
s1[t1.name] = t1
s1.close()
print "Saved. I will remember your name forever"
FIRST_TURTLE_NAME = t1.name
del t1
print "%s is dead."
print "-------------------"
print "We are going to create a new turtle old one based"
s2 = shelve.open("example_shelve/myturtle.txt")
t2 = s2[FIRST_TURTLE_NAME]
print "-------------------"
print "This is the new %s!!!!" % FIRST_TURTLE_NAME
print str(t2)