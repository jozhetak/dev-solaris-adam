# -*- coding: utf-8 -*-
#
# This file is part of the dev-solaris-adam project
#
#
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.


__all__ = ["ADAM6256", "main"]

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

class ADAM6256(Device):
    """ ADAM6256
It is a definition of a class used to control ADAM-6256 controller via
Modbus TCP.
Device contains 16-ch Digital Output.
For each DO there are associated attributes:

 * DigitalOutput(bool) - contains present output value of the channel is
    adjustable
 * PulseOutputLow(int) - contains present value (in milliseconds) of Pulse
    Output Low Level Width of the channel, is adjustable
 * PulseOutputHigh(int) - contains present value (in milliseconds) of
    Pulse Output High Level Width of the channel, is adjustable
 * AbsolutePulse(int) - contains value of Absolute Pulse, is adjustable
 * IncrementalPulse(int) - contains value of Absolute Pulse, is adjustable


"""
    __metaclass__ = DeviceMeta
    connected_ADAM = 0.0

    digital_output_values = [False, False, False, False, False, False,
                            False, False, False, False, False, False,
                            False, False, False, False]
    pulse_output_low = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pulse_output_high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    absolute_pulse_output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    incremental_pulse_output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    DeviceAddress = device_property(
        dtype='str',
        default_value="192.168.120.59",
        doc="An IP address of device"
    )

    # --------------------
    # Additional methods
    # --------------------

    def encode_values(self,value):
        """Prepare list of ints to write to registers responsible for Pulses'
                values"""
        tmp = range(0,32) * 0
        for i in value:
            tmp[2 * i] = int(value[i] / 65536)
            tmp[2 * i + 1] = int(value[i] % 65536)
        return tmp

    # ------------------
    # Attributes methods
    # ------------------

    def read_DigitalOutput(self):
        return self.digital_output_values

    def write_DigitalOutput(self, value):
        self.connected_ADAM.write_coils(16,self.encode(value))

    def read_PulseOutputLow(self):
        return self.pulse_output_low

    def write_PulseOutputLow(self, value):
        self.connected_ADAM.write_registers(0, self.encode_values(value))

    def read_PulseOutputHigh(self):
        return self.pulse_output_high

    def write_PulseOutputHigh(self, value):
        self.connected_ADAM.write_registers(32, self.encode_values(value))

    def read_AbsolutePulse(self):
        return self.absolute_pulse_output

    def write_AbsolutePulse(self, value):
        self.connected_ADAM.write_registers(64, self.encode_values(value))

    def read_IncrementalPulse(self):
        return self.incremental_pulse_output

    def write_IncrementalPulse(self, value):
        self.connected_ADAM.write_registers(96, self.encode_values(value))

    # ----------
    # Attributes
    # ----------

    DigitalOutput = attribute(
        dtype=(bool,),
        access=AttrWriteType.READ_WRITE,
        doc="Bool values at all Digital Output channels",
        max_dim_x=16
    )

    PulseOutputLow = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Pulse Output Low Level at all Digital Output channels",
        max_dim_x=16
    )

    PulseOutputHigh = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Pulse Output High Level at all Digital Output channels",
        max_dim_x=16
    )

    AbsolutePulse = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Absolute Pulse at all Digital Output channels",
        max_dim_x=16
    )

    IncrementalPulse = attribute(
        dtype=(int,),
        access=AttrWriteType.READ_WRITE,
        doc="Incremental Pulse at all Digital Output channels",
        max_dim_x=16
    )




    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """Initialise device and sets its state to STANDBY"""
        Device.init_device(self)
        self.set_state(DevState.STANDBY)
        self.set_status(
            "ADAM-6256 in state STANDBY, ready to connect to "
            "device")

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
            "Device disconnected form ADAM-6256, set state to STANDBY, "
            "ready to connect to device again")

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

    @command(polling_period=500)
    def read_DataFromDevice(self):
        """
         Synchronous reading data from ADAM Module registers
        """
        if self.get_state() == tango.DevState.ON:
            # read Digital Outputs
            tmp = self.connected_ADAM.read_coils(16, 16)
            self.digital_output_values = tmp.bits
            # read Pulse Output Low
            tmp2 = self.connected_ADAM.read_holding_registers(0, 128)
            tmp = tmp2[0:32]
            for i in range(0, 16):
                self.pulse_output_low[i] = tmp.registers[2 * i] + 65536  * \
                                               tmp.registers[2 * i + 1]
            # read Pulse Output High
            tmp = tmp2[32:64]
            for i in range(0, 16):
                self.pulse_output_high[i] = tmp.registers[2 * i] + 65536  * \
                                           tmp.registers[2 * i + 1]
            # read Absolute Pulse Output
            tmp = tmp2[64:96]
            for i in range(0, 16):
                self.absolute_pulse_output[i] = tmp.registers[2 * i] + 65536 \
                                            * tmp.registers[2 * i + 1]
            # read Incremental Pulse Output
            tmp = tmp2[96:128]
            for i in range(0, 16):
                self.incremental_pulse_output[i] = tmp.registers[2 * i] \
                                                   + 65536 * \
                                                     tmp.registers[2 * i + 1]



    # ----------
    # Run server
    # ----------


def main(args=None, **kwargs):
    from tango.server import run
    return run((ADAM6256,), args=args, **kwargs)

if __name__ == '__main__':
    main()
