from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import time
try:
    register_world = ModbusTcpClient('192.168.120.55', port=int(502))
except ModbusException as e:
    print(e.string)
print("Connected!!")


try:
    register_world.write_register(0, 10000)
    time.sleep(10)
    register = register_world.read_input_registers(0, 4)
    register_world.write_register(0, 0)
    time.sleep(5)
    register = register_world.read_input_registers(0, 4)
except ModbusException as e:
    print(e.string)