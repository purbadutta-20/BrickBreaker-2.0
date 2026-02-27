from settings import WHITE, YELLOW

def draw_hud(screen, font, score, lives, level, high_score):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20,10))
    screen.blit(font.render(f"Lives: {lives}", True, WHITE), (20,40))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (750,10))
    screen.blit(font.render(f"High: {high_score}", True, YELLOW), (700,40))