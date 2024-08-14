import pytest
from layerspy import Layer

def compare_dicts(dict1, dict2, tol=1e-6):
    if len(dict1) != len(dict2):
        return False
    for key, value1 in dict1.items():
        if key not in dict2:
            return False
        value2 = dict2[key]
        if isinstance(value1, dict) and isinstance(value2, dict):
            if not compare_dicts(value1, value2, tol):
                return False
        elif isinstance(value1, float) and isinstance(value2, float):
            if abs(value1 - value2) > tol:
                return False
        else:
            if value1 != value2:
                return False
    return True

def test_init_method():
    # Test data
    zone_data = {"zone1": 10, "zone2": 20, "zone3": {'subzone': 'test'}}

    # Create an instance of the class
    my_layer = Layer(zone_data)

    # Perform assertions to check if the initialization is correct
    assert isinstance(my_layer, Layer)
    assert my_layer.zones == zone_data


def test_get_zone_data():
    #Test data
    zone_data = {"zone1": 10, "zone2": 20, "zone3": 30}

    #Create an instance of the class
    my_layer = Layer(zone_data)

    #pull zone data
    test = my_layer.get_zone_data()
    assert test == zone_data


def test_addition():
    data1 = {"zone1": 10, "zone2": 20}
    data2 = {"zone3": 30, "zone4": 40}

    layer1 = Layer(data1)
    layer2 = Layer(data2)

    data3 = {"zone1":10, "zone2": 20, "zone3": 30, "zone4": 40}
    layer3 = Layer(data3)

    test = layer1 + layer2

    assert test == layer3
    assert layer1 != layer2


def test_update_layer():
    # Test data
    initial_data = {"zone1": 10, "zone2": 20}
    new_data = {"zone3": 30, "zone4": 40}
    duplicate_data = {"zone1": 50, "zone2": 60}

    # Create an instance of the class and initialize it with initial_data
    my_layer = Layer(initial_data)

    # Test updating with new_data
    my_layer.update_layer(new_data)
    assert my_layer.zones == {
        "zone1": 10,
        "zone2": 20,
        "zone3": 30,
        "zone4": 40,
    }

    # Test updating with duplicate_data, expect an error
    with pytest.raises(ValueError):
        my_layer.update_layer(duplicate_data)


def test_remove_zones_from_layer():
    # Test data
    initial_data = {"zone1": 10, "zone2": 20, "zone3": 30, "zone4": 40}
    keys_to_remove = ["zone1", "zone3"]  # zone5 doesn't exist in initial_data

    # Create an instance of the class and initialize it with initial_data
    my_layer = Layer(initial_data)

    # Test removing zones with keys_to_remove
    my_layer.remove_zones_from_layer(keys_to_remove)

    # Check if zones have been removed correctly
    assert my_layer.zones == {"zone2": 20, "zone4": 40}

    # Test removing a key that doesn't exist, expect an error
    with pytest.raises(ValueError):
        my_layer.remove_zones_from_layer(["nonexistent_key"])


def test_get_layer_subset_from_function():
    # Test data
    initial_data = {
        "zone1": 10,
        "zone2": 20,
        "zone3": 30,
        "zone4": 40,
        "zone5": 50,
    }

    # Create an instance of the class and initialize it with initial_data
    my_layer = Layer(initial_data)

    # Define a function to select zones with certain properties
    def selection_function(x, y):
        return x >= y

    myfunc = lambda t: selection_function(t, 30)

    # Call get_layer_subset_from_function with the selection_function
    layer_subset = my_layer.get_layer_subset_from_function(myfunc)

    # Check if the layer_subset matches the expected result
    expected_result = {"zone3": 30, "zone4": 40, "zone5": 50}
    assert layer_subset.zones == expected_result


def test_copy():
    #Test data
    data = {
        "zone1": 10, "zone2": 20, "zone3": 30, "zone4": 40, "zone5": 50
    }
    layer = Layer(data)
    layer_copy = layer.copy()
    assert layer == layer_copy


def test_merge_layers():
    # Test data
    layer1_data = {"zone1": 10, "zone2": 20, "zone3": 30}
    layer2_data = {"zone4": 40, "zone5": 50, "zone6": 60}

    # Create instances of YourClass and initialize them with data
    layer1 = Layer(layer1_data)
    layer2 = Layer(layer2_data)

    # Call merge_layers with the two layers
    layer1.merge_layers(layer2)

    # Check if the merged_layer matches the expected result
    expected_result = {
        "zone1": 10,
        "zone2": 20,
        "zone3": 30,
        "zone4": 40,
        "zone5": 50,
        "zone6": 60,
        }
    assert layer1.zones == expected_result

def test_make_weight_dict():
    #Test data
    data = {'zone1' : {'properties' : {'mass' : 10}},
            'zone2' : {'properties' : {'mass' : 20}}
        }

    layer = Layer(data)

    weights = layer.make_weight_dict(prop = 'mass')
    assert weights == {'zone1' : 1/3,
                       'zone2' : 2/3}

    eq_weights = layer.make_weight_dict()
    assert eq_weights == {'zone1' : 1/2,
                          'zone2' : 1/2}

def test_multiplication():
    data = {'zone1' : {'properties' : {'mass' : 10}},
            'zone2' : {'properties' : {'mass' : 20}}
        }
    layer = Layer(data)
    weights = layer.make_weight_dict(prop = 'mass')

    scaled_layer = layer*weights
    result = {'zone1' : {'properties' : {'mass' : 10*1/3}},
            'zone2' : {'properties' : {'mass' : 20*2/3}}
        }

    assert compare_dicts(scaled_layer.zones, result)

def test_make_mixed_layer():
    data = {'zone1' : {'properties' : {'mass' : 10}},
            'zone2' : {'properties' : {'mass' : 20}}
        }
    layer = Layer(data)
    mixture = layer.make_mixed_layer(layer.make_weight_dict(prop='mass'), 'mixture')

    result = {'mixture': {'properties' : {'mass': 10/3 + 40/3}}}

    assert compare_dicts(mixture.zones, result)
