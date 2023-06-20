import pygame
import time
import random
import os


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.clock = pygame.time.Clock()
        
        #Размер окна 
        self.dis_width = 800
        self.dis_height = 800
        
        #заголовок
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Змейка')
        
        #звуки
        self.eat_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "eat_sound.wav"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "game_over.mp3"))
        
        #параметры змейки
        self.snake_block = 10
        self.snake_speed = 15
        self.snake_List = []
        self.Length_of_snake = 1
        
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        
        #логические значения
        self.game_over = False
        self.game_close = False
        self.fullscreen = False
        self.paused = False
        self.menu_active = False
        self.played_game_over_sound = False

        #стартовая позиция
        self.x1 = self.dis_width / 2
        self.y1 = self.dis_height / 2
        
        self.x1_change = 0
        self.y1_change = 0
        
        #количество помех
        self.num_obstacles = 100 
        
        #генерация хавки
        self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        self.foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
        
        #параметры анимации хавки
        self.eat_animation_frames = 10
        self.eat_animation_count = 0
        self.eat_animation_size = 30

    def generate_obstacles(self):
        self.obstacles = []
        for _ in range(self.num_obstacles):
            obstacle_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
            obstacle_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
            obstacle = (obstacle_x, obstacle_y)
            if obstacle != (self.foodx, self.foody):  # Проверка на пересечение с едой
                self.obstacles.append(obstacle)
            else:
                # Если препятствие пересекается с едой, генерируем новые координаты
                obstacle_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                obstacle_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                obstacle = (obstacle_x, obstacle_y)
                self.obstacles.append(obstacle)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            info = pygame.display.Info()
            self.dis = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            self.dis_width = info.current_w
            self.dis_height = info.current_h
        else:
            self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))


    def your_score(self, score):
        return str(score)

    def our_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.dis, (255, 255, 255), [x[0], x[1], self.snake_block, self.snake_block])

    def message(self, msg, color, w, h):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / w, self.dis_height / h])

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.dis, (255, 0, 0), [obstacle[0], obstacle[1], self.snake_block, self.snake_block])



    def game_loop(self):
        self.generate_obstacles()
        while not self.game_over:
            while self.game_close:
                self.dis.fill((255, 200, 0))
                self.message("Вы проиграли!", (255, 0, 0), 3, 5)
                self.message("C-играть заново Q-выйти из игры", (255, 0, 0), 6, 3.5)
                self.message("Ваш счет:" + str(self.Length_of_snake - 1), (255, 255, 255), 3, 2.5)
                self.your_score(self.Length_of_snake - 1)
                pygame.display.update()

                if not self.played_game_over_sound:
                    self.game_over_sound.play()
                    self.played_game_over_sound = True


                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        if event.key == pygame.K_c:
                            self.__init__()  # Переинициализация объекта игры
                            self.game_loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.x1_change != self.snake_block:  
                        self.x1_change = -self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT and self.x1_change != -self.snake_block:  
                        self.x1_change = self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP and self.y1_change != self.snake_block:  
                        self.y1_change = -self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN and self.y1_change != -self.snake_block:  
                        self.y1_change = self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()

            if self.paused:
                #self.message("Пауза", (255, 255, 255), 2, 2)
                pygame.display.update()
                continue

            if self.x1 >= self.dis_width or self.x1 < 0 or self.y1 >= self.dis_height or self.y1 < 0:
                self.game_close = True
            self.x1 += self.x1_change
            self.y1 += self.y1_change
            self.dis.fill((24, 24, 24))

            if self.x1 == self.foodx and self.y1 == self.foody:
                if (self.foodx, self.foody) not in self.obstacles:  # Проверка на пересечение с препятствием
                    self.Length_of_snake += 1
                    self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                    self.foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                    self.eat_animation_count = self.eat_animation_frames
                    self.eat_sound.play()

            if self.eat_animation_count > 0:
                eat_animation_size = self.eat_animation_size * self.eat_animation_count // self.eat_animation_frames
                pygame.draw.rect(self.dis, (0, 255, 0), [
                    self.foodx + (self.snake_block - eat_animation_size) / 2,
                    self.foody + (self.snake_block - eat_animation_size) / 2,
                    eat_animation_size,
                    eat_animation_size
                ])
                self.eat_animation_count -= 1
            else:
                pygame.draw.rect(self.dis, (0, 255, 0), [self.foodx, self.foody, self.snake_block, self.snake_block])

            snake_Head = []
            snake_Head.append(self.x1)
            snake_Head.append(self.y1)
            self.snake_List.append(snake_Head)
            if len(self.snake_List) > self.Length_of_snake:
                del self.snake_List[0]

            for x in self.snake_List[:-1]:
                if x == snake_Head or (snake_Head[0], snake_Head[1]) in self.obstacles:
                    self.game_close = True

            self.our_snake(self.snake_List)
            self.draw_obstacles()
            self.your_score(self.Length_of_snake - 1)

            pygame.display.set_caption('Змейка | Счет: ' + str(self.Length_of_snake - 1))
            pygame.display.update()

            self.clock.tick(self.snake_speed)

        pygame.quit()
        raise SystemExit

if __name__ == "__main__":
    game = SnakeGame()
    game.game_loop()