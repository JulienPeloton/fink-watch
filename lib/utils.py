from PIL import Image

def generate_logo():
    # Logo intro
    img = Image.open('pictures/Fink_SecondaryLogo_WEB.png')
    img = img.convert("RGBA")
    img = img.resize((240, 240))
    img = img.rotate(180)
    return img

def scale(size, pc):
    return pc / 100 * size

# Gradient
def interpolate(f_co, t_co, interval):
    det_co =[(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]

def draw_circles_with_gradient(draw, coord, f_co, t_co, angles0, angles, interval=20, width=5):
    """
    """
    for angle0, angle in zip(angles0, angles):
        for i, color in enumerate(interpolate(f_co, t_co, interval)):
            # Angles are measured from 3 o’clock, increasing clockwise.
            draw.arc(
                coord,
                angle0 + angle / interval*i,
                angle0 + angle / interval * (i + 1),
                fill=tuple(color),
                width=width
            )
