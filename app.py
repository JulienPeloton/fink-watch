import logging
from time import sleep
import numpy as np
from lib.display import main
from lib.utils import generate_logo

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
        logo = generate_logo()
        disp.ShowImage(logo)
        sleep(2)

        while True:
            # Randomly show the logo
            rand = np.random.randint(0, 60)
            if rand == 60:
                disp.ShowImage(logo)
                sleep(2)

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

