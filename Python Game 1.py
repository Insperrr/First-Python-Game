import pygame
import random 
pygame.init()

BACKGROUND = (36, 200, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
TIME = 30

game_font_size = 36
game_font = pygame.font.Font(None, game_font_size)

screen_font_size = 75
screen_font = pygame.font.Font(None, screen_font_size)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_position(self):
        return (self.rect.x, self.rect.y)


class Food(GameObject):
    def __init__(self, width, height, point_amount, color = (20, 60, 75)):
        super().__init__(width = width , height = height, x = random.randint(0, SCREEN_WIDTH - width), y = random.randint (0, SCREEN_HEIGHT - height))
        self.color = color
        self.point_amount = point_amount


    def change_position(self, *objects):
        collision = True
        objects = list(objects)
        objects.remove(self)
        while collision:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            collision = self.check_collision(*objects)
            

    def check_collision(self, *objects):
        for object in objects:
            if self.rect.colliderect(object.rect):
                return True
            else:
                pass
        return False
        

class Player(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.speed = 300
        self.color = (100, 40, 20)
        self.point_amount = 0 


    def move(self, dx, dy, screen, delta_time):
        window_width, window_height = screen.get_size()
        new_x = self.rect.x + dx * delta_time
        new_y = self.rect.y + dy * delta_time
        if 0 <= new_x <= window_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= window_height - self.rect.height:
            self.rect.y = new_y


    def check_collision(self, food):
        return self.rect.colliderect(food.rect)
    

    def movement(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        return dy, dx


    def validate_score(self, food, foods, start = False):
        contact = self.check_collision(food)

        if contact or start:
            food.change_position(self, *foods)
            self.point_amount += food.point_amount


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Pygame Game')
        self.running = True
        self.state = "start"
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            if self.state == "start":
                self.start()
            if self.state == "play":
                self.play()
            if self.state == "end":
                self.end()
    

    def display_start_screen(self):
        self.setup_screen()
        start_text = "Press 'SPACE' To Start"
        self.draw_text(start_text, screen_font, "black", 125, 100)
        pygame.display.flip()


    def start(self):
        while self.state == "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = None
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.state = 'play'

            self.display_start_screen()

    #Unused 
    def end(self):
        pass


    def draw_text(self, text, font, font_col, x, y):
        img = font.render(text, True, font_col)
        self.screen.blit(img, (x, y))


    def play(self):
        start_ticks = pygame.time.get_ticks()
        player = Player(100, 100, 40, 40)
        foods = [Food(50, 50, 1, ("red")),
                 Food(50, 50, 2, ("yellow")),
                 Food(50, 50, 3, ("green"))]
        bad_foods = [Food(80, 80, -1, ("white")),
                     Food(80, 80, -1, ("white")),
                     Food(80, 80, -2, ("white")),
                     Food(80, 80, -2, ("white")),
                     Food(80, 80, -3, ("white")),
                     Food(80, 80, -3, ("white"))]
        all_foods = foods + bad_foods
        # Ensures that all food is spwaned non overlapping
        for food in all_foods:
                player.validate_score(food, all_foods, True)

        player.point_amount = 0
        while self.state == "play":
            elapsed_ticks = pygame.time.get_ticks() - start_ticks
            elapsed_seconds = elapsed_ticks / 1000 
            if elapsed_seconds >= TIME:
                self.state = "start"
            
            #handle inputs
            self.handle_events()
            dy, dx = player.movement()

            #change based on inputs
            delta_time = self.clock.tick(60) / 1000.0
            player.move(dx, dy, self.screen, delta_time)
            for food in all_foods:
                player.validate_score(food, all_foods)
            #change screen
            self.display_game_screen(elapsed_seconds, player, *foods, *bad_foods)


    def display_game_screen(self, elapsed_seconds, player, *args):
        self.setup_screen()
        self.draw_objects(player, *args)
        score = player.point_amount
        score_text = f"Points: {score}"
        time_text = f"Time: {int(elapsed_seconds)}"
        self.draw_text(score_text, game_font, ("black"), 0, 0)
        self.draw_text(time_text, game_font, ("black"), 0, 30)
        pygame.display.flip()


    def draw_objects(self, *args):
        for argument in args:
            argument.draw(self.screen)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


    def setup_screen(self):
        self.screen.fill((BACKGROUND))


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()


if __name__ == "__main__":
    main()
