def collision_detection(obj_rect, rects):
    collided = []
    for tile in rects:
        if obj_rect.colliderect(tile):
            collided.append(tile)
    return collided
