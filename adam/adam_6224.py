
# -*- coding: utf-8 -*-
#
# This file is part of the dev-solaris-adam project
#
#
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.


__all__ = ["ADAM6224", "main"]

# PyTango imports
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device, DeviceMeta
from tango.server import attribute, command
from tango.server import class_property, device_property
from tango import AttrQuality, AttrWriteType, DispLevel, DevState
from functools import partial

# Additional import
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException

class ADAM6224(Device):
    """ ADAM6224
It is a definition of a class used to control ADAM-6224 controller via
Modbus TCP.
Device contains 4-ch Isolated Analog Output and 4-ch Digital Input.
For each AO there are associated attributes:

 * AnalogOutput(double) - contains present output value of the channel (V or
    mA), it is adjustable
 * SafetyValue(double)  - contains present safety value of the channel (V or
    mA), it is adjustable
 * StartupValue(double)  - contains present startup value of the channel (V
    or mA), it is adjustable
 * Status(string)  - contains present status of the channel, available:
    Fail to provide AO Value, No Output Current, Zero/Span Calibration Error,
    DI triggered to Safety Value, DI triggered to Startup Value,
    AO triggered to Fail Safety Value
 * CodeType(string) - contains present type of output of the channel,
    available:  0-20mA, 4-20mA, 0-10V, 0-5V, +-10V, +-5V

For each DI there are associated attributes:

 * DigitalInput(bool) - contains present input value of the channel
 * EventStatus(string) - contains present status of the channel, available:
    Unreliable DI value (UART Timeout), Safety Value triggered,
     Startup Value triggered

"""
    __metaclass__ = DeviceMeta
    connected_ADAM = 0.0
    digital_input_values = [False, False, False, False]
    digital_input_events = [0, 0, 0, 0]
    analog_output_values = [0, 0, 0, 0]
    analog_output_statuses = [0, 0, 0, 0, 0, 0, 0, 0]
    analog_output_types = [0, 0, 0, 0]
    analog_output_startup_values = [0, 0, 0, 0]
    analog_output_safety_values = [0, 0, 0, 0]
    type_to_code_dict = {'0-20mA': int("0182", 16), '4-20mA': int("0180", 16),
                         '0-10V': int("0148", 16), '0-5V': int("0147", 16),
                         '+-10V': int("0143", 16), '+-5V': int("0142", 16)}
    code_to_type_dict = {v: k for k, v in type_to_code_dict.iteritems()}

    event_status_dictionary = {int(1): 'Unreliable DI value (UART Timeout)',
                               int(2): 'Safety Value triggered',
                               int(4): 'Startup Value triggered',
                               int(0):  ' '}

    status_dict_1 = {int(1): 'Fail to provide AO Value',
                     int(8): 'No Output Current',
                     int(512): 'Zero/Span Calibration Error',
                     int(0): ' '}

    status_dict_2 = {int(1): 'DI triggered to Safety Value',
                     int(2): 'DI triggered to Startup Value',
                     int(4): 'AO triggered to Fail Safety Value',
                     int(0): ' '}

    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    DeviceAddress = device_property(
        dtype='str',
        default_value="192.168.120.55",
        doc="An IP address of device"
    )
    
    # ------------------
    # Attributes methods
    # ------------------
    
    # --------------------
    # DigitalInput method
    # --------------------

    def read_DigitalInput(self, channel):
        return self.digital_input_values[channel]

    # --------------------
    # EventStatus method
    # --------------------

    def read_EventStatus(self, channel):
        return self.event_status_dictionary[self.digital_input_events[channel]]

    # --------------------
    # Status method
    # --------------------

    def read_Status(self, channel):
        reg = 2 * channel
        return self.status_dict_1[self.analog_output_statuses[reg]] + \
               ' ' + \
               self.status_dict_2[self.analog_output_statuses[reg + 1]]

    # --------------------
    # AnalogOutput method
    # --------------------

    def read_AnalogOutput(self, channel):
        return self.encode_value(self.analog_output_values[channel], channel)

    def write_AnalogOutput(self, channel, value):
        self.connected_ADAM.write_register(channel, self.decode_value(value,
                                                                  channel, 0))
    # --------------------
    # SafetyValue method
    # --------------------

    def read_SafetyValue(self, channel):
        return self.encode_value(self.analog_output_safety_values[channel],
                                 channel)

    def write_SafetyValue(self, value, channel):
        reg = 410 + channel
        self.connected_ADAM.write_register(reg, self.decode_value(value,
                                                                  channel, 1))
    # --------------------
    # StartupValue method
    # --------------------

    def read_StartupValue(self, channel):
        return self.encode_value(self.analog_output_startup_values[channel],
                                 channel)

    def write_StartupValue(self, value, channel):
        reg = 400 + channel
        self.connected_ADAM.write_register(reg, self.decode_value(value,
                                                                  channel, 2))
    # --------------------
    # TypeCode method
    # --------------------

    def read_TypeCode(self, channel):
        return self.decode_type_code(channel)

    def write_TypeCode(self, value, channel):
        reg = 200 + channel
        self.connected_ADAM.write_register(reg, self.encode_type_code(value))
        
    # ----------
    # Attributes
    # ----------

    DigitalInput_0 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
        doc="Bool value at channel 0 of Digital Input"
    )

    DigitalInput_1 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
        doc="Bool value at channel 1 of Digital Input"
    )

    DigitalInput_2 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
        doc="Bool value at channel 2 of Digital Input"
    )

    DigitalInput_3 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
        doc="Bool value at channel 3 of Digital Input"
    )

    AnalogOutput_0 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Value at channel 0 of Analog Output"
    )

    AnalogOutput_1 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Value at channel 1 of Analog Output"
    )

    AnalogOutput_2 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Value at channel 2 of Analog Output"
    )

    AnalogOutput_3 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Value at channel 3 of Analog Output"
    )

    SafetyValue_0 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Safety Value of channel 0 of Analog Output"
    )

    SafetyValue_1 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Safety Value of channel 1 of Analog Output"
    )

    SafetyValue_2 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Safety Value of channel 2 of Analog Output"
    )

    SafetyValue_3 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Safety Value of channel 3 of Analog Output"
    )

    StartupValue_0 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Startup Value of channel 0 of Analog Output"
    )

    StartupValue_1 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Startup Value of channel 1 of Analog Output"
    )

    StartupValue_2 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Startup Value of channel 2 of Analog Output"
    )

    StartupValue_3 = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        format='%2.4f',
        doc="Startup Value of channel 3 of Analog Output"
    )

    TypeCode_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of output at channel 0 of Analog Output"
    )

    TypeCode_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of output at channel 1 of Analog Output"
    )

    TypeCode_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of output at channel 2 of Analog Output"
    )

    TypeCode_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of output at channel 3 of Analog Output"
    )

    Status_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 0 of Analog Output"
    )

    Status_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 1 of Analog Output"
    )

    Status_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 2 of Analog Output"
    )

    Status_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 3 of Analog Output"
    )

    EventStatus_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Event Status of channel 0 of Digital Input"
    )

    EventStatus_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Event Status of channel 1 of Digital Input"
    )

    EventStatus_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Event Status of channel 2 of Digital Input"
    )

    EventStatus_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Event Status of channel 3 of Digital Input"
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.STANDBY)
        self.set_status("ADAM-6224 in state STANDBY, ready to connect to "
                        "device")

    def delete_device(self):
        self.connected_ADAM.close()

    # --------------------
    # AnalogOutput methods
    # --------------------

    def read_AnalogOutput_0(self):
        return self.read_AnalogOutput(0)

    def write_AnalogOutput_0(self, value):
        return self.write_AnalogOutput(0, value)

    def read_AnalogOutput_1(self):
        return self.read_AnalogOutput(1)

    def write_AnalogOutput_1(self, value):
        return self.write_AnalogOutput(1, value)

    def read_AnalogOutput_2(self):
        return self.read_AnalogOutput(2)

    def write_AnalogOutput_2(self, value):
        return self.write_AnalogOutput(2, value)

    def read_AnalogOutput_3(self):
        return self.read_AnalogOutput(3)

    def write_AnalogOutput_3(self, value):
        return self.write_AnalogOutput(3, value)

    def read_AnalogOutput_4(self):
        return self.read_AnalogOutput(4)

    def write_AnalogOutput_4(self, value):
        return self.write_AnalogOutput(4, value)

    def read_AnalogOutput_5(self):
        return self.read_AnalogOutput(5)

    def write_AnalogOutput_5(self, value):
        return self.write_AnalogOutput(5, value)

    def read_AnalogOutput_6(self):
        return self.read_AnalogOutput(6)

    def write_AnalogOutput_6(self, value):
        return self.write_AnalogOutput(6, value)

    def read_AnalogOutput_7(self):
        return self.read_AnalogOutput(7)

    def write_AnalogOutput_7(self, value):
        return self.write_AnalogOutput(7, value)

    # --------------------
    # SafetyValue methods
    # --------------------

    def read_SafetyValue_0(self):
        return self.read_SafetyValue(0)

    def write_SafetyValue_0(self, value):
        self.write_SafetyValue(0, value)

    def read_SafetyValue_1(self):
        return self.read_SafetyValue(1)

    def write_SafetyValue_1(self, value):
        self.write_SafetyValue(1, value)

    def read_SafetyValue_2(self):
        return self.read_SafetyValue(2)

    def write_SafetyValue_2(self, value):
        self.write_SafetyValue(2, value)

    def read_SafetyValue_3(self):
        return self.read_SafetyValue(3)

    def write_SafetyValue_3(self, value):
        self.write_SafetyValue(3, value)

    def read_SafetyValue_4(self):
        return self.read_SafetyValue(4)

    def write_SafetyValue_4(self, value):
        self.write_SafetyValue(4, value)

    def read_SafetyValue_5(self):
        return self.read_SafetyValue(5)

    def write_SafetyValue_5(self, value):
        self.write_SafetyValue(5, value)

    def read_SafetyValue_6(self):
        return self.read_SafetyValue(6)

    def write_SafetyValue_6(self, value):
        self.write_SafetyValue(6, value)

    def read_SafetyValue_7(self):
        return self.read_SafetyValue(7)

    def write_SafetyValue_7(self, value):
        self.write_SafetyValue(7, value)
    
    # --------------------
    # StartupValue methods
    # --------------------
    
    def read_StartupValue_0(self):
        return self.read_StartupValue(0)

    def write_StartupValue_0(self, value):
        self.write_StartupValue(0, value)

    def read_StartupValue_1(self):
        return self.read_StartupValue(1)

    def write_StartupValue_1(self, value):
        self.write_StartupValue(1, value)

    def read_StartupValue_2(self):
        return self.read_StartupValue(2)

    def write_StartupValue_2(self, value):
        self.write_StartupValue(2, value)

    def read_StartupValue_3(self):
        return self.read_StartupValue(3)

    def write_StartupValue_3(self, value):
        self.write_StartupValue(3, value)

    def read_StartupValue_4(self):
        return self.read_StartupValue(4)

    def write_StartupValue_4(self, value):
        self.write_StartupValue(4, value)

    def read_StartupValue_5(self):
        return self.read_StartupValue(5)

    def write_StartupValue_5(self, value):
        self.write_StartupValue(5, value)

    def read_StartupValue_6(self):
        return self.read_StartupValue(6)

    def write_StartupValue_6(self, value):
        self.write_StartupValue(6, value)

    def read_StartupValue_7(self):
        return self.read_StartupValue(7)

    def write_StartupValue_7(self, value):
        self.write_StartupValue(7, value)

    # --------------------
    # TypeCode methods
    # --------------------

    def read_TypeCode_0(self):
        return self.read_TypeCode(0)

    def write_TypeCode_0(self, value):
        self.write_TypeCode(0, value)

    def read_TypeCode_1(self):
        return self.read_TypeCode(1)

    def write_TypeCode_1(self, value):
        self.write_TypeCode(1, value)

    def read_TypeCode_2(self):
        return self.read_TypeCode(2)

    def write_TypeCode_2(self, value):
        self.write_TypeCode(2, value)

    def read_TypeCode_3(self):
        return self.read_TypeCode(3)

    def write_TypeCode_3(self, value):
        self.write_TypeCode(3, value)

    def read_TypeCode_4(self):
        return self.read_TypeCode(4)

    def write_TypeCode_4(self, value):
        self.write_TypeCode(4, value)

    def read_TypeCode_5(self):
        return self.read_TypeCode(5)

    def write_TypeCode_5(self, value):
        self.write_TypeCode(5, value)

    def read_TypeCode_6(self):
        return self.read_TypeCode(6)

    def write_TypeCode_6(self, value):
        self.write_TypeCode(6, value)

    def read_TypeCode_7(self):
        return self.read_TypeCode(7)

    def write_TypeCode_7(self, value):
        self.write_TypeCode(7, value)
        
    # --------------------
    # DigitalInput methods
    # --------------------

    def read_DigitalInput_0(self):
        return self.read_DigitalInput(0)

    def read_DigitalInput_1(self):
        return self.read_DigitalInput(1)

    def read_DigitalInput_2(self):
        return self.read_DigitalInput(2)

    def read_DigitalInput_3(self):
        return self.read_DigitalInput(3)

    # --------------------
    # EventStatus methods
    # --------------------

    def read_EventStatus_0(self):
        return self.read_EventStatus(0)

    def read_EventStatus_1(self):
        return self.read_EventStatus(1)

    def read_EventStatus_2(self):
        return self.read_EventStatus(2)

    def read_EventStatus_3(self):
        return self.read_EventStatus(3)

    # --------------------
    # EventStatus methods
    # --------------------

    def read_Status_0(self):
        return self.read_Status(0)

    def read_Status_1(self):
        return self.read_Status(1)

    def read_Status_2(self):
        return self.read_Status(2)

    def read_Status_3(self):
        return self.read_Status(3)

    # --------------------
    # Additional methods
    # --------------------

    def decode_value(self, value, channel, type):
        type_code = self.analog_output_types[channel]
        if  ((type_code == int("0182", 16) and not
                (value >= 0 and value <= 0.02)) or
                (type_code == int("0180", 16) and not
                (value >= 0.004 and value <= 0.02)) or
                (type_code == int("0148", 16) and not
                (value >= 0 and value <= 10))   or
                (type_code == int("0147", 16) and not
                (value >= 0 and value <= 5)) or
                (type_code == int("0143", 16) and not
                (value >= -10 and value <= 10)) or
                (type_code == int("0142", 16) and not
                (value >= -5 and value <= 5))):
            if type == 0:
                tmp = self.analog_output_values[channel]
            elif type == 1:
                tmp = self.analog_output_safety_values[channel]
            else:
                tmp = self.analog_output_statup_values[channel]
            self.error_stream('Illegal value')
            raise ValueError
        else:
            if   type_code == int("0182", 16):
                tmp = int(4095 * value / 0.02)
            elif type_code == int("0180", 16):
                tmp = int(4095 * (value - 0.004) / 0.016)
            elif type_code == int("0148", 16):
                tmp = int(4095 * value / 10)
            elif type_code == int("0147", 16):
                tmp = int(4095 * value/ 5 )
            elif type_code == int("0143", 16):
                tmp = int(4095 * (value + 10) / 20)
            elif type_code == int("0142", 16):
                tmp = int(4095 * (value + 5) / 10)
            else:
                if type == 0:      tmp = self.analog_output_values[channel]
                elif type == 1:    tmp = self.analog_output_safety_values[channel]
                else:               tmp = self.analog_output_statup_values[channel]
        return tmp

    def encode_value(self, value, channel):
        type_code = self.analog_output_types[channel]
        if   type_code == int("0182", 16):
            tmp = 0.02  * value/4095.0
        elif type_code == int("0180", 16):
            tmp = (0.016 * value/4095.0) + 0.004
        elif type_code == int("0148", 16):
            tmp = 10    * value/4095.0
        elif type_code == int("0147", 16):
            tmp = 5     * value/4095.0
        elif type_code == int("0143", 16):
            tmp = (20   * value/4095.0) - 10
        elif type_code == int("0142", 16):
            tmp = (10   * value/4095.0) - 5
        else:
            tmp = self.analog_output_values[channel]
        return tmp

    def decode_type_code(self, channel):
        return self.code_to_type_dict[self.analog_output_types[channel]]

    def encode_type_code(self, value="0-20mA"):
        return self.type_to_code_dict[value]

    # --------
    # Commands
    # --------

    @command
    @DebugIt()
    def ConnectWithDevice(self):
        try:
            self.connected_ADAM = ModbusTcpClient(self.DeviceAddress,
                                                  port=int(502))
        except ModbusException as e:
            self.set_state(DevState.FAULT)
            self.set_status("Modbus exception caught while"
                            " connecting to device: \n%s" % e)
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught while connecting to device:"
                            + "\n%s" % e)
        self.set_state(DevState.ON)
        self.set_status("Connected do device with IP: "
                        + str(self.DeviceAddress))

    @command(polling_period=500)
    def read_DataFromDevice(self):
        if self.get_state() == tango.DevState.ON:
            # read Digital Inputs
            tmp = self.connected_ADAM.read_coils(0, 4)
            self.digital_input_values = tmp.bits
            # read Analog Outputs Value
            tmp = self.connected_ADAM.read_holding_registers(0, 4)
            self.analog_output_values = tmp.registers
            # read Analog Outputs Status
            tmp = self.connected_ADAM.read_holding_registers(100, 8)
            self.analog_output_statuses = tmp.registers
            # read Digital Inputs Status
            tmp = self.connected_ADAM.read_holding_registers(110, 4)
            self.digital_input_events = tmp.registers
            # read Type Codes
            tmp = self.connected_ADAM.read_holding_registers(200, 4)
            self.analog_output_types = tmp.registers
            # read Startup Values
            tmp = self.connected_ADAM.read_holding_registers(400, 4)
            self.analog_output_startup_values = tmp.registers
            # read Safety Values
            tmp = self.connected_ADAM.read_holding_registers(410, 4)
            self.analog_output_safety_values = tmp.registers

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    from tango.server import run
    return run((ADAM6224,), args=args, **kwargs)


if __name__ == '__main__':
    main()
