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
"""Create the screen for the watch"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from lib.utils import draw_arcs_with_gradient, scale
from lib.colors import (
    fink_orange,
    dark_fink_orange,
    light_blue,
    dark_blue,
    polygon_color,
)


def screen(width=240, height=240, progression=120000):
    """Image to flash on the LCD screen of the watch

    Parameters
    ----------
    width: int
        Width size in pixels. Default is 240
    height: int
        Height size in pixels. Default is 240
    progression: int
        Number of incoming alerts

    Returns
    -------
    out: Image
        Image to be shown on screen
    """
    # Angles are measured from 3 o'clock, increasing clockwise.
    alert_per_deg = 1000
    min_progression_deg = 90
    max_progression_deg = 360
    progression_deg = (
        np.min((max_progression_deg - min_progression_deg, progression / alert_per_deg))
        + 90
    )

    # Create blank image for drawing.
    background = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(background, "RGBA")

    # Outer ring
    coord_full = (0, 0, width, height)
    draw.arc(coord_full, 0, 360, fill=dark_fink_orange, width=4)

    draw_arcs_with_gradient(
        draw,
        coord=coord_full,
        f_co=dark_blue,
        t_co=light_blue,
        angles0=[0, 80, 190, 250],
        angles=[60, 60, 30, 80],
        interval=50,
        width=5,
    )

    # Second ring
    draw_arcs_with_gradient(
        draw,
        coord=(
            scale(width, 4),
            scale(height, 4),
            width - scale(width, 4),
            height - scale(height, 4),
        ),
        f_co=(*fink_orange, 120),
        t_co=(*fink_orange, 120),
        angles0=[10, 60, 120, 180, 220, 260, 320],
        angles=[30, 40, 20, 30, 20, 30, 20],
        interval=50,
        width=5,
    )

    # Third rings
    draw.arc(
        (
            scale(width, 12.5),
            scale(height, 12.5),
            width - scale(width, 12.5),
            height - scale(height, 12.5),
        ),
        0,
        360,
        fill=(*fink_orange, 120),
        width=8,
    )
    draw.arc(
        (
            scale(width, 12.5),
            scale(height, 12.5),
            width - scale(width, 12.5),
            height - scale(height, 12.5),
        ),
        90,
        int(progression_deg),
        fill=fink_orange,
        width=8,
    )

    # Ticks major/minor
    step_major_ticks = 10
    step_minor_ticks = 2
    for angle in range(min_progression_deg, max_progression_deg, step_major_ticks):
        x0 = width / 2 + (width / 2 - scale(width, 9.5)) * np.cos(np.deg2rad(angle))
        y0 = height / 2 + (height / 2 - scale(height, 9.5)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 12)) * np.cos(np.deg2rad(angle))
        y1 = height / 2 + (height / 2 - scale(height, 12)) * np.sin(np.deg2rad(angle))
        draw.line([(x0, y0), (x1, y1)], fill=(255, 255, 255), width=2)

    for angle in range(min_progression_deg, max_progression_deg - 10, step_minor_ticks):
        x0 = width / 2 + (width / 2 - scale(width, 11.8)) * np.cos(np.deg2rad(angle))
        y0 = height / 2 + (height / 2 - scale(height, 11.8)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 12)) * np.cos(np.deg2rad(angle))
        y1 = height / 2 + (height / 2 - scale(width, 12)) * np.sin(np.deg2rad(angle))
        draw.line([(x0, y0), (x1, y1)], fill=(255, 255, 255), width=1)

    # Inner rings
    for i in range(20):
        radius = scale(width, 28 + i / 5)
        transparency = int(255 / (np.abs(i - 10) + 1))
        draw.arc(
            (radius, radius, width - radius, height - radius),
            0,
            360,
            fill=(*dark_blue, transparency),
            width=4,
        )

    draw.arc(
        (
            scale(width, 27),
            scale(height, 27),
            width - scale(width, 27),
            height - scale(height, 27),
        ),
        90,
        360,
        fill=dark_fink_orange,
        width=3,
    )
    draw.arc(
        (
            scale(width, 27),
            scale(height, 27),
            width - scale(width, 27),
            height - scale(height, 27),
        ),
        90,
        int(progression_deg),
        fill=fink_orange,
        width=3,
    )

    # Text: number of alerts
    size = scale(width, 14)
    font = ImageFont.truetype("fonts/DS-DIGIB.TTF", size)
    draw.text(
        (width / 2, width / 2 - size / 3),
        "{}k".format(int(progression / 1000)),
        anchor="mt",
        font=font,
    )

    # Polygons
    w = 7
    space = 3
    angles = range(min_progression_deg, max_progression_deg, w + space)
    for index, angle in enumerate(angles):
        x0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(np.deg2rad(angle))
        y0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle))
        y1 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle))
        x2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(
            np.deg2rad(angle + w)
        )
        y2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(
            np.deg2rad(angle + w)
        )
        x3 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle + w))
        y3 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle + w))
        draw.polygon(
            [(x0, y0), (x2, y2), (x3, y3), (x1, y1)], fill=(*polygon_color, 40), width=2
        )

    angles = range(min_progression_deg, int(progression_deg), w + space)
    for index, angle in enumerate(angles):
        x0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(np.deg2rad(angle))
        y0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle))
        y1 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle))
        x2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(
            np.deg2rad(angle + w)
        )
        y2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(
            np.deg2rad(angle + w)
        )
        x3 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle + w))
        y3 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle + w))
        transparency = int(255 - index * 255 / len(angles))
        draw.polygon(
            [(x0, y0), (x2, y2), (x3, y3), (x1, y1)],
            fill=(*polygon_color, 255),
            width=2,
        )

    return background
