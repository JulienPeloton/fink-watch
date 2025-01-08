# Copyright 2025 Julien Peloton
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Launch the Fink watch"""

import argparse
import logging
from time import sleep
from lib.display import screen
from lib.utils import generate_logo

logging.basicConfig(level=logging.DEBUG)


def main():
    """Launch the Fink watch"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local",
        action="store_true",
        help="If specified, display on the local computer instead of the LCD screen",
    )
    parser.add_argument(
        "-width",
        type=int,
        default=240,
        help="Width size in pixels. Default is 240",
    )
    parser.add_argument(
        "-height",
        type=int,
        default=240,
        help="Height size in pixels. Default is 240",
    )

    args = parser.parse_args(None)

    image = screen(width=args.width, height=args.height)

    if args.local:
        image.show()
    else:
        assert args.width == 240, "This program works only for 240x240 resolution"
        assert args.height == 240, "This program works only for 240x240 resolution"

        from lib.LCD_1inch28 import LCD_1inch28

        try:
            disp = LCD_1inch28()
            disp.Init()

            # Clear display.
            disp.clear()

            # Set the backlight to 50
            disp.bl_DutyCycle(50)

            # Logo intro
            logo = generate_logo()
            disp.ShowImage(logo)
            sleep(2)

            count = 0
            while True:
                # Show the logo every 60 seconds
                if count % 60:
                    disp.ShowImage(logo)
                    sleep(2)

                # Kafka polling
                # TODO
                import numpy as np

                count = np.random.randint(0, 300000)

                # Generate image
                image = screen(progression=count)
                image = image.rotate(180)
                disp.ShowImage(image)
                sleep(1)
                count += 1
            disp.module_exit()
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            disp.module_exit()
            logging.info("quit:")
            exit()


if __name__ == "__main__":
    main()
