import logging
from lib.display import main

logging.basicConfig(level=logging.DEBUG)

image = main()

LOCAL = True
if LOCAL:
    image.show()
else:
    from lib.LCD_1inch28 import LCD_1inch28

    try:
        disp = LCD_1inch28()
        disp.Init()
        # Clear display.
        disp.clear()
        #Set the backlight to 100
        disp.bl_DutyCycle(50)
        disp.ShowImage(image)
        disp.module_exit()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()

