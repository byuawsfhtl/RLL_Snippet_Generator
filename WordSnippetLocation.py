import pandas as pd

""" Takes a .tsv file for each picture and returns a set of tuples of locations to snippets with words.
 
:param filename: str. The name of the .tsv file associated with one image. The .tsv file needs to have
    columns named 'type', 'row', and 'column' identifying the type and location of the snippet.
    
:returns: set. Set of tuples with locations to word snippets.
"""

VERBOSE = False

def get_word_locations_from_tsv(filename: str) -> set:
    wordLocationsSet = set()
    # read tsv file to dataframe
    data = pd.read_csv(filename, sep='\t', header=0)
    # filter to 'word' type
    words = data.loc[data['type'] == 'word']
    # create set of tuples
    locations = list(zip(words['row'], words['column']))
    wordLocationsSet.update(locations)
    if VERBOSE: print(wordLocationsSet)
    return wordLocationsSet
