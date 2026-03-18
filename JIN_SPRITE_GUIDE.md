# 剑痴·厉沧海动画集成指南

## 📁 文件结构

```
data/jin_frames/
├── Idle_0.png ~ Idle_3.png     (4帧 - 待机)
├── Walking_0.png ~ Walking_5.png  (6帧 - 移动)
├── Attacking_0.png ~ Attacking_3.png  (4帧 - 攻击)
├── Casting_0.png ~ Casting_3.png    (4帧 - 施法)
└── config.json                  (配置文件)
```

## 🎮 如何在游戏中使用

### 方法 1: 修改 entities.py

在 `entities.py` 中的 `Player` 类添加动画帧加载：

```python
import os
from jin_anim_loader import JinAnimationLoader

class Player:
    def __init__(self, char_key, char_data, realms_data, elements_data):
        # ... 现有初始化代码 ...

        # 剑痴·厉沧海专用动画
        if char_key == "金" and os.path.exists("data/jin_frames"):
            self.jin_anim = JinAnimationLoader()
            self.jin_active = True
        else:
            self.jin_active = False

        # 现有动画代码...
        self.anim_frame = 0
        self.state = "Idle"
```

### 方法 2: 修改 draw_player_model

替换 `draw_player_model` 方法：

```python
def draw_player_model(self, x, y):
    """绘制玩家角色模型 - 剑痴·厉沧海使用雪碧图动画"""

    # 剑痴·厉沧海使用雪碧图
    if hasattr(self, 'jin_active') and self.jin_active:
        jin_anim = self.jin_anim

        # 根据状态选择帧数
        frame_count = {
            "Idle": 4,
            "Walking": 6,
            "Attacking": 4,
            "Casting": 4
        }.get(self.state, 4)

        # 计算当前帧索引
        frame_idx = (self.anim_frame // 10) % frame_count

        # 获取帧并绘制
        frame = jin_anim.get_frame(self.state, frame_idx)
        if frame:
            # 面向处理
            if self.direction == -1:
                frame = pygame.transform.flip(frame, True, False)

            # 居中绘制
            self.screen.blit(frame, (x - 128, y - 256))

            # 帧计数
            if pygame.time.get_ticks() % 3 == 0:
                self.anim_frame += 1
            return

    # 其他角色使用水墨风格（原有代码）
    # ... 原有代码 ...
```

## 🎨 帧说明

| 状态 | 帧数 | 说明 |
|------|------|------|
| Idle (待机) | 4帧 | 角色静止呼吸动画 |
| Walking (移动) | 6帧 | 角色行走动画 |
| Attacking (攻击) | 4帧 | 攻击动作 |
| Casting (施法) | 4帧 | 释放功法动画 |

## 📊 帧布局

雪碧图网格（4×4）：
```
[0][1][2][3]  ← Idle (待机)
[4][5][6][7]  ← Walking (移动)
[8][9][10][11] ← Attacking (攻击)
[12][13][14][15] ← Casting (施法)
```

## 🚀 快速测试

运行测试程序：
```bash
python load_jin_anim.py
```

按 `空格键` 切换到移动动画，按 `1` 攻击，按 `2` 施法，按 `0` 待机。

## 📝 配置文件 (config.json)

```json
{
  "name": "剑痴·厉沧海",
  "frames_per_state": {
    "Idle": 4,
    "Walking": 6,
    "Attacking": 4,
    "Casting": 4
  },
  "frame_size": 256,
  "spritesheet": "data/jin_spritesheet.png",
  "output_dir": "data/jin_frames"
}
```

## 💡 使用建议

1. **帧率控制**: 当前设置每10ms切换一帧，速度适中
2. **面向处理**: 自动检测 `self.direction`（1=右，-1=左）并翻转
3. **状态切换**: 自动根据角色状态（Idle/Walking/Attacking/Casting）切换动画
4. **性能优化**: 雪碧图帧已预加载，运行时无额外开销

---

**创建时间**: 2026-03-18
**雪碧图**: 剑痴·厉沧海动画
**总帧数**: 18 帧
