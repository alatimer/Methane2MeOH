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

    #Exp categories
    'Oxide':'lightgreen',
    'Au-Pd':'blanchedalmond',
    'Phthalocyanine':'cyan',
    'Phthalocyanine/zeolite':'cyan',
    'ZSM-5':'forestgreen',
    'SSZ-13':'indianred',
    'MOR':'powderblue',
    'Zeolite(Generic)':'crimson',
    'Phosphate':'goldenrod',
    'Phosphate/zeolite':'darkred',
    'Silicalite':'pink',
    'Sodalite':'plum',
    'Gas-phase':'white',

    
    }

shape_dict = {
        'Rutile(110)':'o',
        'Metal(111)':'s',
        'Graphene':'8',
        'Boron-nitride':'p',
        'CHA-MO':'<',
        'CHA-MOH':'>',
        'MOR-MOM':'^',
        'CHA-MOM':'v',
        'SAPO-34-MO':'D',
        'Porphyrin':'d',

        'aqueous':'d',
        'gas':'o',

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
         
