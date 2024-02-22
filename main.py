import pygame
from game import Game
from objects.drawnobject import DrawnObject
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MIN_WIDTH, MIN_HEIGHT

# pygame setup
pygame.init()

# change the title and icon of the window
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("assets/black-queen.png"))


def main() -> None:
    # setup game
    DrawnObject.set_sizes(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    game = Game()

    # main loop
    while game.active:
        for event in pygame.event.get():
            # if the user hits the x button quit the application
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.VIDEORESIZE:
                # choose the bigger option
                width = max(event.size[0], MIN_WIDTH)
                height = max(event.size[1], MIN_HEIGHT)

                # adjust the screen and reset the sizes in each object
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                DrawnObject.set_sizes(width, height)

            if game.player_to_move:
                # if the players clicks down the mouse, grab the piece
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.grab_piece(*event.pos)

                # if the player releases the mouse, drop the piece
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    game.drop_piece(*event.pos)

        # draw everything to the screen
        game.draw(screen)
        pygame.display.flip()


# run the program
if __name__ == "__main__":
    main()
