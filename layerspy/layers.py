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
    if isinstance(dictionary, dict):
        for key, value in dictionary.items():
            if isinstance(value, (int, float)):
                dictionary[key] = value * multiplier
            elif isinstance(value, dict):
                mult_dict_vals(value, multiplier)


def sum_all_properties_in_all_zones(input_dict):
    """Method used in the mix layer function"""
    summed_dict = {}

    for key, value in input_dict.items():
        if isinstance(value, dict):
            # If the value is a dictionary, recursively sum it
            nested_sum = sum_all_properties_in_all_zones(value)
            for subkey, subvalue in nested_sum.items():
                if subkey in summed_dict:
                    summed_dict[subkey] += subvalue
                else:
                    summed_dict[subkey] = subvalue
        elif isinstance(value, (int, float)):
            if key in summed_dict:
                summed_dict[key] += value
            else:
                summed_dict[key] = value

    return summed_dict


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

    def __mul__(self, weight_dict):
        """Method defining multiplication of a layer by a scalar

        Args:
            ``weight_dict`` (:obj:`dict`): A dictionary filled with weights for each zone

        Returns:
            :obj:`Layer`: A weighted layer
        """

        zones = self.get_zone_data()
        for keys in zones:
            weight = weight_dict[keys]
            mult_dict_vals(zones[keys], weight)
        return Layer(zones)

    def copy(self):
        """Method to return a copy of a layer

        Returns:
            :obj:`Layer`: A copy of self
        """
        return self

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

    def make_mixed_layer(self, weight_dictionary):
        """Method to mix a layer based on a given weight dictionary

        Args:
            ``weight_dictionary`` (:obj:`dict`): A dictionary of weights

        Returns:
            :obj:`Layer`: A single zone layer containing the mixture
        """
        scaled_layer = self * weight_dictionary
        scaled_zone_dict = scaled_layer.get_zone_data()
        mixture = sum_all_properties_in_all_zones(scaled_zone_dict)

        return mixture
