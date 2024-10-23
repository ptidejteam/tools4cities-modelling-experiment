from metamenth.datatypes.address import Address
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import HVACType
from metamenth.enumerations import (RecordingType, MeasurementUnit, RoomType, FloorType, BuildingType,
                                    DuctType, DuctSubType, DuctConnectionEntityType, VentilationType)
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorMeasureType
from metamenth.enumerations import ZoneType
from metamenth.misc import MeasureFactory
from metamenth.structure.building import Building
from metamenth.structure.floor import Floor
from metamenth.structure.room import Room
from metamenth.subsystem.hvac_components.duct import Duct
from metamenth.transducers.sensor import Sensor
from metamenth.virtual.zone import Zone
from metamenth.subsystem.hvac_components.duct_connection import DuctConnection
from metamenth.subsystem.ventilation_system import VentilationSystem
from metamenth.subsystem.hvac_system import HVACSystem
from metamenth.subsystem.building_control_system import BuildingControlSystem


class MetamenthModel:
    """
    Refer to the experiment document here https://docs.google.com/document/d/1DKp66AMj7PCMVDVlVCib_uWwevcJitAwiD9xCYG1w9E/edit?usp=sharing

    """

    def __init__(self):
        # building address
        address = Address("Montreal", "6399 Rue Sherbrooke", "QC", "H1N 2Z3", "Canada")

        # create office one
        area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                             Measure(MeasurementUnit.SQUARE_METERS, 45))
        office_one = Room(area, "Office 1", RoomType.OFFICE)

        # create a floor to host the various spaces (Office 1, Office 2, Kitchen and Corridor)
        # add Office 1 to the floor
        floor = Floor(area=area, number=1, floor_type=FloorType.REGULAR, rooms=[office_one])

        # create the building and add the floor to it
        floor_area = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                   Measure(MeasurementUnit.SQUARE_METERS, 5))
        height = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                               Measure(MeasurementUnit.METERS, 30))
        internal_mass = MeasureFactory.create_measure(RecordingType.BINARY.value,
                                                      Measure(MeasurementUnit.KILOGRAMS, 2000))

        self.building = Building(2009, height, floor_area, internal_mass, address,
                                 BuildingType.COMMERCIAL, [floor])

    def task_one(self):
        self.create_building_structure()
        self.add_sensors_to_spaces()
        self.create_hvac_ducts()
        self.add_hvac_components_to_ducts()

    def task_two(self):
        pass

    def create_building_structure(self):
        """
        provide your code after each set of comments
        """
        # create Office 2 and add it to the floor.
        # Use building.get_floor_by_number(1).add_rooms([office_two]) to add office two

        # create the Corridor and add it to the floor. Use the OpenSpace class
        # Use .add_open_spaces([corridor]) to add the corridor to the floor

        # create the Kitchen and add it to the floor

        # create the zones and assigned them to their respective spaces
        hvac_zone_1 = Zone("HVAC Zone 1", ZoneType.HVAC, HVACType.INTERIOR)
        hvac_zone_2 = Zone("HVAC Zone 1", ZoneType.HVAC, HVACType.INTERIOR)
        # e.g., the code below adds Office 1 to HVAC Zone 1
        self.building.get_floor_by_number(1).get_room_by_name('Office 1').add_zone(hvac_zone_1, self.building)

    def add_sensors_to_spaces(self):
        """
        Create and add sensors to Office 1 & 2, the Kitchen and the Corridor
        """
        # Create and assign sensors to the rooms
        office_one_co2_sensor = Sensor("CO2.SENSOR.OFFICE.1", SensorMeasure.CARBON_DIOXIDE,
                                       MeasurementUnit.PARTS_PER_MILLION, SensorMeasureType.THERMO_COUPLE_TYPE_B, 70)
        office_one_humidity_sensor = Sensor("HUMIDITY.SENSOR.OFFICE.1", SensorMeasure.HUMIDITY,
                                            MeasurementUnit.RELATIVE_HUMIDITY, SensorMeasureType.THERMO_COUPLE_TYPE_B,
                                            90)
        office_one_temp_sensor = Sensor("TEMPERATURE.SENSOR.OFFICE.1", SensorMeasure.TEMPERATURE,
                                        MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.THERMO_COUPLE_TYPE_B,
                                        90)

        # E.g., assign the Co2 temperature to Office 1
        self.building.get_floor_by_number(1).get_room_by_name('Office 1').add_transducer(office_one_co2_sensor)

        # Add the remaining sensors to Office 1

        # Create and add sensors to Office 2

        # Create and add sensors to the Corridor

    def create_hvac_ducts(self):
        """
        Create the various ducts and their connections.
        Follow the comments to insert your code
        """
        # create the supply air duct
        supply_air_duct = Duct("SUPPLY.AIR.DUCT", DuctType.AIR)
        supply_air_duct.duct_sub_type = DuctSubType.FRESH_AIR

        # create the return air duct
        return_air_duct = Duct("RETURN.AIR.DUCT", DuctType.AIR)
        return_air_duct.duct_sub_type = DuctSubType.RETURN_AIR

        # connect the supply air that to the rooms with the spaces as the destination
        sup_air_space_conn = DuctConnection()

        # add Office 1 as a destination
        sup_air_space_conn.add_entity(DuctConnectionEntityType.DESTINATION,
                                      self.building.get_floor_by_number(1).get_room_by_name('Office 1'))

        # add Office 2 as a destination

        # add Kitchen as destination

        # add Corridor as destination

        # connect the supply air duct to the connection object
        supply_air_duct.connections = sup_air_space_conn

        # create another connection object to connect Office 2 (as source) to the return air duct

        # add office 2 as the source to the connection object

        # connect the return air duct to the connection object

        # create the recirculation (fresh) air duct

        # create a duct connection object for (duct.connections) the recirculation air duct

        # add (duct.connections.add_entity) the return air duct as the source to the connection object

        # add the fresh air duct as the destination to the connection object

        # Create HVAC System with the vents and add it to the building
        ventilation_system = VentilationSystem(VentilationType.AIR_HANDLING_UNIT, supply_air_duct)
        hvac_system = HVACSystem()
        hvac_system.add_ventilation_system(ventilation_system)
        control_system = BuildingControlSystem("Ex BLD Control System")
        control_system.hvac_system = hvac_system
        self.building.add_control_system(control_system)

    def add_hvac_components_to_ducts(self):
        """
        Add the various components, e.g., fan to their respective ducts
        """
        pass
