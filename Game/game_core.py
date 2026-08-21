"""游戏核心逻辑模块 - 被main.py和pygame_game.py共享"""
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, Tuple, Callable
import random


class EventType(Enum):
    """事件类型枚举"""
    NOTHING = auto()
    TRAP = auto()
    FOOD = auto()
    MONSTER = auto()


class Direction(Enum):
    """移动方向枚举"""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class GameConfig:
    """游戏配置类"""
    map_size: int = 100
    initial_hp: int = 30
    min_move_distance: int = 1
    max_move_distance: int = 6
    treasure_drop_rate: float = 0.3
    min_treasure_heal: int = 1
    max_treasure_heal: int = 10
    monster_base_hp: int = 1
    monster_hp_increase_interval: int = 10


@dataclass
class GameResult:
    """游戏结果数据类"""
    success: bool
    message: str
    treasure_found: bool = False
    treasure_amount: int = 0


class GameCore:
    """游戏核心逻辑类"""
    
    def __init__(self, config: Optional[GameConfig] = None):
        self.config = config or GameConfig()
        self._reset_state()
    
    def _reset_state(self) -> None:
        """重置游戏状态"""
        self.player_hp: int = self.config.initial_hp
        self.player_pos: list[int] = [
            random.randint(0, self.config.map_size - 1),
            random.randint(0, self.config.map_size - 1)
        ]
        self.move_count: int = 0
        self.game_over: bool = False
        self.monster_hp: int = 0
        self.in_combat: bool = False
    
    def reset(self) -> None:
        """重置游戏"""
        self._reset_state()
    
    @property
    def position(self) -> Tuple[int, int]:
        """获取玩家位置"""
        return tuple(self.player_pos)
    
    def calculate_monster_hp(self) -> int:
        """计算当前怪物血量"""
        if self.move_count <= self.config.monster_hp_increase_interval:
            return self.config.monster_base_hp
        return self.config.monster_base_hp + (
            self.move_count - self.config.monster_hp_increase_interval
        ) // self.config.monster_hp_increase_interval
    
    def move(self, direction: Direction) -> Tuple[bool, str]:
        """
        移动玩家
        返回: (是否成功移动, 消息)
        """
        if self.in_combat:
            return False, "请先处理战斗！"
        
        distance = random.randint(
            self.config.min_move_distance,
            self.config.max_move_distance
        )
        
        old_pos = self.player_pos.copy()
        
        # 使用方向枚举处理移动
        move_handlers = {
            Direction.UP: lambda: max(0, self.player_pos[1] - distance),
            Direction.DOWN: lambda: min(self.config.map_size - 1, self.player_pos[1] + distance),
            Direction.LEFT: lambda: max(0, self.player_pos[0] - distance),
            Direction.RIGHT: lambda: min(self.config.map_size - 1, self.player_pos[0] + distance),
        }
        
        if direction in move_handlers:
            if direction in (Direction.UP, Direction.DOWN):
                self.player_pos[1] = move_handlers[direction]()
            else:
                self.player_pos[0] = move_handlers[direction]()
        
        # 检查是否实际移动了
        if old_pos == self.player_pos:
            return False, "你不能再向前走了！"
        
        self.move_count += 1
        return True, f"移动了 {distance} 格"
    
    def trigger_event(self) -> Tuple[EventType, str]:
        """
        触发随机事件
        返回: (事件类型, 事件消息)
        """
        event_type = random.choice(list(EventType))
        
        if event_type == EventType.NOTHING:
            return event_type, "无事发生，一切平静。"
        
        elif event_type == EventType.TRAP:
            self.player_hp -= 1
            if self.player_hp <= 0:
                self.game_over = True
                return event_type, "踩中陷阱！血量 -1，游戏结束！"
            return event_type, "踩中陷阱！血量 -1"
        
        elif event_type == EventType.FOOD:
            self.player_hp += 1
            return event_type, "发现食物！血量 +1"
        
        else:  # MONSTER
            self.monster_hp = self.calculate_monster_hp()
            self.in_combat = True
            return event_type, f"遇到怪物！怪物血量: {self.monster_hp}"
    
    def fight(self) -> GameResult:
        """
        与怪物战斗
        返回: GameResult对象
        """
        if not self.in_combat:
            return GameResult(False, "没有怪物需要战斗")
        
        result = self.player_hp - self.monster_hp
        
        if result > 0:
            self.player_hp = result
            self.in_combat = False
            
            # 宝箱掉落判定
            if random.random() < self.config.treasure_drop_rate:
                treasure_amount = random.randint(
                    self.config.min_treasure_heal,
                    self.config.max_treasure_heal
                )
                self.player_hp += treasure_amount
                return GameResult(
                    True,
                    f"恭喜！你击败了怪物！剩余血量: {self.player_hp}",
                    treasure_found=True,
                    treasure_amount=treasure_amount
                )
            return GameResult(True, f"恭喜！你击败了怪物！剩余血量: {self.player_hp}")
        else:
            self.game_over = True
            self.in_combat = False
            return GameResult(False, "战斗失败！游戏结束！")
    
    def flee(self) -> GameResult:
        """
        逃跑
        返回: GameResult对象
        """
        if not self.in_combat:
            return GameResult(False, "没有怪物需要逃跑")
        
        self.player_hp -= 1
        self.in_combat = False
        
        if self.player_hp <= 0:
            self.game_over = True
            return GameResult(True, "逃跑成功！血量 -1，游戏结束！")
        
        return GameResult(True, f"逃跑成功！血量 -1，当前血量: {self.player_hp}")
    
    def get_status(self) -> dict:
        """获取游戏状态"""
        return {
            'position': self.position,
            'hp': self.player_hp,
            'move_count': self.move_count,
            'game_over': self.game_over,
            'in_combat': self.in_combat,
            'monster_hp': self.monster_hp if self.in_combat else 0
        }