from metamenth.datatypes.address import Address
from metamenth.datatypes.measure import Measure
from metamenth.enumerations import HVACType
from metamenth.enumerations import RecordingType, MeasurementUnit, RoomType, FloorType, BuildingType, AirVolumeType
from metamenth.enumerations import DuctType, DuctSubType, DuctConnectionEntityType, VentilationType, PowerState
from metamenth.enumerations import DamperType
from metamenth.enumerations import SensorMeasure
from metamenth.enumerations import SensorMeasureType
from metamenth.enumerations import ZoneType
from metamenth.enumerations import OpenSpaceType
from metamenth.enumerations import FilterType
from metamenth.enumerations import HeatExchangerType
from metamenth.enumerations import HeatExchangerFlowType
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
from metamenth.subsystem.hvac_components.fan import Fan
from metamenth.subsystem.hvac_components.air_volume_box import AirVolumeBox
from metamenth.subsystem.hvac_components.damper import Damper
from metamenth.transducers.actuator import Actuator
from metamenth.subsystem.hvac_components.controller import Controller
from metamenth.subsystem.hvac_components.filter import Filter
from metamenth.structure.open_space import OpenSpace


class MetamenthModel:
    """
    Refer to the experiment document here
    https://docs.google.com/document/d/1DKp66AMj7PCMVDVlVCib_uWwevcJitAwiD9xCYG1w9E/edit?usp=sharing
    """

    def __init__(self):
        # building address
        address = Address("Montreal", "123 Main St", "Quebec", "H3A 1A1", "Canada")

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
                                                      Measure(MeasurementUnit.KILOGRAMS, 5000))

        self.building = Building(2009, height, floor_area, internal_mass, address,
                                 BuildingType.COMMERCIAL, [floor])

        self.return_air_duct = None
        self.vav_box_1_damper = None

    def task_one(self):
        self.create_building_structure()
        self.add_sensors_to_spaces()
        self.create_hvac_ducts()
        self.add_hvac_components_to_ducts()

    def task_two(self):
        """
        Note: do not modify any of MetamEnTh's classes in this tasks
        Note it whenever you're not able to complete a task (listed below)
        - A (control) relationship between the actuator and the temperature sensor connected to the controller
        - Add the pressure sensor to the kitchen (create a relationship between the two)
        - Add any of the dampers to Office 1
        - Add the Actuator to the Corridor
        Refer to the task's details here:
        https://docs.google.com/document/d/1DKp66AMj7PCMVDVlVCib_uWwevcJitAwiD9xCYG1w9E/edit?usp=sharing
        """
        # Relationship between actuator and sensor. use self.return_air_duct.get_transducer_by_name('ACT') to get actuator
        # Use actuator.controller.get_transducer_by_name('CTRL.SENSOR') to get the temperature sensor
        # Note: When you encounter and error that can't be resolved, comment the code and move on to the next section


        # Create and add pressure sensor to the kitchen
        # Use self.building.get_floor_by_number(1).get_room_by_name('Kitchen') to get the kitchen
        # Run the code after this task note the output comment it out and continue to the next item


        # Add self.vav_box_1_damper to office one
        # Use self.building.get_floor_by_number(1).get_room_by_name('Office 1') to get Office 1
        # Use .add_hvac_component method to add the VAV BOX
        # Note the error, comment the code and move on to the next item


        # Add the actuator to the corridor
        # Use self.building.get_floor_by_number(1).get_open_space_by_name('Corridor') to get the corridor
        # Use .add_transducer() to add the actuator to the corridor

    def create_building_structure(self):
        """
        provide your code after each set of comments
        """
        # create Office 2 and add it to the floor.
        # Use self.building.get_floor_by_number(1).add_rooms([office_two]) to add office two

        # create the Corridor and add it to the floor. Use the OpenSpace class
        # Use self.building.get_floor_by_number(1).add_open_spaces([corridor]) to add the corridor to the floor

        # create the Kitchen and add it to the floor

        # create the zones and assigned them to their respective spaces
        hvac_zone_1 = Zone("HVAC Zone 1", ZoneType.HVAC, HVACType.INTERIOR)
        hvac_zone_2 = Zone("HVAC Zone 1", ZoneType.HVAC, HVACType.INTERIOR)
        # set hvac_zone_2 as adjacent to hvac_zone_1
        hvac_zone_2.add_adjacent_zones([hvac_zone_1])
        # e.g., the code below adds Office 1 to HVAC Zone 1
        self.building.get_floor_by_number(1).get_room_by_name('Office 1').add_zone(hvac_zone_2, self.building)
        # add the rest of the spaces to their respective zones

    def add_sensors_to_spaces(self):
        """
        Create and add sensors to Office 1 & 2, and the Kitchen
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

        # Create and add CO2, humidity and temperature sensors to Office 2. Note, sensor names should be unique

        # Create and add sensors to the kitchen

    def create_hvac_ducts(self):
        """
        Create the various ducts and their connections.
        Follow the comments to insert your code
        """
        # create the supply air duct
        supply_air_duct = Duct("SUPPLY.AIR.DUCT", DuctType.AIR)
        supply_air_duct.duct_sub_type = DuctSubType.FRESH_AIR

        # create the return air duct
        self.return_air_duct = Duct("RETURN.AIR.DUCT", DuctType.AIR)
        self.return_air_duct.duct_sub_type = DuctSubType.RETURN_AIR

        # connect the supply air that to the rooms with the spaces as the destination
        sup_air_space_conn = DuctConnection()

        # add Office 1 as a destination of supply air duct
        sup_air_space_conn.add_entity(DuctConnectionEntityType.DESTINATION,
                                      self.building.get_floor_by_number(1).get_room_by_name('Office 1'))

        # add Office 2 as a destination of supply air duct

        # add Kitchen as destination of supply air duct

        # add Corridor as destination of supply air duct.
        # Note: Use self.building.get_floor_by_number(1).get_open_space_by_name('Corridor') to retrieve the corridor

        # connect the supply air duct to the connection object
        supply_air_duct.connections = sup_air_space_conn

        # create another connection object to connect Office 2 (as source) to the return air duct

        # add office 2 as the source to the connection object

        # connect the return air duct to the connection object

        # create the recirculation (fresh) air duct with name: RECIRCULATION.AIR.DUCT

        # create a duct connection object for the recirculation air duct

        # add (duct.connections.add_entity) the return air duct as the source to the connection object

        # add the fresh air duct as the destination to the connection object

        # connect the recirculation air duct to the connection object

        # add the recirculation air duct as the source of the supply air duct

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
        control_system = self.building.control_systems[0]
        ventilation_system = control_system.hvac_system.ventilation_systems[0]
        # supply air duct
        supply_air_duct = ventilation_system.principal_duct

        # recirculation air duct
        # Note, this will fail if you don't create the recirculation air duct and assign it as a source entity
        # for the supply air duct in create_hvac_ducts()
        recirculation_air_duct = supply_air_duct.connections.get_source_entities({'name': 'RECIRCULATION.AIR.DUCT'})[0]


        # add fan to the supply air duct
        supp_air_duct_fan = Fan("SUPP.AIR.DUCT.FAN", PowerState.ON, None)
        supply_air_duct.add_fan(supp_air_duct_fan)

        # create and add filter to the supply air duct (use the Filter class)

        # add one heat exchanger to the supply air duct (use the HeatExchanger class)

        # add one temperature sensor to the supply air duct

        # add one pressure sensor to the supply air duct


        # add VAV Box 1 with a damper and temperature sensor to supply air duct
        vav_box_1 = AirVolumeBox('VAV.BOX.1', AirVolumeType.VARIABLE_AIR_VOLUME)
        vav_box_1.has_cooling_capability = True
        vav_box_1.has_heating_capability = True
        # create damper and add it to the vav box
        self.vav_box_1_damper = Damper("VAV.BOX.1.DAMPER", DamperType.BACK_DRAFT)
        vav_box_1.inlet_dampers = [self.vav_box_1_damper]
        # create temperature sensor and add it to the VAV box
        vav_box_1_temp_sensor = Sensor("VAV.BOX.1.TEMP.SENSOR", SensorMeasure.TEMPERATURE,
                                       MeasurementUnit.DEGREE_CELSIUS, SensorMeasureType.THERMO_COUPLE_TYPE_B,
                                       90)
        vav_box_1.add_transducer(vav_box_1_temp_sensor)
        supply_air_duct.add_connected_air_volume_box(vav_box_1)

        # indicate that vav box one supplies Office 1 & 2 and the Corridor
        building_floor = self.building.get_floor_by_number(1)
        vav_box_1.add_spaces([building_floor.get_room_by_name('Office 1'),
                              building_floor.get_room_by_name('Office 2'),
                              building_floor.get_room_by_name('Corridor')])

        # add VAV Box 2 with damper and temperature sensor to the supply air duct

        # indicate that vav box two supplies the Kitchen

        # create and add fan to the return air duct

        # create the actuator (use the Actuator class) and associate the actuator with the fan in the return air duct fan
        # (use the trigger_out property of actuator)

        # add the actuator to the return air duct

        # create a controller (use the Controller class)

        # associate the controller with the controller (use the controller property of the actuator)

        # associate the actuator with the controller (user the add_transducer method of the controller)

        # create a temperature sensor and associate it with the controller (use add_transducer method)


if __name__ == "__main__":
    model = MetamenthModel()
    model.task_one()
    # This should print the ventilation system
    print(model.building.control_systems[0].hvac_system.ventilation_systems[0])
    model.task_two()
