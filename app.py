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
from datetime import datetime
from time import sleep
from fink_watch.display import screen
from fink_watch.utils import generate_logo
from fink_watch.observatory import observatories
from fink_watch.poll import poll_last_offset

logging.basicConfig(level=logging.DEBUG)


def main():
    """Launch the Fink watch"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--demo",
        action="store_true",
        help="If specified, display a fix image on the local computer instead of the LCD screen",
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
    parser.add_argument(
        "-display",
        type=str,
        default="watch",
        help="What to display on screen: watch, logo. Default is watch.",
    )
    parser.add_argument(
        "-observatory",
        type=str,
        default="ZTF",
        help="Name of the observatory to set the local time for the `clock` option. Default is ZTF.",
    )
    parser.add_argument(
        "-alert_per_deg",
        type=int,
        default=1000,
        help="Number of alerts per degree (for the alertmeter). Default is 1000",
    )
    parser.add_argument(
        "-topic",
        type=str,
        default="fink_ztf_{}".format(datetime.now().strftime("%Y%m%d")),
        help="Topic name to read alerts. Default is fink_ztf_<YYYYMMDD>.",
    )

    args = parser.parse_args(None)

    assert args.display in ["watch", "logo"], "`-display` should be among: watch, logo"
    assert args.observatory in observatories.keys(), (
        "{} not found in `fink_watch/observatory.py`. Please, edit the file and relaunch.".format(
            args.observatory
        )
    )

    if args.display == "logo":
        image = generate_logo(width=args.width, height=args.height)
    else:
        image = screen(
            width=args.width,
            height=args.height,
            observatory=args.observatory,
            alert_per_deg=args.alert_per_deg,
        )

    if args.demo:
        # Display on local computer
        # for debugging
        image.show()
    else:
        # Check input args
        assert args.width == 240, "This program works only for 240x240 resolution"
        assert args.height == 240, "This program works only for 240x240 resolution"

        from fink_watch.LCD_1inch28 import LCD_1inch28

        disp = LCD_1inch28()
        disp.Init()

        # Clear display.
        disp.clear()

        # Set the backlight to 50
        disp.bl_DutyCycle(50)

        # Logo intro
        logo = generate_logo()
        disp.ShowImage(logo)
        sleep(1)

        if args.display == "logo":
            disp.module_exit()
        elif args.display == "watch":
            # Counter or Clock
            try:
                counter = 0
                while True:
                    # Show the logo every 60 seconds
                    if counter % 60 == 0:
                        disp.ShowImage(logo)
                        sleep(2)

                    # Kafka polling
                    # TODO: proper yaml
                    cfg = {
                        "group.id": "fink-watch",
                        "bootstrap.servers": "134.158.74.95:24499",
                    }
                    nalerts = poll_last_offset(cfg, topic=args.topic)

                    # Generate image
                    image = screen(
                        progression=nalerts,
                        observatory=args.observatory,
                        alert_per_deg=args.alert_per_deg,
                    )
                    image = image.rotate(180)
                    disp.ShowImage(image)

                    # TODO: 1 second is probably overkill...
                    sleep(1)
                    counter += 1
                disp.module_exit()
            except IOError as e:
                logging.info(e)
            except KeyboardInterrupt:
                disp.module_exit()
                logging.info("quit:")
                exit()


if __name__ == "__main__":
    main()
