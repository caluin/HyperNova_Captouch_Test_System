import MotorDriver
import Constants
import PostProcessing
import datetime
import os
import subprocess
import traceback
import numpy
import time


class TestCases():
    def __init__(self, test_fixture_shared_memory_handler):
        self.motor = MotorDriver.Motor.initialize_new_motor(Constants.MOTOR_COM, "00", 300, 300)
        self.motor.set_params(speed1=2000, acc1=2000, dec1=2000, speed3=10, acc3=400, dec3=400)
        self.motor_off()
        self.test_fixture_shared_memory_handler = test_fixture_shared_memory_handler

    def get_motor_driver_handler(self):
        return self.motor

    def get_motor_position(self):
        x = self.motor.send(f'@01:EX')
        self.motor._serial.write((f'@01:EX' + '\r\n').encode())
        x = self.motor.read()
        self.motor._serial.write((f'@03:EX' + '\r\n').encode())
        y = self.motor.read()
        return x, y

    def motor_off(self):
        self.motor.motors_off()

    def motor_on(self):
        self.motor.motors_on()

    def motor_go_home(self):
        self.motor.go_home()

    def motor_reset(self):
        self.motor.motors_reset()

    def set_motor_position(self, x, y):
        self.motor.go_location(x, y)

    def set_output_filename(self, test_name):
        self.output_filename = str(test_name + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        self.file = open('data/' + self.output_filename + '_raw.txt', 'a')

    def async_dump_logcat(self):
        os.system('adb logcat -c')
        p = subprocess.Popen("adb logcat -s mcuservice", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        num_entries = 0
        while True:
            line = p.stdout.readline()
            try:
                if "[trace  ] {CAPT}: module_captouch.c" in line.decode('utf-8'):
                    if num_entries == Constants.NUM_OF_SAMPLES_PER_MEASUREMENT_NOISE_FULL_SCAN * 2:
                        break
                    print(line.decode('utf-8'))
                    self.file.write(line.decode('utf-8'))
                    self.file.flush()
                    num_entries = num_entries + 1
            except:
                print("TestCases: Unrecognizable character, skip to next line...")
        p.stdout.close()
        p.terminate()

    def async_dump_logcat_press_and_hold(self):
        os.system('adb logcat -c')
        p = subprocess.Popen("adb logcat -s mcuservice", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        num_entries = 0
        while True:
            line = p.stdout.readline()
            try:
                if "[trace  ] {CAPT}: module_captouch.c" in line.decode('utf-8'):
                    # read out value
                    if num_entries == Constants.NUM_OF_SAMPLES_PER_MEASUREMENT_JITTER_LINEARITY:
                        break
                    print(line.decode('utf-8'))
                    self.file.write(line.decode('utf-8'))
                    self.file.flush()
                    num_entries = num_entries + 1
            except:
                print("TestCases: Unrecognizable character, skip to next line...")
        p.stdout.close()
        p.terminate()

    # function open subprocess when it is called with argument, a process handler will be returned. Data capture will happen in the background.
    # function reads the stdout of the process, saves the read to a file and closes the process when it is called with the process handler the second time
    def async_dump_logcat_tap_swipe(self, p=None):
        num_entries = 0
        if p == None:
            os.system('adb logcat -c')
            # execute the subprocess when function gets called the first time
            p = subprocess.Popen("adb logcat -s mcuservice", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return p
        else:
            # start to process the stdout when function gets called the second time
            while True:
                line = p.stdout.readline()
                try:
                    # read out value per NUM_OF_SAMPLES_PER_MEASUREMENT_GESTURE
                    if (num_entries == Constants.NUM_OF_SAMPLES_PER_MEASUREMENT_GESTURE):
                        num_entries = 0
                        break
                    print(line.decode('utf-8'))
                    self.file.write(line.decode('utf-8'))
                    self.file.flush()
                    num_entries = num_entries + 1
                except:
                    print("TestCases: Unrecognizable character, skip to next line...")
            p.stdout.close()
            p.terminate()
            return 0

    def setup_probe_coordinates(self, str, x_min, x_max, y_reference):

        if str == 'Full_Scan_Measurement':
            # take rang of X positions
            X = range(x_min, x_max, Constants.MOTOR_X_STEP_SIZE_IN_MOTOR_UNIT)
            # calculate Y position ranges
            # exponential increase distances??
            n = float(Constants.MOTOR_Y_STEP_SIZE_INCREMENT_BASE_MOTOR_UNIT)
            Y = [int(i) for i in list(y_reference + numpy.array(
                [0, n ** 3, n ** 4, n ** 5, n ** 6, n ** 7, n ** 8, n ** 9, n ** 10, n ** 11, n ** 12, n ** 13,
                 n ** 14, n ** 15]) * Constants.MOTOR_Y_STEP_SIZE_IN_MOTOR_UNIT) if
                 i <= Constants.MOTOR_Y_ABSOLUTE_POSITION_IN_MOTOR_UNIT]
            if len(Y) == 0:
                print('TestCases: Y distance is too large, extend probe to touch glass and redo the calibration.')

        # x_min, x_max, y_reference not used in this case
        elif str == 'Arbitrary_X_Hover_Measurement':
            # take X Y positions
            var = self.get_motor_position()
            X = [int(var[0].strip())]

            # calculate Y position ranges
            # exponential increase distances or linearly increase distances
            n = float(Constants.MOTOR_Y_STEP_SIZE_INCREMENT_BASE_MOTOR_UNIT)
            Y = [int(i) for i in list(y_reference + numpy.array(
                [0, n ** 3, n ** 4, n ** 5, n ** 6, n ** 7, n ** 8, n ** 9, n ** 10, n ** 11, n ** 12, n ** 13,
                 n ** 14, n ** 15]) * Constants.MOTOR_Y_STEP_SIZE_IN_MOTOR_UNIT) if
                 i <= Constants.MOTOR_Y_ABSOLUTE_POSITION_IN_MOTOR_UNIT]
            if len(Y) == 0:
                print('TestCases: Y distance is too large, extend probe to touch glass and redo the calibration.')

        # linearity/jitter: scan(press) through X direction from x_min to x_max at Y=0
        elif str == 'Linearity_Jitter_Measurement':
            # take rang of X positions
            X = range(x_min, x_max, Constants.MOTOR_X_STEP_SIZE_IN_MOTOR_UNIT)
            # take current Y position as starting point
            Y = [y_reference]

        # x_min, x_max, y_reference not used in this case
        elif str == 'Single_Tap_Measurement' or str == 'Double_Tap_Measurement' or str == 'Triple_Tap_Measurement':
            var = self.get_motor_position()
            # take current X position
            X = [int(var[0].strip())]
            # take current Y position
            Y = [int(var[1].strip())]
            Y = [y_reference]

        elif str == 'Swipe_Backward_Measurement' or str == 'Swipe_Forward_Measurement':
            # take rang of X positions
            X = [x_min, x_max]
            # take current Y position
            Y = [y_reference]

        return X, Y

    def noise_measurement(self, x_min, y_reference):
        try:
            try:
                # prepare the file to write
                self.set_output_filename('Noise_Measurement')
                print('TestCases: Noise measurement started...')
                # write motor coordinates
                self.file.write("motor position," + str(0 * 88 / 12000) + ',' + str(
                    (0 - y_reference) * 25.4 / 5097) + '\n')
                self.file.flush()
                # motor moves to the target location and disengage
                self.motor.go_home()
                # process the tap log and close the process
                self.async_dump_logcat()
                print('TestCases: Noise Measurement completed.')
                self.file.close()
                print('TestCases: Processing data...')
                PostProcessing.post_process_noise_full_scan_x_hover('data/' + self.output_filename + '_raw.txt')
                print('TestCases: Data processing completed.')
            except:
                print('TestCases: Error-Test error, check the noise_measurement function.')
                print(traceback.print_exc())
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def full_scan_measurement(self, x_min, x_max, y_reference):
        try:
            try:
                # prepare the file to write
                self.set_output_filename('Full_Scan_Measurement')
                # set X,Y coordinates
                X, Y = self.setup_probe_coordinates('Full_Scan_Measurement', x_min, x_max, y_reference)
                forward = True
                for y in Y:
                    if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                        if forward == True:
                            x_list = list(X)
                            forward = False
                        else:
                            x_list = list(reversed(X))
                            forward = True
                        for x in x_list:
                            if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                                print('TestCases: Full Scan Measurement started...')
                                # write motor coordinates
                                self.file.write("motor position," + str((x - x_min) * 88 / 12000) + ',' + str(
                                    (y - y_reference) * 25.4 / 5097) + '\n')
                                self.file.write("motor actual coordinates," + str(x) + ',' + str(y) + '\n')
                                self.file.flush()
                                # motor moves to the target location and disengage
                                self.motor.go_location(x, y)
                                # process the tap log and close the process
                                self.async_dump_logcat()
                                print('TestCases: Full Scan Measurement paused...')
                            else:
                                # test is interrupted
                                break
                    else:
                        # test is interrupted
                        break
                self.motor.go_home()
                print('TestCases: Full Scan Measurement completed.')
                self.file.close()
                print('TestCases: Processing data...')
                PostProcessing.post_process_noise_full_scan_x_hover('data/' + self.output_filename + '_raw.txt')
                print('TestCases: Data processing completed.')
            except:
                print('TestCases: Error-Test error or Test interrupted, check the full_scan_measurement function.')
                print(traceback.print_exc())
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def arbitrary_x_hover_measurement(self, x_min, x_max, y_reference):
        try:
            try:
                # prepare the file to write
                self.set_output_filename('Arbitrary_X_Hover_Measurement')
                # set X,Y coordinates
                X, Y = self.setup_probe_coordinates('Arbitrary_X_Hover_Measurement', x_min, x_max, y_reference)
                x = X[0]
                for y in Y:
                    if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                        print('TestCases: Arbitrary_X_Hover_Measurement started...')
                        # write motor coordinates
                        self.file.write(
                            "motor position," + str((x - x_min) * 88 / 12000) + ',' + str(
                                (y - Y[0]) * 25.4 / 5097) + '\n')
                        self.file.write("motor actual coordinates," + str(x) + ',' + str(y) + '\n')
                        self.file.flush()
                        # motor moves to the target location and disengage
                        self.motor.go_location(x, y)
                        # process the tap log and close the process
                        self.async_dump_logcat()
                        print('TestCases: Arbitrary_X_Hover_Measurement paused...')
                    else:
                        # test is interrupted
                        break
                self.motor.go_home()
                print('TestCases: Arbitrary X Hover Measurement completed.')
                self.file.close()
                print('TestCases: Processing data...')
                PostProcessing.post_process_noise_full_scan_x_hover('data/' + self.output_filename + '_raw.txt')
                print('TestCases: Data processing completed.')
            except:
                print('TestCases: Error-Test error or Test interrupted, check the arbitrary_x_hover_measurement function.')
                print(traceback.print_exc())
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def linearity_jitter_measurement(self, x_min, x_max, y_reference):
        try:
            # prepare the file to write
            self.set_output_filename('Linearity_Jitter_Measurement')
            # set X,Y coordinates
            X, Y = self.setup_probe_coordinates('Linearity_Jitter_Measurement', x_min, x_max, y_reference)
            y = Y[0]
            x_list = list(X)
            #turn on motor
            self.motor_on()
            for x in x_list:
                if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                    print('TestCases: Linearity Jitter Measurement started...')
                    # write motor coordinates
                    self.file.write("motor position," + str((x - x_min) * 88 / 12000) + ',' + str(
                        (y - y_reference) * 25.4 / 5097) + '\n')
                    self.file.write("motor actual coordinates," + str(x) + ',' + str(y) + '\n')
                    self.file.flush()
                    # motor moves to the target location
                    self.motor.go_location_nonstop(x, y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                    # motor press
                    self.motor.go_location_nonstop(x, y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                    # process the tap log and close the process
                    self.async_dump_logcat_press_and_hold()
                    time.sleep(0.2)
                    # release motor
                    self.motor.go_location_nonstop(x, y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                    print('TestCases: Linearity Jitter Measurement paused...')
                else:
                    # test is interrupted
                    break
            self.motor.go_home()
            print('TestCases: Linearity Jitter Measurement completed.')
            self.file.close()
            print('TestCases: Processing data...')
            PostProcessing.post_process_linearity_jitter('data/' + self.output_filename + '_raw.txt')
            print('TestCases: Data processing completed.')
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            print('TestCases: Error-Test Error, check the linearity_jitter_measurement function.')
            print(traceback.print_exc())
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def single_tap_measurement(self, iterations, x_min, x_max, y_reference):
        try:
            # prepare the file to write
            self.set_output_filename('Single_Tap_Measurement')
            # set X,Y coordinates
            X, Y = self.setup_probe_coordinates('Single_Tap_Measurement', x_min, x_max, y_reference)
            x = X[0]
            y = Y[0]
            # turn on the motor
            self.motor_on()
            # retract the probe at the beginning of measurement to prevent false trigger
            self.motor.go_location_nonstop(x, y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
            os.system('adb logcat -c')
            # wait for DUT states settling down
            time.sleep(5)
            iteration = 0

            try:
                while iteration != iterations:
                    if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                        print('TestCases: Single Tap Measurement started...')
                        # open asynchronous log and save the process handler
                        p = self.async_dump_logcat_tap_swipe()
                        # write motor coordinates
                        self.file.write("motor position," + str((x - x_min) * 88 / 12000) + ',' + str(
                            (y - y_reference) * 25.4 / 5097) + '\n')
                        self.file.write("motor actual coordinates," + str(x) + ',' + str(y) + '\n')
                        self.file.write("motor tap," + str(iteration + 1) + '\n')
                        self.file.flush()

                        # motor taps
                        self.motor.go_location_nonstop(x,
                                                       y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        self.motor.go_location_nonstop(x,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)

                        # process the tap log and close the process
                        self.async_dump_logcat_tap_swipe(p)
                        print('TestCases: Single Tap Measurement paused...')
                    else:
                        # test is interrupted
                        break
                    iteration += 1

                self.motor.go_home()
                print('TestCases: Measurement completed.')
                self.file.close()
                print('TestCases: Processing data...')
                PostProcessing.post_process_tap('data/' + self.output_filename + '_raw.txt')
                print('TestCases: Data processing completed.')
            except:
                print('Error: Test Error, check the single_tap_measurement function!')
                print(traceback.print_exc())
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def double_tap_measurement(self, iterations, x_min, x_max, y_reference):
        try:
            # prepare the file to write
            self.set_output_filename('Double_Tap_Measurement')
            # set X,Y coordinates
            X, Y = self.setup_probe_coordinates('Double_Tap_Measurement', x_min, x_max, y_reference)
            x = X[0]
            y = Y[0]
            # turn on the motor
            self.motor_on()
            # retract the probe at the beginning of measurement to prevent false trigger
            self.motor.go_location_nonstop(x, y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
            os.system('adb logcat -c')
            # wait for DUT states settling down
            time.sleep(5)
            iteration = 0

            try:
                while iteration != iterations:
                    if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                        print('TestCases: Double Tap Measurement started...')
                        # open asynchronous log and save the process handler
                        p = self.async_dump_logcat_tap_swipe()
                        # write motor coordinates
                        self.file.write("motor position," + str((x - x_min) * 88 / 12000) + ',' + str(
                            (y - y_reference) * 25.4 / 5097) + '\n')
                        self.file.write("motor actual coordinates," + str(x) + ',' + str(y) + '\n')
                        self.file.write("motor tap," + str(iteration + 1) + '\n')
                        self.file.flush()

                        # motor taps
                        self.motor.go_location_nonstop(x,
                                                       y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        self.motor.go_location_nonstop(x,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)

                        self.motor.go_location_nonstop(x, y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        self.motor.go_location_nonstop(x, y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        # process the tap log and close the process
                        # process the tap log and close the process
                        self.async_dump_logcat_tap_swipe(p)
                        print('TestCases: Double Tap Measurement paused...')
                    else:
                        # test is interrupted
                        break
                    iteration += 1

                self.motor.go_home()
                print('TestCases: Measurement completed.')
                self.file.close()
                print('TestCases: Processing data...')
                PostProcessing.post_process_tap('data/' + self.output_filename + '_raw.txt')
                print('TestCases: Data processing completed.')
            except:
                print('Error: Test Error, check the double_tap_measurement function!')
                print(traceback.print_exc())
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def triple_tap_measurement(self, iterations, x_min, x_max, y_reference):
        try:
            # prepare the file to write
            self.set_output_filename('Triple_Tap_Measurement')
            # set X,Y coordinates
            X, Y = self.setup_probe_coordinates('Triple_Tap_Measurement', x_min, x_max, y_reference)
            x = X[0]
            y = Y[0]
            # turn on the motor
            self.motor_on()
            # retract the probe at the beginning of measurement to prevent false trigger
            self.motor.go_location_nonstop(x, y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
            os.system('adb logcat -c')
            # wait for DUT states settling down
            time.sleep(5)
            iteration = 0

            try:
                while iteration != iterations:
                    if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                        print('TestCases: Triple Tap Measurement started...')
                        # open asynchronous log and save the process handler
                        p = self.async_dump_logcat_tap_swipe()
                        # write motor coordinates
                        self.file.write("motor position," + str((x - x_min) * 88 / 12000) + ',' + str(
                            (y - y_reference) * 25.4 / 5097) + '\n')
                        self.file.write("motor actual coordinates," + str(x) + ',' + str(y) + '\n')
                        self.file.write("motor tap," + str(iteration + 1) + '\n')
                        self.file.flush()

                        # motor taps
                        self.motor.go_location_nonstop(x,
                                                       y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        self.motor.go_location_nonstop(x,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)

                        self.motor.go_location_nonstop(x,
                                                       y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        self.motor.go_location_nonstop(x,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)

                        self.motor.go_location_nonstop(x,
                                                       y - Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        self.motor.go_location_nonstop(x,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT)
                        # process the tap log and close the process
                        self.async_dump_logcat_tap_swipe(p)
                        print('TestCases: Triple Tap Measurement paused...')
                    else:
                        # test is interrupted
                        break
                    iteration += 1

                self.motor.go_home()
                print('TestCases: Measurement completed.')
                self.file.close()
                print('TestCases: Processing data...')
                PostProcessing.post_process_tap('data/' + self.output_filename + '_raw.txt')
                print('TestCases: Data processing completed.')
            except:
                print('Error: Test Error, check the double_tap_measurement function!')
                print(traceback.print_exc())
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def swipe_forward_measurement(self, iterations, x_min, x_max, y_reference):
        try:
            # prepare the file to write
            self.set_output_filename('Swipe_Forward_Measurement')
            # set X,Y coordinates
            X, Y = self.setup_probe_coordinates('Swipe_Forward_Measurement', x_min, x_max, y_reference)
            x_start = X[1]
            x_end = X[0]
            y = Y[0]
            # turn on the motor
            self.motor_on()
            # retract the probe at the beginning of measurement to prevent false trigger
            self.motor.go_location_nonstop(x_start, y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
            os.system('adb logcat -c')
            # wait for DUT states settling down
            time.sleep(5)

            iteration = 0
            try:
                while iteration != iterations:
                    if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                        print('TestCases:Swipe_Forward_Measurement started...')
                        # open asynchronous log and save the process handler
                        p = self.async_dump_logcat_tap_swipe()
                        # write motor coordinates
                        self.file.write(
                            "motor position," + str((x_start - x_min) * 88 / 12000) + ',' + str(
                                (y - y_reference) * 25.4 / 5097) + '\n')
                        self.file.write("motor swipe," + str(iteration + 1) + '\n')
                        self.file.flush()
                        # motor swipe
                        self.motor.go_location_nonstop(x_start,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
                        time.sleep(0.5)
                        self.motor.go_location_nonstop(x_start, y)
                        self.motor.go_location_nonstop(x_end, y)
                        time.sleep(0.5)
                        self.motor.go_location_nonstop(x_end,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
                        # process the tap log and close the process
                        self.async_dump_logcat_tap_swipe(p)
                        print('TestCases:Swipe_Forward_Measurement paused...')
                    else:
                        break
                    iteration += 1

                self.motor.go_home()
                print('TestCases:Swipe_Forward_Measurement completed.')
                self.file.close()
                print('TestCases:Processing data...')
                PostProcessing.post_process_swipe('data/' + self.output_filename + '_raw.txt')
                print('Data processing completed.')
            except:
                self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
                print('Error: Test error, check the swipe_forward_measurement function!')
                print(traceback.print_exc())

            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False

    def swipe_backward_measurement(self, iterations, x_min, x_max, y_reference):
        try:
            # prepare the file to write
            self.set_output_filename('Swipe_Backward_Measurement')
            X, Y = self.setup_probe_coordinates('Swipe_Backward_Measurement', x_min, x_max, y_reference)
            x_start = X[0]
            x_end = X[1]
            y = Y[0]
            # turn on the motor
            self.motor_on()
            # retract the probe at the beginning of measurement to prevent false trigger
            self.motor.go_location_nonstop(x_start, y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
            os.system('adb logcat -c')
            # wait for DUT states settling down
            time.sleep(5)

            iteration = 0
            try:
                while iteration != iterations:
                    if self.test_fixture_shared_memory_handler['test_cases:interrupt'] == False:
                        print('TestCases:Swipe_Backward_Measurement started...')
                        # open asynchronous log and save the process handler
                        p = self.async_dump_logcat_tap_swipe()
                        # write motor coordinates
                        self.file.write(
                            "motor position," + str((x_start - x_min) * 88 / 12000) + ',' + str(
                                (y - y_reference) * 25.4 / 5097) + '\n')
                        self.file.write("motor swipe," + str(iteration + 1) + '\n')
                        self.file.flush()
                        # motor swipe
                        self.motor.go_location_nonstop(x_start,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
                        time.sleep(0.5)
                        self.motor.go_location_nonstop(x_start, y)
                        self.motor.go_location_nonstop(x_end, y)
                        time.sleep(0.5)
                        self.motor.go_location_nonstop(x_end,
                                                       y + Constants.MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT * 5)
                        # process the tap log and close the process
                        self.async_dump_logcat_tap_swipe(p)
                        print('TestCases:Swipe_Backward_Measurement paused...')
                    else:
                        break
                    iteration += 1

                self.motor.go_home()
                print('TestCases:Swipe_Backward_Measurement completed.')
                self.file.close()
                print('TestCases:Processing data...')
                PostProcessing.post_process_swipe('data/' + self.output_filename + '_raw.txt')
                print('Data processing completed.')
            except:
                self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
                print('Error: Test error, check the swipe_backward_measurement function!')
                print(traceback.print_exc())

            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
        except:
            self.motor_off()
            self.test_fixture_shared_memory_handler['test_cases:interrupt'] = False
