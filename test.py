import sys
import Adafruit_ADS1x15
from pidev.stepper import stepper
from Slush.Devices import L6480Registers as LReg6480, L6470Registers as LReg6470


sys.path.insert(0, "/home/pi/packages/Adafruit_16_Channel_PWM_Module_Easy_Library")
import Adafruit_Ease_Lib as ael
led = ael.Adafruit_Ease_Lib()
led.change_frequency(2000)
pwms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 , 13, 14, 15]
led.change_percentage(pwms, 50)

AXIS_MOTOR_SETTINGS = {
    'hold_current': 20,
    'run_current': 20,
    'acc_current': 20,
    'dec_current': 20,
    'max_speed': 100,
    'min_speed': 0,
    'micro_steps': 1,
    'threshold_speed': 400,
    'over_current': 2000,
    'stall_current': 2031.25,
    'accel': 0xF00,
    'decel': 0xF00,
    'low_speed_opt': False,
    'homing_direction': 0
}
#
# motor_1 = stepper(port=1, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_2 = stepper(port=2, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_3 = stepper(port=3, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_4 = stepper(port=4, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_5 = stepper(port=5, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_6 = stepper(port=6, speed=AXIS_MOTOR_SETTINGS['max_speed'])
#
# motors = [motor_1, motor_2, motor_3, motor_4, motor_5, motor_6]
# for motor in motors:
#     motor.setCurrent(hold=AXIS_MOTOR_SETTINGS['hold_current'], run=AXIS_MOTOR_SETTINGS['run_current'],
#                      acc=AXIS_MOTOR_SETTINGS['acc_current'], dec=AXIS_MOTOR_SETTINGS['dec_current'])
#     motor.setMaxSpeed(AXIS_MOTOR_SETTINGS['max_speed'])
#     motor.setMinSpeed(AXIS_MOTOR_SETTINGS['min_speed'])
#     motor.setMicroSteps(AXIS_MOTOR_SETTINGS['micro_steps'])
#     motor.setThresholdSpeed(AXIS_MOTOR_SETTINGS['threshold_speed'])
#     motor.setOverCurrent(AXIS_MOTOR_SETTINGS['over_current'])
#     motor.setStallCurrent(AXIS_MOTOR_SETTINGS['stall_current'])
#     motor.setAccel(AXIS_MOTOR_SETTINGS['accel'])
#     motor.setDecel(AXIS_MOTOR_SETTINGS['decel'])
#     motor.setLowSpeedOpt(AXIS_MOTOR_SETTINGS['low_speed_opt'])
#     motor.setParam(LReg.CONFIG, 0x3688)
#     motor.home(0)
#     while motor.isBusy():
#         continue


current = 30


motor_1 = stepper(port=1, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)
motor_1.setParam(LReg6480.GATECFG1, 0x5F)
motor_1.setParam(LReg6480.OCD_TH, 0x1F)
motor_1.setParam(LReg6480.CONFIG, 0x3688)
# motor_1.print_status()

motor_2 = stepper(port=2, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)
motor_2.setParam(LReg6480.GATECFG1, 0x5F)
motor_2.setParam(LReg6480.OCD_TH, 0x1F)
motor_2.setParam(LReg6480.CONFIG, 0x3688)
# motor_2.print_status()

motor_3 = stepper(port=3, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)
motor_3.setParam(LReg6470.CONFIG, 0x3688)
# motor_3.print_status()

motor_4 = stepper(port=4, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)
motor_4.setParam(LReg6470.CONFIG, 0x3688)
# motor_4.print_status()

motor_5 = stepper(port=5, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)
motor_5.setParam(LReg6470.CONFIG, 0x3688)
# motor_5.print_status()

motor_6 = stepper(port=6, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)
motor_6.setParam(LReg6470.CONFIG, 0x3688)
# motor_6.print_status()
motors = [motor_1, motor_2, motor_3, motor_4, motor_5, motor_6]
microstepping = 32
for motor in motors:
    motor.setAccel(0xF00)
    motor.setDecel(0xF00)
    motor.set_micro_steps(microstepping)

motor_1.home(0)
motor_2.home(0)
motor_3.home(0)
motor_4.home(1)
motor_5.home(1)
motor_6.home(1)

motor_1.go_to(199 * microstepping)
motor_2.go_to(199 * microstepping)
motor_3.go_to(199 * microstepping)
motor_4.go_to(-76 * microstepping)
motor_5.go_to(-76 * microstepping)
motor_6.go_to(-76 * microstepping)

GAIN = 1
increment = 1
# Create an ADS1115 ADC (16-bit) instance.
adc_red = Adafruit_ADS1x15.ADS1115(0x4A)
adc_blue = Adafruit_ADS1x15.ADS1115(0x48)
adc_green = Adafruit_ADS1x15.ADS1115(0x49)

clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)


def value_to_m(value):
    if value < 5:
        return 0
    if value > 95:
        return 100
    else:
        return value

def value_as_percent(color, value):
    if color == "red":
        return value_to_m(((value-4360)*100)/(15504-4360))
    if color == "green":
        return value_to_m(((value-3850)*100)/(14832-3850))
    if color == "blue":
        return value_to_m(((value-100)*100)/(11280-100))

def scale_joystick_value(value):
    return (value - 6600)/6000

def joy_val_filter(value):
    if value < -0.9:
        return -1
    if value > 0.9:
        return 1
    if value > -0.1 and value < 0.1:
        return 0
    else:
        return value

while True:
    led.change_percentage(0, clamp(value_as_percent("red", adc_red.read_adc(0, gain=GAIN)), 0, 100))
    led.change_percentage(1, clamp(value_as_percent("red", adc_green.read_adc(0, gain=GAIN)), 0, 100))
    led.change_percentage(2, clamp(value_as_percent("red", adc_blue.read_adc(0, gain=GAIN)), 0, 100))


    movement_amount = round(scale_joystick_value(adc_red.read_adc(1, gain=GAIN)) * increment)
    if movement_amount is not 0 and not motor_4.is_busy():
        motor_4.move(round(movement_amount * microstepping / 4))
        # print(motor_4.get_position())

    movement_amount = round(scale_joystick_value(adc_blue.read_adc(1, gain=GAIN)) * increment)
    if movement_amount is not 0 and not motor_5.is_busy():

        motor_5.move(round(movement_amount * microstepping / 4))
        # print(motor_5.get_position())

    movement_amount = round(scale_joystick_value(adc_green.read_adc(1, gain=GAIN)) * increment)
    if movement_amount is not 0 and not motor_6.is_busy():

        motor_6.move(round(movement_amount * microstepping / 4))
        # print(motor_6.get_position())

    movement_amount = round(scale_joystick_value(adc_red.read_adc(2, gain=GAIN)) * increment)
    if movement_amount is not 0 and not motor_1.is_busy():

        motor_1.move(round(-movement_amount * microstepping / 4))
        # print(motor_1.get_position())

    movement_amount = round(scale_joystick_value(adc_green.read_adc(2, gain=GAIN)) * increment)
    if movement_amount is not 0 and not motor_2.is_busy():

        motor_2.move(round(-movement_amount * microstepping / 4))
        # print(motor_2.get_position())

    movement_amount = round(scale_joystick_value(adc_blue.read_adc(2, gain=GAIN)) * increment)
    if movement_amount is not 0 and not motor_3.is_busy():

        motor_3.move(round(-movement_amount * microstepping / 4))
        # print(motor_3.get_position())


    # print("red knob: " + str(adc_red.read_adc(0, gain = GAIN)) + "   red x: " + str(adc_red.read_adc(1, gain = GAIN)) + "  red y: " + str(adc_red.read_adc(2, gain = GAIN)),end = '        ')
    # print("blue knob: " + str(adc_blue.read_adc(0, gain = GAIN)) + "   blue x: " + str(adc_blue.read_adc(1, gain = GAIN)) + "  blue y: " + str(adc_blue.read_adc(2, gain = GAIN)),end = '      ')
    # print("green knob: " + str(adc_green.read_adc(0, gain = GAIN)) + "   green x: " + str(adc_green.read_adc(1, gain = GAIN)) + "  green y: " + str(adc_green.read_adc(2, gain = GAIN)))