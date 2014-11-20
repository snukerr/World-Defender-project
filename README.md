World-Defender-project
======================

Projekti koodirepositoorium/MTAT.03.100

======================

import pygame

pygame.init()

ekraani_pind = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
ekraani_pind.fill( (0,255,0) )

pilt1 = pygame.image.load("fon_space.jpg")
ekraani_pind.blit(pilt1, (-350, -170))

pygame.display.flip()

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

pygame.quit()
