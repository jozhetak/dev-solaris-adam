
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
# Additional import
# PROTECTED REGION ID(ADAM6224.additional_import) ENABLED START #
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException

#mport time
# PROTECTED REGION END #    //  ADAM6224.additional_import


class ADAM6224(Device):
    """ ADAM6224
It is a definition of a class used to control ADAM-6224 controller via Modbus TCP.
Device contains 4-ch Isolated Analog Output and 4-ch Digital Input.
For each AO there are associated attributes:
 - AnalogOutput(double) - contains present output value of the channel (V or mA), it is adjustable
 - SafetyValue(double)  - contains present safety value of the channel (V or mA), it is adjustable
 - StartupValue(double)  - contains present startup value of the channel (V or mA), it is adjustable
 - Status(string)  - contains present status of the channel, available:
  Fail to provide AO Value, No Output Current, Zero/Span Calibration Error, DI triggered to Safety Value,
  DI triggered to Startup Value, AO triggered to Fail Safety Value
 - CodeType(string) - contains present type of output of the channel, available:  0-20mA, 4-20mA, 0-10V, 0-5V, +-10V, +-5V
For each DI there are associated attributes:
 - DigitalInput(bool) - contains present input value of the channel
 - EventStatus(string) - contains present status of the channel, available:
    Unreliable DI value (UART Timeout), Safety Value triggered, Startup Value triggered

"""
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(ADAM6224.class_variable) ENABLED START #
    connected_ADAM = 0.0
    digital_input_values = [False, False, False, False]
    digital_input_events =  [0, 0, 0, 0]
    analog_output_values = [0, 0, 0, 0]
    analog_output_statuses = [0, 0, 0, 0, 0, 0, 0, 0]
    analog_output_types = [0, 0, 0, 0]
    analog_output_startup_values = [0, 0, 0, 0]
    analog_output_safety_values = [0, 0, 0, 0]
    type_code_dictionary = {'0-20mA': int("0182", 16), '4-20mA': int("0180", 16), '0-10V': int("0148", 16),
                            '0-5V': int("0147", 16), '+-10V': int("0143", 16), '+-5V': int("0142", 16)}
    type_code_dictionary.update({v: k for k, v in type_code_dictionary.iteritems()})

    event_status_dictionary = {'Unreliable DI value (UART Timeout)': int(1), 'Safety Value triggered': int(2),
                            'Startup Value triggered': int(4), ' ': int(0)}
    event_status_dictionary.update({v: k for k, v in event_status_dictionary.iteritems()})

    status_dict_1 = {'Fail to provide AO Value': int(1), 'No Output Current': int(8),
                     'Zero/Span Calibration Error': int(512), ' ': int(0)}
    status_dict_1.update({v: k for k, v in status_dict_1.iteritems()})

    status_dict_2 = {'DI triggered to Safety Value': int(1),'DI triggered to Startup Value': int(2),
                     'AO triggered to Fail Safety Value': int(4), ' ': int(0)}
    status_dict_2.update({v: k for k, v in status_dict_2.iteritems()})

    # PROTECTED REGION END #    //  ADAM6224.class_variable
    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    DeviceAddress = device_property(
        dtype='str',
        default_value="192.168.120.55",
        doc="This property contains an IP address of device"
    )

    # ----------
    # Attributes
    # ----------

    DigitalInput_0 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
    )

    DigitalInput_1 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
    )

    DigitalInput_2 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
    )

    DigitalInput_3 = attribute(
        dtype='bool',
        access=AttrWriteType.READ,
    )

    AnalogOutput_0 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    AnalogOutput_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    AnalogOutput_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    AnalogOutput_3 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    SafetyValue_0 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    SafetyValue_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    SafetyValue_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    SafetyValue_3 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )
    
    StartupValue_0 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    StartupValue_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    StartupValue_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    StartupValue_3 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
        format='%2.4f'
    )

    TypeCode_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
    )

    TypeCode_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
    )

    TypeCode_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
    )

    TypeCode_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
    )

    Status_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    Status_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    Status_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    Status_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    EventStatus_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    EventStatus_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    EventStatus_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    EventStatus_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(ADAM6224.init_device) ENABLED START #
        self.set_state(DevState.ON)
        self.set_status("ADAM-6224 enabled")
        # PROTECTED REGION END #    //  ADAM6224.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(ADAM6224.always_executed_hook) ENABLED START #
        # if not self.connected_ADAM.connect():
        #     self.set_state(DevState.ALARM)
        #     self.set_status("Connection  error")
        pass
        # PROTECTED REGION END #    //  ADAM6224.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(ADAM6224.delete_device) ENABLED START #
        self.connected_ADAM.close()
        # PROTECTED REGION END #    //  ADAM6224.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    # --------------------
    # DigitalInput methods
    # --------------------

    def read_DigitalInput_0(self):
        # PROTECTED REGION ID(ADAM6224.DigitalInput_0_read) ENABLED START #
        tmp = self.connected_ADAM.read_coils(0, 4)
        self.digital_input_values = tmp.bits
        return self.digital_input_values[0]
        # PROTECTED REGION END #    //  ADAM6224.DigitalInput_0_read

    def read_DigitalInput_1(self):
        # PROTECTED REGION ID(ADAM6224.DigitalInput_1_read) ENABLED START #
        return self.digital_input_values[1]
        # PROTECTED REGION END #    //  ADAM6224.DigitalInput_1_read

    def read_DigitalInput_2(self):
        # PROTECTED REGION ID(ADAM6224.DigitalInput_2_read) ENABLED START #
        return self.digital_input_values[2]
        # PROTECTED REGION END #    //  ADAM6224.DigitalInput_2_read

    def read_DigitalInput_3(self):
        # PROTECTED REGION ID(ADAM6224.DigitalInput_3_read) ENABLED START #
        return self.digital_input_values[3]
        # PROTECTED REGION END #    //  ADAM6224.DigitalInput_3_read

    # --------------------
    # EventStatus methods
    # --------------------

    def read_EventStatus_0(self):
        # PROTECTED REGION ID(ADAM6224.EventStatus_0_read) ENABLED START #
        tmp = self.connected_ADAM.read_holding_registers(110, 4)
        self.digital_input_events = tmp.registers
        return  self.event_status_dictionary[self.digital_input_events[0]]
        # PROTECTED REGION END #    //  ADAM6224.EventStatus_0_read

    def read_EventStatus_1(self):
        # PROTECTED REGION ID(ADAM6224.EventStatus_1_read) ENABLED START #
        return self.event_status_dictionary[self.digital_input_events[1]]
        # PROTECTED REGION END #    //  ADAM6224.EventStatus_1_read

    def read_EventStatus_2(self):
        # PROTECTED REGION ID(ADAM6224.EventStatus_2_read) ENABLED START #
        return self.event_status_dictionary[self.digital_input_events[2]]
        # PROTECTED REGION END #    //  ADAM6224.EventStatus_2_read

    def read_EventStatus_3(self):
        # PROTECTED REGION ID(ADAM6224.EventStatus_3_read) ENABLED START #
        return self.event_status_dictionary[self.digital_input_events[3]]
        # PROTECTED REGION END #    //  ADAM6224.EventStatus_3_read

    # --------------------
    # Status methods
    # --------------------

    def read_Status_0(self):
        # PROTECTED REGION ID(ADAM6224.Status_0_read) ENABLED START #
        tmp = self.connected_ADAM.read_holding_registers(100, 8)
        self.analog_output_statuses = tmp.registers
        print(self.analog_output_statuses)
        return self.status_dict_1[self.analog_output_statuses[0]] + ' ' + self.status_dict_2[self.analog_output_statuses[1]]
        # PROTECTED REGION END #    //  ADAM6224.Status_0_read

    def read_Status_1(self):
        # PROTECTED REGION ID(ADAM6224.Status_1_read) ENABLED START #
        return self.status_dict_1[self.analog_output_statuses[2]] + ' ' + self.status_dict_2[self.analog_output_statuses[3]]
        # PROTECTED REGION END #    //  ADAM6224.Status_1_read

    def read_Status_2(self):
        # PROTECTED REGION ID(ADAM6224.Status_2_read) ENABLED START #
        return self.status_dict_1[self.analog_output_statuses[4]] + ' ' + self.status_dict_2[self.analog_output_statuses[5]]
        # PROTECTED REGION END #    //  ADAM6224.Status_2_read

    def read_Status_3(self):
        # PROTECTED REGION ID(ADAM6224.Status_3_read) ENABLED START #
        return self.status_dict_1[self.analog_output_statuses[6]] + ' ' + self.status_dict_2[self.analog_output_statuses[7]]
        # PROTECTED REGION END #    //  ADAM6224.Status_3_read

    # --------------------
    # AnalogOutput methods
    # --------------------

    def read_AnalogOutput_0(self):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_0_read) ENABLED START #
        tmp = self.connected_ADAM.read_holding_registers(0, 4)
        self.analog_output_values = tmp.registers
        return self.encode_value(self.analog_output_values[0], 0)
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_0_read

    def read_AnalogOutput_1(self):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_1_read) ENABLED START #
        return self.encode_value(self.analog_output_values[1], 1)
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_1_read

    def read_AnalogOutput_2(self):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_2_read) ENABLED START #
        return self.encode_value(self.analog_output_values[2], 2)
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_2_read

    def read_AnalogOutput_3(self):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_3_read) ENABLED START #
        return self.encode_value(self.analog_output_values[3], 3)
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_3_read

    def write_AnalogOutput_0(self, value):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_0_write) ENABLED START #
        self.connected_ADAM.write_register(0, self.decode_value(value, 0, 0))
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_0_write

    def write_AnalogOutput_1(self, value):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_1_write) ENABLED START #
        self.connected_ADAM.write_register(1, self.decode_value(value, 1, 0))
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_1_write

    def write_AnalogOutput_2(self, value):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_2_write) ENABLED START #
        self.connected_ADAM.write_register(2, self.decode_value(value, 2, 0))
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_2_write

    def write_AnalogOutput_3(self, value):
        # PROTECTED REGION ID(ADAM6224.AnalogOutput_3_write) ENABLED START #
        self.connected_ADAM.write_register(3, self.decode_value(value, 3, 0))
        # PROTECTED REGION END #    //  ADAM6224.AnalogOutput_3_write


    # --------------------
    # SafetyValue methods
    # --------------------

    def read_SafetyValue_0(self):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_0_read) ENABLED START #
        tmp = self.connected_ADAM.read_holding_registers(410, 4)
        self.analog_output_safety_values = tmp.registers
        return self.encode_value(self.analog_output_safety_values[0], 0)
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_0_read

    def read_SafetyValue_1(self):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_1_read) ENABLED START #
        return self.encode_value(self.analog_output_safety_values[1], 1)
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_1_read

    def read_SafetyValue_2(self):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_2_read) ENABLED START #
        return self.encode_value(self.analog_output_safety_values[2], 2)
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_2_read

    def read_SafetyValue_3(self):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_3_read) ENABLED START #
        return self.encode_value(self.analog_output_safety_values[3], 3)
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_3_read

    def write_SafetyValue_0(self, value):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_0_write) ENABLED START #
        self.connected_ADAM.write_register(410, self.decode_value(value, 0, 1))
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_0_write

    def write_SafetyValue_1(self, value):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_1_write) ENABLED START #
        self.connected_ADAM.write_register(411, self.decode_value(value, 1, 1))
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_1_write

    def write_SafetyValue_2(self, value):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_2_write) ENABLED START #
        self.connected_ADAM.write_register(412, self.decode_value(value, 2, 1))
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_2_write

    def write_SafetyValue_3(self, value):
        # PROTECTED REGION ID(ADAM6224.SafetyValue_3_write) ENABLED START #
        self.connected_ADAM.write_register(413, self.decode_value(value, 3, 1))
        # PROTECTED REGION END #    //  ADAM6224.SafetyValue_3_write


    # --------------------
    # StartupValue methods
    # --------------------

    def read_StartupValue_0(self):
        # PROTECTED REGION ID(ADAM6224.StartupValue_0_read) ENABLED START #
        tmp = self.connected_ADAM.read_holding_registers(400, 4)
        self.analog_output_startup_values = tmp.registers
        return self.encode_value(self.analog_output_startup_values[0], 0)
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_0_read

    def read_StartupValue_1(self):
        # PROTECTED REGION ID(ADAM6224.StartupValue_1_read) ENABLED START #
        return self.encode_value(self.analog_output_startup_values[1], 1)
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_1_read

    def read_StartupValue_2(self):
        # PROTECTED REGION ID(ADAM6224.StartupValue_2_read) ENABLED START #
        return self.encode_value(self.analog_output_startup_values[2], 2)
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_2_read

    def read_StartupValue_3(self):
        # PROTECTED REGION ID(ADAM6224.StartupValue_3_read) ENABLED START #
        return self.encode_value(self.analog_output_startup_values[3], 3)
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_3_read

    def write_StartupValue_0(self, value):
        # PROTECTED REGION ID(ADAM6224.StartupValue_0_write) ENABLED START #
        self.connected_ADAM.write_register(400, self.decode_value(value, 0, 2))
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_0_write

    def write_StartupValue_1(self, value):
        # PROTECTED REGION ID(ADAM6224.StartupValue_1_write) ENABLED START #
        self.connected_ADAM.write_register(401, self.decode_value(value, 1, 2))
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_1_write

    def write_StartupValue_2(self, value):
        # PROTECTED REGION ID(ADAM6224.StartupValue_2_write) ENABLED START #
        self.connected_ADAM.write_register(402, self.decode_value(value, 2, 2))
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_2_write

    def write_StartupValue_3(self, value):
        # PROTECTED REGION ID(ADAM6224.StartupValue_3_write) ENABLED START #
        self.connected_ADAM.write_register(403, self.decode_value(value, 3, 2))
        # PROTECTED REGION END #    //  ADAM6224.StartupValue_3_write

    # --------------------
    # TypeCode methods
    # --------------------

    def read_TypeCode_0(self):
        # PROTECTED REGION ID(ADAM6224.TypeCode_0_read) ENABLED START #
        tmp = self.connected_ADAM.read_holding_registers(200, 4)
        self.analog_output_types = tmp.registers
        return self.decode_type_code(0)
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_0_read

    def read_TypeCode_1(self):
        # PROTECTED REGION ID(ADAM6224.TypeCode_1_read) ENABLED START #
        return self.decode_type_code(1)
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_1_read

    def read_TypeCode_2(self):
        # PROTECTED REGION ID(ADAM6224.TypeCode_2_read) ENABLED START #
        return self.decode_type_code(2)
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_2_read

    def read_TypeCode_3(self):
        # PROTECTED REGION ID(ADAM6224.TypeCode_3_read) ENABLED START #
        return self.decode_type_code(3)
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_3_read

    def write_TypeCode_0(self, value):
        # PROTECTED REGION ID(ADAM6224.TypeCode_0_write) ENABLED START #
        self.connected_ADAM.write_register(200,self.code_type_code(value))
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_0_write

    def write_TypeCode_1(self, value):
        # PROTECTED REGION ID(ADAM6224.TypeCode_1_write) ENABLED START #
        self.connected_ADAM.write_register(201, self.code_type_code(value))
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_1_write

    def write_TypeCode_2(self, value):
        # PROTECTED REGION ID(ADAM6224.TypeCode_2_write) ENABLED START #
        self.connected_ADAM.write_register(202, self.code_type_code(value))
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_2_write

    def write_TypeCode_3(self, value):
        # PROTECTED REGION ID(ADAM6224.TypeCode_3_write) ENABLED START #
        self.connected_ADAM.write_register(203, self.code_type_code(value))
        # PROTECTED REGION END #    //  ADAM6224.TypeCode_3_write

    # --------------------
    # Additional methods
    # --------------------


    def decode_value(self, value, channel, type):
        # PROTECTED REGION ID(ADAM6224.decode_value) ENABLED START #
        type_code = self.analog_output_types[channel]
        if  (type_code == int("0182", 16) and not(value >= 0 and value <= 0.02)) or\
                (type_code == int("0180", 16) and not(value >= 0.004 and value <= 0.02)) or\
                (type_code == int("0148", 16) and not(value >= 0 and value <= 10))   or\
                (type_code == int("0147", 16) and not(value >= 0 and value <= 5)) or\
                (type_code == int("0143", 16) and not(value >= -10 and value <= 10)) or\
                (type_code == int("0142", 16) and not(value >= -5 and value <= 5)):
            if type == 0: tmp = self.analog_output_values[channel]
            elif type == 1: tmp = self.analog_output_safety_values[channel]
            else: tmp = self.analog_output_statup_values[channel]
            self.error_stream('Illegal value')
            raise ValueError
        else:
            if   type_code == int("0182", 16) : tmp = int(4095 * value / 0.02)
            elif type_code == int("0180", 16) : tmp = int(4095 * (value - 0.004) / 0.016)
            elif type_code == int("0148", 16) : tmp = int(4095 * value / 10)
            elif type_code == int("0147", 16) : tmp = int(4095 * value/ 5 )
            elif type_code == int("0143", 16) : tmp = int(4095 * (value + 10) / 20)
            elif type_code == int("0142", 16) : tmp = int(4095 * (value + 5) / 10)
            else:
                if type == 0 :      tmp = self.analog_output_values[channel]
                elif type == 1 :    tmp = self.analog_output_safety_values[channel]
                else:               tmp = self.analog_output_statup_values[channel]

        return tmp
        # PROTECTED REGION END #    //  ADAM6224.decode_value

    def encode_value(self, value, channel):
        # PROTECTED REGION ID(ADAM6224.encode_value) ENABLED START #
        type_code = self.analog_output_types[channel]
        if   type_code == int("0182", 16): tmp = 0.02  * value/4095.0
        elif type_code == int("0180", 16): tmp = (0.016 * value/4095.0) + 0.004
        elif type_code == int("0148", 16): tmp = 10    * value/4095.0
        elif type_code == int("0147", 16): tmp = 5     * value/4095.0
        elif type_code == int("0143", 16): tmp = (20   * value/4095.0) - 10
        elif type_code == int("0142", 16): tmp = (10   * value/4095.0) - 5
        else: tmp = self.analog_output_values[channel]
        return tmp
        # PROTECTED REGION END #    //  ADAM6224.encode_value

    def decode_type_code(self, channel):
        # PROTECTED REGION ID(ADAM6224.decode_type_code) ENABLED START #
        return self.type_code_dictionary[self.analog_output_types[channel]]
        # PROTECTED REGION END #    //  ADAM6224.decode_type_code

    def code_type_code(self, value="0-20mA"):
        # PROTECTED REGION ID(ADAM6224.code_type_code) ENABLED START #
        return self.type_code_dictionary[value]
        # PROTECTED REGION END #    //  ADAM6224.code_type_code


    # --------
    # Commands
    # --------

    @command
    @DebugIt()
    def ConnectWithDevice(self):
        # PROTECTED REGION ID(ADAM6224.ConnectWithDevice) ENABLED START #
        try:
            self.connected_ADAM = ModbusTcpClient(self.DeviceAddress, port=int(502))
        except ModbusException as e:
            self.set_state(DevState.FAULT)
            self.set_status("Modbus exception caught while connecting to device:\n%s" % e)
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught while connecting to device:\n%s" % e)
        print("Connected do device with IP: " + self.DeviceAddress)
        # PROTECTED REGION END #    //  ADAM6224.ConnectWithDevice


# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    from tango.server import run
    return run((ADAM6224,), args=args, **kwargs)


if __name__ == '__main__':
    main()
