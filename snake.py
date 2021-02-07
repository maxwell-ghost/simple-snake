# coding=utf-8

#导入一些模块
import pygame, pygame.freetype
import random, sys, os

"""
set_up
这里是一些基本设置
"""
#黑白灰颜色设置
white_color = (255, 255, 255)
grey_color = (230, 230, 230)
black_color = (0, 0, 0)
#窗口大小，窗口标题，最小单元
window_size = width, height = 400, 250
window_title = "Snake"
cell = 10


"""
objects
这里是自己写的一些类
"""
#环境准备类
class Environment(object):
    def __init__(self, window_size, window_title, window_color):
        pygame.init() #初始化游戏引擎
        pygame.display.set_caption(window_title) #设置窗口标题
        self.screen = pygame.display.set_mode(window_size) #设置游戏界面大小
        self.clock = pygame.time.Clock() #游戏时钟
        self.my_font = pygame.freetype.Font(os.path.join("fonts", "Righteous-Regular.ttf")) #游戏所用的字体

        #图标设置
        img = pygame.image.load(os.path.join("images", "icon.ico")) #载入图标
        pygame.display.set_icon(img)

#菜单类
class MainMenu(object):
    def __init__(self, menu_name):
        self.menu_name = menu_name #菜单选项名字列表
        self.menu_num = len(menu_name) #菜单项的个数
        self.menu_state = 0 #目前哪个项处于选中
        self.is_loop = True #是否循环
    
    #菜单界面渲染函数
    def render(self, env):
        env.screen.fill(white_color) #导入环境对象
        #渲染菜单图
        menu_head_image = pygame.image.load(os.path.join("images", "menu_head.png")).convert()
        env.screen.blit(menu_head_image, (10, 10))
        #渲染我的信息和版本信息
        env.my_font.render_to(env.screen, (260, 225), "@Maxwell All rights reserved", black_color, None, size=9)
        env.my_font.render_to(env.screen, (260, 235), "version 1.0", black_color, None, size=9)
        #渲染分割线
        pygame.draw.lines(env.screen, black_color, False, [[251, 9], [251, 241]], 1)
        #渲染菜单选项
        for x in range(self.menu_num):
            #如果当前菜单处于选中状态，渲染为黑色，否则为灰色
            if self.menu_state == x:
                env.my_font.render_to(env.screen, (260, 10 + x*22), self.menu_name[x] + " :)", black_color, None, size=20)
            else: env.my_font.render_to(env.screen, (260, 10 + x*22), self.menu_name[x], grey_color, None, size=20)
        #更新屏幕
        pygame.display.update()
    
    #菜单运行函数
    def run(self, env):
        self.play_bgm()
        while self.is_loop:
            #获取当前发生的时间
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit() #如果点击×，直接退出
                if event.type == pygame.KEYDOWN:
                    #如果键盘按下
                    if event.key == pygame.K_DOWN:
                        self.menu_state += 1
                        self.menu_state %= self.menu_num
                    elif event.key == pygame.K_UP:
                        self.menu_state -= 1
                        self.menu_state %= self.menu_num
                    
                    #如果按回车，表示选择
                    elif event.key == pygame.K_RETURN:
                        if self.menu_state == 0:
                            game = Game()
                            game.run(env)
                        elif self.menu_state == 1:
                            pass
                        elif self.menu_state == 2:
                            pass
                        elif self.menu_state == 3:
                            self.stop_bgm()
                            sys.exit() 
            self.render(env) #渲染菜单
            env.clock.tick(24) #这里设置菜单界面帧率

    #音乐播放函数
    def play_bgm(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("sounds", "menu_bgm.mp3"))
        pygame.mixer.music.play(-1, 0.0)

    #音乐停止函数
    def stop_bgm(self):
        pygame.mixer.music.stop()
   
#蛇类
class Snake(object):
    def __init__(self):
        self.pos = [[120, 120], [110, 120], [100, 120], [90, 120]] #蛇的初始位置
        self.head_pos = [120, 120] #蛇的头
        self.scores = 0 #得分
        self.direction = "RIGHT" #蛇的移动方向
        self.cd_direction = "RIGHT" #键盘按下后的方向
        self.is_die = False #蛇是否死亡

        self.head_image = pygame.image.load(os.path.join("images", "head.png")).convert() #载入蛇头的图片
    
    #判断蛇是否咬到自己
    def is_bite_me(self):
        if self.head_pos in self.pos[1:]:
            return True
        else: return False

    #判断蛇是否撞墙
    def is_hit_wall(self):
        if self.head_pos[0]  > 240  or self.head_pos[0] < 0 or self.head_pos[1] > 240 or self.head_pos[1] < 0:
            return True
        else:
            return False

    #蛇走下一步
    def next_step(self, food):
        if self.direction == "RIGHT": self.head_pos[0] += cell
        elif self.direction == "LEFT": self.head_pos[0] -= cell
        elif self.direction == "UP": self.head_pos[1] -= cell
        elif self.direction == "DOWN": self.head_pos[1] += cell

        self.pos.insert(0, list(self.head_pos))
        #蛇是否吃到食物
        if self.head_pos != food.pos:
            self.pos.pop()
        else:
            self.scores += 1
            food.creat_food(self)
        #判断蛇是否死亡
        if self.is_bite_me() or self.is_hit_wall(): self.is_die = True
    
    #渲染蛇的函数
    def draw_me(self, screen):
        #给蛇头图片转向
        if self.direction == "LEFT": head_image_copy = self.head_image
        elif self.direction == "RIGHT": head_image_copy = pygame.transform.rotate(self.head_image, -180)
        elif self.direction == "UP": head_image_copy = pygame.transform.rotate(self.head_image, -90)
        elif self.direction == "DOWN": head_image_copy = pygame.transform.rotate(self.head_image, -270)
        #渲染蛇头
        screen.blit(head_image_copy, self.pos[0])
        #渲染蛇的身体
        for order, pos in enumerate(self.pos):
            if order == 0: continue
            else: pygame.draw.rect(screen, black_color, pygame.Rect(pos[0] + 1, pos[1] + 1, cell - 2, cell - 2))

#食物类
class Food(object):
    def creat_food(self, snake):
        self.pos = [random.randrange(1, 25) * cell, random.randrange(1, 25) * cell]
        while (self.pos in snake.pos):
            self.pos = [random.randrange(1, 25) * cell, random.randrange(1, 25) * cell]   
    
    def draw_me(self, screen):
        pygame.draw.rect(screen, black_color, pygame.Rect(self.pos[0] + 1, self.pos[1] + 1, cell - 2, cell - 2))

#墙类，但是其实只有一根线
class Wall(object):
    def draw_me(self, screen):
        pygame.draw.lines(screen, black_color, False, [[251, 10], [251, 240]], 1)

#游戏信息类，包括分数和激励的话语
class GameInfo(object):
    def __init__(self):
        self.words = ["Amazing", "Great", "Unbelievable", "Crazy", "Excellent", "Good"] #激励话语
        self.past_scores = 0 #用来判断分数改变的辅助变量
        self.boost_word_state = [random.randint(80, 200), random.randint(0, len(self.words) - 1), random.randint(10, 20)] #为了激励话语
    
    #渲染状态函数
    def render(self, snake, my_font, screen):
        self.game_scores = snake.scores
        #渲染分数
        my_font.render_to(screen, (260, 10), "SCORE", black_color, None, size=15)
        my_font.render_to(screen, (260, 25), str(self.game_scores), black_color, None, size=40)
        #渲染激励话语
        my_font.render_to(screen, (260, self.boost_word_state[0]), self.words[self.boost_word_state[1]], black_color, None, size=(self.boost_word_state[2]))
        #判断分数改变
        if self.past_scores != self.game_scores:
            self.boost_word_state = [random.randint(80, 200), random.randint(0, len(self.words) - 1), random.randint(10, 20)]
            self.past_scores = self.game_scores

#游戏类
class Game(object):
    def __init__(self): 
        self.is_loop = True
        self.fps = 8

    #游戏运行类
    def run(self, env):
        #实例化蛇，食物，墙及游戏信息类
        snake = Snake()
        food = Food()
        wall = Wall() 
        game_info = GameInfo()
        food.creat_food(snake)

        #游戏主循环
        while self.is_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: snake.cd_direction = "LEFT"
                    elif event.key == pygame.K_RIGHT: snake.cd_direction = "RIGHT"
                    elif event.key == pygame.K_UP: snake.cd_direction = "UP"
                    elif event.key == pygame.K_DOWN: snake.cd_direction = "DOWN"
                    elif event.key == pygame.K_SPACE:
                        if self.fps == 8: self.fps = 16
                        else: self.fps = 8
                
                #这里为了防止按下相反方向的按键
                if snake.cd_direction == "LEFT" and snake.direction != "RIGHT": snake.direction = snake.cd_direction 
                if snake.cd_direction == "RIGHT" and snake.direction != "LEFT": snake.direction = snake.cd_direction 
                if snake.cd_direction == "UP" and snake.direction != "DOWN": snake.direction = snake.cd_direction 
                if snake.cd_direction == "DOWN" and snake.direction != "UP": snake.direction = snake.cd_direction
            #蛇得到指令走下一步
            snake.next_step(food)
            #蛇是否死亡
            if snake.is_die: 
                self.is_loop = False
                continue
            
            #渲染
            env.screen.fill(white_color)
            snake.draw_me(env.screen)
            food.draw_me(env.screen)
            wall.draw_me(env.screen)
            game_info.render(snake, env.my_font, env.screen)
            #画面更新
            pygame.display.update()
            env.clock.tick(self.fps) #游戏界面帧率


"""
main_loop
这里是主程序
"""
def main():
    env = Environment(window_size, window_title, white_color) #环境实例化
    #从菜单开始
    start_surface = MainMenu(["Start", "Setting", "Thanks", "Exit"])
    start_surface.run(env)
    start_surface.stop_bgm()
    
if __name__ == "__main__":
    main()