## Pi-PICO PAINT

![Pi-PicoPaint](https://github.com/user-attachments/assets/687c363a-c3ff-4fc4-bead-0ee1e397cdff)

Pi-Pico paint is a physical computing project which implements a web server on a Raspberry Pi Pico 2W and allows users to use a simple paint interface to then show their creations on a sh1106 oled display.

The web app contains a basic paint program where users can change stroke width, select white or black background and then 'print' their creations.

### Technology used

**Software libraries**
- [sh1106](https://github.com/robert-hh/SH1106/blob/master/sh1106.py)
- Micro-python
- Google Fonts Icons

**Physical Requirements**
- Raspberry Pi Pico (2W/W)
- SH1106 OLED module dimensions 128x64px _(I may upgrade the project to adapt to multiple screen sizes in the future)_
- A handful of jumper cables

### How to

To use this project download the code and install the software libraries required. Some tools may filter out the .gz files which is ok but for optimum performance ensure they are loaded.

Then create a `config.py` in the format of `config.example.py` in the repo. 

Ensure you change the country to the correct code. 

Run `main.py`!

If you have a different dimension screen the code can be altered, just ensure you update both backend and frontend code and you can re-zip the files using `gzip -k -9 <filepath>`

### About the project

This project is my first attempt at physical computing and it was an interesting exploration. I found the following document particularly useful for the boilerplate async server code: [Connecting to the internet with Pico W](https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf).

The design of the web app is based on the old MS Paint application with some modernisation with google fonts.

