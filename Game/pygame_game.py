import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏配置
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
MAP_SIZE = 100
CELL_SIZE = 10  # 每个格子的大小
MAP_VIEW_SIZE = 40  # 可视区域大小（格子数）

# 颜色定义 - 更美观的配色方案
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
RED = (220, 60, 60)
GREEN = (60, 180, 100)
BLUE = (60, 120, 220)
YELLOW = (255, 200, 60)
GRAY = (140, 140, 150)
DARK_GRAY = (50, 50, 60)
LIGHT_GRAY = (230, 235, 240)
GOLD = (255, 180, 50)
PURPLE = (150, 80, 180)
ORANGE = (255, 140, 50)
CYAN = (50, 200, 200)
PINK = (255, 120, 150)

# 渐变色生成函数
def create_gradient_color(color1, color2, factor):
    """创建渐变色"""
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor)
    )

# 字体 - 使用支持中文的系统字体
def get_chinese_font(size):
    """获取支持中文的字体"""
    # 尝试多个中文字体，按优先级顺序
    chinese_fonts = ['simhei', 'microsoftyahei', 'simsun', 'simkai', 'fangsong']
    for font_name in chinese_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            # 测试字体是否支持中文
            test_surface = font.render('测试', True, (0, 0, 0))
            if test_surface.get_width() > 0:
                return font
        except:
            continue
    # 如果所有中文字体都失败，使用默认字体
    return pygame.font.SysFont(None, size)

FONT_LARGE = get_chinese_font(48)
FONT_MEDIUM = get_chinese_font(36)
FONT_SMALL = get_chinese_font(24)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("冒险游戏")
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.state = "MENU"  # MENU, PLAYING, GAME_OVER
        
        # 玩家属性
        self.player_hp = 30
        self.player_pos = [random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)]
        self.move_count = 0
        self.game_over = False
        
        # 事件相关
        self.current_event = None
        self.monster_hp = 0
        self.event_message = ""
        self.combat_result = ""
        self.treasure_found = False
        self.treasure_amount = 0
        self.in_combat = False  # 是否在战斗中
        
        # 按钮区域
        self.buttons = []
        
        # 性能优化：缓存surface
        self.map_surface = pygame.Surface((MAP_VIEW_SIZE * CELL_SIZE, MAP_VIEW_SIZE * CELL_SIZE))
        self.draw_grid_to_surface()
        self.text_cache = {}  # 文本缓存
        self.needs_redraw = True  # 是否需要重绘

    def reset_game(self):
        """重置游戏"""
        self.player_hp = 30
        self.player_pos = [random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1)]
        self.move_count = 0
        self.game_over = False
        self.current_event = None
        self.monster_hp = 0
        self.event_message = ""
        self.combat_result = ""
        self.treasure_found = False
        self.treasure_amount = 0
        self.in_combat = False
        self.needs_redraw = True

    def draw_grid_to_surface(self):
        """预渲染网格到surface"""
        self.map_surface.fill(LIGHT_GRAY)
        for i in range(MAP_VIEW_SIZE + 1):
            # 垂直线
            x = i * CELL_SIZE
            pygame.draw.line(self.map_surface, GRAY, (x, 0), (x, MAP_VIEW_SIZE * CELL_SIZE))
            # 水平线
            y = i * CELL_SIZE
            pygame.draw.line(self.map_surface, GRAY, (0, y), (MAP_VIEW_SIZE * CELL_SIZE, y))

    def get_cached_text(self, text, font, color):
        """获取缓存的文本surface"""
        key = (text, font, color)
        if key not in self.text_cache:
            self.text_cache[key] = font.render(text, True, color)
        return self.text_cache[key]

    def draw_text(self, text, font, color, x, y, center=False):
        """绘制文本"""
        text_surface = font.render(text, True, color)
        if center:
            rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, rect)
        else:
            self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, x, y, width, height, color, hover_color):
        """绘制按钮"""
        mouse_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, width, height)
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
        else:
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
        self.draw_text(text, FONT_MEDIUM, WHITE, x + width//2, y + height//2, center=True)
        return rect

    def draw_map(self):
        """绘制地图"""
        # 绘制背景
        for y in range(SCREEN_HEIGHT):
            color = create_gradient_color((240, 245, 250), (220, 230, 240), y / SCREEN_HEIGHT)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # 计算可视区域
        view_x = max(0, min(self.player_pos[0] - MAP_VIEW_SIZE//2, MAP_SIZE - MAP_VIEW_SIZE))
        view_y = max(0, min(self.player_pos[1] - MAP_VIEW_SIZE//2, MAP_SIZE - MAP_VIEW_SIZE))
        
        # 绘制地图区域 - 带装饰边框
        map_x, map_y = 50, 50
        map_w, map_h = MAP_VIEW_SIZE * CELL_SIZE, MAP_VIEW_SIZE * CELL_SIZE
        
        # 地图阴影
        pygame.draw.rect(self.screen, DARK_GRAY, (map_x + 5, map_y + 5, map_w + 4, map_h + 4))
        # 地图背景
        pygame.draw.rect(self.screen, (45, 55, 75), (map_x - 2, map_y - 2, map_w + 4, map_h + 4))
        pygame.draw.rect(self.screen, LIGHT_GRAY, (map_x, map_y, map_w, map_h))
        pygame.draw.rect(self.screen, BLUE, (map_x, map_y, map_w, map_h), 3)
        
        # 绘制网格
        for i in range(MAP_VIEW_SIZE + 1):
            # 垂直线
            x = map_x + i * CELL_SIZE
            pygame.draw.line(self.screen, GRAY, (x, map_y), (x, map_y + map_h))
            # 水平线
            y = map_y + i * CELL_SIZE
            pygame.draw.line(self.screen, GRAY, (map_x, y), (map_x + map_w, y))
        
        # 绘制玩家 - 带光晕效果
        player_screen_x = map_x + (self.player_pos[0] - view_x) * CELL_SIZE + CELL_SIZE // 2
        player_screen_y = map_y + (self.player_pos[1] - view_y) * CELL_SIZE + CELL_SIZE // 2
        
        # 玩家光晕
        pygame.draw.circle(self.screen, CYAN, (player_screen_x, player_screen_y), CELL_SIZE // 2 + 3)
        # 玩家主体
        pygame.draw.circle(self.screen, BLUE, (player_screen_x, player_screen_y), CELL_SIZE // 2 - 1)
        # 玩家高光
        pygame.draw.circle(self.screen, (150, 200, 255), (player_screen_x - 2, player_screen_y - 2), 2)
        
        # 绘制右侧信息面板
        info_x = map_x + map_w + 30
        panel_width = SCREEN_WIDTH - info_x - 20
        
        # 面板阴影
        pygame.draw.rect(self.screen, DARK_GRAY, (info_x - 8, 38, panel_width + 4, SCREEN_HEIGHT - 76))
        # 面板背景
        panel_rect = pygame.Rect(info_x - 10, 40, panel_width, SCREEN_HEIGHT - 80)
        pygame.draw.rect(self.screen, (250, 252, 255), panel_rect)
        pygame.draw.rect(self.screen, PURPLE, panel_rect, 2)
        
        # 面板标题装饰
        pygame.draw.line(self.screen, GOLD, (info_x, 55), (info_x + panel_width - 10, 55), 2)
        
        # 绘制玩家信息
        self.draw_text("【 玩家信息 】", FONT_MEDIUM, PURPLE, info_x + panel_width//2, 55, center=True)
        self.draw_text(f"位置: ({self.player_pos[0]}, {self.player_pos[1]})", FONT_SMALL, DARK_GRAY, info_x, 95)
        
        # 血量显示 - 带颜色变化
        hp_color = GREEN if self.player_hp > 15 else (YELLOW if self.player_hp > 5 else RED)
        self.draw_text(f"血量: {self.player_hp}", FONT_SMALL, hp_color, info_x, 125)
        
        # 移动次数
        self.draw_text(f"移动次数: {self.move_count}", FONT_SMALL, DARK_GRAY, info_x, 155)
        
        # 绘制操作提示
        pygame.draw.line(self.screen, GRAY, (info_x, 185), (info_x + panel_width - 10, 185), 1)
        self.draw_text("【 操作说明 】", FONT_MEDIUM, PURPLE, info_x + panel_width//2, 195, center=True)
        self.draw_text("↑↓←→: 移动", FONT_SMALL, BLUE, info_x, 235)
        
        # 如果在战斗中，高亮显示战斗操作
        if self.in_combat:
            self.draw_text("F: 战斗", FONT_SMALL, RED, info_x, 265)
            self.draw_text("E: 逃跑", FONT_SMALL, RED, info_x, 295)
        else:
            self.draw_text("F: 战斗", FONT_SMALL, GRAY, info_x, 265)
            self.draw_text("E: 逃跑", FONT_SMALL, GRAY, info_x, 295)
        
        # 绘制事件/战斗信息
        if self.event_message:
            pygame.draw.line(self.screen, GRAY, (info_x, 325), (info_x + panel_width - 10, 325), 1)
            self.draw_text("【 事件信息 】", FONT_MEDIUM, PURPLE, info_x + panel_width//2, 335, center=True)
            # 分行显示长消息
            words = self.event_message
            y_pos = 375
            for i in range(0, len(words), 15):
                self.draw_text(words[i:i+15], FONT_SMALL, BLACK, info_x, y_pos)
                y_pos += 25
        
        # 绘制战斗结果
        if self.combat_result:
            pygame.draw.line(self.screen, GRAY, (info_x, y_pos + 10), (info_x + panel_width - 10, y_pos + 10), 1)
            self.draw_text("【 战斗结果 】", FONT_MEDIUM, PURPLE, info_x + panel_width//2, y_pos + 20, center=True)
            y_pos += 60
            words = self.combat_result
            for i in range(0, len(words), 15):
                self.draw_text(words[i:i+15], FONT_SMALL, BLACK, info_x, y_pos)
                y_pos += 25
        
        # 绘制宝箱信息
        if self.treasure_found:
            self.draw_text(f"💎 发现宝箱！恢复{self.treasure_amount}血量", FONT_SMALL, GOLD, info_x, y_pos + 10)

    def draw_event(self):
        """绘制事件界面"""
        # 绘制背景
        pygame.draw.rect(self.screen, WHITE, (100, 100, 600, 400))
        pygame.draw.rect(self.screen, BLACK, (100, 100, 600, 400), 3)
        
        # 绘制事件图标
        if self.current_event == 1:  # 无事发生
            pygame.draw.circle(self.screen, GREEN, (200, 200), 50)
            self.draw_text("无事发生", FONT_MEDIUM, BLACK, 200, 200, center=True)
        elif self.current_event == 2:  # 陷阱
            pygame.draw.rect(self.screen, BLACK, (150, 150, 100, 100))
            self.draw_text("陷阱", FONT_MEDIUM, WHITE, 200, 200, center=True)
        elif self.current_event == 3:  # 食物
            pygame.draw.circle(self.screen, GREEN, (200, 200), 50)
            self.draw_text("食物", FONT_MEDIUM, BLACK, 200, 200, center=True)
        elif self.current_event == 4:  # 怪物
            pygame.draw.rect(self.screen, RED, (150, 150, 100, 100))
            self.draw_text("怪物", FONT_MEDIUM, WHITE, 200, 200, center=True)
        
        # 绘制事件消息
        self.draw_text(self.event_message, FONT_MEDIUM, BLACK, 300, 150)
        
        # 绘制继续按钮
        self.buttons = []
        self.buttons.append(self.draw_button("继续", 350, 400, 100, 50, BLUE, (80, 150, 255)))

    def draw_combat(self):
        """绘制战斗界面"""
        # 绘制背景
        pygame.draw.rect(self.screen, WHITE, (100, 100, 600, 400))
        pygame.draw.rect(self.screen, BLACK, (100, 100, 600, 400), 3)
        
        # 绘制玩家
        pygame.draw.circle(self.screen, BLUE, (200, 200), 50)
        self.draw_text("玩家", FONT_SMALL, WHITE, 200, 200, center=True)
        self.draw_text(f"血量: {self.player_hp}", FONT_MEDIUM, BLACK, 200, 280, center=True)
        
        # 绘制怪物
        pygame.draw.rect(self.screen, RED, (500, 150, 100, 100))
        self.draw_text("怪物", FONT_SMALL, WHITE, 550, 200, center=True)
        self.draw_text(f"血量: {self.monster_hp}", FONT_MEDIUM, BLACK, 550, 280, center=True)
        
        # 绘制战斗结果
        if self.combat_result:
            self.draw_text(self.combat_result, FONT_MEDIUM, BLACK, 400, 350, center=True)
        
        # 绘制宝箱信息
        if self.treasure_found:
            self.draw_text(f"发现宝箱！恢复{self.treasure_amount}血量", FONT_MEDIUM, GOLD, 400, 380, center=True)
        elif self.combat_result == "恭喜！你击败了怪物！":
            self.draw_text("怪物没有掉落宝箱。", FONT_SMALL, GRAY, 400, 380, center=True)
        
        # 绘制按钮
        self.buttons = []
        self.buttons.append(self.draw_button("战斗", 250, 400, 100, 50, RED, (255, 100, 100)))
        self.buttons.append(self.draw_button("逃跑", 450, 400, 100, 50, GREEN, (100, 220, 120)))

    def draw_menu(self):
        """绘制菜单界面"""
        # 绘制渐变背景
        for y in range(SCREEN_HEIGHT):
            color = create_gradient_color((20, 20, 40), (60, 60, 100), y / SCREEN_HEIGHT)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # 绘制装饰性边框
        pygame.draw.rect(self.screen, GOLD, (20, 20, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40), 3)
        pygame.draw.rect(self.screen, PURPLE, (25, 25, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), 1)
        
        # 绘制标题 - 带阴影效果
        self.draw_text("冒险游戏", FONT_LARGE, BLACK, SCREEN_WIDTH//2 + 3, 103, center=True)
        self.draw_text("冒险游戏", FONT_LARGE, GOLD, SCREEN_WIDTH//2, 100, center=True)
        
        # 绘制副标题
        self.draw_text("—— 探索未知的世界 ——", FONT_SMALL, CYAN, SCREEN_WIDTH//2, 155, center=True)
        
        # 绘制规则面板
        panel_x, panel_y = SCREEN_WIDTH//2 - 280, 190
        panel_w, panel_h = 560, 280
        pygame.draw.rect(self.screen, (30, 30, 50), (panel_x, panel_y, panel_w, panel_h))
        pygame.draw.rect(self.screen, GOLD, (panel_x, panel_y, panel_w, panel_h), 2)
        
        # 绘制规则标题
        self.draw_text("游戏规则", FONT_MEDIUM, YELLOW, SCREEN_WIDTH//2, panel_y + 15, center=True)
        
        # 绘制规则
        rules = [
            "• 每次移动距离由1-6的随机数决定",
            "• 移动后会触发随机事件",
            "• 事件包括: 无事发生、陷阱(-1血)、食物(+1血)、怪物",
            "• 遇到怪物可以选择战斗或逃跑",
            "• 战斗: 玩家血量 - 怪物血量，结果>0则胜利",
            "• 逃跑: 血量-1",
            "• 血量<=0时游戏结束",
            "• 怪物血量: 前10次移动为1，之后每10次移动+1",
            "• 击败怪物有30%概率掉落宝箱，恢复1-10滴血量"
        ]
        for i, rule in enumerate(rules):
            self.draw_text(rule, FONT_SMALL, LIGHT_GRAY, SCREEN_WIDTH//2, panel_y + 55 + i * 22, center=True)
        
        # 绘制开始按钮 - 带装饰
        self.buttons = []
        btn_x, btn_y = SCREEN_WIDTH//2 - 120, 500
        # 按钮阴影
        pygame.draw.rect(self.screen, DARK_GRAY, (btn_x + 5, btn_y + 5, 240, 60))
        # 按钮主体
        self.buttons.append(self.draw_button("开始游戏", btn_x, btn_y, 240, 55, BLUE, (80, 150, 255)))
        
        # 绘制底部提示
        self.draw_text("按 空格键 或 点击按钮 开始游戏", FONT_SMALL, GRAY, SCREEN_WIDTH//2, 580, center=True)

    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 绘制渐变背景
        for y in range(SCREEN_HEIGHT):
            color = create_gradient_color((40, 20, 20), (80, 30, 30), y / SCREEN_HEIGHT)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # 绘制装饰边框
        pygame.draw.rect(self.screen, RED, (20, 20, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40), 3)
        pygame.draw.rect(self.screen, PURPLE, (25, 25, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), 1)
        
        # 绘制标题 - 带阴影效果
        self.draw_text("游戏结束", FONT_LARGE, BLACK, SCREEN_WIDTH//2 + 3, 103, center=True)
        self.draw_text("游戏结束", FONT_LARGE, RED, SCREEN_WIDTH//2, 100, center=True)
        
        # 绘制统计信息面板
        panel_x, panel_y = SCREEN_WIDTH//2 - 200, 200
        panel_w, panel_h = 400, 200
        pygame.draw.rect(self.screen, (30, 30, 50), (panel_x, panel_y, panel_w, panel_h))
        pygame.draw.rect(self.screen, RED, (panel_x, panel_y, panel_w, panel_h), 2)
        
        # 绘制统计信息
        stats = [
            (f"最终位置: ({self.player_pos[0]}, {self.player_pos[1]})", YELLOW),
            (f"最终血量: {self.player_hp}", GREEN if self.player_hp > 0 else RED),
            (f"总移动次数: {self.move_count}", CYAN)
        ]
        for i, (text, color) in enumerate(stats):
            self.draw_text(text, FONT_MEDIUM, color, SCREEN_WIDTH//2, panel_y + 40 + i * 50, center=True)
        
        # 绘制按钮
        self.buttons = []
        btn_x1, btn_y1 = SCREEN_WIDTH//2 - 120, 430
        btn_x2, btn_y2 = SCREEN_WIDTH//2 - 120, 500
        
        # 按钮阴影
        pygame.draw.rect(self.screen, DARK_GRAY, (btn_x1 + 5, btn_y1 + 5, 240, 55))
        pygame.draw.rect(self.screen, DARK_GRAY, (btn_x2 + 5, btn_y2 + 5, 240, 55))
        
        self.buttons.append(self.draw_button("重新开始", btn_x1, btn_y1, 240, 50, GREEN, (100, 220, 120)))
        self.buttons.append(self.draw_button("退出", btn_x2, btn_y2, 240, 50, RED, (255, 100, 100)))
        
        # 绘制提示
        self.draw_text("按 R 重新开始 | 按 Q 退出", FONT_SMALL, GRAY, SCREEN_WIDTH//2, 570, center=True)

    def move_player(self, direction):
        """玩家移动"""
        # 如果在战斗中，不能移动
        if self.in_combat:
            self.event_message = "请先处理战斗！按F战斗或E逃跑"
            return False
        
        distance = random.randint(1, 6)
        old_pos = self.player_pos.copy()
        
        if direction == "up":
            self.player_pos[1] = max(0, self.player_pos[1] - distance)
        elif direction == "down":
            self.player_pos[1] = min(MAP_SIZE - 1, self.player_pos[1] + distance)
        elif direction == "left":
            self.player_pos[0] = max(0, self.player_pos[0] - distance)
        elif direction == "right":
            self.player_pos[0] = min(MAP_SIZE - 1, self.player_pos[0] + distance)
        
        # 检查是否到达边界
        if old_pos == self.player_pos:
            self.event_message = "你不能再向前走了！"
            self.current_event = 1
            return False
        else:
            self.move_count += 1
        
        # 清除之前的战斗结果
        self.combat_result = ""
        self.treasure_found = False
        self.treasure_amount = 0
        return True

    def trigger_random_event(self):
        """触发随机事件"""
        self.current_event = random.randint(1, 4)
        
        if self.current_event == 1:
            self.event_message = "无事发生，一切平静。"
        elif self.current_event == 2:
            self.player_hp -= 1
            self.event_message = "踩中陷阱！血量 -1"
            if self.player_hp <= 0:
                self.game_over = True
                self.state = "GAME_OVER"
                return
        elif self.current_event == 3:
            self.player_hp += 1
            self.event_message = "发现食物！血量 +1"
        elif self.current_event == 4:
            # 计算怪物血量
            if self.move_count <= 10:
                self.monster_hp = 1
            else:
                self.monster_hp = 1 + (self.move_count - 10) // 10
            self.event_message = f"遇到怪物！怪物血量: {self.monster_hp}"
            self.combat_result = ""
            self.treasure_found = False
            self.treasure_amount = 0
            self.in_combat = True  # 进入战斗状态
            return

    def handle_combat(self, action):
        """处理战斗"""
        if action == "fight":
            result = self.player_hp - self.monster_hp
            if result > 0:
                self.combat_result = "恭喜！你击败了怪物！"
                self.player_hp = result
                # 宝箱掉落判定
                if random.random() < 0.3:
                    self.treasure_found = True
                    self.treasure_amount = random.randint(1, 10)
                    self.player_hp += self.treasure_amount
            else:
                self.combat_result = "战斗失败！"
                self.game_over = True
                self.state = "GAME_OVER"
                return
        else:  # 逃跑
            self.player_hp -= 1
            self.combat_result = "逃跑成功！血量 -1"
            if self.player_hp <= 0:
                self.game_over = True
                self.state = "GAME_OVER"
                return
        
        # 退出战斗状态
        self.in_combat = False

    def run(self):
        """运行游戏主循环"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # 键盘事件处理
                if event.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            self.reset_game()
                            self.state = "PLAYING"
                    
                    elif self.state == "PLAYING":
                        # 方向键移动
                        if event.key == pygame.K_UP:
                            if self.move_player("up"):
                                self.trigger_random_event()
                        elif event.key == pygame.K_DOWN:
                            if self.move_player("down"):
                                self.trigger_random_event()
                        elif event.key == pygame.K_LEFT:
                            if self.move_player("left"):
                                self.trigger_random_event()
                        elif event.key == pygame.K_RIGHT:
                            if self.move_player("right"):
                                self.trigger_random_event()
                        # 战斗按键（支持大小写）
                        elif event.key == pygame.K_f or event.key == pygame.K_F:
                            if self.in_combat:
                                self.handle_combat("fight")
                        elif event.key == pygame.K_e or event.key == pygame.K_E:
                            if self.in_combat:
                                self.handle_combat("flee")
                    
                    elif self.state == "GAME_OVER":
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.state = "PLAYING"
                        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                
                # 鼠标事件处理（保留菜单和游戏结束的鼠标支持）
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.state == "MENU":
                        if self.buttons[0].collidepoint(mouse_pos):
                            self.reset_game()
                            self.state = "PLAYING"
                    elif self.state == "GAME_OVER":
                        if len(self.buttons) >= 2:
                            if self.buttons[0].collidepoint(mouse_pos):  # 重新开始
                                self.reset_game()
                                self.state = "PLAYING"
                            elif self.buttons[1].collidepoint(mouse_pos):  # 退出
                                pygame.quit()
                                sys.exit()
            
            # 绘制界面
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "PLAYING":
                self.screen.fill(WHITE)
                self.draw_map()
            elif self.state == "GAME_OVER":
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()