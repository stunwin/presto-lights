# Presto Lights

## a lil app for you to control your hue lights with your Pimoroni Presto

This is less meant to be used by anybody else, and more just for me to go through the exercise of making a readme. If you find value, I love that, but I suspect it's a bit of a mess. **It is currently very ugly. I know. I'm sorry**.

### This is for the [Pimoroni Presto](https://shop.pimoroni.com/products/presto?variant=54894104019323)

Which is a very neat little guy, but if you don't have one, this application is incredibly specific to that hardware and firmware, so you'd be out of luck.

### Two versions

The version of `main.py` in the root directory is what I made for my office. The buttons set color temp for the whole room, toggle one specific lamp, and toggle the power for the whole room.

`bedside/main.py` is for, you guessed it, the bedroom, specifically for use before bed. It allows you to go into night mode, which turns off the other rooms in the house, and sets the bedroom to dimmed. Read mode turns one bedside lamp up. Lights off turns off the whole house, and panic sets every single light in the house to bright instantly.

### Using the Hue library

#### Connecting

Pop over and read [the documentation here](https://github.com/FRC4564/HueBridge) for setup. The first time you instantiate the class, it will look for your hue bridge, and you'll need to hit the connect button. That will create a .dat file with the connection credentials

- [ ] TODO: Modify the hue library so that the credentials are added to and stored in secrets.py, since you'll already that on your presto.

#### Presets

I have included some preset colors in here for cool and warm colors that I use in my house. If you want to dramatically change the colors, I would use the hue app to set a scene you like, and then use `h.getGroup()` to read out the status.

- [ ] TODO: package up the args into a dict for easy reference.
