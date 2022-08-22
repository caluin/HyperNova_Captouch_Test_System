import threading
from PyQt5.QtCore import QThread, pyqtSignal
import time
from multiprocessing import Manager


# shared memory for multiple TestFixture threads
def shared_memory_initialization():
    manager = Manager()
    test_fixture_shared_content = manager.dict()
    # load default values
    test_fixture_shared_content['calibration:calibration_status'] = False
    test_fixture_shared_content['test_cases:interrupt'] = False

    return test_fixture_shared_content


class TestFixture(QThread):
    # mutex for thread locking
    test_in_progress = threading.Lock()
    # signals from worker
    update_progress = pyqtSignal(str)
    test_complete = pyqtSignal(str)
    calibration_progress = pyqtSignal(str)
    update_motor_position = pyqtSignal(str)

    # class variables, not thread safe

    def __init__(self, test_case, test_handler, test_fixture_shared_memory_handler, parent=None):
        QThread.__init__(self)
        self.test_case = test_case
        self.test_handler = test_handler
        self.test_fixture_shared_memory_handler = test_fixture_shared_memory_handler

    def run(self):
        if self.test_in_progress.locked() == True:
            if self.test_case == "interrupt_test":
                self.update_progress.emit("TestFixture: Test in progress, interrupt test received.")
                # register interrupt in shared memory
                self.test_fixture_shared_memory_handler['test_cases:interrupt'] = True
            else:
                self.update_progress.emit("TestFixture: Test in progress, unable to perform another test.")
        else:
            self.test_in_progress.acquire()
            # main tab
            if self.test_case == 'calibration_step1':
                self.calibration_step1()
                self.calibration_progress.emit("TestFixture: Calibration step1 completed.")

            elif self.test_case == 'calibration_step2':
                self.calibration_step2()
                self.calibration_progress.emit("TestFixture: Calibration step2 Completed.")

            elif self.test_case == 'noise_measurement':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.noise_measurement()
                    self.test_complete.emit("TestFixture: TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'linearity_jitter_measurement':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.linearity_jitter_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'full_scan_measurement':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.full_scan_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'arbitrary_x_hover_measurement':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.arbitrary_x_hover_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'single_tap':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.single_tap_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'double_tap':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.double_tap_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'triple_tap':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.triple_tap_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'swipe_forward':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.swipe_forward_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            elif self.test_case == 'swipe_backward':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.swipe_backward_measurement()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")            # Test completed
            # advance tab
            elif self.test_case == 'set_motor_position':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.set_motor_position()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")
            elif self.test_case == 'get_motor_position':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    x, y = self.get_motor_position()
                    self.update_motor_position.emit(x+' '+y)
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")
            elif self.test_case == 'motor_on':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.motor_on()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")
            elif self.test_case == 'motor_off':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.motor_off()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")
            elif self.test_case == 'motor_go_home':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.motor_go_home()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")
            elif self.test_case == 'motor_reset':
                if self.test_fixture_shared_memory_handler['calibration:calibration_status'] == True:
                    self.motor_reset()
                    self.test_complete.emit("TestFixture: Test completed.")
                else:
                    print("TestFixture: Please perform calibration first. Test aborted.")

            else:
                print("TestFixture: No test in progress. Nothing to interrupt.")  # Test completed

            self.test_in_progress.release()

    def calibration_step1(self):
        print("TestFixture: Calibration_step1")
        self.test_fixture_shared_memory_handler['calibration:calibration_status'] = False
        calibration_x, calibration_y = self.test_handler.get_motor_position()
        # save the position to shared memory
        self.test_fixture_shared_memory_handler['glass_dimensions:calibration_x1'] = int(calibration_x.strip())
        self.test_fixture_shared_memory_handler['glass_dimensions:calibration_y1'] = int(calibration_y.strip())
        self.test_handler.motor_off()
        print("TestFixture Calibration_step1: x-" + calibration_x.strip() + ", y-" + calibration_y.strip())

    def calibration_step2(self):
        print("TestFixture: Calibration_step2")
        calibration_x, calibration_y = self.test_handler.get_motor_position()
        self.test_handler.motor_off()

        # save the postion to shared memory
        self.test_fixture_shared_memory_handler['glass_dimensions:calibration_x2'] = int(calibration_x.strip())
        self.test_fixture_shared_memory_handler['glass_dimensions:calibration_y2'] = int(calibration_y.strip())

        # read positions and process
        calibration_x1 = self.test_fixture_shared_memory_handler['glass_dimensions:calibration_x1']
        calibration_y1 = self.test_fixture_shared_memory_handler['glass_dimensions:calibration_y1']
        calibration_x2 = self.test_fixture_shared_memory_handler['glass_dimensions:calibration_x2']
        calibration_y2 = self.test_fixture_shared_memory_handler['glass_dimensions:calibration_y2']

        if calibration_x1 >= calibration_x2:
            self.test_fixture_shared_memory_handler['glass_dimensions:x_max'] = calibration_x1
            self.test_fixture_shared_memory_handler['glass_dimensions:x_min'] = calibration_x2
        else:
            self.test_fixture_shared_memory_handler['glass_dimensions:x_max'] = calibration_x2
            self.test_fixture_shared_memory_handler['glass_dimensions:x_min'] = calibration_x1
        self.test_fixture_shared_memory_handler['glass_dimensions:y_reference'] = int(
            (calibration_y1 + calibration_y2) / 2)

        print("TestFixture: Calibration_step2: x-" + calibration_x.strip() + ", y-" + calibration_y.strip())
        self.test_fixture_shared_memory_handler['calibration:calibration_status'] = True

    def noise_measurement(self):
        print("TestFixture: Noise_Measurement")
        self.test_handler.noise_measurement(self.test_fixture_shared_memory_handler['glass_dimensions:x_min'],
                                            self.test_fixture_shared_memory_handler['glass_dimensions:y_reference'])

    def linearity_jitter_measurement(self):
        print("TestFixture: Linearity_Measurement")
        self.test_handler.linearity_jitter_measurement(self.test_fixture_shared_memory_handler['glass_dimensions:x_min'], self.test_fixture_shared_memory_handler['glass_dimensions:x_max'], self.test_fixture_shared_memory_handler['glass_dimensions:y_reference'])

    def full_scan_measurement(self):
        print("TestFixture: Full_Scan_Measurement")
        self.test_handler.full_scan_measurement(self.test_fixture_shared_memory_handler['glass_dimensions:x_min'],
                                                self.test_fixture_shared_memory_handler['glass_dimensions:x_max'],
                                                self.test_fixture_shared_memory_handler[
                                                    'glass_dimensions:y_reference'])

    def arbitrary_x_hover_measurement(self):
        self.test_handler.arbitrary_x_hover_measurement(self.test_fixture_shared_memory_handler['glass_dimensions:x_min'],
                                                self.test_fixture_shared_memory_handler['glass_dimensions:x_max'],
                                                self.test_fixture_shared_memory_handler[
                                                    'glass_dimensions:y_reference'])
        print("TestFixture: Arbitrary_X_Hover_Measurement")

    def single_tap_measurement(self):
        self.test_handler.single_tap_measurement(self.test_fixture_shared_memory_handler['single_tap:number of taps'], self.test_fixture_shared_memory_handler['glass_dimensions:x_min'], self.test_fixture_shared_memory_handler['glass_dimensions:x_max'], self.test_fixture_shared_memory_handler['glass_dimensions:y_reference'])
        print("TestFixture: Single_tap")

    def double_tap_measurement(self):
        self.test_handler.double_tap_measurement(self.test_fixture_shared_memory_handler['double_tap:number of taps'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_min'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_max'],
                                                 self.test_fixture_shared_memory_handler[
                                                     'glass_dimensions:y_reference'])

        print("TestFixture: Double_tap")

    def triple_tap_measurement(self):
        self.test_handler.triple_tap_measurement(self.test_fixture_shared_memory_handler['triple_tap:number of taps'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_min'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_max'],
                                                 self.test_fixture_shared_memory_handler[
                                                     'glass_dimensions:y_reference'])

        print("TestFixture: Triple_tap")

    def swipe_forward_measurement(self):
        self.test_handler.swipe_forward_measurement(self.test_fixture_shared_memory_handler['swipe_forward:number of swipes'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_min'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_max'],
                                                 self.test_fixture_shared_memory_handler[
                                                     'glass_dimensions:y_reference'])
        print("TestFixture: Swipe_forward")

    def swipe_backward_measurement(self):
        self.test_handler.swipe_backward_measurement(self.test_fixture_shared_memory_handler['swipe_backward:number of swipes'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_min'],
                                                 self.test_fixture_shared_memory_handler['glass_dimensions:x_max'],
                                                 self.test_fixture_shared_memory_handler[
                                                     'glass_dimensions:y_reference'])
        print("TestFixture: Swipe_backward")

    def set_motor_position(self):
        self.test_handler.set_motor_position(self.test_fixture_shared_memory_handler['set_motor_position:x'], self.test_fixture_shared_memory_handler['set_motor_position:y'])
        print("TestFixture: Set_motor_position")

    def get_motor_position(self):
        x, y = self.test_handler.get_motor_position()
        print("TestFixture: Get_motor_position")
        return x, y

    def motor_on(self):
        self.test_handler.motor_on()

    def motor_reset(self):
        self.test_handler.motor_reset()

    def motor_go_home(self):
        self.test_handler.motor_go_home()

    def motor_off(self):
        self.test_handler.motor_off()