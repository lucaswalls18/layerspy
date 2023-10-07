import pytest
import io, requests
import wnutils.xml as wx
from layer_mix import make_id, Layer, mix


def mock_zone_data(mock_mass_frac):
    # Create a mock zone_data dictionary for testing
    zone = {}
    for i in range(len(mock_mass_frac)):
        mass_frac = {('si28',14,28): mock_mass_frac[i]}
        zone[str(i)] = {'properties' : {'t9': 10}, 'mass fractions' : mass_frac}
    return zone 
    
def mock_xml():
    return wx.Xml(io.BytesIO(requests.get('https://osf.io/gf8x5/download').content))

def mock_fun(x,frac):
    # Define a mock selection function for testing
    return x>frac

def test_make_id():
    # Test the make_id function
    species = "si28"
    xml = mock_xml()
    expected_result = ("si28", 14, 28)
    result = make_id(species, xml)
    assert result == expected_result


def test_create_layer():
    # Test the create_layer method of the Layers class
    layers = Layer()
    xml = mock_xml()
    test_species = "si28"
    mass_fracs = [0.6,0.5,0.7]
    # Call create_layer and assert the correctness of the result
    expected_result = {"0" : {'properties' : {'t9':10},
                              'mass fractions': {('si28',14,28) : 0.6}},
                       "2" : {'properties' : {'t9':10},
                              'mass fractions': {('si28',14,28) : 0.7}}
                       }
    func = lambda t: mock_fun(t,.5)
    layers.create_layer(mock_zone_data(mass_fracs), func, test_species, xml)
    assert layers.zones == expected_result

def mock_layer1():
    # Create a mock layer1 dictionary for testing
    layers = Layer()
    test_species = "si28"
    mass_fracs = [0.6,0.5,0.7]
    func = lambda t: mock_fun(t,.5)
    xml = mock_xml()
    layers.create_layer(mock_zone_data(mass_fracs), func, test_species, xml)
    return layers


def mock_layer2():
    # Create a mock layer2 dictionary for testing
    layers = Layer()
    test_species = "si28"
    mass_fracs = [0.6,0.5,0.7]
    func = lambda t: mock_fun(t,.6)
    xml = mock_xml()
    layers.create_layer(mock_zone_data(mass_fracs), func, test_species, xml)
    return layers

def test_update_layer():
    layer = Layer()
    expected_result = {"0" : {'properties' : {'t9':10},
                              'mass fractions': {('si28',14,28) : 0.4}}
                       }
    mass_frac = [0.4]
    layer.update_layer(mock_zone_data(mass_frac))
    assert layer.zones == expected_result

def test_make_average_layer():
    layer = mock_layer1()
    avg = (0.6 + 0.7)/2
    result = layer.make_average_layer()
    expected_result = {"0" : {'mass fractions': {('si28',14,28) : avg}}}
    assert result.zones == expected_result
    

#def test_mix(mock_layer1, mock_layer2):
    # Test the mix function
    # Call the mix function and assert the correctness of the result
#    expected_result = # Define the expected result
#    result = mix(mock_layer1, mock_layer2, 0.1)
#    assert result == expected_result
