"""Module providing """

def make_id(species, xml):
    """A function to make the ideas for a given species

    Args:
        ``species`` (:obj:'str'): A string of the species

        ``xml`` (:obj:'xml'): An xml to use the xmlfunction

    """
    z_a = xml.get_z_a_state_from_nuclide_name(species)

    ids = (species, z_a[0], z_a[1])

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

            var = zone_data[keys]['mass fractions'][ids]

            boolean = fun(var)

            if boolean is True:

                self.zones[keys] = zone_data[keys]



    def update_layer(self, zone_data):
        """Method to add zone data to an existing layer.

        Args:
            ``layer`` (:obj:'dict'): A dictionary of layer data

            ``zone_data`` (:obj:'dict') A dictionary of zone data

        Returns: On successful return the additional zone data will
                be added to the layer

        """
        for keys in zone_data:

            self.zones[keys] = zone_data[keys]  ###Posibly creates an issue with dict keys

    def remove_zones_from_layer(self, fun, test_species):
        """Method to remove zone data with certain attributes from a layer

        Args:
            ``fun`` (:obj:'func'): A function that selects properties that are unwanted

            ``test_species`` (:obj:'str'): A string of the isotope that will be unwanted

        Returns:

            On successful return any zones with the unwanted quality will be removed

        """
        #ids = make_id(test_species)

        #for keys in self:

         #   t = self[keys]['mass fractions'][ids]

          #  boolean = fun(t)

            #if boolean == True:

                #remove the zone


    def get_layer_average(self, sp_id):
        """Method to average a species' mass fraction over all zones in a layer

        Args:
            ``sp`` (:obj:'str'): The species to average across the layer

        Returns:
            :obj:`float`: The average value for the species in that zone

        """
        vals = []

        for keys in self.zones:

            vals.append(self.zones[keys]['mass fractions'][sp_id])

        return sum(vals)/len(vals)


    def make_average_layer(self):
        """Method to turn a layer of multiple zones into a layer of a single
            zone with average values as the mass fractions

        Returns: :obj:`dict`: A dictionary of mass fractions of the average

        """
        avg_layer = {'0':{'mass fractions':{}}}

        for species in self.zones['position = last()']['mass fractions']:

            avg_val = self.get_layer_average(species)

            avg_layer['0']['mass fractions'][species] = avg_val

        return avg_layer



def mix(layer1, layer2, frac):
    """Method to mix two layers together

    Args:
        ``layer1`` (:obj:'layer'): Average layer

        ``layer2`` (:obj:'layer'): Average layer

        ``frac`` (:obj:'float'): fraction of layer1

    """

    mixture = {'0':{'mass fractions':{}}}

    for species in layer1['first()']['mass fractions']:

        mixture['position = first()']['mass fractions'][species] = \
                          frac*layer1['position = first()']['mass fractions'][species] +\
                            (1-frac)*layer2['position = first()']['mass fractions'][species]
