BAUD_RATE = 115200
# BAUD_RATE = 9600
RELAY_1_ON = 0x65
RELAY_1_OFF = 0x6F
RELAY_2_ON = 0x66
RELAY_2_OFF = 0x70
INFO = 0x5A
RELAY_STATES = 0x5B
NETID1 = '01'
NETID2 = '02'
NETID3 = '03'
NETID4 = '04'

MOTOR_COM = 'COM4'
SOLENOID_COM = 'COM10'

#Belt Constants
BELTSPEED='2000'
BELTACC='7500'
BELTDEC='7500'
SLIDESPEED='150'
SLIDEACC='1000'
SLIDEDEC='1000'
SWIPESPEED='20000'
SWIPEACC='7500'
SWIPEDEC='7500'
POS0='250'
POS1='1550'
POS2='2900'
POS3='4300'
POS4='5500'

#Voice Coil Constants
VCSPEED='1000'
VCACC='4000'
VCDEC='7000'
VCEXTEND='-1850' #1815
VCRETRACT='-500'

# Gesture Constants
PAD=2

TAPTIME=0.4 #seconds
DOUBLETAPTIME=.3 #seconds
DOUBLETAPDELAY=0.15 #seconds
TAPHOLDTIME=1.25 #seconds #1.5
SWIPETIME=.175 #seconds
SLIDETIME=.3 #seconds


NUM_OF_SAMPLES_PER_MEASUREMENT_NOISE_FULL_SCAN = 50
NUM_OF_SAMPLES_PER_MEASUREMENT_JITTER_LINEARITY = 250
NUM_OF_SAMPLES_PER_MEASUREMENT_GESTURE = 500

NUM_OF_ITERATIONS_PER_MEASUREMENT_GESTURE = 10

MOTOR_X_STEP_SIZE_IN_MOTOR_UNIT = 100

MOTOR_Y_STEP_SIZE_IN_MOTOR_UNIT = 1
MOTOR_Y_STEP_SIZE_INCREMENT_BASE_MOTOR_UNIT = 2

MOTOR_Y_AXIS_ENGAGEMENT_DISTANCE_IN_MOTOR_UNIT = 200

MOTOR_X_ABSOLUTE_POSITION_IN_MOTOR_UNIT = -100
MOTOR_Y_ABSOLUTE_POSITION_IN_MOTOR_UNIT = -900
