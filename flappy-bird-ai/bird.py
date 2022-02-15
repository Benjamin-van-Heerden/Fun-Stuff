import pygame 
from images import BIRD_IMGS

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        # tick count is the analog of time
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.image_identifier = 0
        self.helper_current_image = 0
        self.current_image = 0
        self.img = self.IMGS[self.current_image]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        # projectile motion
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        # terminal velocity
        if d >= 16:
            d = 16
        # makes the movement look a bit nicer
        if d < 0:
            d -= 1.5

        self.y = self.y + d

        # if still moving upwards make the bird tilt so that it looks like it
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # tilt the bird downwards (but not too much as it still has forward momentum)
            if self.tilt > -70:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.image_identifier = (self.image_identifier + 1) % self.ANIMATION_TIME
        if self.image_identifier == 0:
            self.helper_current_image += 1
            # some math magic
            self.current_image = (
                3 * self.helper_current_image ** 3
                + self.helper_current_image ** 2
                + self.helper_current_image
            ) % 4
            self.img = self.IMGS[self.current_image]
            # do not want the value to explode
            if self.helper_current_image == 4:
                self.helper_current_image = 0

        # stop flapping if it is falling
        if self.tilt <= -60:
            self.img = self.IMGS[1]

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # the rotated image is off center so we shift its rectangle boundary
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)