
# -*- coding: utf-8 -*-
#
# This file is part of the dev-solaris-adam project
#
#
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.



__all__ = ["ADAM6217", "main"]

# PyTango imports
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device, DeviceMeta
from tango.server import attribute, command
from tango.server import class_property, device_property
from tango import AttrQuality, AttrWriteType, DispLevel, DevState, AttrDataFormat
# Additional import

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException
#mport time



class ADAM6217(Device):
    """ ADAM6217
It is a definition of a class used to control ADAM-6217 controller via Modbus
TCP.
Device contains 8-ch Isolated Analog Input channels
For each AI there are associated attributes:

 * AnalogInput(double) - contains present output value of the channel (V or
    mA), it is adjustable
 * SafetyValue(double)  - contains present safety value of the channel (V or
    mA), it is adjustable
 * StartupValue(double)  - contains present startup value of the channel (V
    or mA), it is adjustable
 * Status(string)  - contains present status of the channel, available:
    Failed to provide AI value (UART timeout), Over Range, Under Range,
    Open Circuit(Burnout), AD Converter failed, Zero / Span Calibration Error,
 * HistMin(double) - historical minimum value, can be reset to actual
    AnalogInput value using command ResetHistMin (channel number)
 * HistMax(double) - historical minimum value, can be reset to actual
    AnalogInput value using command ResetHistMax(channel number)
 * OpenCircuitFlag(bool) - can be active when measuring 4-20mA, indicates if
    burnout occurred
 * HighAlarmFlag(bool) - it is true if measuring value is above High alarm
 * LowAlarmFlag(bool) - it is true if measuring value is above Low alarm

"""
    __metaclass__ = DeviceMeta
    connected_ADAM = 0.0

    analog_input_values = [0, 0, 0, 0, 0, 0, 0, 0]
    analog_input_statuses = [0, 0, 0, 0, 0, 0, 0, 0]    
    analog_input_types = [0, 0, 0, 0, 0, 0, 0, 0]
    analog_output_startup_values = [0, 0, 0, 0, 0, 0, 0, 0]
    analog_output_safety_values = [0, 0, 0, 0, 0, 0, 0, 0]
    hist_max = [0, 0, 0, 0, 0, 0, 0, 0]
    hist_min =  [0, 0, 0, 0, 0, 0, 0, 0]
    open_circuit_flags = [False, False, False, False, False, False, False, False]
    reset_min = [False, False, False, False, False, False, False, False]
    reset_max = [False, False, False, False, False, False, False, False]
    high_alarm_flag = [False, False, False, False, False, False, False, False]
    low_alarm_flag = [False, False, False, False, False, False, False, False]

    type_to_code_dict = {'0-20mA': int("0182", 16), '4-20mA': int("0180", 16),
                           '0-10V': int("0148", 16), '0-5V': int("0147", 16),
                           '+-10V': int("0143", 16), '+-5V': int("0142", 16),
                           '+-1V': int("0140", 16), '+-500mV': int("0104", 16),
                           '+-150m': int("0103", 16), '+-20mA': int("0181", 16)}
    code_to_type_dict = {v: k for k, v in type_to_code_dict.iteritems()}

    status_dict_1 = {int(1): 'Failed to provide AI value (UART timeout)',
                     int(2): 'Over Range',
                     int(4): 'Under Range',
                     int(8): 'Open Circuit(Burnout)',
                     int(128): 'AD Converter failed',
                     int(512): 'Zero / Span Calibration Error',
                     int(0): ' '}
    status_dict_1.update({v: k for k, v in status_dict_1.iteritems()})

    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    DeviceAddress = device_property(
        dtype='str',
        default_value="192.168.120.56",
        doc = "This property contains an IP address of device"
    )

    # ----------
    # Attributes
    # ----------

    AnalogInput_0 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc = "Value at channel 0"
    )

    AnalogInput_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Value at channel 1"
    )

    AnalogInput_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc = "Value at channel 2"
    )

    AnalogInput_3 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Value at channel 3"
    )

    AnalogInput_4 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Value at channel 4"
    )

    AnalogInput_5 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Value at channel 5"
    )

    AnalogInput_6 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Value at channel 6"
    )

    AnalogInput_7 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Value at channel 7"
    )

    TypeCode_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 0"
    )

    TypeCode_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 1"
    )

    TypeCode_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 2"
    )

    TypeCode_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 3"
    )

    TypeCode_4 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 4"
    )

    TypeCode_5 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 5"
    )

    TypeCode_6 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 6"
    )

    TypeCode_7 = attribute(
        dtype='str',
        access=AttrWriteType.READ_WRITE,
        doc="Type of input at channel 7"
    )

    Status_0 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 0"
    )

    Status_1 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 1"
    )

    Status_2 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 2"
    )

    Status_3 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 3"
    )

    Status_4 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 4"
    )

    Status_5 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 5"
    )

    Status_6 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 6"
    )

    Status_7 = attribute(
        dtype='str',
        access=AttrWriteType.READ,
        doc="Status of channel 7"
    )

    HistMax_0 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 0 since "
            "last reset"
    )

    HistMax_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 1 since "
            "last reset"
    )

    HistMax_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 2 since "
            "last reset"
    )

    HistMax_3 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 3 since "
            "last reset"
    )

    HistMax_4 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 4 since "
            "last reset"
    )

    HistMax_5 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 5 since "
            "last reset"
    )

    HistMax_6 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 6 since "
            "last reset"
    )

    HistMax_7 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the highest value at channel 7 since "
            "last reset"
    )
    
    HistMin_0 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc = "Historical Minimum Value - the lowest value at channel 0 since "
          "last reset"
    )

    HistMin_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc = "Historical Minimum Value - the lowest value at channel 1 since "
          "last reset"
    )

    HistMin_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the lowest value at channel 2 since "
            "last reset"
    )

    HistMin_3 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc = "Historical Minimum Value - the lowest value at channel 3 since "
          "last reset"
    )

    HistMin_4 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the lowest value at channel 4 since "
            "last reset"
    )

    HistMin_5 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc = "Historical Minimum Value - the lowest value at channel 5 since "
          "last reset"
    )

    HistMin_6 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the lowest value at channel 6 since "
            "last reset"
    )

    HistMin_7 = attribute(
        dtype='double',
        access=AttrWriteType.READ,
        format='%2.4f',
        doc="Historical Minimum Value - the lowest value at channel 7 since "
            "last reset"
    )

    OpenCircuitFlags = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ,
        max_dim_x=8,
        doc="Bool values of Open Circuit Flag for channels"
    )

    HighAlarmFlags = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ,
        max_dim_x=8,
        doc="Bool values of High Alarm Flag for channels"
    )

    LowAlarmFlags = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ,
        max_dim_x=8,
        doc="Bool values of Low Alarm Flag for channels"
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """Initialise device and sets its state to STANDBY"""
        Device.init_device(self)
        self.set_state(DevState.STANDBY)
        self.set_status("ADAM-6217 enabled")

    def delete_device(self):
        """Disconnect from physical device before deleting instance"""
        self.connected_ADAM.close()


    @command
    @DebugIt()
    def disconnect(self):
        """Disconnect from device and sets state to STANDBY """
        self.connected_ADAM.close()
        self.set_state(DevState.STANDBY)
        self.set_status(
            "Device disconnected form ADAM-6217, set state to STANDBY, "
            "ready to connect to device again")

    # ------------------
    # Attributes methods
    # ------------------

    # --------------------
    # AnalogInput methods
    # --------------------

    def read_AnalogInput_0(self):
        return self.encode_value(self.analog_input_values[0], 0)

    def read_AnalogInput_1(self):
        return self.encode_value(self.analog_input_values[1], 1)

    def read_AnalogInput_2(self):
        return self.encode_value(self.analog_input_values[2], 2)

    def read_AnalogInput_3(self):
        return self.encode_value(self.analog_input_values[3], 3)
    
    def read_AnalogInput_4(self):
        return self.encode_value(self.analog_input_values[4], 4)

    def read_AnalogInput_5(self):
        return self.encode_value(self.analog_input_values[5], 5)

    def read_AnalogInput_6(self):
        return self.encode_value(self.analog_input_values[6], 6)
    
    def read_AnalogInput_7(self):
        return self.encode_value(self.analog_input_values[7], 7)

    # --------------------
    # TypeCode methods
    # --------------------

    def read_TypeCode_0(self):
        return self.decode_type_code(0)

    def read_TypeCode_1(self):
        return self.decode_type_code(1)

    def read_TypeCode_2(self):
        return self.decode_type_code(2)

    def read_TypeCode_3(self):
        return self.decode_type_code(3)
    
    def read_TypeCode_4(self):
        return self.decode_type_code(4)

    def read_TypeCode_5(self):
        return self.decode_type_code(5)

    def read_TypeCode_6(self):
        return self.decode_type_code(6)
    
    def read_TypeCode_7(self):
        return self.decode_type_code(7)

    def write_TypeCode_0(self, value):
        self.connected_ADAM.write_register(200, self.encode_type_code(value))

    def write_TypeCode_1(self, value):
        self.connected_ADAM.write_register(201, self.encode_type_code(value))

    def write_TypeCode_2(self, value):
        self.connected_ADAM.write_register(202, self.encode_type_code(value))

    def write_TypeCode_3(self, value):
        self.connected_ADAM.write_register(203, self.encode_type_code(value))

    def write_TypeCode_4(self, value):
        self.connected_ADAM.write_register(204, self.encode_type_code(value))

    def write_TypeCode_5(self, value):
        self.connected_ADAM.write_register(205, self.encode_type_code(value))

    def write_TypeCode_6(self, value):
        self.connected_ADAM.write_register(206, self.encode_type_code(value))

    def write_TypeCode_7(self, value):
        self.connected_ADAM.write_register(207, self.encode_type_code(value))

    # --------------------
    # Flags methods
    # -------------------- 

    def read_OpenCircuitFlags(self):
        return self.open_circuit_flags
    
    def read_HighAlarmFlags(self):
        return self.open_circuit_flags
    
    def read_LowAlarmFlags(self):
        return self.open_circuit_flags

    # --------------------
    # Historical Values methods
    # --------------------

    def read_HistMax_0(self):
        return self.encode_value(self.hist_max[0], 0)

    def read_HistMax_1(self):
        return self.encode_value(self.hist_max[1], 1)

    def read_HistMax_2(self):
        return self.encode_value(self.hist_max[2], 2)

    def read_HistMax_3(self):
        return self.encode_value(self.hist_max[3], 3)

    def read_HistMax_4(self):
        return self.encode_value(self.hist_max[4], 4)

    def read_HistMax_5(self):
        return self.encode_value(self.hist_max[5], 5)

    def read_HistMax_6(self):
        return self.encode_value(self.hist_max[6], 6)

    def read_HistMax_7(self):
        return self.encode_value(self.hist_max[7], 7)
    
    def read_HistMin_0(self):
        return self.encode_value(self.hist_min[0], 0)

    def read_HistMin_1(self):
        return self.encode_value(self.hist_min[1], 1)

    def read_HistMin_2(self):
        return self.encode_value(self.hist_min[2], 2)

    def read_HistMin_3(self):
        return self.encode_value(self.hist_min[3], 3)

    def read_HistMin_4(self):
        return self.encode_value(self.hist_min[4], 4)

    def read_HistMin_5(self):
        return self.encode_value(self.hist_min[5], 5)

    def read_HistMin_6(self):
        return self.encode_value(self.hist_min[6], 6)

    def read_HistMin_7(self):
        return self.encode_value(self.hist_min[7], 7)

    # --------------------
    # Status methods
    # --------------------

    def read_Status_0(self):
        return self.status_dict_1[self.analog_input_statuses[0]]

    def read_Status_1(self):
        return self.status_dict_1[self.analog_input_statuses[2]]

    def read_Status_2(self):
        return self.status_dict_1[self.analog_input_statuses[4]]

    def read_Status_3(self):
        return self.status_dict_1[self.analog_input_statuses[6]]
    
    def read_Status_4(self):
        return self.status_dict_1[self.analog_input_statuses[8]]

    def read_Status_5(self):
        return self.status_dict_1[self.analog_input_statuses[10]]

    def read_Status_6(self):
        return self.status_dict_1[self.analog_input_statuses[12]]
    
    def read_Status_7(self):
        return self.status_dict_1[self.analog_input_statuses[14]]

    # --------------------
    # Additional methods
    # --------------------

    def encode_value(self, value, channel):
        """Encode 16-bit value to double depending on Type Code of
        channel """
        type_code = self.analog_output_types[channel]
        if   type_code == int("0182", 16): tmp = 0.02  * value/65535.0
        elif type_code == int("0180", 16): tmp = (0.016 * value/65535.0) + 0.004
        elif type_code == int("0148", 16): tmp = 10    * value/65535.0
        elif type_code == int("0147", 16): tmp = 5     * value/65535.0
        elif type_code == int("0143", 16): tmp = (20   * value/65535.0) - 10
        elif type_code == int("0142", 16): tmp = (10   * value/65535.0) - 5
        elif type_code == int("0140", 16): tmp = (2    * value/65535.0) - 1
        elif type_code == int("0104", 16): tmp =         value/65535.0  - 0.5
        elif type_code == int("0103", 16): tmp = (0.3  * value/65535.0) - 0.15
        elif type_code == int("0181", 16): tmp = (0.04 * value/65535.0) - 0.02
        else: tmp = self.analog_output_values[channel]
        return tmp

    def decode_type_code(self, channel):
        """Decode 16-bit number to Type Code string"""
        return self.code_to_type_dict[self.analog_output_types[channel]]

    def encode_type_code(self, value="0-20mA"):
        """Encodes Type Code string to 16-bit number"""
        return self.type_to_code_dict[value]

    # --------
    # Commands
    # --------

    @command
    @DebugIt()
    def ConnectWithDevice(self):
        """
         Connect with ADAM Module with IP address the same as DeviceAddress
         property and sets its state to ON
        """
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
        self.info_stream("Connected to device with IP: " + str(
             self.DeviceAddress))

    @command(dtype_in=int, doc_in='Channel number')
    @DebugIt()
    def ResetHistMax(self, value):
        """Resets Historical Maximum Value"""
        if 0 <= value < 8:
            self.connected_ADAM.write_coil(100 + value, int('0xff00', 16))
        else:
            raise ValueError

    @command(dtype_in=int, doc_in='Channel number')
    @DebugIt()
    def ResetHistMin(self, value):
        """Resets Historical Minimum Value"""
        if 0 <= value < 8:
            self.connected_ADAM.write_coil(110 + value, int('0xff00', 16))
        else:
            raise ValueError

    @command(polling_period=500)
    def read_DataFromDevice(self):
        """
          Synchronous reading data from ADAM Module registers
         """
        if self.get_state() == tango.DevState.ON:
            # read Open-Circuit Flag
            tmp = self.connected_ADAM.read_coils(120, 32)
            self.open_circuit_flags = tmp.bits[0:8]
            # read LowAlarmFlags
            self.low_alarm_flag = tmp.bits[10:18]
            # read High Alarm Flags
            self.high_alarm_flag = tmp.bits[20:28]
            # read Analog Inputs
            tmp = self.connected_ADAM.read_holding_registers(0, 32)
            self.analog_input_values = tmp.registers[0:8]
            # read Historical Max Values
            self.hist_max = tmp.registers[10:18]
            # read Historical Min Value
            self.hist_min = tmp.registers[20:28]
            # read Statuses
            tmp = self.connected_ADAM.read_holding_registers(100, 16)
            self.analog_input_statuses = tmp.registers
            # read Type Codes
            tmp = self.connected_ADAM.read_holding_registers(200, 8)
            self.analog_output_types = tmp.registers

# ----------
# Run server
# ----------

def main(args=None, **kwargs):
    from tango.server import run
    return run((ADAM6217,), args=args, **kwargs)

if __name__ == '__main__':
    main()
