import pygame
from network import Network

tankImage = pygame.image.load('assets/sprites/tank.png')
shotImage = pygame.image.load('assets/sprites/shot.png')
bgImage = pygame.image.load('assets/sprites/background.png')


def create_window():
    screen_width = 800
    screen_height = 600
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tanks Online")
    pygame.font.init()

    return win


def redraw_window(win, game):
    win.fill((255, 255, 255))

    win.blit(bgImage, (0, 0))

    points = []

    for tank_id in game.tanks:
        points.append((tank_id, game.tanks[tank_id].points))
        if not game.tanks[tank_id].is_hit:
            game.tanks[tank_id].draw(win, tankImage)

    show_points(points, win)

    for shot in game.shots:
        shot.draw(win, shotImage)

    pygame.display.update()


def show_points(points, win):
    font = pygame.font.SysFont('Arial', 30)
    points = sorted(points, key=lambda tup: -tup[1])
    lines = []
    for tup in points:
        ind, pt = tup
        lines.append("tank " + str(ind) + " : " + str(pt))

    i = 0
    for line in lines:
        text = font.render(line, False, (0, 150, 0))
        win.blit(text, (10, i * 30))
        i += 1


def main():
    win = create_window()
    n = Network()
    run = True

    local_player = n.get_p()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

        commands = local_player.make_commands()

        if not commands:
            game = n.send([("none", (0, 0))])
        else:
            game = n.send(commands)

        redraw_window(win, game)


main()
