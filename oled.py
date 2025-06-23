from machine import Pin, I2C
from lib.sh1106 import SH1106_I2C
import time
import framebuf
from config import DISPLAY_SDA_PIN, DISPLAY_SCL_PIN, DISPLAY_HEIGHT, DISPLAY_WIDTH

# initialise I2C panel
sda = Pin(DISPLAY_SDA_PIN)
scl = Pin(DISPLAY_SCL_PIN)
i2c = I2C(0, sda=sda, scl=scl, freq=400000)

time.sleep(1)
display = SH1106_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
display.fill(0)

def display_pixels(pixels: bytearray) -> None:

    """
    Prints pixel array to display
    """

    fb = framebuf.FrameBuffer(pixels, 128, 64, framebuf.MONO_HLSB)
    display.blit(fb, 0, 0)
    display.show()