"""Module providing base functions"""


def mult_dict_vals(dictionary, multiplier):
    """Method to multiply dictionary values to be used in the __mul__
        operator for layers

    Args:
        ``dictionary`` (:obj:`dict`): dictionary to be scaled

        ``multiplier`` (:obj:`float`): Scalar to multiply the dictionary by

    Returns:
        On successful return the dictonary will be scaled by multiplier
    """
    new_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, (int, float)):
            new_dict[key] = value * multiplier
        elif isinstance(value, dict):
            new_dict[key] = {}
            new_dict[key] = mult_dict_vals(value, multiplier)
    return new_dict

def create_empty_dict_structure(dictionary):
    """Method used to average layers"""
    if isinstance(dictionary, dict):
        empty_dict = {}
        for key, value in dictionary.items():
            empty_dict[key] = create_empty_dict_structure(value)
        return empty_dict
    # Initialize with 0 for numeric values, or an appropriate default value
    if isinstance(dictionary, (int, float)):
        return 0
    return None  # This is the implicit return for other types

def add_dicts(dict1,dict2):
    """Method used to average layers"""
    result = {}
    for key in dict1:
        if key in dict2:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                result[key] = add_dicts(dict1[key], dict2[key])
            elif (isinstance(dict1[key], (float,int)) and isinstance(dict2[key], (float,int))):
                result[key] = dict1[key] + dict2[key]
        else:
            result[key] = dict1[key]
    for key in dict2:
        if key not in result:
            result[key] = dict2[key]
    return result

def sum_dicts(dicts):
    """Method used to average layers"""
    if not dicts:
        return create_empty_dict_structure(dicts[0])

    result = create_empty_dict_structure(dicts[0])
    for dictionaries in dicts:
        result = add_dicts(result, dictionaries)
    return result


class Layer:
    """A class for storing layer data"""

    def __init__(self, zone_data):
        """Method for initializing a layer object

        Args:
            ``zone_data`` (:obj:`dict`): A dictionary of zone data

        Returns:
            A layer which represents the given zone data
        """
        self.zones = {}
        self.zones = {keys: zone_data[keys] for keys in zone_data}

    def get_zone_data(self):
        """Method for retrieving the zone data of a given layer

        Returns:
            :obj:`dict`: of zone data
        """
        zones = {}
        zones = {key: self.zones[key] for key in self.zones}
        return zones

    def __eq__(self, other):
        """Method for comparing two Layer instances for equality

        Args:
            other (Layer): Another Layer instance to compare with self

        Returns:
            bool: True if the zone data of both instances is equal, False otherwise
        """
        return self.zones == other.zones

    def __add__(self, layer):
        """Method defining addition between two layers as a union

        Args:
            ``layer`` (:obj:`Layer`): Layer to add to self

        Returns:
            :obj:`Layer`: A new layer containing zone data from self and layer
        """
        union = {**self.get_zone_data(), **layer.get_zone_data()}
        return Layer(union)

    def copy(self):
        """Method to return a copy of a layer

        Returns:
            :obj:`Layer`: A copy of self
        """
        zone_data = self.get_zone_data()
        copy = Layer(zone_data)
        return copy

    def __mul__(self, weight_dict):  ##generalize for no nested structure  - needs testing
        """Method defining multiplication of a layer by a scalar

        Args:
            ``weight_dict`` (:obj:`dict`): A dictionary filled with weights for each zone to scale
            the layer

        Returns:
            :obj:`Layer`: A weighted layer
        """
        self_copy = self.copy_layer()
        zones = self_copy.get_zone_data()
        new_zones = {}
        for keys, values in zones.items():
            weight = weight_dict[keys]
            if isinstance(values, (int,float)):
                new_zones[keys] = weight*values
            else:
                new_zones[keys] = mult_dict_vals(zones[keys], weight)
        return Layer(new_zones)


    def update_layer(self, zone_data):
        """Method to add zone data to an existing layer.

        Args:

            ``zone_data`` (:obj:`dict`) A dictionary of zone data

        Returns: On successful return the additional zone data will
        be added to the layer

        """
        existing_keys = set(self.zones.keys())
        for keys in zone_data:
            if keys in existing_keys:
                raise ValueError(f"Duplicate key found: {keys}")
            self.zones[keys] = zone_data[keys]


    def remove_zones_from_layer(self, zone_keys):
        """Method to remove zone data by keys from a layer

        Args:
            ``zone_keys`` (:obj:`list`) A list of keys to remove from zone data

        Returns:

            On successful return any zones with the unwanted keys will be removed.

        Raises:
            ValueError: If any of the keys in zone_keys does not exist in the layer

        """
        existing_keys = set(self.zones.keys())
        for keys in zone_keys:
            if keys not in existing_keys:
                raise ValueError("Key {keys} does not match existing keys")
            self.zones.pop(keys, None)

    def get_layer_subset_from_function(self, fun):
        """Method to create a layer object from a selection function.

        Args:
            ``fun`` (:obj:`func`): A function to select zones with
                                  certain properties

        Returns:
            :obj:`Layer`: defined by new similarities defined by your function

        """
        layer_subset = {}

        for zone, data in self.zones.items():
            if fun(data):
                layer_subset[zone] = self.zones[zone]

        return Layer(layer_subset)

    def merge_layers(self, layer):
        """Method to merge a layer into self

        Args:
            ``Layer`` (:obj:`Layer`): A layer to merge with self

        Returns:
            On successful return 'self' will contain zone data from layer
        """
        for keys in layer.zones:
            self.zones[keys] = layer.zones[keys]

    def get_sum_of_property(self, prop):
        """Method to ge the sum of a specific property in all zones"""
        prop_sum = 0
        for keys in self.zones:
            prop_sum += self.zones[keys]["properties"][prop]
        return prop_sum


    def make_weight_dict(self, prop=None):
        """Method to make a weight dictionary for weighted averages

        Args:
            ``prop`` (:obj:`str`): A string of a property to define the weights of each
            zone

        Returns:
            :obj:`dict`: of the weight to be assigned to each zone in a layer. Defaults to
            equal weights.
        """
        weights = {}
        total_zones = len(self.zones)

        if prop is None:
            weight = 1 / total_zones
            weights = {key: weight for key in self.zones}
        else:
            prop_sum = self.get_sum_of_property(prop)
            weights = {
                key: self.zones[key]["properties"][prop] / prop_sum
                for key in self.zones
            }
        return weights

    def make_mixed_layer(self, weight_dictionary, mix_label='mixture'):
        """Method to mix a layer based on a given weight dictionary

        Args:
            ``weight_dictionary`` (:obj:`dict`): A dictionary of weights

            ``mix_label`` (:obj:`str`): A string to label the mixed zone data

        Returns:
            :obj:`Layer`: A single zone layer containing the mixture of all zones scaled by
            the given weight dictionary 
        """
#        self_copy = self.copy_layer()
        scaled_layer = self * weight_dictionary
        scaled_zone_dict = scaled_layer.get_zone_data()
        dicts = list(scaled_zone_dict.values())
        result_dict = sum_dicts(dicts)
        mix_zone = {}
        mix_zone[mix_label] = result_dict

        return Layer(mix_zone)
