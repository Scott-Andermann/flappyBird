import pygame
import random
import neat

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_SPACE,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
gen = 0
high_score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, y=10):
        super(Player, self).__init__()
        self.x = 100
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,30,24)
        self.raw_image = pygame.image.load('bird.png')
        self.angle = 0
        self.image = pygame.transform.rotate(self.raw_image, self.angle)
        self.vel = 0


        # self.surf = pygame.Surface((30, 30))
        # self.surf.fill((0,0,0))
        # surf_center = ((SCREEN_WIDTH - self.surf.get_width()) / 2,
        #                (SCREEN_HEIGHT - self.surf.get_height()) / 2)
        # self.rect = self.surf.get_rect(center=surf_center)

    def update(self):
        self.vel += .35
        self.y = self.y + self.vel
        self.rect.move_ip(0, self.vel)
        if self.vel >= 0:
            self.angle = -30
        else:
            self.angle = 40
        self.image = pygame.transform.rotate(self.raw_image, self.angle)
        """if pressed_keys[K_UP]:
            self.rect.move_ip(0,-40)
            vel = 0
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)"""
        if self.vel > 20:
            self.vel = 20
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y = 570
        #if self.rect.top <= SCREEN_HEIGHT:

        #return vel
    def update_launch(self):
        self.rect.move_ip(0, 0)
        self.vel = -8

class Wall(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Wall, self).__init__()
        #position = random.randint(200,500)
        self.x = 800
        self.y = position
        self.rect = pygame.Rect(self.x,self.y,70,410)
        self.image = pygame.image.load('pipe.png')


        # self.surf = pygame.Surface((70, random.randint(200, 500)))
        # self.surf.fill((34,139,34))
        # self.rect = self.surf.get_rect(center=(800, random.randint(100, SCREEN_HEIGHT-100)))
        self.speed = 5

    def update(self):
        global no_walls
        self.x = self.x - self.speed
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Top_Wall(pygame.sprite.Sprite):
    def __init__(self, position, gap):
        super(Top_Wall, self).__init__()
        self.pos = position-410-gap
        self.x = 800
        self.y = position - 410 - gap
        #position = random.randint(200, 500)
        self.rect = pygame.Rect(self.x, self.y, 70, 410)
        self.image = pygame.image.load('pipe.png')
        self.image = pygame.transform.flip(self.image, False, True)

        # self.surf = pygame.Surface((70, random.randint(200, 500)))
        # self.surf.fill((34,139,34))
        # self.rect = self.surf.get_rect(center=(800, random.randint(100, SCREEN_HEIGHT-100)))
        self.speed = 5

    def update(self):
        self.x = self.x - self.speed
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Need to figure out how to adapt to a NN
def eval_genomes(genomes, config):
    global gen, high_score
    gen +=1
    nets = []
    birds = []
    ge = []
    # no_players = 10
    players = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(y=random.randint(10,200)))
        ge.append(genome)

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    font = pygame.font.Font('freesansbold.ttf', 32)

    ADDWALL = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDWALL, 1500)
    # for i in range(0, no_players):
    #     players.append(Player(y=random.randint(10, 200)))
    walls = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    for player in players:
        all_sprites.add(player)

    """surf = pygame.Surface((50,50))
    surf.fill((0,0,0))
    rect = surf.get_rect()
    
    surf_center = ((SCREEN_WIDTH - surf.get_width())/2,
                   (SCREEN_HEIGHT - surf.get_height())/2)
    
    screen.blit(surf, surf_center)
    pygame.display.flip()"""

    running = True
    clock = pygame.time.Clock()
    count = 0
    no_walls = 0
    text = font.render(str(no_walls), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    text_high_score = font.render(f'High Score: {high_score}', True, (0, 0, 0))
    text_high_score_rect = text_high_score.get_rect()
    text_high_score_rect.center = (120, 50)

    text_birds = font.render(f'Birds Alive: {len(players)}', True, (0,0,0))
    text_birds_rect = text_birds.get_rect()
    text_birds_rect.center = (680, 50)

    text_gen = font.render(f'Generation: {gen}', True, (0, 0, 0))
    text_gen_rect = text_gen.get_rect()
    text_gen_rect.center = (120, 550)
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    for player in players:
                        player.update_launch()
            elif event.type == QUIT:
                running = False
            elif event.type == ADDWALL:
                position = random.randint(200, 500)
                gap = 200
                new_wall = Wall(position)
                top_wall = Top_Wall(position, gap)
                walls.add(new_wall)
                walls.add(top_wall)
                all_sprites.add(new_wall)
                all_sprites.add(top_wall)

        # for player in players:
        #     player.update()

        # p_pos = (player.x, player.y)
        w_pos = []
        for wall in walls:
            w_pos.append((wall.x, wall.y))
        # #print(w_pos)
        if len(w_pos) > 0:
            if len(w_pos) > 2 and w_pos[0][0] < 70:
                w1 = (w_pos[2][0], w_pos[2][1], w_pos[3][1])
            else:
                w1 = (w_pos[0][0], w_pos[0][1], w_pos[1][1])  # x position, y_lower, y_upper
            if w1[0] == 100:
                no_walls += 1  # contribute to fitness
                if no_walls > high_score: high_score = no_walls
            # print(f'wall position: {w1}')
        for x, player in enumerate(players):
            # simple reward function: survive longer and model is more fit
            ge[x].fitness += 0.1
            player.update()
            try:
                output = nets[players.index(player)].activate((player.y, abs(player.y - w1[1]), abs(player.y - w1[2])))
            except UnboundLocalError:
                output = nets[players.index(player)].activate((player.y, abs(player.y - 300), abs(player.y - 300)))
            if output[0] > 0.5:
                player.update_launch()
            # print(f'player position: {p_pos}')

        walls.update()
        screen.fill((255, 255, 255))
        text = font.render(str(no_walls), True, (0, 0, 0))
        text_gen = font.render(f'Generation: {gen}', True, (0, 0, 0))
        text_high_score = font.render(f'High Score: {high_score}', True, (0, 0, 0))
        text_birds = font.render(f'Birds Alive: {len(players)}', True, (0, 0, 0))

        screen.blit(text, text_rect)
        screen.blit(text_gen, text_gen_rect)
        screen.blit(text_high_score, text_high_score_rect)
        screen.blit(text_birds, text_birds_rect)

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        for i, player in enumerate(players):
            if pygame.sprite.spritecollideany(player, walls):
                player.kill()
                ge[i].fitness -= 1
                players.pop(i)
                nets.pop(i)
                ge.pop(i)
            if player.y >= 780 or player.y <= -50:
                player.kill()
                ge[i].fitness -= 1
                players.pop(i)
                nets.pop(i)
                ge.pop(i)

                #running = False
        #print(len(players))
        if len(players) == 0:
            running = False
        pygame.display.flip()
        clock.tick(60)

