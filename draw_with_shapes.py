import random
from collections import namedtuple

import numpy as np
from PIL import Image, ImageDraw

Circle = namedtuple('Circle', ['x', 'y', 'r'])

DRAW_OVER_IMAGE = False
DRAW_OVER_IMAGE_PATH = ''
if DRAW_OVER_IMAGE:
    draw_over_image_np = np.asarray(Image.open(DRAW_OVER_IMAGE_PATH))

RESULTING_IMAGE_PATH = 'shapes.png'

TOTAL_SHAPES = 6500
NUMEBR_OF_SIDES_PER_SHAPE = 6

BACKGROUND_COLOUR = (255,255,255)
GREYS = [
    (154,155,156),
    (213,214,210),
]
BLUES = [
    (  0, 92,132),
    (  0,122,135),
]
GREENS = [
    (91, 143, 34),
    (171,173, 35),
]
YELLOWS = [
    (215,169,  0),
    (202,119,  0),
]
SCALE_FACTOR = 50

CANVAS_WIDTH = int(20*SCALE_FACTOR)
CANVAS_HEIGHT = int(14*SCALE_FACTOR)
IMAGE_WIDTH = CANVAS_WIDTH
IMAGE_HEIGHT = CANVAS_HEIGHT
DIAMOND_MAJOR_SIDE = int(16.6*SCALE_FACTOR)
DIAMOND_MINOR_SIDE = int(10.6*SCALE_FACTOR)
FLAG_CIRCLE_RADIUS = int(3.5*SCALE_FACTOR)

MAX_CIRCLE_RADIUS = int(CANVAS_HEIGHT/50)
MIN_CIRCLE_RADIUS = int(CANVAS_HEIGHT/200)

def main():
    flag_canvas = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT),
                            BACKGROUND_COLOUR)
    draw_image = ImageDraw.Draw(flag_canvas)

    circles = []

    try:

        for i in range(TOTAL_SHAPES-1):
            max_circle_radius = MAX_CIRCLE_RADIUS
            circle, rotation = generate_circle(max_radius=max_circle_radius)
            print(f'{i}/{TOTAL_SHAPES}')
            tries = 0
            while any(circles_intersect(circle, circle2) for circle2 in circles):
                tries += 1
                if max_circle_radius > MIN_CIRCLE_RADIUS+1:
                    max_circle_radius -= 1
                circle, rotation = generate_circle(max_radius=max_circle_radius)
            print(f'\tTried {tries} times')
            draw_inside_circle(draw_image, circle,
                               n_sides=NUMEBR_OF_SIDES_PER_SHAPE,
                               rotation=rotation)
            circles.append(circle)

    except (KeyboardInterrupt, SystemExit):
        pass

    flag_canvas.show()
    flag_canvas.save(RESULTING_IMAGE_PATH)

def draw_inside_circle(draw_image, circle,
                       n_sides=None, is_regular=True, rotation=0):
    fill_colour = calculate_circle_colour(circle.x, circle.y)
    if n_sides is not None:
        if is_regular:
            draw_image.regular_polygon((circle.x, circle.y, circle.r),
                                        n_sides,
                                        rotation=rotation,
                                        fill=fill_colour,
                                        outline=fill_colour)
    else:
        draw_image.ellipse((circle.x-circle.r, circle.y-circle.r,
                            circle.x+circle.r, circle.y+circle.r),
                            fill=fill_colour,
                            outline=fill_colour)

def calculate_circle_colour(x, y):
    fill_colour = BACKGROUND_COLOUR
    if DRAW_OVER_IMAGE and point_inside_draw_over_image(x, y):
        fill_colour = random.choice(BLUES)
    elif point_inside_circle(x, y):
        # fill_colour = random.choice(GREYS)
        fill_colour = random.choice(BLUES)
    elif point_inside_diamond(x, y):
        fill_colour = random.choice(YELLOWS)
    else:
        fill_colour = random.choice(GREENS)
    return fill_colour

def get_shape_drawing_function(draw_image, n_sides, is_regular):
    if n_sides is not None:
        if is_regular:
            return draw_image.regular_polygon

    return draw_image.ellipse


def generate_circle(min_radius=MIN_CIRCLE_RADIUS,
                    max_radius=MAX_CIRCLE_RADIUS):
    x = random.randrange(-CANVAS_WIDTH/2, CANVAS_WIDTH/2) + CANVAS_WIDTH/2
    y = random.randrange(-CANVAS_HEIGHT/2, CANVAS_HEIGHT/2) + CANVAS_HEIGHT/2
    radius = random.randrange(min_radius, max_radius)
    rotation = random.randrange(0, 360)
    return Circle(x, y, radius), rotation

def point_inside_draw_over_image(x, y):
    return np.any(draw_over_image_np[int(y)][int(x)] != 0)

def point_inside_circle(x, y):
    abs_x, abs_y = relative_coordinates_to_absolute(x, y)
    return abs_x**2 + abs_y**2 <= FLAG_CIRCLE_RADIUS**2

def point_inside_diamond(x, y):
    abs_x, abs_y = relative_coordinates_to_absolute(x, y)
    m = DIAMOND_MINOR_SIDE/DIAMOND_MAJOR_SIDE
    n = DIAMOND_MINOR_SIDE/2
    return (
        abs_y <= abs(abs_x)*(-1)*m + n
        and
        abs_y >= abs(abs_x)*m - n
    )

def circles_intersect(circle_1, circle_2):
    return ( (circle_1.x - circle_2.x)**2 + (circle_1.y - circle_2.y)**2
             < (circle_1.r + circle_2.r)**2 )

def relative_coordinates_to_absolute(x, y):
    return (int(x-CANVAS_WIDTH/2), int(y-CANVAS_HEIGHT/2))

if __name__ == '__main__':
    main()
