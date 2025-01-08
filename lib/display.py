from PIL import Image, ImageDraw, ImageFont
import numpy as np

from lib.utils import interpolate, draw_circles_with_gradient, scale
from lib.colors import framboise, dark_framboise, light_blue, dark_blue, central_dot


def main(width=240, height=240, progression=120000):
    # Angles are measured from 3 o’clock, increasing clockwise.
    min_progression_deg = 90
    max_progression_deg = 360
    alert_per_deg = 1000

    # Create blank image for drawing.
    background = Image.new("RGB", (width, height), "BLACK")
    draw = ImageDraw.Draw(background, "RGBA")

    # Calibration
    #draw.point((120, 120), fill="WHITE")

    # Outer ring
    coord_full = (0, 0, width, height)
    draw.arc(coord_full, 0, 360, fill=dark_framboise, width=4)

    draw_circles_with_gradient(
        draw,
        coord=coord_full,
        f_co=dark_blue, 
        t_co=light_blue, 
        angles0=[0, 80, 190, 250], 
        angles=[60, 60, 30, 80], 
        interval=50, 
        width=5
    )

    # Second round
    draw_circles_with_gradient(
        draw,
        coord=(scale(width, 4), scale(height, 4), width - scale(width, 4), height - scale(height, 4)),
        f_co=(*framboise, 120),
        t_co=(*framboise, 120),
        angles0=[10, 60, 120, 180, 220, 260, 320],
        angles=[30, 40, 20, 30, 20, 30, 20],
        interval=50,
        width=5
    )

    draw.arc((30, 30, width - 30, height - 30), 0, 360, fill=(*framboise, 120), width=8)

    step_major_ticks = 10
    step_minor_ticks = 2
    for angle in range(min_progression_deg, max_progression_deg, step_major_ticks):
        x0 = width / 2 + (width / 2 - scale(width, 10)) * np.cos(np.deg2rad(angle))
        y0 = height / 2 + (height / 2 - scale(height, 10)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 12.5)) * np.cos(np.deg2rad(angle))
        y1 = height / 2 + (height / 2 - scale(height, 12.5)) * np.sin(np.deg2rad(angle))
        draw.line([(x0, y0),(x1, y1)], fill = (255, 255, 255), width = 2)

        #if angle % 20:
        #    x2 = width / 2 + (width / 2 - 75) * np.cos(np.deg2rad(angle))
        #    y2 = width / 2 + (width / 2 - 75) * np.sin(np.deg2rad(angle))
        #    draw.text((x2, y2), "{}k".format(angle-90), anchor="ms")

    for angle in range(min_progression_deg, max_progression_deg - 10, step_minor_ticks):
        x0 = width / 2 + (width / 2 - scale(width, 12.3)) * np.cos(np.deg2rad(angle))
        y0 = height / 2 + (height / 2 - scale(height, 12.3)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 12.5)) * np.cos(np.deg2rad(angle))
        y1 = height / 2 + (height / 2 - scale(width, 12.5)) * np.sin(np.deg2rad(angle))
        draw.line([(x0, y0),(x1, y1)], fill = (255, 255, 255), width = 1)

    for i in range(20):
        radius = scale(width, 28 + i / 5)
        transparency = int(255 / (np.abs(i - 10) + 1))
        draw.arc((radius, radius, width - radius, height - radius), 0, 360, fill=(*dark_blue, transparency), width=4)

    draw.arc((scale(width, 27), scale(height, 27), width - scale(width, 27), height - scale(height, 27)), 0, 360, fill=framboise, width=3)

    size = 35
    font = ImageFont.truetype("fonts/DS-DIGIB.TTF", size)
    draw.text((width/2, width/2 - size / 3), "{}k".format(int(progression/1000)), anchor="mt", font=font)

    # Draw polygone de la meme maniere que les traits (x0, y0, ...)
    # Angles are measured from 3 o’clock, increasing clockwise.
    w = 7
    space = 3
    angles = range(min_progression_deg, max_progression_deg, w + space)
    for index, angle in enumerate(angles):
        x0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(np.deg2rad(angle))
        y0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle))
        y1 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle))
        x2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(np.deg2rad(angle+w))
        y2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(np.deg2rad(angle+w))
        x3 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle+w))
        y3 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle+w))
        draw.polygon([(x0, y0),(x2, y2),(x3, y3),(x1, y1)], fill = (*central_dot, 40), width = 2)


    # Draw polygone de la meme maniere que les traits (x0, y0, ...)
    # Angles are measured from 3 o’clock, increasing clockwise.
    progression_deg = np.min(
        (
            max_progression_deg - min_progression_deg, 
            progression / alert_per_deg
        )
    ) + 90
    angles = range(min_progression_deg, int(progression_deg), w + space)
    for index, angle in enumerate(angles):
        x0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(np.deg2rad(angle))
        y0 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle))
        y1 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle))
        x2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.cos(np.deg2rad(angle+w))
        y2 = width / 2 + (width / 2 - scale(width, 16.6)) * np.sin(np.deg2rad(angle+w))
        x3 = width / 2 + (width / 2 - scale(width, 25)) * np.cos(np.deg2rad(angle+w))
        y3 = width / 2 + (width / 2 - scale(width, 25)) * np.sin(np.deg2rad(angle+w))
        transparency = int(255 - index * 255/len(angles))
        draw.polygon([(x0, y0),(x2, y2),(x3, y3),(x1, y1)], fill = (*central_dot, 255), width = 2)

    return background

