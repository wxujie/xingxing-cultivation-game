# -*- coding: utf-8 -*-
"""
杏杏修仙录 v2 - 修仙肉鸽游戏 (修复版)
"""

import pygame
import random
import sys
import math
import json
from entities import Player, Enemy, Particle
from data_loader import load_all

# Initialize
pygame.init()

# 加载数据
DATA = load_all()
REALMS = DATA["realms"]
CHARACTERS = DATA["characters"]
TECHNIQUES = DATA["techniques"]
ENEMIES = DATA["enemies"]
WEAPONS = DATA["items"]["weapons"]
ARMORS = DATA["items"]["armors"]

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WORLD_WIDTH = 4800
WORLD_HEIGHT = 3200
FPS = 60

# 东方仙侠水墨风格配色
INK_BLACK = (20, 20, 25)          # 墨黑
PAPER = (245, 240, 225)           # 宣纸黄
INK_GRAY = (60, 65, 70)           # 墨灰
RED = (180, 40, 40)               # 朱砂红
GREEN = (60, 140, 60)             # 青绿
BLUE = (40, 80, 160)              # 青蓝
GOLD = (200, 160, 40)             # 金色
PURPLE = (120, 60, 140)           # 紫
ORANGE = (200, 120, 40)           # 橙
CYAN = (60, 160, 160)             # 青
SILVER = (180, 180, 190)          # 银白
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (45, 50, 55)
BROWN = (100, 70, 50)
LIGHT_BLUE = (120, 180, 200)
DARK_GREEN = (40, 80, 40)

# ===== 五行系统 =====
ELEMENTS = {
    "金": {"color": (200, 180, 50), "weakness": "木", "strength": "土", "bonus": "attack"},
    "木": {"color": (50, 180, 50), "weakness": "金", "strength": "水", "bonus": "defense"},
    "水": {"color": (50, 100, 200), "weakness": "火", "strength": "火", "bonus": "hp"},
    "火": {"color": (220, 60, 40), "weakness": "水", "strength": "金", "bonus": "damage"},
    "土": {"color": (180, 140, 80), "weakness": "水", "strength": "木", "bonus": "all"},
}

# 境界系统
REALMS = [
    ("练气", 100),
    ("筑基", 300),
    ("金丹", 1500),
    ("元婴", 6000),
    ("化神", 20000),
    ("渡劫", 80000),
    ("飞升", 500000)
]

# 角色选择 - 五行角色
CHARACTERS = {
    "金": {
        "name": "剑痴·厉沧海", "element": "金", "desc": "铸剑山庄弃徒，一生唯剑为伴，追求极致锋芒。",
        "base_attack": 15, "base_defense": 8, "base_hp": 100,
        "skills": ["金剑术", "金虹贯日", "庚金神光", "分金斩", "金甲护体", "金戈铁马", "金星爆", "金风玉露", "金榜题名", "金蝉脱壳",
                   "金汤固守", "金碧辉煌", "金玉满堂", "金石为开", "金戈之声", "金蛇狂舞", "金羽翔天", "金纹护盾", "金雷降世", "金莲绽放"]
    },
    "木": {
        "name": "药仙·苏青青", "element": "木", "desc": "隐居药谷的医修，慈悲为怀，以草木之力治愈苍生。",
        "base_attack": 10, "base_defense": 15, "base_hp": 110,
        "skills": ["木藤术", "荆棘之刺", "生命绽放", "盘根错节", "木甲护体", "万木逢春", "木叶飘零", "木桩大法", "木龙出海", "木魅幻术",
                   "森林之怒", "木灵祝福", "扎根大地", "枝繁叶茂", "木刺穿心", "绿意盎然", "木之领域", "枯木逢春", "木灵守护", "森林之王"]
    },
    "水": {
        "name": "霜月·洛冰璃", "element": "水", "desc": "北冥极地的冰雪之女，体内封印着万年玄冰之力。",
        "base_attack": 10, "base_defense": 10, "base_hp": 150,
        "skills": ["水波术", "冰封千里", "水幕天华", "滴水穿石", "水甲护体", "海纳百川", "水龙吟", "寒冰射线", "水月镜像", "水灵祝福",
                   "惊涛骇浪", "水之愈合", "冰晶雪莲", "水墨丹青", "水漫金山", "寒气逼人", "水循环", "蓝蓝的海", "水之壁垒", "波涛汹涌"]
    },
    "火": {
        "name": "狂刀·烈焰天", "element": "火", "desc": "乱世中崛起的刀客，刀意如火，焚尽一切来犯之敌。",
        "base_attack": 14, "base_defense": 6, "base_hp": 90,
        "skills": ["火球术", "烈焰焚烧", "火凤燎原", "火焰冲击", "火甲护体", "烈焰风暴", "火眼金睛", "星火燎原", "燃尽八荒", "火德星君",
                   "祝融神火", "火舞九天", "烈焰之魂", "火龙出海", "烽火连天", "火树银花", "灼热之魂", "爆炸的艺术", "烈焰审判", "火神降世"]
    },
    "土": {
        "name": "苦行·石敢当", "element": "土", "desc": "大地之子，行走于荒原的行者，身如磐石，不动如山。",
        "base_attack": 12, "base_defense": 12, "base_hp": 120,
        "skills": ["土盾术", "大地守护", "地震术", "土牢术", "土甲护体", "山崩地裂", "大地脉动", "尘土飞扬", "固若金汤", "土灵祝福",
                   "移山填海", "厚土载物", "地动山摇", "土龙翻身", "稳如泰山", "尘土蔽日", "大地之怒", "岩石装甲", "土之领域", "山河破碎"]
    },
}

# 通用功法
# 敌人数据 (添加更多特征)
ENEMIES = [
    {"name": "小兔子", "hp": 25, "damage": 4, "exp": 8, "speed": 0.6, "color": (200, 180, 180), "size": 18, "element": "木"},
    {"name": "野狼", "hp": 50, "damage": 10, "exp": 20, "speed": 1.2, "color": (100, 100, 100), "size": 25, "element": "金"},
    {"name": "山贼", "hp": 70, "damage": 14, "exp": 30, "speed": 0.9, "color": BROWN, "size": 28, "element": "土"},
    {"name": "僵尸", "hp": 90, "damage": 12, "exp": 35, "speed": 0.4, "color": (80, 120, 80), "size": 30, "element": "木"},
    {"name": "狐妖", "hp": 60, "damage": 20, "exp": 45, "speed": 1.4, "color": ORANGE, "size": 26, "element": "火"},
    {"name": "蛇妖", "hp": 120, "damage": 22, "exp": 60, "speed": 1.1, "color": GREEN, "size": 28, "element": "木"},
    {"name": "虎妖", "hp": 180, "damage": 28, "exp": 100, "speed": 1.5, "color": (255, 140, 0), "size": 35, "element": "金"},
    {"name": "筑基修士", "hp": 250, "damage": 35, "exp": 150, "speed": 1.0, "color": BLUE, "size": 32, "element": "水"},
    {"name": "金丹修士", "hp": 500, "damage": 50, "exp": 300, "speed": 1.2, "color": PURPLE, "size": 36, "element": "火"},
    {"name": "元婴老怪", "hp": 1000, "damage": 70, "exp": 600, "speed": 1.6, "color": RED, "size": 40, "element": "土"},
]

# 品质颜色
QUALITY_COLORS = {
    "普通": (200, 200, 200),
    "优秀": (0, 255, 0),
    "稀有": (50, 150, 255),
    "史诗": (200, 0, 255),
    "传说": (255, 215, 0)
}

# 装备数据
WEAPONS = [
    {"name": "木剑", "attack": 8, "quality": "普通", "cost": 80},
    {"name": "铁剑", "attack": 18, "quality": "优秀", "cost": 200},
    {"name": "青锋剑", "attack": 35, "quality": "稀有", "cost": 500},
    {"name": "玄冰剑", "attack": 60, "quality": "史诗", "cost": 1500},
    {"name": "轩辕剑", "attack": 100, "quality": "传说", "cost": 5000},
]

ARMORS = [
    {"name": "布衣", "defense": 5, "quality": "普通", "cost": 80},
    {"name": "皮甲", "defense": 12, "quality": "优秀", "cost": 200},
    {"name": "铁甲", "defense": 25, "quality": "稀有", "cost": 500},
    {"name": "银鳞甲", "defense": 45, "quality": "史诗", "cost": 1500},
    {"name": "金缕玉衣", "defense": 80, "quality": "传说", "cost": 5000},
]



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("杏杏修仙录 v2")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("simhei", 22)
        self.title_font = pygame.font.SysFont("simhei", 56)
        self.small_font = pygame.font.SysFont("simhei", 18)
        
        self.state = "menu"
        self.player = None
        self.enemies = []
        self.particles = []
        self.shop_items = []
        self.confirm_item = None # 待确认购买的物品
        self.message = ""
        self.message_timer = 0
        self.attack_range = 150
        self.camera_x = 0
        self.camera_y = 0
        self.attack_target = None
        self.attack_anim = None
        
        # Load portraits
        self.portraits = {}
        portrait_files = {"金": "jin.png", "木": "mu.png", "水": "shui.png", "火": "huo.png", "土": "tu.png"}
        for elem, filename in portrait_files.items():
            path = f"data/portraits/{filename}"
            try:
                img = pygame.image.load(path).convert_alpha()
                self.portraits[elem] = pygame.transform.scale(img, (300, 300))
                print(f"DEBUG: Successfully loaded portrait: {path}")
            except Exception as e:
                print(f"DEBUG: Failed to load portrait {path}: {e}")
                self.portraits[elem] = None
        
        # Menu state
        self.menu_buttons = []
        self.menu_selection_idx = 0
        self.handbook_tab = "金"
        self.handbook_page = 0
        self.char_selection_idx = 0
        
        # 突破相关
        self.breakthrough_boss = None
        self.reward_choices = []
        self.reward_selected = False
        self.boss_spawned = False
        
        # 静态地图元素 (增加种类和数量)
        self.map_elements = []
        for _ in range(100):
            x = random.randint(100, WORLD_WIDTH - 100)
            y = random.randint(100, WORLD_HEIGHT - 100)
            self.map_elements.append({"type": random.choice(["tree", "rock", "river", "flower"]), "x": x, "y": y})
        
        # 移动目标
        self.move_target = None
        self.attack_target = None
        
        # 按钮区域
        self.buttons = []
        self.shop_buttons = []
        
        # 游戏数据
        self.map_seed = random.randint(0, 10000)
        self.game_time = 0
        
        # Load background
        try:
            self.bg_image = pygame.image.load("data/menu_bg.png").convert()
        except:
            self.bg_image = None
        
        # Load spritesheet
        try:
            self.shui_spritesheet = pygame.image.load("data/shui_spritesheet_nobg.png").convert_alpha()
            self.shui_spritesheet = pygame.transform.scale(self.shui_spritesheet, (400, 400)) # Simple scale
        except:
            self.shui_spritesheet = None

    def trigger_attack_anim(self, target_x, target_y, skill_type):
        self.attack_anim = {
            'x': target_x,
            'y': target_y,
            'start': pygame.time.get_ticks(),
            'type': skill_type
        }

    def start_breakthrough_challenge(self):
        boss = self.create_enemy()
        boss.name = "突破心魔BOSS"
        boss.max_hp *= 2
        boss.hp = boss.max_hp
        boss.damage *= 1.5
        boss.color = PURPLE
        boss.size *= 1.5
        self.enemies.append(boss)
        self.breakthrough_boss = boss
        self.boss_spawned = True
        self.show_message("注意：突破心魔BOSS出现！")

    def on_boss_defeat(self):
        self.breakthrough_boss = None
        self.boss_spawned = False
        self.player.breakthrough()
        self.show_reward_selection()

    def show_reward_selection(self):
        self.reward_choices = []
        for _ in range(3):
            # 随机选择功法或装备
            if random.random() < 0.6:
                new_techs = [t for t in TECHNIQUES.keys() if t not in self.player.techniques]
                if new_techs:
                    self.reward_choices.append(("tech", random.choice(new_techs)))
                else:
                    self.reward_choices.append(("gold", 1000))
            else:
                if random.random() < 0.5:
                    weapon = random.choice(WEAPONS)
                    self.reward_choices.append(("weapon", weapon))
                else:
                    armor = random.choice(ARMORS)
                    self.reward_choices.append(("armor", armor))
        self.state = "reward_selection"

    def draw_reward_selection(self):
        self.screen.fill(PAPER)
        self.draw_text("突破成功！选择一项奖励", self.title_font, RED, SCREEN_WIDTH//2, 100, center=True)
        
        for i, choice in enumerate(self.reward_choices):
            rect = (SCREEN_WIDTH//2 - 150, 200 + i * 100, 300, 80)
            pygame.draw.rect(self.screen, INK_BLACK, rect, 2)
            pygame.draw.rect(self.screen, PAPER, (rect[0]+2, rect[1]+2, rect[2]-4, rect[3]-4))
            
            label = ""
            if choice[0] == "tech": label = f"功法: {choice[1]}"
            elif choice[0] == "weapon": label = f"武器: {choice[1]['name']}"
            elif choice[0] == "armor": label = f"防具: {choice[1]['name']}"
            elif choice[0] == "gold": label = f"灵石: {choice[1]}"
            
            self.draw_text(label, self.font, INK_BLACK, SCREEN_WIDTH//2, 240 + i * 100, center=True)

    def apply_reward(self, choice):
        if choice[0] == "tech":
            self.player.techniques.append(choice[1])
            self.show_message(f"获得功法: {choice[1]}")
        elif choice[0] == "weapon":
            self.player.equip(choice[1], "weapon")
            self.show_message(f"获得装备: {choice[1]['name']}")
        elif choice[0] == "armor":
            self.player.equip(choice[1], "armor")
            self.show_message(f"获得装备: {choice[1]['name']}")
        elif choice[0] == "gold":
            self.player.gold += choice[1]
            self.show_message(f"获得灵石: {choice[1]}")

    def set_move_target(self, x, y):
        self.move_target = (x, y)
    
    def perform_attack(self, target):
        # 攻击逻辑 (统一方法，方便调用)
        skill = self.player.use_skill(TECHNIQUES)
        if skill:
            self.player.state = "Casting" if skill["type"] == "heal" else "Attacking"
            if skill["type"] == "attack":
                damage = skill.get("damage", 0)
                target.take_damage(damage)
                self.spawn_attack_particles(target.x, target.y, skill["color"])
                self.show_message(f"使用 {self.player.current_skill}!")
            elif skill["type"] == "heal":
                self.player.heal(skill["heal"])
                self.show_message(f"治疗术 +{skill['heal']}!")
                self.spawn_attack_particles(self.player.x, self.player.y, GREEN)
        else:
            self.player.state = "Attacking"
            dmg = self.player.attack
            target.take_damage(dmg)
            self.spawn_attack_particles(target.x, target.y, WHITE)
        
        # Reset state after a short delay
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)
        
        # 处理死亡奖励
        if not target.is_alive():
            self.player.gold += target.gold
            self.player.add_exp(target.exp)
            self.show_message(f"击败{target.name} +{target.gold}灵石 +{target.exp}修为")
            for _ in range(12):
                self.particles.append(Particle(target.x, target.y, target.color, 4, 40))
    
    def update_movement(self):
        if self.move_target and self.player:
            dx = self.move_target[0] - self.player.x
            dy = self.move_target[1] - self.player.y
            dist = math.hypot(dx, dy)
            if dist < 10:
                self.move_target = None
                # 到达目的地后如果由攻击目标，则尝试攻击
                if self.attack_target and self.attack_target.is_alive():
                    # 再次检查距离
                    if math.hypot(self.attack_target.x - self.player.x, self.attack_target.y - self.player.y) <= self.attack_range:
                        self.perform_attack(self.attack_target)
                    else:
                        self.show_message("目标已逃脱!")
                    self.attack_target = None
            else:
                speed = 5
                move_x = (dx / dist) * speed
                move_y = (dy / dist) * speed
                self.player.move(move_x, move_y, WORLD_WIDTH, WORLD_HEIGHT)
                # 移动粒子
                if random.random() < 0.2:
                    self.particles.append(Particle(
                        self.player.x + random.randint(-10, 10),
                        self.player.y + 20,
                        (100, 150, 200), 0.5, 15
                    ))
        
    def show_message(self, msg, duration=90):
        self.message = msg
        self.message_timer = duration
    
    def create_enemy(self):
        realm = self.player.realm if self.player else 0
        return Enemy(realm, ENEMIES)
    
    def start_game(self, char_key="金"):
        self.player = Player(char_key, CHARACTERS[char_key], REALMS, ELEMENTS)
        self.enemies = []
        self.particles = []
        self.boss_spawned = False
        self.breakthrough_boss = None
        for _ in range(5):
            self.enemies.append(self.create_enemy())
        self.generate_shop()
        self.state = "game"
    
    def generate_shop(self):
        self.shop_items = []
        available_techs = list(TECHNIQUES.keys())
        for _ in range(3):
            self.shop_items.append(("tech", random.choice(available_techs)))
        for w in WEAPONS[:4]:
            self.shop_items.append(("weapon", w.copy()))
        for a in ARMORS[:4]:
            self.shop_items.append(("armor", a.copy()))
    
    def update(self):
        if self.state != "game" or self.player is None:
            return
        
        self.game_time += 1
        
        # 粒子更新
        self.particles = [p for p in self.particles if p.update()]
        
        # ===== 自动释放所有冷却好的功法 =====
        for tech_name in self.player.techniques:
            skill = self.player.use_skill_by_name(tech_name, TECHNIQUES)
            if not skill:
                continue
            
            # 找攻击范围内的敌人
            targets = []
            for enemy in self.enemies:
                if enemy.is_alive():
                    d = math.hypot(enemy.x - self.player.x, enemy.y - self.player.y)
                    if d < self.attack_range:
                        targets.append(enemy)
            
            if not targets:
                continue
            
            # 应用五行加成
            damage = skill.get("damage", 0)
            if skill["element"] == self.player.element:
                # 同属性功法有加成
                if self.player.element_bonus == "attack":
                    damage = int(damage * 1.3)
                elif self.player.element_bonus == "damage":
                    damage = int(damage * 1.4)
            
            # 五行相克伤害加成（克敌属性+50%伤害）
            player_elem = self.player.element
            skill_elem = skill.get("element", "无")
            if skill_elem != "无":
                for e in targets:
                    e_elem = getattr(e, 'element', None)
                    if e_elem and ELEMENTS.get(player_elem, {}).get("weakness") == e_elem:
                        damage = int(damage * 1.5)  # 相克加成
                        break
            
            if skill["type"] == "attack":
                # 攻击功法
                for e in targets:
                    e.take_damage(damage)
                    self.spawn_attack_particles(e.x, e.y, skill["color"])
                
                # 攻击动画
                if targets:
                    self.trigger_attack_anim(targets[0].x, targets[0].y, skill.get("color", RED))
                self.show_message(f"◆{tech_name}")
                
            elif skill["type"] == "aoe":
                # AOE功法
                for e in targets:
                    e.take_damage(damage)
                    self.spawn_attack_particles(e.x, e.y, skill["color"])
                if targets:
                    self.trigger_attack_anim(targets[0].x, targets[0].y, skill.get("color", ORANGE))
                self.show_message(f"◇{tech_name}")
                
            elif skill["type"] == "heal":
                # 治疗功法
                heal_amt = skill.get("heal", 0)
                self.player.heal(heal_amt)
                self.spawn_attack_particles(self.player.x, self.player.y, GREEN)
                self.show_message(f"♥{tech_name}+{heal_amt}")
                
            elif skill["type"] == "buff":
                # 增益功法
                shield = skill.get("shield", 0)
                if shield:
                    self.player.heal(shield)
                    self.show_message(f"◎{tech_name}+{shield}护盾")
                    
            elif skill["type"] == "dodge":
                # 闪避
                self.show_message(f"★{tech_name}闪避")
        
        # ===== 链技触发系统 =====
        for tech_name in self.player.techniques:
            skill = TECHNIQUES.get(tech_name, {})
            chain_skill_name = skill.get("chain")
            # chain 可能是列表或字符串
            if not chain_skill_name:
                continue
            if isinstance(chain_skill_name, list):
                chain_skill_name = chain_skill_name[0] if chain_skill_name else None
            if not chain_skill_name:
                continue
            
            # 检查链技是否已学会且冷却好
            if chain_skill_name not in self.player.techniques:
                continue
            
            chain_skill = TECHNIQUES[chain_skill_name]
            last_used = self.player.skill_cooldowns.get(chain_skill_name, 0)
            now = pygame.time.get_ticks()
            if now - last_used < chain_skill["cooldown"]:
                continue
            
            # 检查是否有敌人
            targets = [e for e in self.enemies if e.is_alive() and 
                       math.hypot(e.x - self.player.x, e.y - self.player.y) < self.attack_range]
            if not targets:
                continue
            
            # 链技触发概率（30%基础）
            trigger_chance = 0.3
            
            # 五行相生加成：同属性+10%
            if chain_skill.get("element") == self.player.element:
                trigger_chance += 0.1
            
            # 五行相克加成：克敌属性+15%
            player_elem = self.player.element
            for e in targets:
                e_elem = getattr(e, 'element', None)
                if e_elem and ELEMENTS.get(player_elem, {}).get("weakness") == e_elem:
                    trigger_chance += 0.15
                    break
            
            if random.random() < trigger_chance:
                # 触发链技！
                damage = chain_skill.get("damage", 0)
                damage = int(damage * 1.5)  # 链技伤害+50%
                
                for e in targets:
                    e.take_damage(damage)
                    self.spawn_attack_particles(e.x, e.y, chain_skill.get("color", GOLD))
                
                self.show_message(f"🔥链技 {chain_skill_name}!")
                self.player.skill_cooldowns[chain_skill_name] = now
                
                if targets:
                    self.trigger_attack_anim(targets[0].x, targets[0].y, chain_skill.get("color", GOLD))
        
        # 敌人AI
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.move_toward(self.player.x, self.player.y)
                dist = math.hypot(enemy.x - self.player.x, enemy.y - self.player.y)
                if dist < 50:
                    self.player.take_damage(enemy.damage)
        
        # 移除死亡敌人并发放奖励
        remaining_enemies = []
        for e in self.enemies:
            if e.is_alive():
                remaining_enemies.append(e)
            else:
                # 发放奖励
                self.player.gold += e.gold
                self.player.add_exp(e.exp)
                self.show_message(f"击败{e.name} +{e.gold}灵石 +{e.exp}修为")
                # 死亡特效
                for _ in range(12):
                    self.particles.append(Particle(e.x, e.y, e.color, 4, 40))
        self.enemies = remaining_enemies
        
        # 玩家死亡
        if self.player.hp <= 0:
            self.state = "dead"
        
        # 突破逻辑
        if self.player.can_breakthrough() and not self.boss_spawned and self.state == "game":
            self.start_breakthrough_challenge()
        
        if self.breakthrough_boss and not self.breakthrough_boss.is_alive():
             self.on_boss_defeat()
        
        # 生成新敌人 (控制数量和频率)
        # 增加敌人最大数量上限，随境界增加
        max_enemies = 10 + self.player.realm * 3
        # 优化生成频率
        if len(self.enemies) < max_enemies and self.game_time % 60 == 0:
            self.enemies.append(self.create_enemy())
        
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if self.state == "game":
            # 键盘移动
            speed = 5
            moved = False
            dx, dy = 0, 0
            if keys[pygame.K_w]:
                dy = -speed
                moved = True
            if keys[pygame.K_s]:
                dy = speed
                moved = True
            if keys[pygame.K_a]:
                dx = -speed
                moved = True
            if keys[pygame.K_d]:
                dx = speed
                moved = True
            
            if moved:
                self.player.state = "Walking"
                self.move_target = None  # 取消鼠标移动
                self.player.move(dx, dy, WORLD_WIDTH, WORLD_HEIGHT)
                if random.random() < 0.3:
                    self.particles.append(Particle(
                        self.player.x + random.randint(-10, 10),
                        self.player.y + 20,
                        (100, 150, 200), 0.5, 20
                    ))
            elif self.move_target:
                self.player.state = "Walking"
                # 自动移动到目标
                self.update_movement()
            else:
                self.player.state = "Idle"
    
    def spawn_attack_particles(self, x, y, color):
        for _ in range(8):
            self.particles.append(Particle(x, y, color, 3, 30))
    
    def handle_click(self, pos):
        # 菜单点击
        if self.state == "menu":
            for name, rect in self.menu_buttons:
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    if name == "new": self.state = "char_selection"
                    elif name == "load": self.load_game()
                    elif name == "handbook": self.state = "handbook"
                    elif name == "exit": 
                        pygame.quit()
                        sys.exit()
                    return
        
        elif self.state == "char_selection":
            # 导航按钮
            for name, rect in self.char_nav_buttons:
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    if name == "prev": 
                        self.char_selection_idx = (self.char_selection_idx - 1) % len(CHARACTERS)
                    elif name == "next":
                        self.char_selection_idx = (self.char_selection_idx + 1) % len(CHARACTERS)
                    elif name == "select":
                        elem = list(CHARACTERS.keys())[self.char_selection_idx]
                        self.start_game(elem)
                    return

        # 游戏菜单点击
        elif self.state == "esc_menu":
            for name, rect in self.esc_buttons:
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    if name == "resume": self.state = "game"
                    elif name == "save": self.save_game()
                    elif name == "load": self.load_game()
                    elif name == "menu": self.state = "menu"
                    return
        
        # 游戏状态点击
        elif self.state == "game":
            # 检查底部按钮点击
            for btn_name, btn_rect in self.buttons:
                if btn_rect[0] < pos[0] < btn_rect[0] + btn_rect[2]:
                    if btn_rect[1] < pos[1] < btn_rect[1] + btn_rect[3]:
                        if btn_name == 'shop':
                            self.state = 'shop'
                        elif btn_name == 'breakthrough':
                            self.state = 'breakthrough'
                        elif btn_name == 'equipment':
                            self.state = 'equipment'
                        elif btn_name == 'handbook':
                            self.state = 'handbook'
                        elif btn_name == 'esc_menu':
                            self.state = 'esc_menu'
                        return
            
            # 查找点击的敌人
            world_pos_x = pos[0] + self.camera_x
            world_pos_y = pos[1] + self.camera_y
            clicked_enemy = None
            for enemy in self.enemies:
                dist = math.hypot(world_pos_x - enemy.x, world_pos_y - enemy.y)
                if dist < enemy.size + 15:
                    clicked_enemy = enemy
                    break
            
            if clicked_enemy:
                # 攻击敌人
                self.move_target = None
                dist_to_enemy = math.hypot(clicked_enemy.x - self.player.x, clicked_enemy.y - self.player.y)
                if dist_to_enemy > self.attack_range:
                    self.show_message("距离太远! 正在自动靠近...")
                    self.set_move_target(clicked_enemy.x, clicked_enemy.y)
                    self.attack_target = clicked_enemy
                    return
                
                # 攻击逻辑
                self.perform_attack(clicked_enemy)
                return
            else:
                # 点击地面 - 移动
                self.set_move_target(world_pos_x, world_pos_y)
                self.attack_target = None
        
        # 商店点击
        elif self.state == "shop":
            # 检查物品点击
            for idx, btn in getattr(self, 'shop_buttons', []):
                if btn[0] < pos[0] < btn[0] + btn[2] and btn[1] < pos[1] < btn[1] + btn[3]:
                    if idx == 'back':
                        self.state = 'game'
                    else:
                        self.buy_item(idx)
                    return
        
        elif self.state == "reward_selection":
            for i, choice in enumerate(self.reward_choices):
                rect = (SCREEN_WIDTH//2 - 150, 200 + i * 100, 300, 80)
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    self.apply_reward(choice)
                    self.state = "game"
                    return
        
        # 突破界面点击
        elif self.state == "breakthrough":
            # 返回按钮
            if SCREEN_WIDTH//2 - 60 < pos[0] < SCREEN_WIDTH//2 + 60:
                if SCREEN_HEIGHT - 80 < pos[1] < SCREEN_HEIGHT - 35:
                    self.state = 'game'
                    return
            # 自动突破
            if self.player.can_breakthrough() and not self.boss_spawned:
                self.start_breakthrough_challenge()
            self.state = 'game'
        
        elif self.state == "confirm":
            for name, rect in self.confirm_buttons:
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    self.confirm_purchase(name == "yes")
                    return
        
        # 装备界面点击
        elif self.state == "equipment":
            if SCREEN_WIDTH//2 - 60 < pos[0] < SCREEN_WIDTH//2 + 60:
                if SCREEN_HEIGHT - 80 < pos[1] < SCREEN_HEIGHT - 35:
                    self.state = 'game'
        
        # 确认购买界面
        elif self.state == "confirm":
             for name, rect in self.confirm_buttons:
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    self.confirm_purchase(name == "yes")
                    return

        # 技能图鉴点击
        elif self.state == "handbook":
            # 返回按钮
            if SCREEN_WIDTH//2 - 60 < pos[0] < SCREEN_WIDTH//2 + 60 and SCREEN_HEIGHT - 60 < pos[1] < SCREEN_HEIGHT - 20:
                self.state = 'game'
            # 标签页切换
            tabs = ["金", "木", "水", "火", "土", "无"]
            for i, tab in enumerate(tabs):
                rect = (100 + i * 150, 120, 140, 40)
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    self.handbook_tab = tab
                    self.handbook_page = 0
            # 翻页按钮
            prev_btn = (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 100, 100, 40)
            next_btn = (SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 100, 100, 40)
            if prev_btn[0] < pos[0] < prev_btn[0] + prev_btn[2] and prev_btn[1] < pos[1] < prev_btn[1] + prev_btn[3]:
                self.handbook_page = max(0, self.handbook_page - 1)
            elif next_btn[0] < pos[0] < next_btn[0] + next_btn[2] and next_btn[1] < pos[1] < next_btn[1] + next_btn[3]:
                self.handbook_page += 1
        
        # 死亡界面
        elif self.state == "dead":
            if SCREEN_WIDTH//2 - 80 < pos[0] < SCREEN_WIDTH//2 + 80:
                if 400 < pos[1] < 450:
                    self.start_game()
                elif 460 < pos[1] < 500:
                    pygame.quit()
                    sys.exit()
    
    def handle_key(self, key):
        if key == pygame.K_ESCAPE:
            if self.state == "menu":
                pygame.quit()
                sys.exit()
            elif self.state == "dead":
                pygame.quit()
                sys.exit()
            elif self.state == "char_selection":
                self.state = "menu"
            elif self.state == "game":
                self.state = "esc_menu"
            elif self.state == "esc_menu":
                self.state = "game"
            else:
                # 任何子界面按 ESC 都返回 game
                self.state = "game"
        
        elif self.state == "menu":
            if key == pygame.K_UP:
                self.menu_selection_idx = (self.menu_selection_idx - 1) % len(self.menu_buttons)
            elif key == pygame.K_DOWN:
                self.menu_selection_idx = (self.menu_selection_idx + 1) % len(self.menu_buttons)
            elif key == pygame.K_RETURN:
                name, _ = self.menu_buttons[self.menu_selection_idx]
                if name == "new": self.state = "char_selection"
                elif name == "load": self.load_game()
                elif name == "handbook": self.state = "handbook"
                elif name == "exit": 
                    pygame.quit()
                    sys.exit()
        
        elif key == pygame.K_RETURN and self.state == "menu":
             # This block might be redundant but keeping logic consistent
             pass

        elif self.state == "char_selection":
            if key == pygame.K_LEFT:
                self.char_selection_idx = (self.char_selection_idx - 1) % len(CHARACTERS)
            elif key == pygame.K_RIGHT:
                self.char_selection_idx = (self.char_selection_idx + 1) % len(CHARACTERS)
            elif key == pygame.K_RETURN:
                elem = list(CHARACTERS.keys())[self.char_selection_idx]
                self.start_game(elem)

        if self.state == "game":
            if key == pygame.K_b:
                self.state = "shop"
            elif key == pygame.K_t:
                self.state = "breakthrough"
            elif key == pygame.K_e:
                self.state = "equipment"
            elif key == pygame.K_h:
                self.state = "handbook"
            elif key == pygame.K_1:
                self.player.equipped_idx = 0
            elif key == pygame.K_2:
                if len(self.player.techniques) > 1:
                    self.player.equipped_idx = 1
            elif key == pygame.K_3:
                if len(self.player.techniques) > 2:
                    self.player.equipped_idx = 2
        
        elif self.state == "shop":
            if key == pygame.K_b:
                self.state = "game"
            elif key == pygame.K_1: self.buy_item(0)
            elif key == pygame.K_2: self.buy_item(1)
            elif key == pygame.K_3: self.buy_item(2)
            elif key == pygame.K_4: self.buy_item(3)
            elif key == pygame.K_5: self.buy_item(4)
            elif key == pygame.K_6: self.buy_item(5)
        
        elif self.state == "breakthrough":
            if key == pygame.K_b:
                self.state = "game"
            elif key == pygame.K_t:
                if self.player.can_breakthrough():
                    self.player.breakthrough()
                    self.show_message(f"突破成功! 踏入{self.player.realm_name}境!")
                    self.generate_shop()
                self.state = "game"
        
        elif self.state == "equipment":
            if key == pygame.K_e or key == pygame.K_b:
                self.state = "game"
        elif self.state == "handbook":
            if key == pygame.K_ESCAPE or key == pygame.K_b:
                self.state = "game"
            elif key == pygame.K_LEFT:
                self.handbook_page = max(0, self.handbook_page - 1)
            elif key == pygame.K_RIGHT:
                self.handbook_page += 1
            elif key == pygame.K_UP or key == pygame.K_DOWN:
                tabs = ["金", "木", "水", "火", "土", "无"]
                idx = tabs.index(self.handbook_tab) if self.handbook_tab in tabs else 0
                if key == pygame.K_UP:
                    idx = (idx - 1) % len(tabs)
                else:
                    idx = (idx + 1) % len(tabs)
                self.handbook_tab = tabs[idx]
                self.handbook_page = 0
    
    def buy_item(self, idx):
        if idx < len(self.shop_items):
            self.confirm_item = idx
            self.state = "confirm"
            
    def confirm_purchase(self, confirmed):
        if confirmed and self.confirm_item is not None:
            idx = self.confirm_item
            type_, item = self.shop_items[idx]
            
            cost = 0
            if type_ == "tech":
                if item in self.player.techniques:
                    self.show_message("已学会")
                else:
                    cost = TECHNIQUES[item].get("cost", 50) * 20
                    if self.player.gold >= cost:
                        self.player.gold -= cost
                        self.player.techniques.append(item)
                        self.show_message(f"成功购买: {item}!")
                    else:
                        self.show_message("灵石不足!")
            else:
                cost = item.get("cost", 100)
                if self.player.gold >= cost:
                    self.player.gold -= cost
                    if type_ == "weapon": self.player.equip(item, "weapon")
                    elif type_ == "armor": self.player.equip(item, "armor")
                    self.show_message(f"购买成功!")
                else:
                    self.show_message("灵石不足!")
        self.state = "shop"
        self.confirm_item = None

    def draw_confirm(self):
        # 覆盖在商店上层
        self.draw_shop() 
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        rect = (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 100, 300, 200)
        pygame.draw.rect(self.screen, PAPER, rect)
        pygame.draw.rect(self.screen, INK_BLACK, rect, 3)
        self.draw_text("是否确认购买?", self.font, INK_BLACK, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50, center=True)
        
        yes_btn = (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2 + 20, 60, 40)
        no_btn = (SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2 + 20, 60, 40)
        
        pygame.draw.rect(self.screen, GREEN, yes_btn)
        pygame.draw.rect(self.screen, RED, no_btn)
        self.draw_text("是", self.small_font, WHITE, yes_btn[0]+30, yes_btn[1]+20, center=True)
        self.draw_text("否", self.small_font, WHITE, no_btn[0]+30, no_btn[1]+20, center=True)
        self.confirm_buttons = [("yes", yes_btn), ("no", no_btn)]
    
    def draw_text(self, text, font, color, x, y, center=False):
        img = font.render(text, True, color)
        if center:
            self.screen.blit(img, (x - img.get_width()//2, y - img.get_height()//2))
        else:
            self.screen.blit(img, (x, y))
        return img
    
    def draw_hp_bar(self, x, y, current, max_val, width, color):
        ratio = current / max_val if max_val > 0 else 0
        pygame.draw.rect(self.screen, (40, 40, 40), (x, y, width, 10))
        pygame.draw.rect(self.screen, color, (x, y, int(width * ratio), 10))
        pygame.draw.rect(self.screen, WHITE, (x, y, width, 10), 1)
    
    def draw_skill_tooltip(self, skill_name, pos):
        """绘制技能详情提示框"""
        skill = TECHNIQUES.get(skill_name)
        if not skill:
            return
        
        # 计算提示框位置（避免超出屏幕）
        tip_w, tip_h = 250, 180
        x = pos[0] + 15
        y = pos[1] + 15
        if x + tip_w > SCREEN_WIDTH:
            x = pos[0] - tip_w - 10
        if y + tip_h > SCREEN_HEIGHT:
            y = pos[1] - tip_h - 10
        
        # 绘制背景
        pygame.draw.rect(self.screen, (45, 42, 38), (x, y, tip_w, tip_h))
        pygame.draw.rect(self.screen, (180, 160, 120), (x, y, tip_w, tip_h), 2)
        
        # 技能名称和五行
        elem = skill.get("element", "无")
        level = skill.get("level", 1)
        level_names = ["基础", "初级", "中级", "高级"]
        level_str = level_names[level-1] if 1 <= level <= 4 else "未知"
        elem_color = ELEMENTS.get(elem, {}).get("color", (200, 200, 200))
        self.draw_text(f"【{elem}】【{level_str}】{skill_name}", self.font, elem_color, x + 10, y + 10)
        
        # 类型和冷却
        skill_type = skill.get("type", "unknown")
        cooldown = skill.get("cooldown", 0) / 1000
        self.draw_text(f"类型:{skill_type} | 冷却:{cooldown:.1f}s", self.small_font, (200, 200, 180), x + 10, y + 35)
        
        # 详细效果
        y_offset = 60
        if "damage" in skill:
            self.draw_text(f"攻击: {skill['damage']}", self.small_font, (255, 100, 100), x + 10, y + y_offset)
            y_offset += 20
        if "heal" in skill:
            self.draw_text(f"治疗: {skill['heal']}", self.small_font, (100, 255, 100), x + 10, y + y_offset)
            y_offset += 20
        if "shield" in skill:
            self.draw_text(f"护盾: {skill['shield']}", self.small_font, (100, 200, 255), x + 10, y + y_offset)
            y_offset += 20
        if "aoe" in skill and skill["aoe"]:
            self.draw_text("范围: 全体攻击", self.small_font, (255, 255, 150), x + 10, y + y_offset)
            y_offset += 20
        if "chain" in skill:
            chain = skill["chain"]
            if isinstance(chain, list): chain = chain[0] if chain else "无"
            self.draw_text(f"触发: {chain}", self.small_font, (255, 200, 100), x + 10, y + y_offset)
            y_offset += 20
            
        self.draw_text(f"描述: {skill.get('desc', '')}", self.small_font, (200, 200, 200), x + 10, y + y_offset + 10)
        
        # 冷却时间条
        if skill_name in self.player.skill_cooldowns:
            last_used = self.player.skill_cooldowns[skill_name]
            now = pygame.time.get_ticks()
            cd = skill.get("cooldown", 1000)
            remaining = max(0, cd - (now - last_used)) / 1000
            if remaining > 0:
                self.draw_text(f"冷却中: {remaining:.1f}秒", self.small_font, (255, 200, 100), x + 10, y + 155)
    
    def draw_player_model(self, x, y):
        """绘制玩家角色模型 - 水墨武侠风格"""
        if self.player.element == "水" and self.shui_spritesheet:
            # Simple spritesheet rendering for Shui
            # Use self.player.anim_frame to animate
            frame_width = self.shui_spritesheet.get_width() // 4
            frame_height = self.shui_spritesheet.get_height() // 4
            
            # Map state to row
            state_map = {"Idle": 0, "Walking": 1, "Attacking": 2, "Casting": 3}
            new_row = state_map.get(self.player.state, 0)
            
            # Reset frame if state changed
            if not hasattr(self.player, '_last_row') or self.player._last_row != new_row:
                self.player.anim_frame = 0
            self.player._last_row = new_row
            
            row = new_row
            col = (self.player.anim_frame // 10) % 4
            rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            self.screen.blit(self.shui_spritesheet, (x - frame_width // 2, y - frame_height // 2), rect)
            self.player.anim_frame += 1
            return
        
        # 呼吸动画
        breath_offset = math.sin(pygame.time.get_ticks() * 0.003) * 2
        
        # 御剑 (脚下的剑)
        if self.player.weapon:
            # 剑身
            pygame.draw.line(self.screen, (180, 180, 190), (x - 25, y + 15), (x + 25, y + 10), 4)
            pygame.draw.line(self.screen, CYAN, (x - 25, y + 15), (x + 25, y + 10), 2)
        
        # 身体 (长袍)
        pygame.draw.polygon(self.screen, (60, 80, 140), [
            (x - 20, y + breath_offset),
            (x + 20, y + breath_offset),
            (x + 28, y + 35),
            (x - 28, y + 35)
        ])
        # 腰带
        pygame.draw.rect(self.screen, GOLD, (x - 15, y + 8 + breath_offset, 30, 4))
        
        # 手臂
        pygame.draw.circle(self.screen, (255, 220, 180), (x - 22, y + 5 + breath_offset), 8)
        pygame.draw.circle(self.screen, (255, 220, 180), (x + 22, y + 5 + breath_offset), 8)
        
        # 头部
        pygame.draw.circle(self.screen, (255, 220, 180), (x, y - 12 + breath_offset), 16)
        
        # 头发 (发髻)
        pygame.draw.circle(self.screen, INK_BLACK, (x, y - 20 + breath_offset), 14)
        pygame.draw.circle(self.screen, INK_BLACK, (x, y - 28 + breath_offset), 8)
        
        # 眼睛
        pygame.draw.circle(self.screen, INK_BLACK, (x - 5, y - 14 + breath_offset), 2)
        pygame.draw.circle(self.screen, INK_BLACK, (x + 5, y - 14 + breath_offset), 2)
        
        # 武器特效
        if self.player.weapon:
            quality = self.player.weapon.get("quality", "普通")
            if quality == "传说":
                # 金光特效
                for i in range(3):
                    ox = math.cos(pygame.time.get_ticks() * 0.01 + i * 2) * 5
                    oy = math.sin(pygame.time.get_ticks() * 0.01 + i * 2) * 5
                    pygame.draw.circle(self.screen, GOLD, (x + 30 + ox, y - 10 + oy), 3)
            elif quality == "史诗":
                pygame.draw.circle(self.screen, PURPLE, (x + 30, y - 10), 4)
    
    def draw_enemy_model(self, enemy, x, y):
        """绘制敌人模型 - 各具特色"""
        size = enemy.size
        breath = math.sin(pygame.time.get_ticks() * 0.004) * 2
        
        # 根据敌人类型绘制不同模型
        name = enemy.name
        
        if "兔子" in name:
            # 兔子 - 长耳朵
            pygame.draw.ellipse(self.screen, enemy.color, (x - 12, y - size - 15, 8, 20))
            pygame.draw.ellipse(self.screen, enemy.color, (x + 4, y - size - 15, 8, 20))
            pygame.draw.circle(self.screen, enemy.color, (x, y), size)
            # 眼睛
            pygame.draw.circle(self.screen, RED, (x - 5, y - 5), 3)
            pygame.draw.circle(self.screen, RED, (x + 5, y - 5), 3)
            # 嘴巴
            pygame.draw.circle(self.screen, (255, 150, 150), (x, y + 3), 3)
            
        elif "狼" in name or "妖" in name:
            # 狼妖 - 尖耳朵 獠牙
            # 耳朵
            pygame.draw.polygon(self.screen, enemy.color, [(x-10, y-10), (x-15, y-size-5), (x-3, y-10)])
            pygame.draw.polygon(self.screen, enemy.color, [(x+10, y-10), (x+15, y-size-5), (x+3, y-10)])
            # 身体
            pygame.draw.circle(self.screen, enemy.color, (x, y), size)
            # 眼睛 (发亮)
            eye_glow = (min(255, 200 + math.sin(pygame.time.get_ticks() * 0.01) * 55), 0, 0)
            pygame.draw.circle(self.screen, eye_glow, (x - size//3, y - size//4), 5)
            pygame.draw.circle(self.screen, eye_glow, (x + size//3, y - size//4), 5)
            # 獠牙
            pygame.draw.polygon(self.screen, WHITE, [(x-6, y+5), (x-3, y+12), (x, y+5)])
            pygame.draw.polygon(self.screen, WHITE, [(x+6, y+5), (x+3, y+12), (x, y+5)])
            
        elif "僵尸" in name:
            # 僵尸 - 僵硬 手臂前伸
            pygame.draw.circle(self.screen, (80, 120, 80), (x, y), size)
            # 手臂
            pygame.draw.rect(self.screen, (60, 100, 60), (x - size - 5, y - 5, size, 8))
            # 眼睛 (空洞)
            pygame.draw.circle(self.screen, (20, 20, 20), (x - 5, y - 5), 4)
            pygame.draw.circle(self.screen, (20, 20, 20), (x + 5, y - 5), 4)
            # 牙齿
            pygame.draw.rect(self.screen, (180, 180, 180), (x - 4, y + 5, 3, 5))
            pygame.draw.rect(self.screen, (180, 180, 180), (x + 1, y + 5, 3, 5))
            
        elif "修士" in name:
            # 修仙者 - 穿道袍 拿法器
            # 道袍
            pygame.draw.polygon(self.screen, enemy.color, [
                (x - size + 5, y + breath),
                (x + size - 5, y + breath),
                (x + size, y + size),
                (x - size, y + size)
            ])
            # 头部
            pygame.draw.circle(self.screen, (255, 220, 180), (x, y - size//2 + breath), size//2)
            # 帽子
            pygame.draw.polygon(self.screen, enemy.color, [
                (x - size//2 - 3, y - size + breath),
                (x + size//2 + 3, y - size + breath),
                (x, y - size - 10 + breath)
            ])
            # 眼睛
            pygame.draw.circle(self.screen, INK_BLACK, (x - 4, y - size//2 - 3 + breath), 2)
            pygame.draw.circle(self.screen, INK_BLACK, (x + 4, y - size//2 - 3 + breath), 2)
            
        else:
            # 默认怪物
            pygame.draw.circle(self.screen, enemy.color, (x, y), size)
            pygame.draw.circle(self.screen, INK_BLACK, (x, y), size, 2)
            # 眼睛
            eye_color = RED if enemy.damage > 25 else WHITE
            pygame.draw.circle(self.screen, eye_color, (x - size//3, y - size//4), 4)
            pygame.draw.circle(self.screen, eye_color, (x + size//3, y - size//4), 4)
        
        # 名字
        self.draw_text(enemy.name, self.small_font, INK_BLACK, x, y - size - 20, center=True)
        # 血条
        self.draw_hp_bar(x - 25, y + size + 3, enemy.hp, enemy.max_hp, 50, RED)
    
    def draw_dead(self):
        self.screen.fill(INK_BLACK)
        self.draw_text("身死道消", self.title_font, RED, SCREEN_WIDTH//2, 140, center=True)
        self.draw_text("───────────", self.font, GRAY, SCREEN_WIDTH//2, 200, center=True)
        self.draw_text(f"境界: {self.player.realm_name} {self.player.level}层", self.font, PAPER, SCREEN_WIDTH//2, 250, center=True)
        self.draw_text(f"修为: {self.player.realm * 10 + self.player.level}", self.font, GOLD, SCREEN_WIDTH//2, 300, center=True)
        
        self.draw_text("Enter 重新开始", self.font, GREEN, SCREEN_WIDTH//2, 420, center=True)
        self.draw_text("Esc 退出", self.font, GRAY, SCREEN_WIDTH//2, 480, center=True)

    def draw_dead(self):
        self.screen.fill(INK_BLACK)
        self.draw_text("身死道消", self.title_font, RED, SCREEN_WIDTH//2, 140, center=True)
        self.draw_text("───────────", self.font, GRAY, SCREEN_WIDTH//2, 200, center=True)
        self.draw_text(f"境界: {self.player.realm_name} {self.player.level}层", self.font, PAPER, SCREEN_WIDTH//2, 250, center=True)
        self.draw_text(f"修为: {self.player.realm * 10 + self.player.level}", self.font, GOLD, SCREEN_WIDTH//2, 300, center=True)
        
        self.draw_text("Enter 重新开始", self.font, GREEN, SCREEN_WIDTH//2, 420, center=True)
        self.draw_text("Esc 退出", self.font, GRAY, SCREEN_WIDTH//2, 480, center=True)

    def draw_menu(self):
        # 绘制背景
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(PAPER)
            # 背景装饰 - 墨点
            for _ in range(15):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                pygame.draw.circle(self.screen, INK_GRAY, (x, y), random.randint(1, 3))
        
        # 标题 - 书法风格
        self.draw_text("杏杏修仙录", self.title_font, RED, SCREEN_WIDTH//2, 80, center=True)
        self.draw_text("─────────────", self.font, INK_GRAY, SCREEN_WIDTH//2, 140, center=True)
        
        # 菜单按钮
        menu_items = [("new", "新游戏"), ("load", "读取存档"), ("handbook", "图鉴"), ("achievements", "成就 (未开发)"), ("exit", "退出")]
        self.menu_buttons = []
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (name, label) in enumerate(menu_items):
            rect = (SCREEN_WIDTH//2 - 120, 250 + i * 70, 240, 50)
            
            # 检测鼠标悬停
            if rect[0] < mouse_pos[0] < rect[0] + rect[2] and rect[1] < mouse_pos[1] < rect[1] + rect[3]:
                self.menu_selection_idx = i
                
            is_selected = (self.menu_selection_idx == i)
            color = (200, 200, 200) if is_selected else PAPER
            border = RED if is_selected else INK_BLACK
            thickness = 4 if is_selected else 2
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, border, rect, thickness)
            
            label_color = RED if is_selected else INK_BLACK
            self.draw_text(label, self.font, label_color, SCREEN_WIDTH//2, 275 + i * 70, center=True)
            self.menu_buttons.append((name, rect))

    def split_text(self, text, length):
        return [text[i:i+length] for i in range(0, len(text), length)]

    def draw_char_selection(self):
        # 绘制背景
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
            # 增加遮罩层，让文字更清晰
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill(PAPER)

        # Draw character portrait
        elem_keys = list(CHARACTERS.keys())
        current_elem = elem_keys[self.char_selection_idx]
        char = CHARACTERS[current_elem]
        
        # Left: Portrait + Name
        if self.portraits.get(current_elem):
            self.screen.blit(self.portraits[current_elem], (100, 200))
        self.draw_text(char["name"], self.title_font, WHITE, 250, 550, center=True)
        
        # Right-Top: Story
        self.draw_text("背景故事", self.title_font, RED, 800, 200, center=True)
        desc_lines = self.split_text(char["desc"], 15)
        for i, line in enumerate(desc_lines):
            self.draw_text(line, self.font, WHITE, 800, 260 + i * 35, center=True)
            
        # Right-Bottom: Stats
        self.draw_text("角色属性", self.title_font, RED, 800, 450, center=True)
        self.draw_text(f"属性: {char['element']}", self.font, WHITE, 800, 500, center=True)
        self.draw_text(f"初始攻击: {char['base_attack']}", self.font, WHITE, 800, 530, center=True)
        self.draw_text(f"初始防御: {char['base_defense']}", self.font, WHITE, 800, 560, center=True)
        self.draw_text(f"初始气血: {char['base_hp']}", self.font, WHITE, 800, 590, center=True)
        
        # Navigation
        prev_btn = (100, 650, 100, 50)
        next_btn = (300, 650, 100, 50)
        select_btn = (800, 650, 120, 50)
        
        for btn, text in [(prev_btn, "上一个"), (next_btn, "下一个"), (select_btn, "选择")]:
            pygame.draw.rect(self.screen, PAPER, btn)
            pygame.draw.rect(self.screen, INK_BLACK, btn, 2)
            self.draw_text(text, self.font, INK_BLACK, btn[0]+50, btn[1]+25, center=True)
        
        self.char_nav_buttons = [("prev", prev_btn), ("next", next_btn), ("select", select_btn)]
    
    def draw_game(self):
        if not self.player: return
        # 水墨风格背景
        self.screen.fill(PAPER)
        
        # 计算摄像机位置 (让玩家居中)
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        # 限制摄像机范围
        self.camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, self.camera_x))
        self.camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, self.camera_y))
        
        # 转换坐标函数
        def to_screen(x, y):
            return (int(x - self.camera_x), int(y - self.camera_y))
        
        # 绘制地图元素
        for elem in self.map_elements:
            sx, sy = to_screen(elem["x"], elem["y"])
            if -100 < sx < SCREEN_WIDTH + 100 and -100 < sy < SCREEN_HEIGHT + 100:
                if elem["type"] == "tree":
                    # 水墨风格树：更具层次
                    pygame.draw.circle(self.screen, (40, 100, 40), (sx, sy), 20)
                    pygame.draw.circle(self.screen, (60, 120, 60), (sx-8, sy-8), 12)
                    pygame.draw.rect(self.screen, (80, 60, 40), (sx-4, sy+10, 8, 20))
                elif elem["type"] == "rock":
                    # 岩石：更有质感
                    pygame.draw.polygon(self.screen, (100, 100, 100), [(sx-15, sy+10), (sx, sy-15), (sx+15, sy+10)])
                    pygame.draw.polygon(self.screen, (80, 80, 80), [(sx-5, sy+5), (sx, sy-5), (sx+5, sy+5)])
                elif elem["type"] == "river":
                    # 河流：简单水墨流线
                    pygame.draw.ellipse(self.screen, (150, 200, 255), (sx, sy, 60, 30))
                elif elem["type"] == "flower":
                    # 花丛
                    pygame.draw.circle(self.screen, (255, 100, 150), (sx, sy), 8)
        
        # 粒子特效 (需要应用坐标转换)
        for p in self.particles:
            sx, sy = to_screen(p.x, p.y)
            # 为了能在Particle里使用to_screen，可以直接在这里draw
            alpha = p.life / p.max_life
            if alpha > 0.3:
                pygame.draw.circle(self.screen, p.color, (sx, sy), 4)
        
        # 攻击动画效果
        if self.attack_anim:
            elapsed = pygame.time.get_ticks() - self.attack_anim['start']
            if elapsed < 300:
                progress = elapsed / 300
                start_x, start_y = to_screen(self.player.x, self.player.y)
                end_x, end_y = to_screen(self.attack_anim['x'], self.attack_anim['y'])
                
                cur_x = start_x + (end_x - start_x) * progress
                cur_y = start_y + (end_y - start_y) * progress
                
                color = self.attack_anim.get('type', CYAN)
                pygame.draw.circle(self.screen, color, (int(cur_x), int(cur_y)), 8)
                
                for i in range(3):
                    t = max(0, progress - i * 0.1)
                    tail_x = start_x + (end_x - start_x) * t
                    tail_y = start_y + (end_y - start_y) * t
                    pygame.draw.circle(self.screen, color, (int(tail_x), int(tail_y)), 4 - i)
            else:
                self.attack_anim = None
        
        # 敌人
        for enemy in self.enemies:
            sx, sy = to_screen(enemy.x, enemy.y)
            self.draw_enemy_model(enemy, sx, sy)
        
        # 玩家
        px, py = to_screen(self.player.x, self.player.y)
        self.draw_player_model(px, py)
        self.draw_hp_bar(px - 30, py + 38, self.player.hp, self.player.max_hp, 60, RED)
        
        # ===== UI面板 =====
        
        # ===== UI面板优化 =====
        
        # 左侧 - 状态面板 (修仙风格)
        ui_x, ui_y = 20, 20
        ui_w, ui_h = 200, 240
        pygame.draw.rect(self.screen, (80, 60, 40), (ui_x, ui_y, ui_w, ui_h), 4) # 木质边框
        pygame.draw.rect(self.screen, (245, 235, 210), (ui_x+4, ui_y+4, ui_w-8, ui_h-8)) # 纸质背景
        
        stats = [
            f"境界: {self.player.realm_name} {self.player.level}层",
            f"生命: {self.player.hp}/{self.player.max_hp}",
            f"攻击: {self.player.attack}",
            f"防御: {self.player.defense}",
            f"修为: {self.player.exp}/{self.player.exp_to_next}",
            f"灵石: {self.player.gold}",
        ]
        for i, s in enumerate(stats):
            color = (30, 30, 30)
            if "境界" in s: color = (160, 40, 40)
            elif "灵石" in s: color = (180, 100, 0)
            self.draw_text(s, self.font, color, ui_x + 15, ui_y + 20 + i * 35)
        
        # 底部导航栏 (修仙风格面板)
        nav_h = 60
        nav_y = SCREEN_HEIGHT - nav_h - 10
        pygame.draw.rect(self.screen, (80, 60, 40), (100, nav_y, SCREEN_WIDTH-200, nav_h), 3)
        pygame.draw.rect(self.screen, (245, 235, 210), (105, nav_y+5, SCREEN_WIDTH-210, nav_h-10))
        
        # 经验/灵石显示移到这里 (原在状态栏)
        self.draw_text(f"修为: {self.player.exp}/{self.player.exp_to_next}", self.font, (30, 30, 30), 120, nav_y + 15)
        self.draw_text(f"灵石: {self.player.gold}", self.font, (180, 100, 0), 120, nav_y + 35)
        
        btn_spacing = 40
        btn_w = 120
        start_x = SCREEN_WIDTH // 2 - (4 * btn_w + 3 * btn_spacing) // 2
        
        btns = [
            ('shop', "商店", start_x),
            ('breakthrough', "突破", start_x + btn_w + btn_spacing),
            ('equipment', "装备", start_x + 2 * (btn_w + btn_spacing)),
            ('handbook', "图鉴", start_x + 3 * (btn_w + btn_spacing))
        ]
        
        self.buttons = []
        for name, label, x in btns:
            btn_rect = (x, nav_y + 10, btn_w, 40)
            # 按钮样式
            pygame.draw.rect(self.screen, (160, 120, 80), btn_rect, 2)
            self.draw_text(label, self.font, (50, 40, 30), x + btn_w//2, nav_y + 30, center=True)
            self.buttons.append((name, btn_rect))
        
        # 功法栏 - 右侧 (扩展显示所有已学功法)
        tech_x = SCREEN_WIDTH - 220
        tech_y = 15
        tech_h = 40 + len(self.player.techniques) * 45
        pygame.draw.rect(self.screen, (80, 60, 40), (tech_x, tech_y, 200, tech_h), 3) # 木质边框
        pygame.draw.rect(self.screen, (245, 235, 210), (tech_x+4, tech_y+4, 192, tech_h-8)) # 纸质背景
        
        self.draw_text("所学功法", self.font, (80, 40, 40), tech_x + 100, tech_y + 20, center=True)
        
        self.tech_buttons = []
        for i, tech_name in enumerate(self.player.techniques):
            tech = TECHNIQUES[tech_name]
            # 计算冷却百分比 (对于所有技能，不仅仅是装备的)
            cd_pct = self.player.get_skill_cooldown_pct(TECHNIQUES, tech_name)
            
            # 绘制技能图标 (小方块)
            icon_rect = (tech_x + 15, tech_y + 45 + i * 40, 30, 30)
            pygame.draw.rect(self.screen, tech["color"], icon_rect)
            pygame.draw.rect(self.screen, INK_BLACK, icon_rect, 2)
            
            # 显示技能名称和冷却指示
            text_color = INK_BLACK if cd_pct >= 1.0 else GRAY
            self.draw_text(tech_name, self.small_font, text_color, tech_x + 60, tech_y + 60 + i * 40)
            
            self.tech_buttons.append((tech_name, icon_rect))
            
            # 冷却条
            if cd_pct < 1.0:
                pygame.draw.rect(self.screen, (200, 200, 200), (tech_x + 60, tech_y + 70 + i * 40, 100, 4))
                pygame.draw.rect(self.screen, tech["color"], (tech_x + 60, tech_y + 70 + i * 40, int(100 * cd_pct), 4))
        
        # 悬停显示技能详情
        mouse_pos = pygame.mouse.get_pos()
        for tech_name, btn in self.tech_buttons:
            if btn[0] < mouse_pos[0] < btn[0] + btn[2] and btn[1] < mouse_pos[1] < btn[1] + btn[3]:
                self.draw_skill_tooltip(tech_name, mouse_pos)
                break
        
        # 底部提示
        self.draw_text("点击地面移动 · 点击怪物攻击 · 点击按钮操作", self.small_font, INK_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 100, center=True)
        
        # 消息 (水墨风格 - 移至中间顶部)
        if self.message_timer > 0:
            pygame.draw.rect(self.screen, INK_BLACK, (SCREEN_WIDTH//2 - 200, 50, 400, 40), 2)
            pygame.draw.rect(self.screen, PAPER, (SCREEN_WIDTH//2 - 198, 52, 396, 36))
            self.draw_text(self.message, self.font, RED, SCREEN_WIDTH//2, 70, center=True)
    
    def draw_shop(self):
        self.screen.fill(PAPER)
        # 边框装饰
        pygame.draw.rect(self.screen, INK_BLACK, (10, 10, SCREEN_WIDTH-20, SCREEN_HEIGHT-20), 3)
        
        self.draw_text("商店", self.title_font, RED, SCREEN_WIDTH//2, 60, center=True)
        self.draw_text(f"灵石: {self.player.gold}", self.font, ORANGE, SCREEN_WIDTH//2, 130, center=True)
        
        y = 190
        shop_item_btns = []
        for i, (type_, item) in enumerate(self.shop_items[:6]):
            if type_ == "tech":
                tech = TECHNIQUES.get(item, {})
                cost = tech.get("cost", 50) * 20  # 默认50
                color = tech.get("color", GOLD)
                desc = tech.get("desc", "")
                text = f"{item} - {cost}灵石"
            elif type_ == "weapon":
                color = QUALITY_COLORS.get(item["quality"], INK_BLACK)
                text = f"{item['name']}(+{item['attack']}) - {item['cost']}灵石"
            elif type_ == "armor":
                color = QUALITY_COLORS.get(item["quality"], INK_BLACK)
                text = f"{item['name']}(+{item['defense']}) - {item['cost']}灵石"
            
            # 物品按钮
            item_btn = (SCREEN_WIDTH//2 - 160, y, 320, 45)
            pygame.draw.rect(self.screen, color, item_btn, 2)
            pygame.draw.rect(self.screen, (250, 245, 230), (item_btn[0]+2, item_btn[1]+2, item_btn[2]-4, item_btn[3]-4))
            self.draw_text(text, self.font, color, SCREEN_WIDTH//2, y + 22, center=True)
            shop_item_btns.append((i, item_btn))
            y += 55
        
        # 返回按钮
        back_btn = (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 80, 120, 45)
        pygame.draw.rect(self.screen, INK_BLACK, back_btn, 2)
        pygame.draw.rect(self.screen, (245, 240, 225), (back_btn[0]+2, back_btn[1]+2, back_btn[2]-4, back_btn[3]-4))
        self.draw_text("返回", self.font, INK_BLACK, SCREEN_WIDTH//2, SCREEN_HEIGHT - 57, center=True)
        
        self.shop_buttons = shop_item_btns + [('back', back_btn)]
    
    def draw_breakthrough(self):
        self.screen.fill(PAPER)
        pygame.draw.rect(self.screen, INK_BLACK, (10, 10, SCREEN_WIDTH-20, SCREEN_HEIGHT-20), 3)
        
        self.draw_text("突破", self.title_font, RED, SCREEN_WIDTH//2, 80, center=True)
        
        cur = self.player.realm_name
        next_r = REALMS[self.player.realm + 1][0] if self.player.realm < len(REALMS) - 1 else "已飞升"
        
        self.draw_text(f"当前境界: {cur} {self.player.level}层", self.font, INK_BLACK, SCREEN_WIDTH//2, 180, center=True)
        self.draw_text(f"↓", self.font, RED, SCREEN_WIDTH//2, 230, center=True)
        self.draw_text(f"突破: {next_r}", self.font, CYAN, SCREEN_WIDTH//2, 280, center=True)
        
        if self.player.can_breakthrough():
            self.draw_text("达到10层 自动突破", self.font, GREEN, SCREEN_WIDTH//2, 380, center=True)
        else:
            self.draw_text("修炼至10层可突破", self.font, GRAY, SCREEN_WIDTH//2, 380, center=True)
        
        self.draw_text("B返回", self.font, INK_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, center=True)
    
    def draw_equipment(self):
        self.screen.fill(PAPER)
        pygame.draw.rect(self.screen, INK_BLACK, (10, 10, SCREEN_WIDTH-20, SCREEN_HEIGHT-20), 3)
        
        self.draw_text("装备", self.title_font, RED, SCREEN_WIDTH//2, 80, center=True)
        
        w = self.player.weapon
        if w:
            c = QUALITY_COLORS.get(w["quality"], INK_BLACK)
            self.draw_text(f"武器: {w['name']} +{w['attack']}", self.font, c, SCREEN_WIDTH//2, 200, center=True)
        else:
            self.draw_text("武器: 无", self.font, GRAY, SCREEN_WIDTH//2, 200, center=True)
        
        a = self.player.armor
        if a:
            c = QUALITY_COLORS.get(a["quality"], INK_BLACK)
            self.draw_text(f"防具: {a['name']} +{a['defense']}", self.font, c, SCREEN_WIDTH//2, 280, center=True)
        else:
            self.draw_text("防具: 无", self.font, GRAY, SCREEN_WIDTH//2, 280, center=True)
        
        self.draw_text("E 或 B 返回", self.font, INK_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, center=True)

    def draw_handbook(self):
        self.screen.fill(PAPER)
        pygame.draw.rect(self.screen, INK_BLACK, (10, 10, SCREEN_WIDTH-20, SCREEN_HEIGHT-20), 3)
        
        self.draw_text("技能图鉴", self.title_font, RED, SCREEN_WIDTH//2, 50, center=True)
        
        # Tabs
        tabs = ["金", "木", "水", "火", "土", "无"]
        for i, tab in enumerate(tabs):
            rect = (100 + i * 150, 120, 140, 40)
            color = (180, 160, 120) if self.handbook_tab == tab else (220, 220, 220)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, INK_BLACK, rect, 2)
            self.draw_text(tab, self.font, INK_BLACK, rect[0] + 70, rect[1] + 20, center=True)
            
        # Get skills for current tab
        skills = []
        for name, tech in TECHNIQUES.items():
            if tech.get("element", "无") == self.handbook_tab:
                skills.append((name, tech))
        
        # Display skills with scrolling (using pages of 12 skills)
        page_size = 12
        num_pages = (len(skills) + page_size - 1) // page_size
        self.handbook_page = max(0, min(self.handbook_page, num_pages - 1))
        
        start_idx = self.handbook_page * page_size
        end_idx = min(start_idx + page_size, len(skills))
        
        y = 200
        for i in range(start_idx, end_idx):
            name, tech = skills[i]
            info = f"{name} | {tech.get('type', '未知')} | Dmg:{tech.get('damage', 0)} | CD:{tech.get('cooldown', 0)/1000:.1f}s"
            self.draw_text(info, self.font, INK_BLACK, 150, y)
            self.draw_text(tech.get("desc", ""), self.small_font, GRAY, 700, y)
            y += 40
            
        # Draw navigation buttons
        prev_btn = (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 110, 100, 40)
        next_btn = (SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 110, 100, 40)
        
        pygame.draw.rect(self.screen, (220, 220, 220), prev_btn)
        pygame.draw.rect(self.screen, (220, 220, 220), next_btn)
        pygame.draw.rect(self.screen, INK_BLACK, prev_btn, 2)
        pygame.draw.rect(self.screen, INK_BLACK, next_btn, 2)
        self.draw_text("上一页", self.small_font, INK_BLACK, prev_btn[0]+50, prev_btn[1]+20, center=True)
        self.draw_text("下一页", self.small_font, INK_BLACK, next_btn[0]+50, next_btn[1]+20, center=True)
            
        self.draw_text(f"第 {self.handbook_page + 1} / {max(1, num_pages)} 页", self.small_font, INK_GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 70, center=True)
        
        # 返回按钮
        back_btn = (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 60, 120, 40)
        pygame.draw.rect(self.screen, (220, 220, 220), back_btn)
        pygame.draw.rect(self.screen, INK_BLACK, back_btn, 2)
        self.draw_text("返回 (B)", self.font, INK_BLACK, back_btn[0]+60, back_btn[1]+20, center=True)

    def save_game(self):
        data = {
            "player": self.player.to_dict(),
            "map_seed": self.map_seed,
            "game_time": self.game_time,
            "state": "game"
        }
        with open("data/save.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        self.show_message("游戏已保存")
        self.state = "game"

    def load_game(self):
        try:
            with open("data/save.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Reconstruct player
            p_data = data["player"]
            self.player = Player(p_data["char_key"], CHARACTERS[p_data["char_key"]], REALMS, ELEMENTS)
            # Apply saved stats
            for k, v in p_data.items():
                if hasattr(self.player, k):
                    setattr(self.player, k, v)
            
            self.map_seed = data["map_seed"]
            self.game_time = data["game_time"]
            self.state = "game"
            self.show_message("游戏已读取")
        except FileNotFoundError:
            self.show_message("无存档文件")
    
    def draw_esc_menu(self):
        self.screen.fill(PAPER)
        pygame.draw.rect(self.screen, INK_BLACK, (10, 10, SCREEN_WIDTH-20, SCREEN_HEIGHT-20), 3)
        self.draw_text("游戏菜单", self.title_font, RED, SCREEN_WIDTH//2, 100, center=True)
        
        btns = [("resume", "继续游戏"), ("save", "保存游戏"), ("load", "读取游戏"), ("menu", "回到主界面")]
        self.esc_buttons = []
        for i, (name, label) in enumerate(btns):
            rect = (SCREEN_WIDTH//2 - 100, 250 + i * 80, 200, 50)
            pygame.draw.rect(self.screen, INK_BLACK, rect, 2)
            self.draw_text(label, self.font, INK_BLACK, SCREEN_WIDTH//2, 275 + i * 80, center=True)
            self.esc_buttons.append((name, rect))
    
    def run(self):
        running = True
        while running:
            self.handle_input()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT + 1:
                    if self.player: self.player.state = "Idle"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.state == "dead":
                        self.start_game()
                    else:
                        self.handle_key(event.key)
            
            self.update()
            
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "char_selection":
                self.draw_char_selection()
            elif self.state == "game":
                self.draw_game()
            elif self.state == "shop":
                self.draw_shop()
            elif self.state == "breakthrough":
                self.draw_breakthrough()
            elif self.state == "equipment":
                self.draw_equipment()
            elif self.state == "handbook":
                self.draw_handbook()
            elif self.state == "reward_selection":
                self.draw_reward_selection()
            elif self.state == "confirm":
                self.draw_confirm()
            elif self.state == "esc_menu":
                self.draw_esc_menu()
            elif self.state == "dead":
                self.draw_dead()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()