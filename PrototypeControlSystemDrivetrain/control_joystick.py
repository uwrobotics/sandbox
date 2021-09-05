import pygame

def joystick_inits() -> pygame.joystick.Joystick:
    #Pygame inits
    pygame.init()
    pygame.time.Clock().tick(20)
    pygame.joystick.init()

    #Joystick inits
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    controller = joysticks[0]
    controller.init()
    return controller

def read_from_joystick(controller: pygame.joystick.Joystick) -> list:
    for event in pygame.event.get(): # NOTE: THIS IS IMPORTANT! Removing this for loop means the joystick won't work
        pass

    axes = controller.get_numaxes()
    axesvalues = []
    for i in range(axes):
        axis = controller.get_axis(i)
        axesvalues.append(axis)
    
    return axesvalues

if __name__ == "__main__":
    controller = joystick_inits()
    #First element of the joystick is only used for simplification
    while True:
        print(read_from_joystick(controller))
        
        