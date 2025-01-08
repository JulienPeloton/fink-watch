from PIL import Image, ImageDraw, ImageFont
import numpy as np

from lib.utils import interpolate, draw_circles_with_gradient, scale
from lib.colors import framboise, dark_framboise, light_blue, dark_blue, central_dot


def main(width=240, height=240):
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

    draw.arc((30, 30, width - 30, height - 30), 0, 360, fill=framboise, width=8)

    # Angles are measured from 3 o’clock, increasing clockwise.
    for angle in range(90, 360, 10):
        x0 = width / 2 + (width / 2 - scale(width, 10)) * np.cos(np.deg2rad(angle))
        y0 = height / 2 + (height / 2 - scale(height, 10)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 12.5)) * np.cos(np.deg2rad(angle))
        y1 = height / 2 + (height / 2 - scale(height, 12.5)) * np.sin(np.deg2rad(angle))
        draw.line([(x0, y0),(x1, y1)], fill = (255, 255, 255), width = 2)

        #if angle % 20:
        #    x2 = width / 2 + (width / 2 - 75) * np.cos(np.deg2rad(angle))
        #    y2 = width / 2 + (width / 2 - 75) * np.sin(np.deg2rad(angle))
        #    draw.text((x2, y2), "{}k".format(angle-90), anchor="ms")

    for angle in range(90, 350, 2):
        x0 = width / 2 + (width / 2 - scale(width, 12.3)) * np.cos(np.deg2rad(angle))
        y0 = height / 2 + (height / 2 - scale(height, 12.3)) * np.sin(np.deg2rad(angle))
        x1 = width / 2 + (width / 2 - scale(width, 12.5)) * np.cos(np.deg2rad(angle))
        y1 = height / 2 + (height / 2 - scale(width, 12.5)) * np.sin(np.deg2rad(angle))
        draw.line([(x0, y0),(x1, y1)], fill = (255, 255, 255), width = 1)

    for i in range(20):
        radius = scale(width, 28 + i / 5)
        transparency = int(255 / (np.abs(i - 10) + 1))
        draw.arc((radius, radius, width - radius, height - radius), 0, 360, fill=(*light_blue, transparency), width=4)

    #draw.arc((160, 160, width - 160, height - 160), 0, 360, fill=light_blue, width=4)
    #draw.arc((163, 163, width - 160, height - 160), 0, 360, fill=light_blue, width=4)

    draw.arc((scale(width, 27), scale(height, 27), width - scale(width, 27), height - scale(height, 27)), 0, 360, fill=framboise, width=3)

    #for i in range(20):
    #    radius = 220 + i
    #    transparency = int(i * 255 / 20)
    #    print(transparency)
    #    draw.arc((radius, radius, width - radius, height - radius), 0, 360, fill=(*central_dot, transparency), width=2)

    draw.text((width/2, width/2), "120k", anchor="mb")

    # Draw polygone de la meme maniere que les traits (x0, y0, ...)
    # Angles are measured from 3 o’clock, increasing clockwise.
    w = 7
    space = 3
    angles = range(90, 360, w + space)
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
    angles = range(90, 200, w + space)
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

