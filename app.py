import logging
from time import sleep
import numpy as np
from lib.display import main

from PIL import Image

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

        # Logo intro
        img = Image.open('pictures/Fink_PrimaryLogo_WEB.png')
        img = img.convert("RGBA")
        img = img.resize((240, 240))
        disp.ShowImage(img)
        sleep(2)

        while True:
            # Kafka polling
            count = np.random.randint(0, 300000)

            # Generate image
            image = main(progression=count)
            image = image.rotate(180)
            disp.ShowImage(image)
            sleep(1)
        disp.module_exit()
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()

