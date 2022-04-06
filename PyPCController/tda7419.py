#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
from json import load as json_load
from json import dump as json_dump
import smbus

class tda7419():
    '''ST TDA7419 Audioprocessor Controller Class'''
    def __init__(self, i2c_bus_number=0, path_to_saved_settings=None, chip_address=0x44):

        self.__path_to_load_from = path_to_saved_settings
        self.__i2c_bus_number = i2c_bus_number
        self.__chip_address = chip_address

        self.__tda7419_switchers = {
            "global_testing_mode" : 0,
            "global_autozero_remain" : 1,
            "global_auto_increment_mode" : 0,

            "global_softmute_switch" : 1,
            "global_pin_influence_for_mute" : 1,
            "global_softmute_time" : 0,
            "global_softstep_time" : 0,
            "global_clock_fast_mode" : 1,

            "global_external_reference" : 1,
            "global_enable_smoothing_filter" : 1,

            "global_reset_mode" : 1,
            "global_reset" : 1,
            "global_external_clock_source" : 0,

            "global_testing_mode_enable" : 0,
            "global_testing_multiplexer" : 0,

            "spectrum_analyzer_source_selector" : 1,
            "spectrum_analyzer_quality_factor" : 0,
            "spectrum_analyzer_run" : 1,

            "main_coupling_mode" : 1,
            "main_hpf_gain_attenuator" : 10,

            "main_source_selector" : 1,
            "main_source_gain_attenuator" : 0,
            "main_source_autozero" : 0,

            "second_source_selector" : 5,
            "second_source_gain_attenuator" : 0,

            "main_loudness_attenuator" : 0,
            "main_loudness_freq" : 0,
            "main_loudness_highboost" : 0,
            "main_loudness_softstep" : 0,

            "main_volume_attenuator" : 56,
            "main_volume_softstep" : 0,

            "main_treble_attenuator" : 0,
            "main_treble_center_freq" : 0,

            "main_middle_attenuator" : 0,
            "main_middle_center_freq" : 0,
            "main_middle_quality_factor" : 0,
            "main_middle_softstep" : 0,

            "main_bass_attenuator" : 0,
            "main_bass_center_freq" : 0,
            "main_bass_quality_factor" : 0,
            "main_bass_softstep" : 0,
            "main_bass_dc_mode" : 1,

            "speaker_front_left_attenuator" : 56,
            "speaker_front_left_softstep" : 0,

            "speaker_front_right_attenuator" : 56,
            "speaker_front_right_softstep" : 0,

            "speaker_rear_source_selector" : 0,

            "speaker_rear_left_attenuator" : 56,
            "speaker_rear_left_softstep" : 0,

            "speaker_rear_right_attenuator" : 56,
            "speaker_rear_right_softstep" : 0,

            "subwoofer_attenuator" : 56,
            "subwoofer_cutoff_freq" : 0,
            "subwoofer_softstep" : 0,
            "subwoofer_enable" : 1,

            "mixing_attenuator" : 56,
            "mixing_to_front_left" : 1,
            "mixing_to_front_right" : 1,
            "mixing_softstep" : 0,
            "mixing_enable" : 1
        }

        self.__tda7419_switchers_shift_register_mask = {
            "global_softmute_switch" :          (0, 2, 0b11111110),
            "global_pin_influence_for_mute" :   (1, 2, 0b11111101),
            "global_softmute_time" :            (2, 2, 0b11110011),
            "global_softstep_time" :            (4, 2, 0b10001111),
            "global_clock_fast_mode" :          (7, 2, 0b01111111),

            "global_external_reference" :       (7, 4, 0b01111111),
            "global_enable_smoothing_filter" :  (7, 8, 0b01111111),

            "global_reset_mode" :               (1,16, 0b11111101),
            "global_reset" :                    (4,16, 0b11101111),
            "global_external_clock_source" :    (5,16, 0b11011111),

            "global_testing_mode_enable" :      (0, 17, 0b11111110),
            "global_testing_multiplexer" :      (1, 17, 0b11000001),

            "spectrum_analyzer_source_selector" :   (2, 16, 0b11111011),
            "spectrum_analyzer_quality_factor" :    (0, 16, 0b11111110),
            "spectrum_analyzer_run" :               (3, 16, 0b11110111),

            "main_coupling_mode" :              (6, 16, 0b00111111),
            "main_hpf_gain_attenuator" :        (4, 9, 0b00001111),

            "main_source_selector" :            (0, 0, 0b11111000),
            "main_source_gain_attenuator" :     (3, 0, 0b10000111),
            "main_source_autozero" :            (7, 0, 0b01111111),

            "second_source_selector" :          (0, 7, 0b11111000),
            "second_source_gain_attenuator" :   (3, 7, 0b10000111),

            "main_loudness_attenuator" :        (0, 1, 0b11110000),
            "main_loudness_freq" :              (4, 1, 0b11001111),
            "main_loudness_highboost" :         (6, 1, 0b10111111),
            "main_loudness_softstep" :          (7, 1, 0b01111111),

            "main_volume_attenuator" :          (0, 3, 0b10000000),
            "main_volume_softstep" :            (7, 3, 0b01111111),

            "main_treble_attenuator" :          (0, 4, 0b11100000),
            "main_treble_center_freq" :         (5, 4, 0b10011111),

            "main_middle_attenuator" :          (0, 5, 0b11100000),
            "main_middle_center_freq" :         (2, 8, 0b11110011),
            "main_middle_quality_factor" :      (5, 5, 0b10011111),
            "main_middle_softstep" :            (7, 5, 0b01111111),

            "main_bass_attenuator" :            (0, 6, 0b11100000),
            "main_bass_center_freq" :           (4, 8, 0b11001111),
            "main_bass_quality_factor" :        (5, 6, 0b10011111),
            "main_bass_softstep" :              (7, 6, 0b01111111),
            "main_bass_dc_mode" :               (6, 8, 0b10111111),

            "speaker_front_left_attenuator" :   (0, 10, 0b10000000),
            "speaker_front_left_softstep" :     (7, 10, 0b01111111),

            "speaker_front_right_attenuator" :  (0, 11, 0b10000000),
            "speaker_front_right_softstep" :    (7, 11, 0b01111111),

            "speaker_rear_source_selector" :    (7, 7, 0b01111111),

            "speaker_rear_left_attenuator" :    (0, 12, 0b10000000),
            "speaker_rear_left_softstep" :      (7, 12, 0b01111111),

            "speaker_rear_right_attenuator" :   (0, 13, 0b10000000),
            "speaker_rear_right_softstep" :     (7, 13, 0b01111111),

            "subwoofer_attenuator" :            (0, 15, 0b10000000),
            "subwoofer_cutoff_freq" :           (0, 8, 0b11111100),
            "subwoofer_softstep" :              (7, 15, 0b01111111),
            "subwoofer_enable" :                (3, 9, 0b11110111),

            "mixing_attenuator" :               (0, 14, 0b10000000),
            "mixing_to_front_left" :            (0, 9, 0b11111110),
            "mixing_to_front_right" :           (1, 9, 0b11111101),
            "mixing_softstep" :                 (7, 14, 0b01111111),
            "mixing_enable" :                   (2, 9, 0b11111011)
        }

        self.__tda7419_registers = {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
            9 : 0,
            10 : 0,
            11 : 0,
            12 : 0,
            13 : 0,
            14 : 0,
            15 : 0,
            16 : 0,
            17 : 0
        }

        if type(self.__i2c_bus_number) is int:
            try:
                smbus.SMBus.open(self.__i2c_bus_number)
                smbus.SMBus.write_quick(self.__chip_address)
            except Exception as error:
                raise error

        if self.__path_to_load_from is not None:
            if os.path.exists(self.__path_to_load_from):
                with open(file=self.__path_to_load_from, mode="r", encoding="utf8") as self.__opened_file:
                    self.__tda7419_switchers = json_load(self.__opened_file)
            else:
                print("settings file not found")
        else:
            print("settings file not given")

        self.__listd = list(self.__tda7419_switchers.keys())
        self.__listd.remove("global_testing_mode")
        self.__listd.remove("global_autozero_remain")
        self.__listd.remove("global_auto_increment_mode")
        for item in self.__listd:
            self.__shift, self.__register, self.__mask = self.__tda7419_switchers_shift_register_mask.get(item)

            self.__tda7419_registers[self.__register] = (
                self.__tda7419_registers.get(self.__register) & self.__mask
                ) | (
                    self.__tda7419_switchers.get(item) << self.__shift
                    )

        for item in self.__tda7419_registers:
            self.__send_i2c(item)

    def save_settings(self, path_to_save="./tda7419_settings.json"):
        try:
            with open(
            file=path_to_save,
            mode = "w" if os.path.exists(path_to_save) else "x",
            encoding="utf8"
            ) as self.__opened_file:
                json_dump(fp=self.__opened_file, obj=self.__tda7419_switchers)
            return os.path.abspath(path_to_save)
        except IOError as error:
            raise error

# ===========================================================================================


    def __send_switch(self, switch_to_send):

        self.__shift, self.__register, self.__mask = self.__tda7419_switchers_shift_register_mask.get(switch_to_send)

        self.__tda7419_registers[self.__register] = (
            self.__tda7419_registers.get(self.__register) & self.__mask
            ) | (
                self.__tda7419_switchers.get(switch_to_send) << self.__shift
                )

        self.__send_i2c(self.__register)

        return self

    def __send_i2c(self, register=0):
        self.__address = (
            self.__tda7419_switchers.get("global_testing_mode") << 7 | 
            self.__tda7419_switchers.get("global_autozero_remain") << 6 | 
            self.__tda7419_switchers.get("global_auto_increment_mode") << 5 | 
            register
        )

        self.__data = self.__tda7419_registers.get(register)

        return self

# ===========================================================================================
    def global_testing_mode(self, new_state=None):
        if new_state == None:
            result = bool(self.__tda7419_switchers.get("global_testing_mode"))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_testing_mode"] = int(new_state)
            self.__send_switch("global_testing_mode")
            return new_state
        else: 
            raise TypeError("Argument must be bool")

    def global_autozero_remain(self, new_state=None):
        if new_state == None:
            result = bool(self.__tda7419_switchers.get("global_autozero_remain"))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_autozero_remain"] = int(new_state)
            self.__send_switch("global_autozero_remain")
            return new_state
        else: 
            raise TypeError("Argument must be bool")

    def global_auto_increment_mode(self, new_state=None):
        if new_state == None:
            result = bool(self.__tda7419_switchers.get("global_auto_increment_mode"))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_auto_increment_mode"] = int(new_state)
            self.__send_switch("global_auto_increment_mode")
            return new_state
        else: 
            raise TypeError("Argument must be bool")
# ===========================================================================================

    def global_softmute_switch(self, new_state=None):
        '''True = Soft-mute ON = 0 in r2b0
        False = Soft-mute OFF = 1 in r2b0'''
        if new_state == None:
            result = not(bool(self.__tda7419_switchers.get("global_softmute_switch")))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_softmute_switch"] = int(not(new_state))
            self.__send_switch("global_softmute_switch")
            return new_state
        else: 
            raise TypeError("Argument must be bool")

    def global_pin_influence_for_mute(self, new_state=None):
        '''True = Mute Pin enabled = 0 in r2b1
        False = Mute Pin disabled = 1 in r2b1'''
        if new_state == None:
            result = not(bool(self.__tda7419_switchers.get("global_pin_influence_for_mute")))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_pin_influence_for_mute"] = int(not(new_state))
            self.__send_switch("global_pin_influence_for_mute")
            return new_state
        else: 
            raise TypeError("Argument must be bool")

    def global_softmute_time(self, new_state=None):
        self.__global_softmute_time_truth_table = ["0.48 ms", "0.96 ms", "123 ms"]
        if new_state == None:
            result = self.__global_softmute_time_truth_table[ self.__tda7419_switchers.get("global_softmute_time") ]
            return result
        elif type(new_state) is str:
            if new_state in self.__global_softmute_time_truth_table:
                self.__tda7419_switchers["global_softmute_time"] = self.__global_softmute_time_truth_table.index(new_state)
                self.__send_switch("global_softmute_time")
                return new_state
            else:
                raise ValueError("Wrong value. Chooze Softmute between \"0.48 ms\", \"0.96 ms\" and \"123 ms\".")
        else:
            raise TypeError("Argument must be string")

    def global_softstep_time(self, new_state=None):
        self.__global_softstep_time_truth_table = ["0.160 ms", "0.321 ms", "0.642 ms", "1.28 ms", "2.56 ms", "5.12 ms", "10.24 ms", "20.48 ms"]
        if new_state == None:
            result = self.__global_softstep_time_truth_table[ self.__tda7419_switchers.get("global_softstep_time") ]
            return result
        elif type(new_state) is str:
            if new_state in self.__global_softstep_time_truth_table:
                self.__tda7419_switchers["global_softstep_time"] = self.__global_softstep_time_truth_table.index(new_state)
                self.__send_switch("global_softstep_time")
                return new_state
            else:
                raise ValueError("Wrong value. Chooze Softmute between \"0.160 ms\", \"0.321 ms\", \"0.642 ms\", \"1.28 ms\", \"2.56 ms\", \"5.12 ms\", \"10.24 ms\", \"20.48 ms\".")
        else:
            raise TypeError("Argument must be string")

    def global_clock_fast_mode(self, new_state=None):
        '''True = Clock fast mode ON = 0 in r2b7
        False = Clock fast mode OFF = 1 in r2b7'''
        if new_state == None:
            result = not(bool(self.__tda7419_switchers.get("global_clock_fast_mode")))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_clock_fast_mode"] = int(not(new_state))
            self.__send_switch("global_clock_fast_mode")
            return new_state
        else: 
            raise TypeError("Argument must be bool")

    def global_external_reference(self, new_state=None):
        '''True = External Vref (4 V) = 0 in r4b7
        False = Internal Vref (3.3 V) = 1 in r4b7'''
        if new_state == None:
            result = not(bool(self.__tda7419_switchers.get("global_external_reference")))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_external_reference"] = int(not(new_state))
            self.__send_switch("global_external_reference")
            return new_state
        else: 
            raise TypeError("Argument must be bool")

    def global_enable_smoothing_filter(self, new_state=None):
        '''True = Smoothing Filter ON = 0 in r8b7
        False = Smoothing Filter OFF = 1 in r8b7'''
        if new_state == None:
            result = not(bool(self.__tda7419_switchers.get("global_enable_smoothing_filter")))
            return result
        elif type(new_state) is bool:
            self.__tda7419_switchers["global_enable_smoothing_filter"] = int(not(new_state))
            self.__send_switch("global_enable_smoothing_filter")
            return new_state
        else: 
            raise TypeError("Argument must be bool")

    def global_reset_mode(self, new_state=None):
        pass
    def global_reset(self, new_state=None):
        pass
    def global_external_clock_source(self, new_state=None):
        pass
    
    def system_testing_mode(self, enable=None, mode=None):
        '''
        '''

        if mode != None:
            if type(mode) is str:
                self.__system_testing_mode_truth_table = {
                    "Left_In_gain" : 0,
                    # "Left_In_gain" : 1,
                    "Left_Loudness" : 2,
                    # "Left_Loudness" : 3,
                    "Left_Volume" : 4,
                    # "Left_Volume" : 5,
                    "Left_Treble" : 6,
                    # "Left_Treble" : 7,
                    "Left_Middle" : 8,
                    "SMCLK" : 9,
                    "Left_Bass" : 10,
                    "VrefSCR" : 11,
                    "VGB1.26" : 12,
                    "SSCLK" : 13,
                    "Clock200" : 14,
                    "Mon" : 15,
                    "Ref5V5" : 16,
                    "BPout<1>" : 18,
                    "BPout<2>" : 20,
                    "BPout<3>" : 22,
                    "BPout<4>" : 24,
                    "BPout<5>" : 26,
                    "BPout<6>" : 28,
                    "BPout<7>" : 30
                    }

                if mode in self.__system_testing_mode_truth_table.keys():
                    self.__tda7419_switchers["global_testing_multiplexer"] = self.__system_testing_mode_truth_table.get(mode)
                    self.__send_switch("global_testing_multiplexer")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__system_testing_mode_truth_table.keys()))
            else: 
                raise TypeError("Argument must be str type.")

        if enable != None:
            if type(enable) is bool:
                self.__tda7419_switchers["global_testing_mode_enable"] = int(enable)
                self.__send_switch("global_testing_mode_enable")
            else: 
                raise TypeError("Argument must be bool.")

        return self
    
    def spectrum_analyzer(self, source_selector=None, quality_factor=None, run=None):
        '''
        '''

        if source_selector != None:
            self.__spectrum_analyzer_source_selector_truth_table = ["bass", "in_gain"]
            if type(source_selector) is str:
                if source_selector in self.__spectrum_analyzer_source_selector_truth_table:
                    self.__tda7419_switchers["spectrum_analyzer_source_selector"] = self.__spectrum_analyzer_source_selector_truth_table.index(source_selector)
                    self.__send_switch("spectrum_analyzer_source_selector")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__spectrum_analyzer_source_selector_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if quality_factor != None:
            self.__spectrum_analyzer_quality_factor_truth_table = ["bass", "in_gain"]
            if type(quality_factor) is str:
                if quality_factor in self.__spectrum_analyzer_quality_factor_truth_table:
                    self.__tda7419_switchers["spectrum_analyzer_quality_factor"] = self.__spectrum_analyzer_quality_factor_truth_table.index(quality_factor)
                    self.__send_switch("spectrum_analyzer_quality_factor")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__spectrum_analyzer_quality_factor_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if run != None:
            if type(run) is bool:
                self.__tda7419_switchers["spectrum_analyzer_run"] = int(not(run))
                self.__send_switch("spectrum_analyzer_run")
            else: 
                raise TypeError("Argument must be bool")

        return self

    def main_coupling(self, mode=None, hpf_gain_attenuator=None):
        '''
        '''

        if hpf_gain_attenuator != None:
            self.__hpf_gain_attenuator_truth_table = []
            if type(hpf_gain_attenuator) is int:
                if hpf_gain_attenuator == 0:
                    self.__tda7419_switchers["main_hpf_gain_attenuator"] = 10
                elif hpf_gain_attenuator in range(4,23,2):
                    self.__tda7419_switchers["main_hpf_gain_attenuator"] = int((hpf_gain_attenuator-4)/2)
                else:
                    raise ValueError ("Argument value must be in range 4,6,8...20,22 or 0.")
                self.__send_switch("main_hpf_gain_attenuator")
            else:
                raise TypeError ("Argument must be int type.")
        
        if mode != None:
            self.__main_coupling_mode_truth_table = ["dc", "ac_ingain", "dc_hpf", "ac_bass"]
            if type(mode) is str:
                if mode in self.__main_coupling_mode_truth_table:
                    self.__tda7419_switchers["main_coupling_mode"] = self.__main_coupling_mode_truth_table.index(mode)
                    self.__send_switch("main_coupling_mode")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_coupling_mode_truth_table))
            else:
                raise TypeError("Argument must be str type.")

        return self

    def main_source(self, selector=None, gain_attenuator=None, autozero=None):
        '''
        '''

        if selector != None:
            self.__main_source_selector_truth_table = ["qd", "se1", "se2", "se3", "se4", "mute"]
            if type(selector) is str:
                if selector in self.__main_source_selector_truth_table:
                    self.__tda7419_switchers["main_source_selector"] = self.__main_source_selector_truth_table.index(selector)
                    self.__send_switch("main_source_selector")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_source_selector_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if gain_attenuator != None:
            if type(gain_attenuator) is int:
                if gain_attenuator in range(0,16):
                    self.__tda7419_switchers["main_source_gain_attenuator"] = gain_attenuator
                    self.__send_switch("main_source_gain_attenuator")
                else:
                    raise ValueError("Attenuator value must be in range 0...15.")
            else:
                raise TypeError("Attenuator value must be int type (0...15).")

        if autozero != None:
            if type(autozero) is bool:
                self.__tda7419_switchers["main_source_autozero"] = int(not(autozero))
                self.__send_switch("main_source_autozero")
            else: 
                raise TypeError("Argument must be bool")

        return self

    def second_source(self, selector=None, gain_attenuator=None):
        '''
        '''

        if selector != None:
            self.__second_source_selector_truth_table = ["qd", "se1", "se2", "se3", "se4", "mute"]
            if type(selector) is str:
                if selector in self.__second_source_selector_truth_table:
                    self.__tda7419_switchers["second_source_selector"] = self.__second_source_selector_truth_table.index(selector)
                    self.__send_switch("second_source_selector")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__second_source_selector_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if gain_attenuator != None:
            if type(gain_attenuator) is int:
                if gain_attenuator in range(0,16):
                    self.__tda7419_switchers["second_source_gain_attenuator"] = gain_attenuator
                    self.__send_switch("second_source_gain_attenuator")
                else:
                    raise ValueError("Attenuator value must be in range 0...15.")
            else:
                raise TypeError("Attenuator value must be int type (0...15).")

        return self

    def main_loudness(self, attenuator=None, softstep=None, freq=None, highboost=None):
        '''
        '''

        if attenuator != None:
            if type(attenuator) is int:
                if attenuator in range(-15,1):
                    self.__tda7419_switchers["main_loudness_attenuator"] = (attenuator*-1)
                    self.__send_switch("main_loudness_attenuator")
                else:
                    raise ValueError("Attenuator value must be in range 0...-15.")
            else:
                raise TypeError("Attenuator value must be int type (0...-15).")

        if softstep != None:
            if type(softstep) is bool:
                self.__tda7419_switchers["main_loudness_softstep"] = int(not(softstep))
                self.__send_switch("main_loudness_softstep")
            else: 
                raise TypeError("Argument must be bool")

        if freq != None:
            self.__main_loudness_freq_truth_table = ["flat", "400 Hz", "800 Hz", "2400 Hz"]
            if type(freq) is str:
                if freq in self.__main_loudness_freq_truth_table:
                    self.__tda7419_switchers["main_loudness_freq"] = self.__main_loudness_freq_truth_table.index(freq)
                    self.__send_switch("main_loudness_freq")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_loudness_freq_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if highboost != None:
            if type(softstep) is bool:
                self.__tda7419_switchers["main_loudness_highboost"] = int(not(highboost))
                self.__send_switch("main_loudness_highboost")
            else: 
                raise TypeError("Argument must be bool")
        
        return self

    def main_volume(self, attenuator=None, softstep=None):
        '''
        '''

        if attenuator != None:
            if type(attenuator) is int:
                if attenuator in range(1,16):
                    self.__tda7419_switchers["main_volume_attenuator"] = attenuator
                elif attenuator in range(-80,1):
                    self.__tda7419_switchers["main_volume_attenuator"] = (attenuator*-1)+16
                else:
                    raise ValueError("Attenuator value must be in range -80...15.")
                self.__send_switch("main_volume_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-80...15).")

        if softstep != None:
            if type(softstep) is bool:
                self.__tda7419_switchers["main_volume_softstep"] = int(not(softstep))
                self.__send_switch("main_volume_softstep")
            else: 
                raise TypeError("Argument must be bool")

        return self

    def main_treble(self, attenuator=None, center_freq=None):

        if attenuator != None:
            if type(attenuator) is int:
                if attenuator in range(-15,0):
                    self.__tda7419_switchers["main_treble_attenuator"] = attenuator*(-1)
                elif attenuator in range(0,16):
                    self.__tda7419_switchers["main_treble_attenuator"] = attenuator+16
                else:
                    raise ValueError("Attenuator value must be in range -15...15.")
                self.__send_switch("main_treble_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-15...15).")

        if center_freq != None:
            self.__main_treble_center_freq_truth_table = ["10.0 kHz", "12.5 kHz", "15.0 kHz", "17.5 kHz"]
            if type(center_freq) is str:
                if center_freq in self.__main_treble_center_freq_truth_table:
                    self.__tda7419_switchers["main_treble_center_freq"] = self.__main_treble_center_freq_truth_table.index(center_freq)
                    self.__send_switch("main_treble_center_freq")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_treble_center_freq_truth_table))
            else:
                raise TypeError("Argument must be str.")

        return self

    def main_middle(self, attenuator=None, center_freq=None, quality_factor=None, softstep=None):
        '''
        '''

        if attenuator != None:
            if type(attenuator) is int:
                if attenuator in range(-15,0):
                    self.__tda7419_switchers["main_middle_attenuator"] = attenuator*-1
                elif attenuator in range(0,16):
                    self.__tda7419_switchers["main_middle_attenuator"] = attenuator+16
                else:
                    raise ValueError("Attenuator value must be in range -15...15.")
                self.__send_switch("main_middle_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-15...15).")

        if softstep != None:
            if type(softstep) is bool:
                self.__tda7419_switchers["main_middle_softstep"] = int(not(softstep))
                self.__send_switch("main_middle_softstep")
            else:
                raise TypeError("Argument must be bool")

        if quality_factor != None:
            self.__main_middle_quality_factor_truth_table = ["0.5", "0.75", "1.0", "1.25"]
            if type(quality_factor) is str:
                if quality_factor in self.__main_middle_quality_factor_truth_table:
                    self.__tda7419_switchers["main_middle_quality_factor"] = self.__main_middle_quality_factor_truth_table.index(quality_factor)
                    self.__send_switch("main_middle_quality_factor")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_middle_quality_factor_truth_table))
            else:
                raise TypeError("Argument must be str.")
        
        if center_freq != None:
            self.__main_middle_center_freq_truth_table = ["0.5 kHz", "1.0 kHz", "1.5 kHz", "2.5 kHz"]
            if type(center_freq) is str:
                if center_freq in self.__main_treble_center_freq_truth_table:
                    self.__tda7419_switchers["main_middle_center_freq"] = self.__main_middle_center_freq_truth_table.index(center_freq)
                    self.__send_switch("main_middle_center_freq")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_middle_center_freq_truth_table))
            else:
                raise TypeError("Argument must be str.")
        
        return self

    def main_bass(self, attenuator=None, center_freq=None, quality_factor=None, softstep=None, dc_mode=None):
        '''
        '''

        if attenuator != None:
            if type(attenuator) is int:
                if attenuator in range(-15,0):
                    self.__tda7419_switchers["main_bass_attenuator"] = attenuator*-1
                elif attenuator in range(0,16):
                    self.__tda7419_switchers["main_bass_attenuator"] = attenuator+16
                else:
                    raise ValueError("Attenuator value must be in range -15...15.")
                self.__send_switch("main_bass_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-15...15).")

        if softstep != None:
            if type(softstep) is bool:
                self.__tda7419_switchers["main_bass_softstep"] = int(not(softstep))
                self.__send_switch("main_bass_softstep")
            else:
                raise TypeError("Argument must be bool")

        if quality_factor != None:
            self.__main_bass_quality_factor_truth_table = ["1.0", "1.25", "1.5", "2.0"]
            if type(quality_factor) is str:
                if quality_factor in self.__main_bass_quality_factor_truth_table:
                    self.__tda7419_switchers["main_bass_quality_factor"] = self.__main_bass_quality_factor_truth_table.index(quality_factor)
                    self.__send_switch("main_bass_quality_factor")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_bass_quality_factor_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if center_freq != None:
            self.__main_bass_center_freq_truth_table = ["60 Hz", "80 Hz", "100 Hz", "200 Hz"]
            if type(center_freq) is str:
                if center_freq in self.__main_treble_center_freq_truth_table:
                    self.__tda7419_switchers["main_bass_center_freq"] = self.__main_bass_center_freq_truth_table.index(center_freq)
                    self.__send_switch("main_bass_center_freq")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__main_bass_center_freq_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if dc_mode != None:
            if type(dc_mode) is bool:
                self.__tda7419_switchers["main_bass_dc_mode"] = int(not(dc_mode))
                self.__send_switch("main_bass_dc_mode")
            else:
                raise TypeError("Argument must be bool")

        return self

    def front_speaker(self, left_attenuator=None, left_softstep=None, right_attenuator=None, right_softstep=None):
        '''
        '''

        if left_attenuator != None:
            if type(left_attenuator) is int:
                if left_attenuator in range(1,16):
                    self.__tda7419_switchers["speaker_front_left_attenuator"] = left_attenuator
                elif left_attenuator in range(-80,1):
                    self.__tda7419_switchers["speaker_front_left_attenuator"] = (left_attenuator*-1)+16
                else:
                    raise ValueError("Attenuator value must be in range -80...15.")
                self.__send_switch("speaker_front_left_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-80...15).")

        if left_softstep != None:
            if type(left_softstep) is bool:
                self.__tda7419_switchers["speaker_front_left_softstep"] = int(not(left_softstep))
                self.__send_switch("speaker_front_left_softstep")
            else: 
                raise TypeError("Argument must be bool")

        if right_attenuator != None:
            if type(right_attenuator) is int:
                if right_attenuator in range(1,16):
                    self.__tda7419_switchers["speaker_front_right_attenuator"] = right_attenuator
                elif right_attenuator in range(-80,1):
                    self.__tda7419_switchers["speaker_front_right_attenuator"] = (right_attenuator*-1)+16
                else:
                    raise ValueError("Attenuator value must be in range -80...15.")
                self.__send_switch("speaker_front_right_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-80...15).")

        if right_softstep != None:
            if type(right_softstep) is bool:
                self.__tda7419_switchers["speaker_front_right_softstep"] = int(not(right_softstep))
                self.__send_switch("speaker_front_right_softstep")
            else: 
                raise TypeError("Argument must be bool")

        return self

    def rear_speaker(self, source_selector=None, left_attenuator=None, left_softstep=None, right_attenuator=None, right_softstep=None):
        '''
        '''

        if source_selector != None:
            self.__speaker_rear_source_selector_truth_table = ["main", "second"]
            if type(source_selector) is str:
                if source_selector in self.__speaker_rear_source_selector_truth_table:
                    self.__tda7419_switchers["speaker_rear_source_selector"] = self.__speaker_rear_source_selector_truth_table.index(source_selector)
                    self.__send_switch("speaker_rear_source_selector")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__speaker_rear_source_selector_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if left_attenuator != None:
            if type(left_attenuator) is int:
                if left_attenuator in range(1,16):
                    self.__tda7419_switchers["speaker_rear_left_attenuator"] = left_attenuator
                elif left_attenuator in range(-80,1):
                    self.__tda7419_switchers["speaker_rear_left_attenuator"] = (left_attenuator*-1)+16
                else:
                    raise ValueError("Attenuator value must be in range -80...15.")
                self.__send_switch("speaker_rear_left_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-80...15).")

        if left_softstep != None:
            if type(left_softstep) is bool:
                self.__tda7419_switchers["speaker_rear_left_softstep"] = int(not(left_softstep))
                self.__send_switch("speaker_rear_left_softstep")
            else: 
                raise TypeError("Argument must be bool")

        if right_attenuator != None:
            if type(right_attenuator) is int:
                if right_attenuator in range(1,16):
                    self.__tda7419_switchers["speaker_rear_right_attenuator"] = right_attenuator
                elif right_attenuator in range(-80,1):
                    self.__tda7419_switchers["speaker_rear_right_attenuator"] = (right_attenuator*-1)+16
                else:
                    raise ValueError("Attenuator value must be in range -80...15.")
                self.__send_switch("speaker_rear_right_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-80...15).")

        if right_softstep != None:
            if type(right_softstep) is bool:
                self.__tda7419_switchers["speaker_rear_right_softstep"] = int(not(right_softstep))
                self.__send_switch("speaker_rear_right_softstep")
            else: 
                raise TypeError("Argument must be bool")

        return self

    def subwoofer(self, attenuator=None, cutoff_freq=None, softstep=None, enable=None):
        '''
        '''
        
        if attenuator != None:
            if type(attenuator) is int:
                if attenuator in range(1,16):
                    self.__tda7419_switchers["subwoofer_attenuator"] = attenuator
                elif attenuator in range(-80,1):
                    self.__tda7419_switchers["subwoofer_attenuator"] = (attenuator*-1)+16
                else:
                    raise ValueError("Attenuator value must be in range -80...15.")
                self.__send_switch("subwoofer_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-80...15).")

        if softstep != None:
            if type(softstep) is bool:
                self.__tda7419_switchers["subwoofer_softstep"] = int(not(softstep))
                self.__send_switch("subwoofer_softstep")
            else: 
                raise TypeError("Argument must be bool")

        if cutoff_freq != None:
            self.__subwoofer_cutoff_freq_truth_table = ["flat", "80 Hz", "120 Hz", "160 Hz"]
            if type(cutoff_freq) is str:
                if cutoff_freq in self.__main_treble_center_freq_truth_table:
                    self.__tda7419_switchers["subwoofer_cutoff_freq"] = self.__subwoofer_cutoff_freq_truth_table.index(cutoff_freq)
                    self.__send_switch("subwoofer_cutoff_freq")
                else:
                    raise ValueError("Argument must be in: {}".format(self.__subwoofer_cutoff_freq_truth_table))
            else:
                raise TypeError("Argument must be str.")

        if enable != None:
            if type(enable) is bool:
                self.__tda7419_switchers["subwoofer_enable"] = int(not(enable))
                self.__send_switch("subwoofer_enable")
            else: 
                raise TypeError("Argument must be bool")

        return self

    def mixing(self, attenuator=None, front_left=None, front_right=None, softstep=None, enable=None):
        '''
        '''

        if attenuator != None:
            if type(attenuator) is int:
                if attenuator in range(1,16):
                    self.__tda7419_switchers["mixing_attenuator"] = attenuator
                elif attenuator in range(-80,1):
                    self.__tda7419_switchers["mixing_attenuator"] = (attenuator*-1)+16
                else:
                    raise ValueError("Attenuator value must be in range -80...15.")
                self.__send_switch("mixing_attenuator")
            else:
                raise TypeError("Attenuator value must be int type (-80...15).")

        if front_left != None:
            if type(front_left) is bool:
                self.__tda7419_switchers["mixing_to_front_left"] = int(not(front_left))
                self.__send_switch("mixing_to_front_left")
            else: 
                raise TypeError("Argument must be bool")

        if front_right != None:
            if type(front_right) is bool:
                self.__tda7419_switchers["mixing_to_front_right"] = int(not(front_right))
                self.__send_switch("mixing_to_front_right")
            else: 
                raise TypeError("Argument must be bool")

        if softstep != None:
            if type(softstep) is bool:
                self.__tda7419_switchers["mixing_softstep"] = int(not(softstep))
                self.__send_switch("mixing_softstep")
            else: 
                raise TypeError("Argument must be bool")

        if enable != None:
            if type(enable) is bool:
                self.__tda7419_switchers["mixing_enable"] = int(not(enable))
                self.__send_switch("mixing_enable")
            else: 
                raise TypeError("Argument must be bool")

        return self
