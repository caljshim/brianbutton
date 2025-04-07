import pygame
import random
from PIL import Image
import os

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("brianbutton")

IMAGE_PATH = "test.png"

if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"Image file {IMAGE_PATH} not found")

pil_image = Image.open(IMAGE_PATH)
pil_image = pil_image.convert("RGBA")
pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

# Button properties
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 125, 75)
button_color = (168, 60, 50)  # Red
button_text = pygame.font.Font(None, 48).render("brian", True, (255, 255, 255))  # White text
button_text_rect = button_text.get_rect(center=button_rect.center)

button_pressed = False
pressed_scale = 0.9

# Particle class to represent each mini image
class Particle:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.vx = random.uniform(-15, 15)
        self.vy = random.uniform(-15, 15)
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy *= 0.99
        self.angle += self.rotation_speed
        self.vy += 0.1

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_image, rect)

particles = []

particle_size = (100, 217)
scaled_pil_image = pil_image.resize(particle_size, Image.Resampling.LANCZOS)
particle_image = pygame.image.fromstring(
    scaled_pil_image.tobytes(), scaled_pil_image.size, scaled_pil_image.mode
)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_pressed = True
                for _ in range(30):
                    particle = Particle(button_rect.centerx, button_rect.centery, particle_image)
                    particles.append(particle)
        elif event.type == pygame.MOUSEBUTTONUP:
            if button_pressed and button_rect.collidepoint(event.pos):
                button_pressed = False

    for particle in particles[:]:
        particle.update()
        if (particle.x < -particle_size[0] or particle.x > WIDTH + particle_size[0] or
                particle.y < -particle_size[1] or particle.y > HEIGHT + particle_size[1]):
            particles.remove(particle)

    screen.fill((255, 255, 255))

    for particle in particles:
        particle.draw(screen)

    # Calculate button appearance based on pressed state
    if button_pressed:
        scaled_rect = button_rect.copy()
        scaled_rect.width = int(button_rect.width * pressed_scale)
        scaled_rect.height = int(button_rect.height * pressed_scale)
        scaled_rect.center = button_rect.center  # Keep it centered

        scaled_text = pygame.transform.scale(
            button_text,
            (int(button_text.get_width() * pressed_scale), int(button_text.get_height() * pressed_scale))
        )
        scaled_text_rect = scaled_text.get_rect(center=button_rect.center)
    else:
        scaled_rect = button_rect
        scaled_text = button_text
        scaled_text_rect = button_text_rect

    # Draw the scaled button and text
    pygame.draw.rect(screen, button_color, scaled_rect, border_radius=20)
    screen.blit(scaled_text, scaled_text_rect)

    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()