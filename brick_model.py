import brickschema
from brickschema.namespaces import A, BRICK, UNIT
from rdflib import Namespace, Literal, XSD


class BrickModel:
    """
        Refer to the experiment document here
        https://docs.google.com/document/d/1DKp66AMj7PCMVDVlVCib_uWwevcJitAwiD9xCYG1w9E/edit?usp=sharing
    """
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
        self.ahu = None
        self.hvac_zone_2 = None
        self.hvac_zone_1 = None

    def task_one(self):
        self.create_building_structure()
        self.add_sensors_to_spaces()
        self.create_hvac_ducts()
        self.add_hvac_components_to_ducts()

    def task_two(self):
        """
            Note it whenever you're not able to complete a task (listed below)
            - A (control) relationship between the actuator and the temperature sensor connected to the controller
            - Add the pressure sensor to the kitchen (create a relationship between the two)
            - Add any of the dampers to Office 1
            - Add the Actuator to the Corridor
            Refer to the task's details here:
            https://docs.google.com/document/d/1DKp66AMj7PCMVDVlVCib_uWwevcJitAwiD9xCYG1w9E/edit?usp=sharing
        """
        # Your code below

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
        self.hvac_zone_1 = self.bldg["HVAC_Zone_1"]
        self.hvac_zone_2 = self.bldg["HVAC_Zone_2"]

        self.graph.add((self.hvac_zone_1, A, BRICK.HVAC_Zone))
        self.graph.add((self.hvac_zone_1, BRICK.hasName, Literal("HVAC Zone 1", datatype=XSD.string)))
        self.graph.add((self.hvac_zone_2, A, BRICK.HVAC_Zone))
        self.graph.add((self.hvac_zone_2, BRICK.hasName, Literal("HVAC Zone 2", datatype=XSD.string)))

        # Make HVAC Zone 2 adjacent to HVAC Zone 1
        self.graph.add((self.hvac_zone_2, BRICK.adjacentTo, self.hvac_zone_1))

        # Add zones to the building
        self.graph.add((self.building, BRICK.hasPart, self.hvac_zone_1))
        self.graph.add((self.building, BRICK.hasPart, self.hvac_zone_2))

        # add office 1 to HVAC Zone 2
        self.graph.add((self.hvac_zone_2, BRICK.hasPart, self.office_one))

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
        """
        Use tha Air_Handling_Unit in Bricks.
        Currently, there is no support for ventilation ducts.
        The three connected ducts can be modelled as an air handling unit
        """
        # Add an air handling unit (AHU)
        self.ahu = self.bldg["AHU"]
        self.graph.add((self.ahu, A, BRICK.Air_Handling_Unit))
        self.graph.add((self.building, BRICK.hasPart, self.ahu))

    def add_hvac_components_to_ducts(self):
        # create a heat exchanger and add it to the AHU
        heat_exchanger_1 = self.bldg["Heat_Exchanger_1"]
        self.graph.add((heat_exchanger_1, A, BRICK.Heat_Exchanger))
        self.graph.add((self.ahu, BRICK.hasPart, heat_exchanger_1))

        # create the second heat exchanger and add it to the AHU

        # create the supply air fan and add it to the AHU
        supply_air_fan = self.bldg["Supply_Air_Fan"]
        self.graph.add((supply_air_fan, A, BRICK.Supply_Fan))
        self.graph.add((self.ahu, BRICK.hasPart, supply_air_fan))

        # create the return air fan and add it to the AHU

        # create VAV Box 1 with damper and temperature sensor and add it to the AHU
        vav_box_1 = self.bldg["VAV_Box_1"]
        self.graph.add((vav_box_1, A, BRICK.Variable_Air_Volume_Box_With_Reheat))
        # create damper for VAV Box 1
        vav_box_1_damper = self.bldg["VAV_Box_1_DAMPER"]
        self.graph.add((vav_box_1_damper, A, BRICK.Damper))
        self.graph.add((vav_box_1, BRICK.hasPart, vav_box_1_damper))
        # create temperature sensor for VAV Box 1
        vav_box_1_temp_sensor = self.bldg["VAV_BOX_1_Temperature_Sensor"]
        self.graph.add((vav_box_1_temp_sensor, A, BRICK.Temperature_Sensor))
        self.graph.add((vav_box_1, BRICK.hasPoint, vav_box_1_temp_sensor))
        # indicate the zone fed by vav box 1
        self.graph.add((self.hvac_zone_2, BRICK.isFedBy, vav_box_1))
        self.graph.add((self.ahu, BRICK.hasPart, vav_box_1))

        # create VAV Box 2 with damper and temperature sensor and add it to the AHU

        # add one temperature sensor to the AHU

        # add one pressure sensor to the AHU

        # add filter to the AHU (use BRICK.Filter)

        # add one damper to the AHU

        # Add the actuator in the return air duct (AHU)
        actuator = self.bldg["Actuator"]
        self.graph.add((actuator, A, BRICK.Point))  # There is no Actuator class in Brick
        self.graph.add((actuator, BRICK.hasTag, BRICK.Actuator))

        # create the controller in the return air duct (AHU)
        controller = self.bldg["Controller"]
        self.graph.add((controller, A, BRICK.Controller))

        # establish relationship between actuator and controller
        self.graph.add((controller, BRICK.hasPoint, actuator))
        # indicate the actuator controls (BRICK.controls) the return air fan
        # (the fan should be been created above)

        # create the temperature sensor and associate it with controller

        # add the controller and actuator to the return air duct (AHU)


if __name__ == "__main__":
    model = BrickModel()
    model.task_one()
    model.task_two()
    model.graph.serialize(destination="building_model.ttl", format="turtle")
