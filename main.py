from presto import Presto
import hue
from touch import Button
from picovector import PicoVector, Polygon, Transform, ANTIALIAS_BEST
import time


presto = Presto()
display = presto.display
WIDTH, HEIGHT = display.get_bounds()
vector = PicoVector(display)
touch = presto.touch
transform = Transform()
presto.set_backlight(0.2)


last_touch = time.ticks_ms()
# time to sleep
t_threshold = 5000
dimmed = False
# time to wait after wakeup until we can listen for buttons again
t_wakeup = 500
# records the moment we wake up from sleep
awake_time = None


vector.set_transform(transform)
vector.set_antialiasing(ANTIALIAS_BEST)
vector.set_font("OpenSans-Medium.af", 12)

wifi = presto.connect()

# look... there's a lot of work to be done in this section, i get it.
BG = display.create_pen(216, 196, 182)
WHITE = display.create_pen(251, 251, 251)
BUTTONCOLOR = display.create_pen(65, 167, 252)
BUTTONBRIGHT = display.create_pen(246, 199, 148)
BUTTONDARK = display.create_pen(62, 88, 121)
PRESSED = display.create_pen(246, 199, 148)
RED = display.create_pen(232, 102, 113)

daybutton = Button(10, 10, 100, 100)
nightbutton = Button(120, 10, 100, 100)
backlightbutton = Button(10, 120, 100, 100)
powerbutton = Button(120, 120, 100, 100)

# if these rects are declared in the main while loop it causes heinous visual glitches
dayvector = Polygon().rectangle(*daybutton.bounds, corners=(20, 0, 0, 0))
nightvector = Polygon().rectangle(*nightbutton.bounds, corners=(0, 20, 0, 0))
backlightvector = Polygon().rectangle(*backlightbutton.bounds, corners=(0, 0, 0, 20))
powervector = Polygon().rectangle(*powerbutton.bounds, corners=(0, 0, 20, 0))

vector.set_font_size(25)

# This library requires some configuration the first time it runs in order to connect to the bridge and save settings see https://github.com/FRC4564/HueBridge for details
h = hue.Bridge()


def powertoggle():  # if only some lights are off, all will be turned on. if all lights are on, all will be turned off
    any = h.getGroup(4)["state"]["any_on"]
    all = h.getGroup(4)["state"]["all_on"]
    if all:
        return False
    elif any:
        return True
    else:
        return True


def screendim(last_touch, t_threshold, dimmed, awake_time):
    if presto.touch_a.touched:
        last_touch = time.ticks_ms()
        if dimmed:
            presto.set_backlight(0.2)
            dimmed = False
            awake_time = time.ticks_ms()

    elapsed = time.ticks_diff(time.ticks_ms(), last_touch)
    print(elapsed)
    if elapsed > t_threshold and not dimmed:
        presto.set_backlight(0.0)
        dimmed = True
    return last_touch, dimmed, awake_time


while True:
    touch.poll()
    last_touch, dimmed, awake_time = screendim(
        last_touch, t_threshold, dimmed, awake_time
    )

    if dimmed or time.ticks_diff(time.ticks_ms(), awake_time) < t_wakeup:
        continue

    display.set_pen(WHITE)
    display.clear()

    if daybutton.is_pressed():
        display.set_pen(PRESSED)
        h.setGroup(  # this specifically is set on a just slightly warm, but cooler than normal color i use for productivity
            4,
            ct=292,
            effect="none",
            sat=61,
            xy=[0.41, 0.394],
            hue=9186,
            bri=254,
            transitiontime=50,
        )
    else:
        display.set_pen(BUTTONBRIGHT)

    vector.draw(dayvector)

    display.set_pen(BUTTONDARK)
    vector.text("day", daybutton.x + 25, daybutton.y + 50)

    if nightbutton.is_pressed():
        display.set_pen(PRESSED)
        h.setGroup(
            4,
            ct=443,
            effect="none",
            sat=197,
            xy=[0.4998, 0.4152],
            hue=7726,
            bri=143,
            transitiontime=50,
        )
    else:
        display.set_pen(BUTTONDARK)

    vector.draw(nightvector)

    display.set_pen(WHITE)
    vector.text("night", nightbutton.x + 25, nightbutton.y + 50)

    # this can be any one specific light. in this case light 13 sits behind my desk
    if backlightbutton.is_pressed():
        display.set_pen(PRESSED)
        status = h.getLight(13)["state"]["on"]
        print(status)
        h.setLight(13, on=not status)
    else:
        display.set_pen(BUTTONDARK)

    vector.draw(backlightvector)

    display.set_pen(WHITE)
    vector.text("backlight", backlightbutton.x + 5, backlightbutton.y + 50)

    if powerbutton.is_pressed():
        display.set_pen(PRESSED)
        print(powertoggle())
        h.setGroup(4, on=powertoggle())
    else:
        display.set_pen(BUTTONCOLOR)
    vector.draw(powervector)

    display.set_pen(WHITE)
    vector.text("pwr", powerbutton.x + 25, powerbutton.y + 50)
    presto.update()
