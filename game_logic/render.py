import pygame.sprite


def move_objects(objects, asteroid_spawner, movement_x, movement_y, t):
    """ Render objects distance when player is moving """

    for obj in objects:
        if not isinstance(obj, pygame.sprite.Group):
            obj.rect.center = (obj.rect.centerx + t * movement_x,
                               obj.rect.centery + t * movement_y)
        else:
            for sub_obj in obj:
                sub_obj.rect.center = (sub_obj.rect.centerx + t * movement_x,
                                       sub_obj.rect.centery + t * movement_y)

    # asteroid_spawner.spawnX, asteroid_spawner.spawnY = (asteroid_spawner.spawnX + t * movement_x,
    #                                                     asteroid_spawner.spawnY + t * movement_y)
