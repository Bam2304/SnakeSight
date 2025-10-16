count = 0

everyline = []
scores = {}

import csv
with open( 'Questions.csv', mode = 'r' ) as file:
    csvFile = csv.reader( file )
    for lines in csvFile: # makes a giant list of lists where each line in its own list
        templst = []
        for i in range( 0, 24 ): # this number has to be exact or index out of range 
            templst.append( lines[ i ])
        if( lines[ 0 ] != "Snake"): # makes a dict that will keep track of snake and thier current score
            scores[ lines[ 0 ]] = 0
        everyline.append( templst )


# this is the questionare
checker = True
tracker = []
print( "what catagory (type 'stop' to end)" )
for i in range( 1, len( everyline[0])):
    print( everyline[0][i] + ": " + str( i ))
while( checker ):
    user_data = input()
    for i in range( len( tracker )):
        if( user_data == tracker[ i ]):
            break # isn't stopping duplicates properly
    if( user_data == "stop" ):
        checker = False
    elif( int( user_data ) > 23 or int( user_data ) < 1 ): # fail safe, but still fails at random letters
                                                           # shouldn't matter because this will eventually be called with indexes from ui
        print( "Please try again with a working number" )
    else:
        tracker.append( i )
        keys = list( scores.keys())
        for i in range( 1, len( scores ) + 1):
            # if( int( user_data ) == 1 ): # associated with catagory Brown, etc...
            key = keys[i-1]
            currentVal = scores[key]
            scores[ key ] = float( currentVal ) + float( everyline[ i ][ int( user_data )])


# now to organize by most points to least points
# skips index 12 
rating = {}
indexes = []

values = list( scores.values())
value = list( scores.values()) # making a second list to get index value to for return 
for i in range( len( values )):
    max_value = max( values ) # gets the max value from pr
    indexMax = values.index( max_value ) # gets the index of that max
    
    for i in range( len( value )): # get a list of the indexes of top scores in order
        if( max_value == value[ i ]):
            if( i < 11 ): # to compensate for the messup on the database skipping 12
                rating[ i + 1 ] = float( max_value ) # plus 1 so its 1-11
            else:
                rating[ i + 2 ] = float( max_value ) # plus 2 so its 13-18

    # remove to avoid repeats
    del values[ indexMax ]
  #  del keys[ indexMax ]
print( rating ) #change to return

