import random
import time

class Game:
    def __init__(self):
        self.map_size = 100
        self.player_hp = 30  # 初始血量
        self.player_pos = [random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1)]
        self.game_over = False
        self.monster_hp = 0  # 当前遇到的怪物血量
        self.move_count = 0  # 移动次数计数器
        
    def display_status(self):
        print("\n" + "="*50)
        print(f"玩家位置: ({self.player_pos[0]}, {self.player_pos[1]})")
        print(f"玩家血量: {self.player_hp}")
        print(f"移动次数: {self.move_count}")
        print("="*50 + "\n")
    
    def move_player(self):
        """玩家移动，返回是否成功移动（未到达边界）"""
        print("请选择移动方向:")
        print("1. 上")
        print("2. 下")
        print("3. 左")
        print("4. 右")
        
        while True:
            try:
                choice = int(input("请输入选择(1-4): "))
                if choice in [1, 2, 3, 4]:
                    break
                else:
                    print("请输入1-4之间的数字!")
            except ValueError:
                print("请输入有效的数字!")
        
        # 随机移动距离1-6
        distance = random.randint(1, 6)
        print(f"\n移动距离: {distance}")
        
        # 保存旧位置
        old_pos = self.player_pos.copy()
        
        # 根据选择移动
        if choice == 1:  # 上
            self.player_pos[1] = max(0, self.player_pos[1] - distance)
            print(f"向上移动 {distance} 格")
        elif choice == 2:  # 下
            self.player_pos[1] = min(self.map_size - 1, self.player_pos[1] + distance)
            print(f"向下移动 {distance} 格")
        elif choice == 3:  # 左
            self.player_pos[0] = max(0, self.player_pos[0] - distance)
            print(f"向左移动 {distance} 格")
        elif choice == 4:  # 右
            self.player_pos[0] = min(self.map_size - 1, self.player_pos[0] + distance)
            print(f"向右移动 {distance} 格")
        
        # 检查是否到达边界
        if old_pos == self.player_pos:
            print("你不能再向前走了！")
            return False  # 未成功移动，不触发事件
        else:
            print(f"新位置: ({self.player_pos[0]}, {self.player_pos[1]})")
            self.move_count += 1
            return True  # 成功移动，触发事件
    
    def trigger_random_event(self):
        """触发随机事件"""
        event = random.randint(1, 4)
        print(f"\n{'='*50}")
        print(f"触发随机事件...")
        time.sleep(0.5)
        
        if event == 1:
            print("无事发生，一切平静。")
        elif event == 2:
            print("踩中陷阱！")
            self.player_hp -= 1
            print(f"血量 -1，当前血量: {self.player_hp}")
            if self.player_hp <= 0:
                self.game_over = True
                print("\n血量耗尽，游戏结束！")
        elif event == 3:
            print("发现食物！")
            self.player_hp += 1
            print(f"血量 +1，当前血量: {self.player_hp}")
        elif event == 4:
            print("遇到怪物！")
            # 根据移动次数计算怪物血量
            if self.move_count <= 10:
                self.monster_hp = 1
            else:
                self.monster_hp = 1 + (self.move_count - 10) // 10
            print(f"怪物血量: {self.monster_hp}")
            self.handle_monster_encounter()
        
        print(f"{'='*50}\n")
    
    def handle_monster_encounter(self):
        """处理怪物遭遇"""
        print("\n请选择行动:")
        print("A. 开始战斗")
        print("B. 逃跑")
        
        while True:
            choice = input("请输入选择(A/B): ").upper()
            if choice in ['A', 'B']:
                break
            else:
                print("请输入A或B!")
        
        if choice == 'A':
            print("\n开始战斗！")
            print(f"玩家血量: {self.player_hp}")
            print(f"怪物血量: {self.monster_hp}")
            time.sleep(0.5)
            
            result = self.player_hp - self.monster_hp
            print(f"\n战斗结果: {self.player_hp} - {self.monster_hp} = {result}")
            
            if result > 0:
                print("恭喜！你击败了怪物！")
                self.player_hp = result
                print(f"剩余血量: {self.player_hp}")
                
                # 宝箱掉落判定（30%概率）
                if random.random() < 0.3:
                    print("\n发现宝箱！")
                    heal_amount = random.randint(1, 10)
                    self.player_hp += heal_amount
                    print(f"宝箱中恢复了 {heal_amount} 滴血量！")
                    print(f"当前血量: {self.player_hp}")
                else:
                    print("\n怪物没有掉落宝箱。")
            else:
                print("战斗失败，游戏结束！")
                self.game_over = True
        else:  # 逃跑
            print("\n选择逃跑...")
            self.player_hp -= 1
            print(f"逃跑成功，但血量 -1，当前血量: {self.player_hp}")
            if self.player_hp <= 0:
                self.game_over = True
                print("\n血量耗尽，游戏结束！")
    
    def run(self):
        """运行游戏主循环"""
        print("欢迎来到冒险游戏！")
        print(f"地图大小: {self.map_size}x{self.map_size}")
        print(f"初始血量: {self.player_hp}")
        print(f"初始位置: ({self.player_pos[0]}, {self.player_pos[1]})")
        print("\n游戏规则:")
        print("- 每次移动距离由1-6的随机数决定")
        print("- 移动后会触发随机事件（到达边界除外）")
        print("- 事件包括: 无事发生、陷阱(-1血)、食物(+1血)、怪物")
        print("- 遇到怪物可以选择战斗或逃跑")
        print("- 战斗: 玩家血量 - 怪物血量，结果>0则胜利")
        print("- 逃跑: 血量-1")
        print("- 血量<=0时游戏结束")
        print("- 怪物血量: 前10次移动为1，之后每10次移动+1")
        print("- 击败怪物有30%概率掉落宝箱，恢复1-10滴血量")
        
        while not self.game_over:
            self.display_status()
            moved = self.move_player()
            
            # 只有成功移动时才触发随机事件
            if moved and not self.game_over:
                self.trigger_random_event()
        
        print("\n" + "="*50)
        print("游戏结束！")
        print(f"最终位置: ({self.player_pos[0]}, {self.player_pos[1]})")
        print(f"最终血量: {self.player_hp}")
        print(f"总移动次数: {self.move_count}")
        print("="*50)

if __name__ == "__main__":
    game = Game()
    game.run()