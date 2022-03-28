import serial
import serial.tools.list_ports as list_ports

__all__ = ['ble_dev_serial_dev_read', 'ble_dev_serial_dev_open', 'ble_dev_serial_dev_close', 'ble_dev_serial_port_list']

def ble_dev_serial_port_list():
    open_ports = list_ports.comports()
    return [x for x in open_ports]

def ble_dev_serial_dev_read(read_dev, decode=None):
    while True:
        try:
            if decode is None:
                data = read_dev.read(read_dev.in_waiting or 100)
            else:
                data = read_dev.read(read_dev.in_waiting or 100).decode(decode)
            if len(data) <= 0:
#                 print('recv timeout!!')
                continue
            else:
                return data

        except Exception as e:
            print('recv error please reconnect serial dev [%s] !!\n' %(repr(e)))
            return []

def ble_dev_serial_dev_open(open_inf):
    port = None
    baudrate = None

    try:
        port_baudrate_list = open_inf.split(":")
        if len(port_baudrate_list) == 1:
            if len(port_baudrate_list[0]) == 0:
                port = '/dev/ttyACM0'
                baudrate = 115200
            else:
                port = port_baudrate_list[0]
                baudrate = 115200
        elif len(port_baudrate_list) == 2:
            port = port_baudrate_list[0]
            baudrate = int(port_baudrate_list[1])
        if port is not None and baudrate is not None:
            serial_instance = serial.Serial(port, baudrate, timeout = 5)
            serial_instance.flushInput()
            return serial_instance
        else:
            return None
    except Exception as e:
        print('Open port {!r} err : {}\n'.format(open_inf, e))
        return None

def ble_dev_serial_dev_close(close_dev):
    try:
        close_dev.close()
    except Exception as e:
        print('Could not close dev {!r}: {}\n'.format(close_dev, e))
    pass
