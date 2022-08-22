from serial import Serial
import time
import Constants


class Motor():
    # Constants (COMMANDS)
    ACC = 'ACC'
    DEC = 'DEC'
    EX = 'EX'
    HSPD = 'HSPD'
    LED = 'LED'
    MST = 'MST'
    PWRC = 'PWRC'
    PWRV = 'PWRV'
    RGB = 'RGB'
    TEMP = 'TEMP'
    SYSTIME = 'SYSTIME'
    SVON = 'SVON'
    SVOFF = 'SVOFF'
    JOGXP = 'JOGXP'
    JOGXN = 'JOGXN'
    STOPX = 'STOPX'
    X = 'X'
    HMODE = 'HMODE'
    HOMEX = 'HOMEX'
    RESET = 'RESET'
    ECLEARX = 'ECLEARX'
    SVRST = 'SVRST'
    STORE = 'STORE'
    INPOS = 'INPOS'
    POSD = 'POSD'
    COMERR = 'COMERR'
    ERROR = 'ERROR'

    def __init__(self, com_port: str, netId: str, baud=115200):
        self._serial = Serial(com_port, baud, timeout=1)  # was .1
        self._baud = baud
        self._id = netId

    @classmethod
    def initialize_new_motor(cls, com_port: str, netId: str, acc: int, hspd: int):
        time.sleep(0.01)
        try:
            new_motor = cls(com_port, netId, baud=115200)
            return new_motor
        except:
            raise Exception("Attempt to initialize motor failed.")

    def send(self, cmd):
        try:
            self._serial.write((cmd + '\r\n').encode())
            self.read()
        except:
            raise Exception(f"Sorry, cmd_str {cmd} failed.")

    def send_tap(self, cmd):
        try:
            self._serial.write((cmd + '\r\n').encode())
            time.sleep(0.2)
        except:
            raise Exception(f"Sorry, cmd_str {cmd} failed.")

    def write(self, command, value=None):
        try:
            if value != None:
                msg = f'@{self._id}:{command}={str(value)}\r\n'
            else:
                msg = f'@{self._id}:{command}\r\n'

            self._serial.write(msg.encode())
        except:
            raise Exception(f"Sorry, command {command} failed.")

    def read(self):
        resp = self._serial.readline()
        resp = resp.decode()
        value = resp.split('=')
        if Motor.COMERR in resp:
            value = Motor.ERROR
        else:
            value = value[-1]
        return value

    def close(self):
        self._serial.close()

    def get_acceleration(self):
        try:
            self.write(Motor.ACC)
            resp = self.read()
            return resp
        except Exception as e:
            return -1

    def set_acceleration(self, value):
        try:
            self.write(Motor.ACC, value)
        except:
            return -1

    def set_hspd(self, value):
        try:
            self.write(Motor.HSPD, value)
            resp = self.read()
            return resp
        except:
            return -1

    def get_hspd(self):
        try:
            self.write(Motor.HSPD)
            resp = self.read()
            return resp
        except:
            return -1

    def set_deceleration(self, value):
        try:
            self.write(Motor.DEC, value)
            resp = self.read()
            return resp
        except:
            return -1

    def get_deceleration(self):
        try:
            self.write(Motor.DEC)
            resp = self.read()
            return resp
        except:
            return -1

    def set_led(self, value):
        try:
            self.write(Motor.LED, value)
        except:
            return -1

    def get_led(self):
        try:
            self.write(Motor.LED)
            resp = self.read()
            return resp
        except:
            return -1

    def set_rgb(self, value):
        try:
            self.write(Motor.RGB, value)
            resp = self.read()
            return resp
        except:
            return -1

    def get_rgb(self):
        try:
            self.write(Motor.RGB)
            resp = self.read()
            return resp
        except:
            return -1

    def mst(self):
        '''
        To read the status, use the command MST. The reply to this command will be a hex
        number that represents the motor status, with each bit representing the various states of
        the motion. page26 for more details
        0 Enabled
        1 In-Position
        2 Moving
        3 In Fault 
        '''
        try:
            self.write(Motor.MST)
            resp = self.read()
            return resp
        except:
            return -1

    def get_prv(self):
        # Power source voltage
        try:
            self.write(Motor.PWRV)
            resp = self.read()
            return resp
        except:
            return -1

    def get_prc(self):
        # Power source current (not working need to fix)
        try:
            self.write(Motor.PWRC)
            resp = self.read()
            return resp
        except:
            return -1

    def get_temp(self):
        # returns temp in C
        try:
            self.write(Motor.TEMP)
            resp = self.read()
            return resp
        except:
            return -1

    def get_system_time(self):
        # returns system time in seconds since last powerup
        try:
            self.write(Motor.SYSTIME)
            resp = self.read()
            return resp
        except:
            return -1

    def on(self):
        # turns servo on
        try:
            self.write(Motor.SVON)
            resp = self.read()
            return resp
        except:
            return -1

    def off(self):
        try:
            self.write(Motor.SVOFF)
            resp = self.read()
            return resp
        except:
            return -1

    def jogxp(self):
        # jog in pos direction
        try:
            self.write(Motor.JOGXP)
        except:
            return -1

    def jogxn(self):
        # jog in neg direction
        try:
            self.write(Motor.JOGXN)
        except:
            return -1

    def stopx(self):
        try:
            self.write(Motor.STOPX)
        except:
            return -1

    def get_x(self):
        # move to X
        try:
            self.write(Motor.X)
        except:
            return -1

    def set_x(self, value):
        try:
            self.write(Motor.X, value)
        except:
            return -1

    def hmode(self, value):
        try:
            self.write(Motor.HMODE, value)
        except:
            return -1

    def homex(self):
        try:
            self.write(Motor.HOMEX)
        except:
            return -1

    def reset(self):
        try:
            self.write(Motor.RESET)
        except:
            return -1

    def eclearx(self):
        try:
            self.write(Motor.ECLEARX)
        except:
            return -1

    # def get_position(self):
    #     self.write(Motor.EX)
    #     resp = self.readline().decode("utf-8")
    #     return resp

    def get_position(self):
        try:
            self.write(Motor.EX)
            resp = self.read()
            return resp
        except:
            return -1

    def set_position(self, value):
        try:
            self.write(Motor.EX, value)
        except:
            return -1

    def reset_servo(self):
        try:
            self.write(Motor.SVRST)
            resp = self.read()
            return resp
        except:
            return -1

    def store_to_flash(self):
        # store all parameters to flash memory
        try:
            self.write(Motor.STORE)
            resp = self.read()
            return resp
        except:
            return -1

    def get_inpositon_value(self):
        # In-position value
        try:
            self.write(Motor.INPOS)
            resp = self.read()
            return resp
        except:
            return -1

    def get_target_position(self):
        # read motor target position
        try:
            self.write(Motor.POSD)
            resp = self.read()
            return resp
        except:
            return -1

    def set_params(self, speed1, acc1, dec1, speed3, acc3, dec3):
        try:
            self.send(f'@01:ECLEARX;SVOFF;SVON')
            self.send(f'@01:HSPD={speed1};ACC={acc1};DEC={dec1}')
            self.send(f'@01:SVOFF')
            self.send(f'@03:ECLEARX;SVOFF;SVON')
            self.send(f'@03:HSPD={speed3};ACC={acc3};DEC={dec3}')
            self.send(f'@03:SVOFF')
            self.send(f'@00:CA=15;SVON')
        except:
            return -1

    def home(self):
        try:
            x = 0
            y = -100
            self.go_location(x, y)
        except:
            return -1

    def read_position(self):
        # self.motors_off()
        x = self.send(f'@01:EX')
        self._serial.write((f'@01:EX' + '\r\n').encode())
        x = self.read()
        time.sleep(1)
        self._serial.write((f'@03:EX' + '\r\n').encode())
        y = self.read()
        time.sleep(1)
        return {'x': int(x.rstrip().lstrip()), 'y': int(y.rstrip().lstrip())}

    def go_home(self):
        try:
            self.motors_on()
            time.sleep(1)
            self.send(f'@03:JOGXP')
            time.sleep(0.2)
            self.send(f'@01:JOGXP')
            time.sleep(1)
            self.motors_off()
        except:
            return -1

    def go_location(self, x, y):
        try:
            X = self.int2hex(x)
            Y = self.int2hex(y)
            self.motors_on()
            time.sleep(1)
            test = self.read_position()
            while test['x'] != x or test['y'] != y:
                self.send(f'@00:CM={X}00000000{Y}')
                time.sleep(1)
                test = self.read_position()
            self.motors_off()
        except:
            return -1

    def go_location_nonstop(self, x, y):
        try:
            X = self.int2hex(x)
            Y = self.int2hex(y)
            self.send_tap(f'@00:CM={X}00000000{Y}')
        except:
            return -1

    def motors_reset(self):
        try:
            self.send(f'@01:ECLEARX;SVOFF;SVON')
            self.send(f'@03:ECLEARX;SVOFF;SVON')
            self.send(f'@00:CA=15;SVON')
        except:
            return -1

    def motors_off(self):
        try:
            self.send(f'@01:SVOFF')
            self.send(f'@03:SVOFF')
        except:
            return -1

    def motors_on(self):
        try:
            self.send(f'@01:SVON')
            self.send(f'@03:SVON')
        except:
            return -1

    def int2hex(self, i):
        return hex(i & (2 ** 32 - 1))[-8:].replace('0x', '').zfill(8).upper()


if __name__ == '__main__':
    my_motor = Motor.initialize_new_motor(Constants.MOTOR_COM, "00", 30, 30)
    my_motor.set_params(speed1=100, acc1=200, dec1=200, speed3=10, acc3=400, dec3=400)
    my_motor.home()
    my_motor.go_location(-12000, -4400)
    my_motor.home()
    my_motor.go_location(-12000, -4400)
    my_motor.home()
    my_motor.go_location(-12000, -4400)
    my_motor.send(f'@01:SVOFF')
    my_motor.send(f'@03:SVOFF')
    my_motor.close()
