import pygame
import sys
import random
import time
import cv2
import numpy as np

pygame.init()
pygame.mixer.init()
# Kích thước cửa sổ
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kien Nghich Nguuuu")

#set chu cua so
font = pygame.font.SysFont("Arial", 30, bold=True)
logo_font = pygame.font.SysFont("Courier New", 30)

# setup
clock = pygame.time.Clock()
lines_index, word_index = 0, 0
last_word_time = time.time()
cap = cv2.VideoCapture("D:\\Download_for_D\\Kirito.mp4")
sound = pygame.mixer.Sound("D:\\Download_for_D\\baybi.mp3")
FPS = cap.get(cv2.CAP_PROP_FPS)
#Colors
BLACK = (0, 0, 0)
Lavender = (230, 230, 250)

# Lyrics
lyrics = [
    ("Baby hoi khi nao ve ?????", 0.45, 0.43),
    ("Anh tung ngay đong xuuuu!!", 0.3, 0.65), 
    ("Chi la 50/50,", 0.25, 0.35),
    ("Anh biet the thoi", 0.26, 0.20),
    ("Nen anh ....", 0.19, 0.19),
    ("Se phai chien thang (Ohhhhhh....)", 0.17, 0.19),
    ("Du nem cay dang (.....Oh)", 0.17, 0.19),
    ("Bay len cao vut !!!", 0.17, 0.26),
    ("Mang ca nang ve ...", 0.18, 0.24),
    ("De thap sang trai tim ", 0.18, 0.22),
    ("Mac cho doi nhan chim ", 0.18, 0.22),
    ("Tinh yeu nay ngoi len", 0.17, 0.22),
    ("Nhu vi sao bang trong dem", 0.17, 0.24),
    ("Sao bang trong dem !!!!!!", 0.18, 3),
]
# tach dong + chu
def wrap_text(words, font, max_width):
    lines, current = [], []
    for w in words:
        test_line = " ".join(current + [w])
        if font.size(test_line)[0] <= max_width:
            current.append(w)
        else:
            lines.append(current)
            current = [w]
    if current:
        lines.append(current)
    return lines

#tao may + mau
fog = []
for i in range(8):
    fog.append([random.randint(0, WIDTH), random.randint(0, HEIGHT),
                random.randint(80, 200), random.randint(40, 100), random.randint(1, 3)])  
    
blood_drops = []

# play nhac
pygame.mixer.Sound.play(sound)

# Main
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            cap.release()

    screen.fill(BLACK)

    ret, frame = cap.read()
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        screen.blit(frame_surface, (0,0))
        clock.tick(FPS)

    for fx in fog:
        rect = pygame.Surface((fx[2], fx[3]), pygame.SRCALPHA)
        rect.fill((200, 200, 200, 30))
        screen.blit(rect, (fx[0], fx[1]))
        fx[0] -= fx[4]
        if fx[0] + fx[2] < 0:
            fx[0] = WIDTH
            fx[1] = random.randint(0, HEIGHT)

    if lines_index < len(lyrics):
        line, word_delay, line_delay = lyrics[lines_index]
        words  = line.split()

        if time.time() - last_word_time > word_delay and word_index < len(words):
            word_index += 1
            for a in range(random.randint(0, 3)):
                blood_drops.append(
                    [random.randint(WIDTH//8-200, WIDTH//8+200), HEIGHT * 3 // 4.1, 0])
            last_word_time = time.time()

        wrapped = wrap_text(words[:word_index], font, WIDTH * 0.3)   
        y_start = HEIGHT * 3 // 4.1 
        for row, line_words in enumerate(wrapped):
            line_text = " ".join(line_words)
            text_surface = font.render(line_text, True, Lavender)
            rect = text_surface.get_rect(topleft=(WIDTH//8, y_start + row*50))
            screen.blit(text_surface, rect) 

        if word_index == len(words):
            if time.time() - last_word_time > line_delay:
                lines_index += 1
                word_index = 0   
                last_word_time = time.time()

    for drop in blood_drops:
        pygame.draw.circle(screen, Lavender, (drop[0], drop[1]), 2)
        drop[1] += 5
    blood_drops = [d for d in blood_drops if d[1] < HEIGHT]

    for _ in range(80):
        pygame.draw.circle(screen, Lavender, (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 1)
    
    logo_text = "TikTok: @ntkienfl"
    logo_surface = logo_font.render(logo_text, True, Lavender)
    logo_rect = logo_surface.get_rect(center=(WIDTH-600, HEIGHT-585))
    screen.blit(logo_surface, logo_rect)
    pygame.display.flip()
    clock.tick(FPS)
   
cap.release()
pygame.mixer.Sound.stop(sound) 
pygame.quit()