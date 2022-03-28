import numpy as np

# about this code please see README

class AOA_CLS():
    CONST_CSI_TYPE = 6
    CONST_RSSI_MIN = -92
    
    aoa_feature_matrix_file = './bin/aoa_feature_matrix.npz'
    ble_channel_freqs = {
        37 : 2402*1000*1000,
        38 : 2426*1000*1000,
        39 : 2480*1000*1000
    }
    
    def __init__(self):
        self.feature_matrix_inf = self.feature_matrix_load()

    def feature_matrix_load(self, load_file=aoa_feature_matrix_file):
        feature_matrix_inf = {
            'az_begin' : 0,
            'az_step' : 3,
            'az_end' : 360,
            'freqs_feature': None,
        }
        feature_matrix_inf['az_degs'] = np.arange(feature_matrix_inf['az_begin'], feature_matrix_inf['az_end'], feature_matrix_inf['az_step'])

        freqs_feature = {}
        if load_file is not None:
            freqs_feature_load = np.load(load_file)
            freqs_feature[2402*1000*1000] = freqs_feature_load['arr_0']
            freqs_feature[2426*1000*1000] = freqs_feature_load['arr_1']
            freqs_feature[2480*1000*1000] = freqs_feature_load['arr_2']
            feature_matrix_inf['freqs_feature'] = freqs_feature
        return feature_matrix_inf
 
    def csi_find_aoa_frame(self, frame):
        csi = frame['csi']
        feature_array = self.feature_matrix_inf['freqs_feature'][frame['freq']][0]
        azimuth_degrees = self.feature_matrix_inf['az_degs']
        
        csi_dot = csi @ np.conj(csi).T
        e_value, e_vector = np.linalg.eigh(csi_dot)
        eig_a = e_vector[:,:11]

        ret = np.conj(feature_array).T @ eig_a @ np.conj(eig_a).T @ feature_array
        ret = np.diag(ret)
        aoa = int(azimuth_degrees[ret.argmin()])
        frame['aoa_azimuth'] = (aoa - 90 + 360) % 360
        
        return frame['aoa_azimuth']

    def csi_load_from_server_json_obj(self, data_json):
        if data_json['type'] != self.CONST_CSI_TYPE:
            return None
        if data_json['rssi'] < self.CONST_RSSI_MIN:
            return None
        
        ant_sample_cnt = 8
        ant_cnt = len(data_json['csi_data']) // 2 // ant_sample_cnt
        
        iq_phase = np.empty(ant_cnt*ant_sample_cnt)
        iq_ampl = np.empty(ant_cnt*ant_sample_cnt)
        for i in range( len(data_json['csi_data'])//2 ):
            iq_phase[i] = np.deg2rad(data_json['csi_data'][i*2])
            iq_ampl[i] = data_json['csi_data'][i*2+1]
        iq_phase.resize((ant_cnt, ant_sample_cnt))
        iq_ampl.resize((ant_cnt, ant_sample_cnt))

        frame = {}
        frame['type'] = data_json['type']
        frame['seq'] = data_json['seq']
        frame['sta_mac'] = data_json['mac']
        frame['channel'] = data_json['channel']
        frame['freq'] = self.ble_channel_freqs[data_json['channel']]
        frame['rssi'] = data_json['rssi']
        frame['aoa_azimuth'] = None
        frame['csi_phase'] = iq_phase
        frame['csi_ampl'] = iq_ampl
        frame['csi'] = np.exp(1j*frame['csi_phase']) * frame['csi_ampl']

        return frame