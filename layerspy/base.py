"""Module providing base functions"""


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
        for keys in zone_data:
            self.zones[keys] = zone_data[keys]

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
            A layer that is defined by new similarities defined by your function

        """
        layer_subset = {}

        for zone, data in self.zones.items():
            if fun(data):
                layer_subset[zone] = self.zones[zone]

        return Layer(layer_subset)


def merge_layers(layer1, layer2):
    """Method to combine two layers

    Args:
        ``layer1`` (:obj:`Layer`): The first layer to be merged

        ``layer2`` (:obj:`Layer`): The second layer to be merged

    Returns:
        :obj:`Layer`: A new layer with the zone data from the two
        individual layers

    """
    new_layer = {}
    for keys in layer1.zones:
        new_layer[keys] = layer1.zones[keys]
    for keys in layer2.zones:
        new_layer[keys] = layer2.zones[keys]

    return Layer(new_layer)
