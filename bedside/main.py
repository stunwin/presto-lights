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
t_threshold = 10000
dimmed = False
# time to wait after wakeup until we can listen for buttons again
t_wakeup = 500
# records the moment we wake up from sleep
awake_time = None

readmode = False

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

gnightbutton = Button(10, 10, 100, 100)
readbutton = Button(120, 10, 100, 100)
lightsoffbutton = Button(10, 120, 100, 100)
powerbutton = Button(120, 120, 100, 100)

# if these rects are declared in the main while loop it causes heinous visual glitches
gnightvector = Polygon().rectangle(*gnightbutton.bounds, corners=(20, 0, 0, 0))
readvector = Polygon().rectangle(*readbutton.bounds, corners=(0, 20, 0, 0))
lightsoffvector = Polygon().rectangle(*lightsoffbutton.bounds, corners=(0, 0, 0, 20))
powervector = Polygon().rectangle(*powerbutton.bounds, corners=(0, 0, 20, 0))

vector.set_font_size(25)

# This library requires some configuration the first time it runs in order to connect to the bridge and save settings see https://github.com/FRC4564/HueBridge for details
h = hue.Bridge()


# def powertoggle():  # if only some lights are off, all will be turned on. if all lights are on, all will be turned off
#     any = h.getGroup(4)["state"]["any_on"]
#     all = h.getGroup(4)["state"]["all_on"]
#     if all:
#         return False
#     elif any:
#         return True
#     else:
#         return True


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

    if gnightbutton.is_pressed():
        display.set_pen(PRESSED)
        h.setGroup(1, on=False)
        h.setGroup(4, on=False)
        h.setGroup(
            2,
            on=True,
            ct=455,
            effect="none",
            sat=203,
            xy=[0.5058, 0.4151],
            hue=7613,
            bri=34,
            transitiontime=50,
        )
        readmode = False
    else:
        display.set_pen(BUTTONBRIGHT)

    vector.draw(gnightvector)

    display.set_pen(BUTTONDARK)
    vector.text("gnight", gnightbutton.x + 25, gnightbutton.y + 50)

    if readbutton.is_pressed():
        display.set_pen(PRESSED)
        if not readmode:
            h.setLight(
                10,
                on=True,
                ct=427,
                effect="none",
                sat=187,
                xy=[0.4916, 0.415],
                hue=7875,
                bri=123,
                transitiontime=50,
            )
            readmode = True
        else:
            h.setLight(
                10,
                ct=455,
                effect="none",
                sat=203,
                xy=[0.5058, 0.4151],
                hue=7613,
                bri=34,
                transitiontime=50,
            )
            readmode = False

    else:
        display.set_pen(BUTTONDARK)

    vector.draw(readvector)

    display.set_pen(WHITE)
    vector.text("read", readbutton.x + 25, readbutton.y + 50)

    # this can be any one specific light. in this case light 13 sits behind my desk
    if lightsoffbutton.is_pressed():
        display.set_pen(PRESSED)
        h.setGroup(1, on=False)
        h.setGroup(2, on=False)
        h.setGroup(4, on=False)
    else:
        display.set_pen(BUTTONDARK)

    vector.draw(lightsoffvector)

    display.set_pen(WHITE)
    vector.text("lightsoff", lightsoffbutton.x + 5, lightsoffbutton.y + 50)

    if powerbutton.is_pressed():
        display.set_pen(PRESSED)
        h.setGroup(  # this specifically is set on a just slightly warm, but cooler than normal color i use for productivity
            1,
            on=True,
            ct=292,
            effect="none",
            sat=61,
            xy=[0.41, 0.394],
            hue=9186,
            bri=254,
            transitiontime=50,
        )
        h.setGroup(  # this specifically is set on a just slightly warm, but cooler than normal color i use for productivity
            2,
            on=True,
            ct=292,
            effect="none",
            sat=61,
            xy=[0.41, 0.394],
            hue=9186,
            bri=254,
            transitiontime=50,
        )
        h.setGroup(  # this specifically is set on a just slightly warm, but cooler than normal color i use for productivity
            4,
            on=True,
            ct=292,
            effect="none",
            sat=61,
            xy=[0.41, 0.394],
            hue=9186,
            bri=254,
            transitiontime=50,
        )
    else:
        display.set_pen(BUTTONCOLOR)
    vector.draw(powervector)

    display.set_pen(WHITE)
    vector.text("ALLON", powerbutton.x + 25, powerbutton.y + 50)
    presto.update()
