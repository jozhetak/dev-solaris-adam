# -*- coding: utf-8 -*-
#
# This file is part of the dev-solaris-adam project
#
#
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.


__all__ = ["ADAM6250", "main"]

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

class ADAM6250(Device):
    """ ADAM6250
It is a definition of a class used to control ADAM-6250 controller via
Modbus TCP.
Device contains 15-ch Isolated Digital I/O (8 inputs, 7 outputs).
For each DI there are associated attributes:

 * DigitalOutput(bool) - contains present output value of the channel is
    adjustable
 * Counter(bool)  - contains present status of the counter associated with
    specific channel (True - enabled, False - stopped), is adjustable
 * LatchStatus(bool)  - contains present status of latch associated with
    specific channel (True - latch closed, False - latch open), is adjustable
 * ClearOverflow(bool)  - indicate if counter value will be reset when
    overflow occurs
 * Counter/Frequency(int) - contains present value of counter associated with
    specific channel or encoded value of temporary input signal frequency,
    counter can be reset by ClearCounter(channel) command

For each DO there are associated attributes:

 * DigitalOutput(bool) - contains present output value of the channel is
    adjustable
 * Pulse Output Low(int) - contains present value (in milliseconds) of Pulse
    Output Low Level Width of the channel, is adjustable
 * Pulse Output high(int) - contains present value (in milliseconds) of
    Pulse Output High Level Width of the channel, is adjustable
 * AbsolutePulse(int) - contains value of Absolute Pulse, is adjustable
 * IncrementalPulse(int) - contains value of Absolute Pulse, is adjustable


"""
    __metaclass__ = DeviceMeta
    connected_ADAM = 0.0
    digital_input_values = [False, False, False, False, False, False,
                            False, False]
    counter = [False, False, False, False, False, False, False, False]
    clear_overflow = [False, False, False, False, False, False, False,
                      False]
    latch_status = [False, False, False, False, False, False, False,
                    False]
    digital_output_values = [False, False, False, False, False, False,
                             False]
    counter_frequency = [0, 0, 0, 0, 0, 0, 0]
    pulse_output_low = [0, 0, 0, 0, 0, 0, 0]
    pulse_output_high = [0, 0, 0, 0, 0, 0, 0]
    absolute_pulse_output = [0, 0, 0, 0, 0, 0, 0]
    incremental_pulse_output = [0, 0, 0, 0, 0, 0, 0]

    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    DeviceAddress = device_property(
        dtype='str',
        default_value="192.168.120.57",
        doc="An IP address of device"
    )

    # --------------------
    # Additional methods
    # --------------------

    def encode(self,value):
        tmp = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in value:
            if value[i] == True:
                tmp[i] = int('0xff00', 16)
        return tmp

    def encode_values(self,value):
        tmp = range(0,14) * 0
        for i in value:
            tmp[2 * i] = int(value[i] / 65536)
            tmp[2 * i + 1] = int(value[i] % 65536)
        return tmp

    # ------------------
    # Attributes methods
    # ------------------

    def read_DigitalInput(self):
        return self.digital_input_values

    def read_DigitalOutput(self):
        return self.digital_output_values

    def write_DigitalOutput(self, value):
        self.connected_ADAM.write_coils(16,self.encode(value))

    def read_Counter(self):
        return self.counter

    def write_Counter(self, value):
        self.connected_ADAM.write_coils(32,self.encode(value))

    def read_Overflow(self):
        return self.clear_overflow

    def write_Overflow(self, value):
        self.connected_ADAM.write_coils(48,self.encode(value))

    def read_LatchStatus(self):
        return self.latch_status

    def write_LatchStatus(self, value):
        self.connected_ADAM.write_coils(56, self.encode(value))

    def read_CounterFrequency(self):
        return self.counter_frequency

    def read_PulseOutputLow(self):
        return self.pulse_output_low

    def write_PulseOutputLow(self, value):
        self.connected_ADAM.write_registers(16, self.encode_values(value))

    def read_PulseOutputHigh(self):
        return self.pulse_output_high

    def write_PulseOutputHigh(self, value):
        self.connected_ADAM.write_registers(30, self.encode_values(value))

    def read_AbsolutePulse(self):
        return self.absolute_pulse_output

    def write_AbsolutePulse(self, value):
        self.connected_ADAM.write_registers(44, self.encode_values(value))

    def read_IncrementalPulse(self):
        return self.incremental_pulse_output

    def write_IncrementalPulse(self, value):
        self.connected_ADAM.write_registers(58, self.encode_values(value))

    # ----------
    # Attributes
    # ----------

    DigitalInput = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ,
        doc="Bool values at all Digital Input channels",
        max_dim_x=8,
    )

    DigitalOutput = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ_WRITE,
        doc="Bool values at all Digital Output channels",
        max_dim_x=7
    )

    Counter = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ_WRITE,
        doc="Counter status at all Digital Input channels",
        max_dim_x=8
    )

    Overflow = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ_WRITE,
        doc="Overflow flags at all Digital Input channels",
        max_dim_x=8
    )

    LatchStatus = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ_WRITE,
        doc="Latch Status at all Digital Input channels",
        max_dim_x=8
    )

    CounterFrequency = attribute(
        dtype=(int,),
        access=AttrWriteType.READ,
        doc="Counter / frequency values at all Digital Input channels",
        max_dim_x=8
    )

    PulseOutputLow = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Pulse Output Low Level at all Digital Output channels",
        max_dim_x=7
    )

    PulseOutputHigh = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Pulse Output High Level at all Digital Output channels",
        max_dim_x=7
    )

    AbsolutePulse = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Absolute Pulse at all Digital Output channels",
        max_dim_x=7
    )

    IncrementalPulse = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Incremental Pulse at all Digital Output channels",
        max_dim_x=7
    )




    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """Initiate device and sets its state to STANDBY"""
        Device.init_device(self)
        self.set_state(DevState.STANDBY)
        self.set_status(
            "ADAM-6250 in state STANDBY, ready to connect to "
            "device")

    def delete_device(self):
        """Delete device"""
        self.connected_ADAM.close()

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
            self.set_status(
                "Exception caught while connecting to device:"
                + "\n%s" % e)
        self.set_state(DevState.ON)
        self.set_status("Connected to device with IP: "
                        + str(self.DeviceAddress))

    @command(dtype_in=int, doc_in='Channel number')
    @DebugIt()
    def ClearCounter(self, value):
        """
         Clear counter value of given channel number
        """
        self.connected_ADAM.write_coil(40 + value, int('0xff00', 16))

    @command(polling_period=500)
    def read_DataFromDevice(self):
        """
         Synchronous reading data from ADAM Module registers
        """
        if self.get_state() == tango.DevState.ON:
            # read Digital Inputs
            tmp = self.connected_ADAM.read_coils(0, 8)
            self.digital_input_values = tmp.bits
            # read Counter Flags
            tmp = self.connected_ADAM.read_coils(32, 32)
            self.counter = tmp.bits[0:8]
            # read Clear Overflow
            self.clear_overflow = tmp.bits[17:24]
            # read Latch Statuses
            self.latch_status = tmp.bits[25:32]
            # read Digital Outputs
            tmp = self.connected_ADAM.read_coils(16, 7)
            self.digital_output_values = tmp.bits[0:7]
            # read Counter/Frequency
            tmp = self.connected_ADAM.read_holding_registers(0, 16)
            for i in range(0, 7):
                self.counter_frequency[i] = tmp.registers[2 * i] + 65536  * \
                                               tmp.registers[2 * i + 1]
            # read Pulse Output Low
            tmp = self.connected_ADAM.read_holding_registers(16, 14)
            for i in range(0, 7):
                self.pulse_output_low[i] = tmp.registers[2 * i] + 65536  * \
                                               tmp.registers[2 * i + 1]
            # read Pulse Output High
            tmp = self.connected_ADAM.read_holding_registers(30, 14)
            for i in range(0, 7):
                self.pulse_output_high[i] = tmp.registers[2 * i] + 65536  * \
                                           tmp.registers[2 * i + 1]
            # read Absolute Pulse Output
            tmp = self.connected_ADAM.read_holding_registers(44, 14)
            for i in range(0, 7):
                self.absolute_pulse_output[i] = tmp.registers[2 * i] + 65536 \
                                            * tmp.registers[2 * i + 1]
            # read Incremental Pulse Output
            tmp = self.connected_ADAM.read_holding_registers(58, 14)
            for i in range(0, 7):
                self.incremental_pulse_output[i] = tmp.registers[2 * i] \
                                                   + 65536 * \
                                                     tmp.registers[2 * i + 1]



    # ----------
    # Run server
    # ----------


def main(args=None, **kwargs):
    from tango.server import run
    return run((ADAM6250,), args=args, **kwargs)

if __name__ == '__main__':
    main()
