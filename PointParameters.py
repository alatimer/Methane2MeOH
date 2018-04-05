clrs_dict = {
    'Mn':'lime',
    'Cr':'lightblue',
    'Tc':'salmon',
    'Au':'gold',
    'Pd':'darkviolet',
    'Ag':'darkgray',
    'Pt':'lavender',
    'Ir':'navy',
    'Ru':'darkcyan',
    'Fe':'firebrick',
    'Cu':'goldenrod',
    'Cu-Fe':'firebrick',
    'V':'blue',
    'Mo':'m',
    'Ga':'green',
    'W':'orange',
    'Co':'cyan',
    'Ni':'pink',
    'Rh':'lightskyblue',
    'Au-Pd':'palegoldenrod',
    'Gas-Phase(Radical)':'grey',

    'Rutile(110)':'firebrick',
    'Metal(111)':'goldenrod',
    'Graphene':'pink',
    'Boron-nitride':'forestgreen',
    'CHA-MO':'lightgreen',
    'CHA-MOH':'m',
    'SAPO-34-MO':'lightskyblue',
    'CHA-MOM':'indianred',
    'MOR-MOM':'grey',
    'Porphyrin':'cyan',
    
    }

shape_dict = {
        'Rutile(110)':'o',
        'Metal(111)':'s',
        'Graphene':'8',
        'Boron-nitride':'p',
        'CHA-MO':'<',
        'CHA-MOH':'>',
        'MOR-MOM':'^',

}

def get_shape(key):
    if key in shape_dict:
        return shape_dict[key]
    else:
        print "No shape found for: ", key
        return "o"

def get_color(key):
    if key in clrs_dict:
       return clrs_dict[key]
    else:
       print "No color found for: ",key
       return 'grey'
         
