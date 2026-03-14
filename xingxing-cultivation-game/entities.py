# -*- coding: utf-8 -*-
"""
实体类模块：处理玩家、敌人、粒子及动画对象
"""

import pygame
import random
import math

class Player:
    @property
    def realm_name(self):
        return self.realms_data[self.realm][0]

    def __init__(self, char_key, char_data, realms_data, elements_data):
        self.char_key = char_key # 保存 char_key
        self.realms_data = realms_data # 保存 realms_data
        self.name = char_data["name"]
        self.element = char_data["element"]
        self.realm = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next = realms_data[0][1]
        self.max_hp = char_data["base_hp"]
        self.hp = self.max_hp
        self.attack = char_data["base_attack"]
        self.defense = char_data["base_defense"]
        self.gold = 0
        self.x = 600
        self.y = 400
        
        # 五行加成
        self.element_bonus = elements_data[self.element]["bonus"]
        
        # 功法 - 初始3个
        self.techniques = char_data["skills"][:3]
        self.equipped_idx = 0
        self.skill_cooldowns = {}
        
        # 装备
        self.weapon = None
        self.armor = None
        
        # 动画
        self.anim_frame = 0

    def move(self, dx, dy, world_width, world_height):
        # 允许移动到世界边界
        self.x = max(60, min(world_width - 60, self.x + dx))
        self.y = max(60, min(world_height - 80, self.y + dy))

    def take_damage(self, dmg):
        actual = max(1, dmg - self.defense // 2)
        self.hp -= actual
        return actual

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def use_skill(self, techniques_data):
        if not self.techniques:
            return None
        skill_name = self.current_skill
        return self.use_skill_by_name(skill_name, techniques_data)

    def use_skill_by_name(self, skill_name, techniques_data):
        if not skill_name or skill_name not in techniques_data:
            return None
        now = pygame.time.get_ticks()
        last = self.skill_cooldowns.get(skill_name, 0)
        skill = techniques_data[skill_name]
        if now - last >= skill.get("cooldown", 0):
            self.skill_cooldowns[skill_name] = now
            return skill
        return None

    @property
    def current_skill(self):
        if self.techniques:
            return self.techniques[self.equipped_idx]
        return None

    def get_skill_cooldown_pct(self, techniques_data, skill_name=None):
        if not self.techniques:
            return 1.0
        if skill_name is None:
            skill_name = self.current_skill
        if not skill_name or skill_name not in techniques_data:
            return 1.0
        now = pygame.time.get_ticks()
        last = self.skill_cooldowns.get(skill_name, 0)
        skill = techniques_data[skill_name]
        cd = skill.get("cooldown", 500)
        elapsed = now - last
        return min(1.0, elapsed / cd)

    def add_exp(self, exp):
        self.exp += exp
        while self.exp >= self.exp_to_next and self.level < 10:
            self.level_up()
        
    def level_up(self):
        self.exp -= self.exp_to_next
        self.level += 1
        self.max_hp += 40
        self.hp = self.max_hp
        self.attack += 10
        self.defense += 5
        self.exp_to_next = int(self.exp_to_next * 1.3) # 降低增长曲线，升级更快
        
    def equip(self, item, slot):
        if slot == "weapon":
            if self.weapon:
                self.attack -= self.weapon["attack"]
            self.weapon = item
            self.attack += item["attack"]
        elif slot == "armor":
            if self.armor:
                self.defense -= self.armor["defense"]
            self.armor = item
            self.defense += item["defense"]

    def to_dict(self):
        return {
            "char_key": self.char_key,
            "realm": self.realm,
            "level": self.level,
            "exp": self.exp,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "gold": self.gold,
            "techniques": self.techniques,
            "equipped_idx": self.equipped_idx,
            "skill_cooldowns": self.skill_cooldowns,
            "weapon": self.weapon,
            "armor": self.armor
        }

    def can_breakthrough(self):
        return self.realm < len(self.realms_data) - 1 and self.level >= 10

    def breakthrough(self):
        if self.can_breakthrough():
            self.realm += 1
            self.level = 1
            self.exp = 0
            self.exp_to_next = int(self.exp_to_next * 2)
            self.max_hp = int(self.max_hp * 1.6)
            self.hp = self.max_hp
            self.attack = int(self.attack * 1.5)
            self.defense = int(self.defense * 1.5)
            return True
        return False

class Enemy:
    def __init__(self, realm, enemy_data_list):
        max_idx = min(realm + 4, len(enemy_data_list) - 1)
        base = random.choice(enemy_data_list[:max_idx+1])
        
        scale = 1 + realm * 0.5
        self.name = base["name"]
        self.max_hp = int(base["hp"] * scale)
        self.hp = self.max_hp
        self.damage = int(base["damage"] * scale)
        self.exp = int(base["exp"] * scale)
        self.gold = random.randint(10, 25) * (realm + 1)
        self.speed = base["speed"]
        self.color = base["color"]
        self.size = base["size"]
        self.element = base.get("element", "土")
        
        # Spawn random pos
        self.x = random.randint(60, 1140)
        self.y = random.randint(60, 700)
    
    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 50:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
    
    def take_damage(self, dmg):
        actual = max(1, dmg - 2)
        self.hp -= actual
        return actual
    
    def is_alive(self):
        return self.hp > 0

class Particle:
    """攻击特效粒子"""
    def __init__(self, x, y, color, speed, life):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-speed, speed)
        self.vy = random.uniform(-speed, speed)
        self.life = life
        self.max_life = life
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life > 0
    
    def draw(self, screen, font=None):
        alpha = self.life / self.max_life
        if alpha > 0.3:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
