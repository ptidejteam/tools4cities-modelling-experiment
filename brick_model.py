import brickschema
from brickschema.namespaces import A, BRICK, UNIT
from rdflib import Namespace, Literal, XSD


class BrickModel:

    def __init__(self):
        # create the building
        self.bldg = Namespace("https://www.ptidej.net:experimental-building#")
        self.qudt = Namespace("http://qudt.org/schema/qudt/")
        self.qudt_unit = Namespace("http://qudt.org/vocab/unit/")
        # create a graph model to store the model
        self.graph = brickschema.Graph()
        self.graph.bind("bldg", self.bldg)
        self.graph.bind("qudt", self.qudt)
        self.graph.bind("qudt_unit", self.qudt_unit)

        self.building = self.bldg["Experimental_Building"]
        address = self.bldg["Address"]

        # Add the building and address to the graph
        self.graph.add((self.building, A, BRICK.Building))
        self.graph.add((self.building, BRICK.hasAddress, address))
        self.graph.add((address, A, BRICK.Address))
        self.graph.add((address, BRICK.streetAddress, Literal("123 Main St")))
        self.graph.add((address, BRICK.city, Literal("Montreal")))
        self.graph.add((address, BRICK.state, Literal("Quebec")))
        self.graph.add((address, BRICK.postalCode, Literal("H3A 1A1")))
        self.graph.add((address, BRICK.country, Literal("Canada")))

        internal_mass = self.bldg["Internal_Mass"]
        self.graph.add((internal_mass, A.type, self.qudt.Quantity))
        self.graph.add((internal_mass, self.qudt.unit, self.qudt_unit.Kilogram))
        self.graph.add((internal_mass, self.qudt.numericValue, Literal(50000, datatype=XSD.decimal)))
        self.graph.add((self.building, self.bldg.hasInternalMass, internal_mass))

        # Define the height of the building
        height = self.bldg["Height"]
        self.graph.add((height, A.type, self.qudt.QuantityValue))
        self.graph.add((height, self.qudt.unit, self.qudt_unit.Meter))
        self.graph.add((height, self.qudt.numericValue, Literal(50, datatype=XSD.decimal)))
        self.graph.add((self.building, self.bldg.hasHeight, height))

        # Define the floor area of the building
        floor_area = self.bldg["FloorArea"]
        self.graph.add((floor_area, A.type, BRICK.Area))
        self.graph.add((floor_area, self.qudt.unit, self.qudt_unit.SquareMeter))
        self.graph.add((floor_area, self.qudt.numericValue, Literal(6000, datatype=XSD.decimal)))
        self.graph.add((self.building, BRICK.hasArea, floor_area))

        self.office_one = None
        self.kitchen = None
        self.office_two = None
        self.corridor = None

    def task_one(self):
        pass

    def task_two(self):
        pass

    def create_building_structure(self):
        # Define the floor of the building
        floor = self.bldg["Floor"]
        self.graph.add((floor, A.type, BRICK.Floor))
        self.graph.add((floor, BRICK.hasName, Literal("First Floor", datatype=XSD.string)))
        self.graph.add((self.building, BRICK.hasPart, floor))

        # create Office 1 and add it to the floor
        self.office_one = self.bldg["Office1"]
        self.graph.add((self.office_one, A.type, BRICK.Room))
        self.graph.add((self.office_one, BRICK.hasName, Literal("Office 1", datatype=XSD.string)))
        self.graph.add((self.office_one, BRICK.hasTag, Literal("office", datatype=XSD.string)))
        self.graph.add((floor, BRICK.hasPart, self.office_one))

        # Create Office 2 and add it to the floor

        # create the Kitchen and assign it to the floor

        # Create the corridor and assign it to the floor (use BRICK.Room to create corridor)

        # Define HVAC zones
        hvac_zone_1 = self.bldg["HVAC_Zone_1"]
        hvac_zone_2 = self.bldg["HVAC_Zone_2"]

        self.graph.add((hvac_zone_1, A, BRICK.HVAC_Zone))
        self.graph.add((hvac_zone_1, BRICK.hasName, Literal("HVAC Zone 1", datatype=XSD.string)))
        self.graph.add((hvac_zone_2, A, BRICK.HVAC_Zone))
        self.graph.add((hvac_zone_2, BRICK.hasName, Literal("HVAC Zone 2", datatype=XSD.string)))

        # Add zones to the building
        self.graph.add((self.building, BRICK.hasPart, hvac_zone_1))
        self.graph.add((self.building, BRICK.hasPart, hvac_zone_2))

        # add office 1 to HVAC Zone 2
        self.graph.add((hvac_zone_2, BRICK.hasPart, self.office_one))

        # add office 2 and the corridor to HVAC Zone 2

        # add the kitchen to HVAC Zone 1

    def add_sensors_to_spaces(self):
        """
        Create and add sensors to Office 1 & 2, the Kitchen and the Corridor
        """
        # Add CO2, humidity and temperature sensors to Office 1
        office_one_co2_sensor = self.bldg["Office_One_CO2_Sensor"]
        office_one_humidity_sensor = self.bldg["Office_One_Humidity_Sensor"]
        office_one_temperature_sensor = self.bldg["Office_One_Temperature_Sensor"]

        self.graph.add((office_one_co2_sensor, A, BRICK.CO2_Sensor))
        self.graph.add((office_one_humidity_sensor, A, BRICK.Humidity_Sensor))
        self.graph.add((office_one_temperature_sensor, A, BRICK.Temperature_Sensor))

        self.graph.add((self.office_one, BRICK.hasPoint, office_one_co2_sensor))
        self.graph.add((self.office_one, BRICK.hasPoint, office_one_humidity_sensor))
        self.graph.add((self.office_one, BRICK.hasPoint, office_one_temperature_sensor))

        # Add CO2, humidity and temperature sensors to Office 2

        # Add CO2, CO (BRICK.CO_Sensor), humidity and temperature sensors to the Kitchen

    def create_hvac_ducts(self):
        pass

    def add_hvac_components_to_ducts(self):
        pass

