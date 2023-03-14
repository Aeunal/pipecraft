import pygame
from world import World
from camera import Camera

def quit_game():
    pygame.quit()
    quit()

def main():
    pygame.init()
    
    FULLSCREEN_MODE = True
    if FULLSCREEN_MODE:
        # Get the screen size
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        display = (screen_width, screen_height)
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
    else:
        display = (800, 600)
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        
    # Get the screen center coordinates
    #screen_center = (display[0] // 2, display[1] // 2)
    #pygame.mouse.set_pos(screen_center)

    # Create world and camera objects
    world = World()
    camera = Camera()

    # gluPerspective(60, (display[0] / display[1]), 0.1, 100.0)
    # glTranslatef(0.0, 0.0, -40.0)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            camera.handle_event(event)

        # Handle key input
        keys = pygame.key.get_pressed()
        # Check if ESC key is pressed
        if keys[pygame.K_ESCAPE]:
            quit_game()
        
        camera.handle_keys(keys)
        world.handle_keys(keys)

        # Update camera and draw world
        camera.update()
        world.draw(camera)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()