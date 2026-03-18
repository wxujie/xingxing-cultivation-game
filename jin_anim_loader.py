# -*- coding: utf-8 -*-
"""
剑痴·厉沧海动画加载器
使用雪碧图帧替代水墨风格角色动画
"""

import pygame
import os
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = str(Path(__file__).parent)

class JinAnimationLoader:
    """剑痴·厉沧海动画加载器"""

    def __init__(self):
        self.frames = {
            "Idle": [],
            "Walking": [],
            "Attacking": [],
            "Casting": []
        }
        self.load_frames()

    def load_frames(self):
        """加载所有动画帧"""
        output_dir = os.path.join(SCRIPT_DIR, "data", "jin_frames")

        for state in self.frames:
            count = {
                "Idle": 4,
                "Walking": 4,
                "Attacking": 4,
                "Casting": 4
            }[state]

            print(f"加载 {state} 帧...")

            for i in range(count):
                filename = os.path.join(output_dir, f"{state}_{i}.png")
                try:
                    frame = pygame.image.load(filename).convert_alpha()
                    # 默认素材朝向与游戏相反，翻转之
                    frame = pygame.transform.flip(frame, True, False)
                    # 缩小30% (即设为原来的70%)
                    w, h = frame.get_size()
                    frame = pygame.transform.scale(frame, (int(w * 0.7), int(h * 0.7)))
                    self.frames[state].append(frame)
                    print(f"  ✓ {filename}")
                except Exception as e:
                    print(f"  ✗ 加载失败: {e}")

    def get_frame(self, state, frame_idx):
        """获取指定帧"""
        if state not in self.frames:
            return None
        frames = self.frames[state]
        if frame_idx >= len(frames):
            return frames[0] if frames else None
        return frames[frame_idx]

    def get_state_frames(self, state):
        """获取状态的所有帧"""
        return self.frames.get(state, [])


# 测试代码（如果单独运行）
if __name__ == "__main__":
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("剑痴·厉沧海动画测试")
    clock = pygame.time.Clock()

    # 加载动画
    jin_loader = JinAnimationLoader()

    print("\n✓ 动画加载完成！")
    print(f"  - Idle:    {len(jin_loader.frames['Idle'])} 帧")
    print(f"  - Walking: {len(jin_loader.frames['Walking'])} 帧")
    print(f"  - Attacking: {len(jin_loader.frames['Attacking'])} 帧")
    print(f"  - Casting: {len(jin_loader.frames['Casting'])} 帧")

    # 演示动画
    frame_count = 0
    state = "Idle"
    running = True

    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = "Walking"
                elif event.key == pygame.K_1:
                    state = "Attacking"
                elif event.key == pygame.K_2:
                    state = "Casting"
                elif event.key == pygame.K_0:
                    state = "Idle"

        # 更新动画
        frame_idx = frame_count // 10 % len(jin_loader.frames[state])
        frame = jin_loader.get_frame(state, frame_idx)

        # 绘制
        screen.fill((240, 235, 225))  # 宣纸背景
        if frame:
            screen.blit(frame, (300, 150))

        # 绘制提示文字
        font = pygame.font.SysFont("simhei", 24)
        text = f"状态: {state} | 帧: {frame_idx + 1}/{len(jin_loader.frames[state])}"
        screen.blit(font.render(text, True, (50, 50, 60)), (250, 400))

        hint = "按空格键: 移动 | 1: 攻击 | 2: 施法 | 0: 待机"
        screen.blit(font.render(hint, True, (100, 100, 120)), (150, 450))

        pygame.display.flip()
        clock.tick(60)

        frame_count += 1

    pygame.quit()
