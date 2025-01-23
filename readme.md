# Presto Lights

## a lil app for you to control your hue lights with your Pimoroni Presto

This is really just for me to build out a repo with a readme and instructions and whatnot. If you find value, I love that, but I suspect it's a bit of a mess.

### This is for the Pimoroni Presto

Which is a very neat little guy, but if you don't have one, this application is incredibly specific to that hardware and firmware, so you'd be out of luck.

### Using the Hue library

#### Connecting

Pop over and read the documentation here for setup. The first time you instantiate the class, it will look for your hue bridge, and you'll need to hit the connect button. That will create a .dat file with the connection credentials

- [ ] TODO: Modify the hue library so that the credentials are added to and stored in secrets.py, since you'll already that on your presto.

#### Presets

I have included some preset colors in here for cool and warm colors that I use in my house. If you want to dramatically change the colors, I would use the hue app to set a scene you like, and then use `h.getGroup()` to read out the status.

- [ ] TODO: package up the args into a dict for easy reference.
