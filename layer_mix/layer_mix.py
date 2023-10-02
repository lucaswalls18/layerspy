"""Module providing """


def f(x,y):
    return x > y


def make_id(sp,xml):
    
    id = get_z_a_state_from_nuclide_name(sp)

    ids = (sp,id[0],id[1])

    return ids
    

class Layers:
    """A class for storing layer data"""

    def __init__(self):
        self.zones = {}


    def create_layer(self, zone_data, fun, test_species):
        """Method to create a layer object from a selection function.

        Args:
            ``zone_data`` (:obj:'dict'): A dictionary of zone data  
            
            ``fun`` (:obj:'func'): A function to select zones with 
                                        certain properties

            ``test_species`` (:obj:'str'): The name of the isotope
                                        your test function is meant to
                                        compare

        Returns:
            :obj:`dict`: A dictionary with all zones that belong to that 
                            layer

        """
        ids = make_id(test_species)
        
        for keys in zone_data:

            t = zone_data[keys]['mass fractions'][ids]

            bool = fun(t)

            if bool == True:
                
                self[keys] = zone_data[keys]

            

    def update_layer(self, zone_data):  
        """Method to add zone data to an existing layer.

        Args:
            ``layer`` (:obj:'dict'): A dictionary of layer data 

            ``zone_data`` (:obj:'dict') A dictionary of zone data 

        Returns: On successful return the additional zone data will be added to the layer

        """
        for keys in zone_data:
            
            self[keys] = zone_data[keys]  ###Posibly creates an issue with dict keys 


    def get_layer_average(self,sp_id):
        """Method to average a species' mass fraction over all zones in a layer 

        Args:
            ``sp`` (:obj:'str'): The species to average across the layer

        Returns:
            :obj:`float`: The average value for the species in that zone

        """
        #ids = make_id[sp]

        vals = []
        
        for keys in self:
            
            vals.append(self[keys]['mass fractions'][sp_id])

        return sum(vals)/len(vals)


    def make_average_layer(self):
        """Method to turn a layer of multiple zones into a layer of a single
            zone with average values as the mass fractions

        Returns: :obj:`dict`: A dictionary of mass fractions of the average

        """
        avg_layer = {'0':{'mass fractions':{}}}
        
        for sp in self['position = last()']['mass fractions']:

            avg_val = get_layer_average(sp)

            avg_layer['0']['mass fractions'][sp] = avg_val

        return avg_layer

        

def mix(layer1,layer2,f):
    """Method to mix two layers together

    Args:
        ``layer1`` (:obj:'layer'): 

    """

    mixture = {'0':{'mass fractions':{}}}

    for sp in layer1['first()']['mass fractions']:
        
        mixture['first()']['mass fractions'][sp] = f*layer1['first()']['mass fractions'][sp] + (1-f)*layer2['first()']['mass fractions'][sp]


   


