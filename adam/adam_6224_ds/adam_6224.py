
# -*- coding: utf-8 -*-
#
# This file is part of the dev-solaris-adam project
#
#
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.

""" Adam6224
It is a definicion of a class used to control ADAM-6224 controller via Modbus/TCP.
"""

__all__ = ["Adam6224", "main"]

# PyTango imports
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device, DeviceMeta
from tango.server import attribute, command
from tango.server import class_property, device_property
from tango import AttrQuality, AttrWriteType, DispLevel, DevState
# Additional import
# PROTECTED REGION ID(Adam6224.additionnal_import) ENABLED START #
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException
#mport time
# PROTECTED REGION END #    //  Adam6224.additionnal_import


class Adam6224(Device):
    """
    It is a definicion of a class used to control ADAM-6224 controller via Modbus/TCP.
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(Adam6224.class_variable) ENABLED START #
    connected_adam = 0.0
    digital_input_values = [False, False, False, False]
    analog_output_values = [0, 0, 0, 0]
    analog_output_statuses = [0, 0, 0, 0]
    analog_output_types = [0, 0, 0, 0]
    type_code_dictionary = {'0-20mA': int("0182", 16), '4-20mA': int("0180", 16),
                           '0-10V': int("0148", 16), '0-5V': int("0147", 16),
                           '+-10V': int("0143", 16), '+-5V': int("0142", 16)}
    type_code_dictionary.update({v: k for k, v in type_code_dictionary.iteritems()})

    # PROTECTED REGION END #    //  Adam6224.class_variable
    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    DeviceAdress = device_property(
        dtype='str',
        default_value="192.168.120.55"
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
    )

    AnalogOutput_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
    )

    AnalogOutput_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
    )

    AnalogOutput_3 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
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

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(Adam6224.init_device) ENABLED START #
        self.set_state(DevState.ON)
        self.set_status("ADAM-6224 enabled")
        # PROTECTED REGION END #    //  Adam6224.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(Adam6224.always_executed_hook) ENABLED START #
        if not self.connected_adam.connect():
            self.set_state(DevState.ALARM)
            self.set_status("Connection  error")
        # PROTECTED REGION END #    //  Adam6224.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(Adam6224.delete_device) ENABLED START #
        self.connected_adam.close()
        # PROTECTED REGION END #    //  Adam6224.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    # --------------------
    # DigitalInput methods
    # --------------------

    def read_DigitalInput_0(self):
        # PROTECTED REGION ID(Adam6224.DigitalInput_0_read) ENABLED START #
        tmp = self.connected_adam.read_coils(0, 4)
        self.digital_input_values = tmp.bits
        return self.digital_input_values[0]
        # PROTECTED REGION END #    //  Adam6224.DigitalInput_0_read

    def read_DigitalInput_1(self):
        # PROTECTED REGION ID(Adam6224.DigitalInput_1_read) ENABLED START #
        return self.digital_input_values[1]
        # PROTECTED REGION END #    //  Adam6224.DigitalInput_1_read

    def read_DigitalInput_2(self):
        # PROTECTED REGION ID(Adam6224.DigitalInput_2_read) ENABLED START #
        return self.digital_input_values[2]
        # PROTECTED REGION END #    //  Adam6224.DigitalInput_2_read

    def read_DigitalInput_3(self):
        # PROTECTED REGION ID(Adam6224.DigitalInput_3_read) ENABLED START #
        return self.digital_input_values[3]
        # PROTECTED REGION END #    //  Adam6224.DigitalInput_3_read

    # --------------------
    # AnalogOutput methods
    # --------------------

    def read_AnalogOutput_0(self):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_0_read) ENABLED START #
        tmp = self.connected_adam.read_holding_registers(0, 4)
        self.analog_output_values = tmp.registers
        return self.encode_value(self.analog_output_values[0], 0)
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_0_read

    def read_AnalogOutput_1(self):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_1_read) ENABLED START #
        return self.encode_value(self.analog_output_values[1], 1)
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_1_read

    def read_AnalogOutput_2(self):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_2_read) ENABLED START #
        return self.encode_value(self.analog_output_values[2], 2)
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_2_read

    def read_AnalogOutput_3(self):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_3_read) ENABLED START #
        return self.encode_value(self.analog_output_values[3], 3)
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_3_read

    def write_AnalogOutput_0(self, value):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_0_write) ENABLED START #
        self.connected_adam.write_register(0, self.decode_value(value, 0))
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_0_write

    def write_AnalogOutput_1(self, value):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_1_write) ENABLED START #
        self.connected_adam.write_register(1, self.decode_value(value, 1))
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_1_write

    def write_AnalogOutput_2(self, value):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_2_write) ENABLED START #
        self.connected_adam.write_register(2, self.decode_value(value, 2))
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_2_write

    def write_AnalogOutput_3(self, value):
        # PROTECTED REGION ID(Adam6224.AnalogOutput_3_write) ENABLED START #
        self.connected_adam.write_register(3, self.decode_value(value, 3))
        # PROTECTED REGION END #    //  Adam6224.AnalogOutput_3_write


    # --------------------
    # TypeCode methods
    # --------------------

    def read_TypeCode_0(self):
        # PROTECTED REGION ID(Adam6224.TypeCode_0_read) ENABLED START #
        tmp = self.connected_adam.read_holding_registers(200, 4)
        self.analog_output_types = tmp.registers
        return self.decode_type_code(0)
        # PROTECTED REGION END #    //  Adam6224.TypeCode_0_read

    def read_TypeCode_1(self):
        # PROTECTED REGION ID(Adam6224.TypeCode_1_read) ENABLED START #
        return self.decode_type_code(1)
        # PROTECTED REGION END #    //  Adam6224.TypeCode_1_read

    def read_TypeCode_2(self):
        # PROTECTED REGION ID(Adam6224.TypeCode_2_read) ENABLED START #
        return self.decode_type_code(2)
        # PROTECTED REGION END #    //  Adam6224.TypeCode_2_read

    def read_TypeCode_3(self):
        # PROTECTED REGION ID(Adam6224.TypeCode_3_read) ENABLED START #
        return self.decode_type_code(3)
        # PROTECTED REGION END #    //  Adam6224.TypeCode_3_read

    def write_TypeCode_0(self, value):
        # PROTECTED REGION ID(Adam6224.TypeCode_0_write) ENABLED START #
        self.connected_adam.write_register(200,self.code_type_code(value))
        # PROTECTED REGION END #    //  Adam6224.TypeCode_0_write

    def write_TypeCode_1(self, value):
        # PROTECTED REGION ID(Adam6224.TypeCode_1_write) ENABLED START #
        self.connected_adam.write_register(201, self.code_type_code(value))
        # PROTECTED REGION END #    //  Adam6224.TypeCode_1_write

    def write_TypeCode_2(self, value):
        # PROTECTED REGION ID(Adam6224.TypeCode_2_write) ENABLED START #
        self.connected_adam.write_register(202, self.code_type_code(value))
        # PROTECTED REGION END #    //  Adam6224.TypeCode_2_write

    def write_TypeCode_3(self, value):
        # PROTECTED REGION ID(Adam6224.TypeCode_3_write) ENABLED START #
        self.connected_adam.write_register(203, self.code_type_code(value))
        # PROTECTED REGION END #    //  Adam6224.TypeCode_3_write

    # --------------------
    # Additional methods
    # --------------------

    def decode_value(self, value, channel):
        # PROTECTED REGION ID(Adam6224.decode_value) ENABLED START #
        tmp = self.analog_output_values[channel]
        try:
            type_code = self.analog_output_types[channel]
            if   type_code == int("0182", 16): tmp = int(4095 * value / 0.02)
            elif type_code == int("0180", 16): tmp = int(4095 * (value - 0.004) / 0.016)
            elif type_code == int("0148", 16): tmp = int(4095 * value / 10)
            elif type_code == int("0147", 16): tmp = int(4095 * value/ 5 )
            elif type_code == int("0143", 16): tmp = int(4095 * (value + 10) / 20)
            elif type_code == int("0142", 16): tmp = int(4095 * (value + 5) / 10)
            else: tmp = self.analog_output_values[channel]
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught while encoding value:\n%s" % e)
        return tmp
        # PROTECTED REGION END #    //  Adam6224.decode_value

    def encode_value(self, value, channel):
        # PROTECTED REGION ID(Adam6224.encode_value) ENABLED START #
        tmp = self.analog_output_values[channel]
        try:
            type_code = self.analog_output_types[channel]
            if   type_code == int("0182", 16): tmp = 0.02  * value/4095
            elif type_code == int("0180", 16): tmp = (0.016 * value/4095) + 0.004
            elif type_code == int("0148", 16): tmp = 10    * value/4095
            elif type_code == int("0147", 16): tmp = 5     * value/4095
            elif type_code == int("0143", 16): tmp = (20   * value/4095) + 10
            elif type_code == int("0142", 16): tmp = (10   * value/4095) + 5
            else: tmp = self.analog_output_values[channel]
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught while encoding value:\n%s" % e)
        return tmp
        # PROTECTED REGION END #    //  Adam6224.encode_value

    def decode_type_code(self, channel):
        # PROTECTED REGION ID(Adam6224.decode_type_code) ENABLED START #
        return self.type_code_dictionary[self.analog_output_types[channel]]
        # PROTECTED REGION END #    //  Adam6224.decode_type_code

    def code_type_code(self, value="0-20mA"):
        # PROTECTED REGION ID(Adam6224.code_type_code) ENABLED START #
        return self.type_code_dictionary[value]
        # PROTECTED REGION END #    //  Adam6224.code_type_code


    # --------
    # Commands
    # --------

    @command
    @DebugIt()
    def ConnectWithDevice(self):
        # PROTECTED REGION ID(Adam6224.ConnectWithDevice) ENABLED START #
        try:
            self.connected_adam = ModbusTcpClient(self.DeviceAdress, port=int(502))
        except ModbusException as e:
            self.set_state(DevState.FAULT)
            self.set_status("Modbus exception caught while connecting to device:\n%s" % e)
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught while connecting to device:\n%s" % e)
        print("Connected do device with IP: " + self.DeviceAdress)
        # PROTECTED REGION END #    //  Adam6224.ConnectWithDevice


# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    from tango.server import run
    return run((Adam6224,), args=args, **kwargs)


if __name__ == '__main__':
    main()
