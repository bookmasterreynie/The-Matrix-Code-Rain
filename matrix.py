import pygame
import random
import sys

# Initial screen settings
WIDTH, HEIGHT = 1280, 720
FPS = 60
BASE_FONT_SIZE = 28
HEAD_FONT_SIZE = 36

# Colors
CRT_BLACK = (5, 10, 5)
TRAIL_GREEN = (0, 180, 50)
HEAD_GREEN = (150, 255, 150)

# Katakana symbols + numbers
SYMBOLS = list("アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("The Matrix")
clock = pygame.time.Clock()

# Fonts (will be updated dynamically)
font = pygame.font.SysFont("MS Gothic", BASE_FONT_SIZE, bold=True)
head_font = pygame.font.SysFont("MS Gothic", HEAD_FONT_SIZE, bold=True)

# Helper: create streams for a given width
def create_streams(width, height, font_size):
    columns = width // font_size
    streams = []
    for i in range(columns):
        x_offset = i * font_size + random.randint(0, 3)
        stream_length = random.randint(15, 30)
        speed = random.randint(1, 2)  # discrete pixel steps
        y = random.randint(-height, 0)
        pause_timer = random.randint(0, 30)
        streams.append({
            "x": x_offset,
            "y": y,
            "length": stream_length,
            "speed": speed,
            "symbols": [random.choice(SYMBOLS) for _ in range(stream_length)],
            "update_timer": random.randint(5, 20),
            "pause_timer": pause_timer
        })
    return streams

# Initial streams
FONT_SIZE = BASE_FONT_SIZE
HEAD_FONT_SIZE = int(BASE_FONT_SIZE * 1.3)
streams = create_streams(WIDTH, HEIGHT, FONT_SIZE)

# Draw a single stream
def draw_stream(stream):
    x = stream["x"]
    y = stream["y"]
    length = stream["length"]

    for i in range(length):
        char_y = y - i * FONT_SIZE
        if char_y < -FONT_SIZE:
            continue
        symbol = stream["symbols"][i]

        if i == 0:
            color = HEAD_GREEN
            alpha = random.randint(200, 255)
            for offset in [(-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,1)]:
                glow = head_font.render(symbol, True, HEAD_GREEN)
                glow.set_alpha(80)
                screen.blit(glow, (x + offset[0], char_y + offset[1]))
            s = head_font.render(symbol, True, color)
        else:
            color = TRAIL_GREEN
            alpha = max(30, 255 - i * (255 // length))
            s = font.render(symbol, True, color)

        jitter_x = x + random.randint(-1, 1)
        s.set_alpha(alpha)
        screen.blit(s, (jitter_x, char_y))

# Draw scanlines
def draw_scanlines():
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(screen, (0, 20, 0), (0, y), (WIDTH, y), 1)

# Scale fonts and adjust streams if window size changes
def adjust_to_new_size(new_width, new_height):
    global WIDTH, HEIGHT, FONT_SIZE, HEAD_FONT_SIZE, font, head_font, streams
    WIDTH, HEIGHT = new_width, new_height
    FONT_SIZE = BASE_FONT_SIZE
    HEAD_FONT_SIZE = int(BASE_FONT_SIZE * 1.3)
    font = pygame.font.SysFont("MS Gothic", FONT_SIZE, bold=True)
    head_font = pygame.font.SysFont("MS Gothic", HEAD_FONT_SIZE, bold=True)

    # Add extra columns if window bigger than current streams
    existing_columns = len(streams)
    new_columns = WIDTH // FONT_SIZE
    if new_columns > existing_columns:
        for i in range(existing_columns, new_columns):
            x_offset = i * FONT_SIZE + random.randint(0, 3)
            stream_length = random.randint(15, 30)
            speed = random.randint(1, 2)
            y = random.randint(-HEIGHT, 0)
            pause_timer = random.randint(0, 30)
            streams.append({
                "x": x_offset,
                "y": y,
                "length": stream_length,
                "speed": speed,
                "symbols": [random.choice(SYMBOLS) for _ in range(stream_length)],
                "update_timer": random.randint(5, 20),
                "pause_timer": pause_timer
            })

# Main loop
fullscreen = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_f:  # toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                WIDTH, HEIGHT = screen.get_size()
                adjust_to_new_size(WIDTH, HEIGHT)
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                adjust_to_new_size(event.w, event.h)
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    # Fade overlay for trails
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(CRT_BLACK)
    fade_surface.set_alpha(60)
    screen.blit(fade_surface, (0, 0))

    # Draw streams
    for stream in streams:
        draw_stream(stream)

        if stream["pause_timer"] > 0:
            stream["pause_timer"] -= 1
        else:
            stream["y"] += stream["speed"]
            if random.random() < 0.02:
                stream["pause_timer"] = random.randint(1, 10)

        if stream["pause_timer"] == 0:
            stream["update_timer"] -= 1
            if stream["update_timer"] <= 0:
                stream["symbols"] = [random.choice(SYMBOLS) for _ in range(stream["length"])]
                stream["update_timer"] = random.randint(5, 20)

        if stream["y"] - stream["length"] * FONT_SIZE > HEIGHT:
            stream["y"] = random.randint(-200, 0)
            stream["length"] = random.randint(15, 30)
            stream["speed"] = random.randint(1, 2)
            stream["symbols"] = [random.choice(SYMBOLS) for _ in range(stream["length"])]
            stream["update_timer"] = random.randint(5, 20)
            stream["pause_timer"] = random.randint(0, 30)
            stream["x"] = (streams.index(stream)) * FONT_SIZE + random.randint(0, 3)

    # Draw scanlines overlay
    draw_scanlines()

    pygame.display.flip()
    clock.tick(FPS)
