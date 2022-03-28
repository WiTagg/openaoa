import argparse
import time
import sys
import json

from aoa_serial_port import *
from aoa_cls import AOA_CLS

def csi_aoa_process(aoa_cls, data):
    raw_frame = json.loads(data.decode())
    if raw_frame['type'] != aoa_cls.CONST_CSI_TYPE:
        print("unknown frame type : %d" %(raw_frame['type']))
        return None
    
    frame = aoa_cls.csi_load_from_server_json_obj(raw_frame)
    if frame is None:
        return
    aoa_cls.csi_find_aoa_frame(frame)

    aoa_ret = {
        'recv_time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'mac' : frame['sta_mac'],
        'seq' : frame['seq'],
        'rssi' : frame['rssi'],
        'freq' : frame['freq'],
        "aoa" : 0
    }
    if frame['aoa_azimuth'] is not None:
        aoa_ret['aoa'] = frame['aoa_azimuth']
    print(repr(aoa_ret))
    return aoa_ret
            
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_source', type=str, dest='data_source', default='/dev/ttyACM0', help='please input data_source')
    parser.add_argument('--list_serial_port', '-l', action="store_true", default=False, help='list_serial_port')

    args = parser.parse_args()

    if args.list_serial_port == True:
        ports = ble_dev_serial_port_list()
        for port in ports:
            print(port)
        return

    aoa_cls = AOA_CLS()
    while True:
        try:
            serial_dev = None
            serial_dev = ble_dev_serial_dev_open(args.data_source)
            while serial_dev is None:
                time.sleep(2)
                serial_dev = ble_dev_serial_dev_open(args.data_source)
                continue
            print("read_serial_process start!!")

            recv_data = b''
            while True:
                read_data = ble_dev_serial_dev_read(serial_dev)
                if len(read_data) <= 0:
                    break;
                else:
                    recv_data += read_data
                    
                    while(True):
                        end_index = recv_data.find(b'END')
                        if end_index >= 0:
                            start_index = recv_data[:end_index].rfind(b'START')
                            if start_index >= 0:
                                csi_aoa_process(aoa_cls, recv_data[start_index+5:end_index])
                            recv_data = recv_data[end_index+3:]
                        else:
                            break

        except Exception as e:
            print("read_serial_process : get Exception %s!" %(repr(e)))
            print(recv_data)
            if serial_dev is not None:
                ble_dev_serial_dev_close(serial_dev)
            time.sleep(1)
            continue

if __name__ == '__main__':
    main(argv=sys.argv[1:])