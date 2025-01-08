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
"""Various utilities"""

from PIL import Image


def generate_logo():
    """Generate the logo for the screen

    Returns
    -------
    out: Image
        240x240 logo
    """
    img = Image.open("pictures/Fink_SecondaryLogo_WEB.png")
    img = img.convert("RGBA")
    img = img.resize((240, 240))
    img = img.rotate(180)
    return img


def scale(size, pc):
    """Scale size

    Parameters
    ----------
    size: int
        Input length in pixels
    pc: float
        Percentage of the input length
    """
    return pc / 100 * size


def interpolate(f_co, t_co, interval):
    """Interpolate colors

    Parameters
    ----------
    f_co: list of 3 int
        Starting RGB tuple
    t_co: list of 3 int
        Ending RGB tuple
    interval: int
        Interval between steps

    Yields
    ------
    out: list of 3 int
        Interpolated colors
    """
    det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]


def draw_arcs_with_gradient(
    draw, coord, f_co, t_co, angles0, angles, interval=20, width=5
):
    """Draw arcs with a gradient color

    Parameters
    ----------
    draw: ImageDraw
        Current drawer
    coord: list of 4 int
        Two points to define the bounding box: [x0, y0, x1, y1]
    f_co: list of 3 int
        Starting RGB tuple
    t_co: list of 3 int
        Ending RGB tuple
    angles0: list of float
        Starting angles of the arcs, in degree
    angles: list of tuples
        Opening angles for arcs, in degree
    interval: int
        Interval between steps, for the color interpolation
    width: int
        Width of the arc, in pixels
    """
    for angle0, angle in zip(angles0, angles):
        for i, color in enumerate(interpolate(f_co, t_co, interval)):
            draw.arc(
                coord,
                angle0 + angle / interval * i,
                angle0 + angle / interval * (i + 1),
                fill=tuple(color),
                width=width,
            )
