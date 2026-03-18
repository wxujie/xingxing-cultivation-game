# -*- coding: utf-8 -*-
"""
解析雪碧图并提取帧
剑痴·厉沧海动画帧
使用PIL替代pygame避免显示依赖
"""

import sys
import os
from PIL import Image

# 雪碧图路径
spritesheet_path = "data/jin_spritesheet.png"

# 获取雪碧图
try:
    spritesheet = Image.open(spritesheet_path)
    width, height = spritesheet.size
    print(f"✓ 雪碧图加载成功: {width}x{height}")
except Exception as e:
    print(f"✗ 加载雪碧图失败: {e}")
    sys.exit(1)

# 帧配置
frames_per_state = {
    "Idle": 4,
    "Walking": 6,
    "Attacking": 4,
    "Casting": 4
}

# 雪碧图布局: 4x4 网格
# 行：从上到下分别是 Idle, Walking, Attacking, Casting
# 列：从左到右按顺序排列
rows = 4
cols = 4
frame_size = 256

# 创建输出目录
output_dir = "data/jin_frames"
os.makedirs(output_dir, exist_ok=True)

print(f"\n开始提取帧...")
print(f"输出目录: {output_dir}")

# 提取每一帧
for row_idx, state in enumerate(["Idle", "Walking", "Attacking", "Casting"]):
    print(f"\n提取 {state} 帧...")

    for col_idx in range(frames_per_state[state]):
        # 计算源区域
        x = col_idx * frame_size
        y = row_idx * frame_size

        # 提取帧
        frame = spritesheet.crop((x, y, x + frame_size, y + frame_size))

        # 保存帧
        filename = os.path.join(output_dir, f"{state}_{col_idx}.png")
        frame.save(filename)
        print(f"  保存: {filename}")

# 生成配置文件
config_path = os.path.join(output_dir, "config.json")
config = {
    "name": "剑痴·厉沧海",
    "frames_per_state": frames_per_state,
    "frame_size": frame_size,
    "spritesheet": spritesheet_path,
    "output_dir": output_dir
}

import json
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f"\n✓ 配置文件生成: {config_path}")
print(f"\n所有帧已提取完成！")
print(f"你可以使用这些帧来替代现有的水墨风格角色动画。")
