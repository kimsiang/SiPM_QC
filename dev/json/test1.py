#!/usr/bin/python

# This only uses the json package
import json

# Create a dictionary (a key-value-pair structure in Python)
my_dict = {
         'Name':      'KAIRA',
         'Location':  u'Kilpisj\u00E4rvi',
         'Longitude': 20.76,
         'Latitude':  69.07,
         }

# We can print the dictionary to show we have data. E.g.
print my_dict
print my_dict['Location']

# Open a file for writing
out_file = open("test.json","w")

# Save the dictionary into this file
# (the 'indent=4' is optional, but makes it more readable)
json.dump(my_dict, out_file)

# Close the file
out_file.close()
