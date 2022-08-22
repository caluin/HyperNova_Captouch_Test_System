import CalibrationGUI, CapTouchGUI
import TestFixture
import TestCases
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial
from sys import stdout


class CapTouchLogic(CapTouchGUI.Ui_CapTouchMain):
    def __init__(self, test_handler, test_fixture_shared_memory_handler, CapTouchQDialog, CalibrationQDialog,
                 parent=None):
        # CapTouchGUI.Ui_CapTouchMain.__init__(self)
        # set up GUI
        self.setupUi(CapTouchQDialog)
        # save object reference
        self.CalibrationQDialog = CalibrationQDialog
        self.test_handler = test_handler
        self.test_fixture_shared_memory_handler = test_fixture_shared_memory_handler

    def setup_functions(self):
        # connect functions
        self.StartCalibrationButton.clicked.connect(self.on_start_calibration)
        self.NoiseButton.clicked.connect(partial(self.on_noise_measurement))
        self.LinearityJitterButton.clicked.connect(partial(self.on_linearity_jitter_measurement))
        self.FullScanButton.clicked.connect(partial(self.on_full_scan_measurement))
        self.ArbitraryXHoverButton.clicked.connect(partial(self.on_arbitrary_x_hover_measurement))
        self.SingleTapButton.clicked.connect(partial(self.on_single_tap))
        self.DoubleTapButton.clicked.connect(partial(self.on_double_tap))
        self.TripleTapButton.clicked.connect(partial(self.on_triple_tap))
        self.SwipeForwardButton.clicked.connect(partial(self.on_swipe_forward))
        self.SwipeBackwardButton.clicked.connect(partial(self.on_swipe_backward))
        self.InterruptTestButton.clicked.connect(partial(self.on_interrupt_test))

        self.GetMotorPositionButton.clicked.connect(self.on_get_motor_position)
        self.SetMotorPositionButton.clicked.connect(self.on_set_motor_position)
        self.MotorONButton.clicked.connect(self.on_motor_on)
        self.MotorOFFButton.clicked.connect(self.on_motor_off)
        self.MotorGoHomeButton.clicked.connect(self.on_motor_go_home)
        self.MotorResetButton.clicked.connect(self.on_motor_reset)


    def on_start_calibration(self):
        # kick off calibration logic
        print("CapTouchTestSystem: start_calibration")
        self.CalibrationQDialog.show()

    def on_noise_measurement(self):
        print("CapTouchTestSystem: noise_measurement")
        self.worker = TestFixture.TestFixture("noise_measurement", self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_linearity_jitter_measurement(self):
        print("CapTouchTestSystem: linearity_jitter_measurement")
        self.worker = TestFixture.TestFixture('linearity_jitter_measurement', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_full_scan_measurement(self):
        print("CapTouchTestSystem: full_scan_measurement")
        self.worker = TestFixture.TestFixture('full_scan_measurement', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_arbitrary_x_hover_measurement(self):
        print("CapTouchTestSystem: arbitrary_x_hover_measurement")
        self.worker = TestFixture.TestFixture('arbitrary_x_hover_measurement', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_single_tap(self):
        print("CapTouchTestSystem: single_tap " + self.SingleTapNum.text())
        self.test_fixture_shared_memory_handler['single_tap:number of taps'] = int(self.SingleTapNum.text())
        self.worker = TestFixture.TestFixture('single_tap', self.test_handler, self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_double_tap(self):
        print("CapTouchTestSystem: double_tap " + self.DoubleTapNum.text())
        self.test_fixture_shared_memory_handler['double_tap:number of taps'] = int(self.DoubleTapNum.text())
        self.worker = TestFixture.TestFixture('double_tap', self.test_handler, self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_triple_tap(self):
        print("CapTouchTestSystem: triple_tap " + self.TripleTapNum.text())
        self.test_fixture_shared_memory_handler['triple_tap:number of taps'] = int(self.TripleTapNum.text())
        self.worker = TestFixture.TestFixture('triple_tap', self.test_handler, self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_swipe_forward(self):
        print("CapTouchTestSystem: swipe_forward " + self.SwipeForwardNum.text())
        self.test_fixture_shared_memory_handler['swipe_forward:number of swipes'] = int(self.SwipeForwardNum.text())
        self.worker = TestFixture.TestFixture('swipe_forward', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_swipe_backward(self):
        print("CapTouchTestSystem: swipe_backward " + self.SwipeBackwardNum.text())
        self.test_fixture_shared_memory_handler['swipe_backward:number of swipes'] = int(self.SwipeBackwardNum.text())
        self.worker = TestFixture.TestFixture('swipe_backward', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_get_motor_position(self):
        print("CapTouchTestSystem: get_motor_position ")
        self.worker = TestFixture.TestFixture('get_motor_position', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)
        self.worker.update_motor_position.connect(self.evt_update_motor_position)

    def on_set_motor_position(self):
        print("CapTouchTestSystem: set_motor_position ")
        # x needs to be within boundary
        if int(self.XPositionText.toPlainText()) > self.test_fixture_shared_memory_handler['glass_dimensions:x_max']:
            self.XPositionText.setText(str(self.test_fixture_shared_memory_handler['glass_dimensions:x_max']))
        if int(self.XPositionText.toPlainText()) < self.test_fixture_shared_memory_handler['glass_dimensions:x_min']:
            self.XPositionText.setText(str(self.test_fixture_shared_memory_handler['glass_dimensions:x_min']))
        # y needs to be within boundary
        if int(self.YPositionText.toPlainText()) < self.test_fixture_shared_memory_handler['glass_dimensions:y_reference']:
            self.YPositionText.setText(str(self.test_fixture_shared_memory_handler['glass_dimensions:y_reference']))
        if int(self.YPositionText.toPlainText()) > 0:
            self.YPositionText.setText(str(0))

        self.test_fixture_shared_memory_handler['set_motor_position:x'] = int(self.XPositionText.toPlainText())
        self.test_fixture_shared_memory_handler['set_motor_position:y'] = int(self.YPositionText.toPlainText())
        self.worker = TestFixture.TestFixture('set_motor_position', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def on_motor_on(self):
        print("CapTouchTestSystem: motor_on ")
        self.worker = TestFixture.TestFixture('motor_on', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)
        self.worker.update_motor_position.connect(self.evt_update_motor_position)

    def on_motor_off(self):
        print("CapTouchTestSystem: motor_off ")
        self.worker = TestFixture.TestFixture('motor_off', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)
        self.worker.update_motor_position.connect(self.evt_update_motor_position)

    def on_motor_go_home(self):
        print("CapTouchTestSystem: motor_go_home ")
        self.worker = TestFixture.TestFixture('motor_go_home', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)
        self.worker.update_motor_position.connect(self.evt_update_motor_position)

    def on_motor_reset(self):
        print("CapTouchTestSystem: motor_reset ")
        self.worker = TestFixture.TestFixture('motor_reset', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)
        self.worker.update_motor_position.connect(self.evt_update_motor_position)

    def on_interrupt_test(self):
        print("CapTouchTestSystem: interrupt_test")
        self.worker = TestFixture.TestFixture('interrupt_test', self.test_handler,
                                              self.test_fixture_shared_memory_handler)
        self.worker.start()
        self.worker.test_complete.connect(self.evt_test_complete)
        self.worker.update_progress.connect(self.evt_update_progress)

    def evt_test_complete(self, str):
        # QtWidgets.QMessageBox.information(self, "Test Complete.")
        print("CapTouchTestSystem: Test Complete.")

    def evt_update_motor_position(self, str):
        self.XPositionText.setText(str.split(' ')[0].strip())
        self.YPositionText.setText(str.split(' ')[1].strip())
        print("CapTouchTestSystem: Motor Position Updated.")

    def evt_update_progress(self, str):
        print(str)


class CalibrationLogic(CalibrationGUI.Ui_Calibration):
    # class variables
    calibration_steps = 0

    def __init__(self, test_handler, test_fixture_shared_memory_handler, CalibrationQDialog, parent=None):
        CalibrationGUI.Ui_Calibration.__init__(self)
        # set up GUI
        self.setupUi(CalibrationQDialog)
        # save object reference
        self.CalibrationQDialog = CalibrationQDialog
        self.test_handler = test_handler
        self.test_fixture_shared_memory_handler = test_fixture_shared_memory_handler
        # check image folder

        # connect dialog box signals to functions
        CalibrationQDialog.dialog_box_closed_signal.connect(self.evt_dialog_box_closed_signal)
        # set up GUI stuff
        self.Instruction_1.show()
        self.Instruction_2.hide()

    def setup_functions(self):
        # connect functions
        self.Cancel.clicked.connect(self.onCancel)
        self.NextButton.clicked.connect(self.onNext)

    def onCancel(self):
        self.CalibrationQDialog.close()
        self.calibration_steps = 0
        self.Photo.setPixmap(QtGui.QPixmap(":/CalibrationImages/resource/photo1.jpg"))
        self.NextButton.setText("Next")
        self.Cancel.setEnabled(True)
        self.Instruction_1.show()
        self.Instruction_2.hide()
        self.Instruction_3.hide()

    def onNext(self):
        if self.calibration_steps == 0:
            stdout.write("CapTouchTestSystem: Calibration_Logic_start_calibration_step1")
            self.Instruction_1.show()
            self.Instruction_2.hide()
            self.Instruction_3.hide()
            self.NextButton.setEnabled(False)
            self.Cancel.setEnabled(False)
            # execute calibration step1
            self.worker = TestFixture.TestFixture('calibration_step1', self.test_handler,
                                                  self.test_fixture_shared_memory_handler)
            self.worker.start()
            self.worker.calibration_progress.connect(self.evt_calibration_progress)
            self.worker.update_progress.connect(self.evt_update_progress)
            self.calibration_steps = 1

        elif self.calibration_steps == 1:
            self.Instruction_1.hide()
            self.Instruction_2.show()
            self.Instruction_3.hide()
            # display photo of next step
            self.Photo.setPixmap(QtGui.QPixmap(":/CalibrationImages/resource/photo2.jpg"))
            self.NextButton.setEnabled(True)
            self.calibration_steps = 2

        elif self.calibration_steps == 2:
            print("CapTouchTestSystem: Calibration_Logic_start_calibration_step2")
            self.NextButton.setEnabled(False)
            self.Cancel.setEnabled(False)
            # execute calibration step2
            self.worker = TestFixture.TestFixture('calibration_step2', self.test_handler,
                                                  self.test_fixture_shared_memory_handler)
            self.worker.start()
            self.worker.calibration_progress.connect(self.evt_calibration_progress)
            self.worker.update_progress.connect(self.evt_update_progress)
            # calculating and report
            self.calibration_steps = 3

        elif self.calibration_steps == 3:
            self.Instruction_1.hide()
            self.Instruction_2.hide()
            self.Instruction_3.show()
            self.Photo.hide()
            # refresh button characters
            self.NextButton.setText("Finish")
            self.NextButton.setEnabled(True)
            self.Cancel.setEnabled(False)
            self.calibration_steps = 4

        elif self.calibration_steps == 4:
            self.calibration_steps = 0
            self.Photo.setPixmap(QtGui.QPixmap(":/CalibrationImages/resource/photo1.jpg"))
            self.Instruction_1.show()
            self.Instruction_2.hide()
            self.Instruction_3.hide()
            self.Photo.show()
            self.NextButton.setText("Next")
            self.Cancel.setEnabled(True)
            self.CalibrationQDialog.close()

    def evt_test_complete(self, str):
        # QtWidgets.QMessageBox.information(self, "This calibration step is completed.")
        print("CapTouchTestSystem: Test completed.\n")

    def evt_update_progress(self, str):
        print(str)
        self.calibration_steps = 0
        self.Photo.setPixmap(QtGui.QPixmap(":/CalibrationImages/resource/photo1.jpg"))
        self.NextButton.setText("Next")
        self.NextButton.setEnabled(True)
        self.Cancel.setEnabled(True)

    def evt_dialog_box_closed_signal(self, str):
        # clean calibration window
        self.calibration_steps = 0
        self.Photo.setPixmap(QtGui.QPixmap(":/CalibrationImages/resource/photo1.jpg"))
        self.NextButton.setText("Next")
        self.Cancel.setEnabled(True)
        self.Instruction_1.show()
        self.Instruction_2.hide()
        self.Instruction_3.hide()
        self.Photo.show()
        self.CalibrationQDialog.close()

    def evt_calibration_progress(self, str):
        # QtWidgets.QMessageBox.information(self, "This calibration step is completed.")
        print("CapTouchTestSystem: This calibration step is completed.")
        self.onNext()


class DialogBox(QtWidgets.QDialog):
    # signals emit to other module
    dialog_box_closed_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(DialogBox, self).__init__(parent)

    def closeEvent(self, event):
        self.dialog_box_closed_signal.emit('Dialog box closed')
        event.accept()


if __name__ == '__main__':
    import sys

    # invoke glass system reset
    # os.system("adb wait-for-device && adb root && adb remount")
    # os.system("adb shell mfg_tool mcu raw set dev")
    # os.system("adb shell mfg_tool mcu raw set w ConfigHallInactiveOverride 1")
    # os.system("adb shell mfg_tool mcu reset")
    # os.system("adb shell mfg_tool mcu raw captouch force-streaming")
    # os.system("adb shell mfg_tool mcu raw loglevel capt trace")

    # initialize shared memory for test fixture
    test_fixture_shared_memory_handler = TestFixture.shared_memory_initialization()

    # initialize test_handler
    test_handler = TestCases.TestCases(test_fixture_shared_memory_handler)
    # setup GUI related stuff
    app = QtWidgets.QApplication(sys.argv)
    # create CalibrationLogic and initialize it
    CalibrationQDialog = DialogBox()
    CalibrationLogicInstance = CalibrationLogic(test_handler, test_fixture_shared_memory_handler, CalibrationQDialog,
                                                CalibrationGUI.Ui_Calibration)
    CalibrationLogicInstance.setup_functions()
    # create the CapTouchLogic and initialize it
    CapTouchQDialog = QtWidgets.QDialog()
    CapTouchLogicInstance = CapTouchLogic(test_handler, test_fixture_shared_memory_handler, CapTouchQDialog,
                                          CalibrationQDialog, CapTouchGUI.Ui_CapTouchMain)
    CapTouchLogicInstance.setup_functions()
    CapTouchQDialog.show()

    sys.exit(app.exec_())
