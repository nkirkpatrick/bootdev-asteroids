import sys
import pygame
# Import screen size constants so we can set up the window
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
# Import logging helpers to track game events and state
from logger import log_state, log_event
# Import all game objects
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot



def main():
    # Print startup info to the terminal so we know the game is launching correctly
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame — this must happen before using any pygame features
    pygame.init()
    # Create the game window with the specified width and height
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Sprite groups let us manage multiple game objects at once
    # "updatable" holds everything that needs its logic updated each frame (movement, etc.)
    updatable = pygame.sprite.Group()
    # "drawable" holds everything that needs to be drawn to the screen each frame
    drawable = pygame.sprite.Group()
    # "asteroids" holds only asteroids so we can check them for collisions separately
    asteroids = pygame.sprite.Group()
    # "shots" holds only bullets so we can check them against asteroids
    shots = pygame.sprite.Group()

    # Tell each class which groups to automatically add themselves to when created
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)   # AsteroidField isn't drawn directly
    Shot.containers = (updatable, drawable, shots)
    Player.containers = (updatable, drawable)

    # Create the player and place them in the center of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Create the asteroid field, which spawns asteroids over time
    asteroid_field = AsteroidField()

    running = True

    # Clock keeps the game running at a consistent speed regardless of computer performance
    clock = pygame.time.Clock()
    # dt (delta time) is the time in seconds since the last frame — used to make movement
    # frame-rate independent (so the game runs the same speed on fast and slow computers)
    dt = 0

    # Main game loop — runs once per frame until the player quits
    while running:
        # Log the current game state (useful for debugging)
        log_state()

        # Check for window/input events (like clicking the X button to close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Exit the game loop if the user closes the window

        # Clear the screen by filling it with black before drawing the new frame
        screen.fill("black")

        # Update all game objects (move the player, asteroids, shots, etc.)
        updatable.update(dt)

        # Check for collisions between asteroids and the player or shots
        for asteroid in asteroids:
            # If an asteroid touches the player, the game is over
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            # If a shot hits an asteroid, destroy the shot and split the asteroid
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()    # Remove the shot from all groups
                    asteroid.split()  # Break the asteroid into smaller pieces (or destroy it)

        # Draw all visible game objects to the screen
        for obj in drawable:
            obj.draw(screen)

        # Push the finished frame to the display (makes everything we drew visible)
        pygame.display.flip()

        # Wait to cap the game at 60 frames per second, then get the elapsed time in seconds
        dt = clock.tick(60) / 1000

# Only run main() if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
