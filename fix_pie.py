#!/usr/bin/env python3
"""主仓库构建辅助（幂等）：
  1. 用 libs/libnx-fix/ 下维护的副本覆盖 $(DEVKITPRO)/libnx 的 switch.specs / switch.ld
     （新版 gcc 15+ 下 libnx 原 specs 的 PIE 选项会生成 entry=0 的损坏 ELF）
  2. 临时替换 chesto 子模块工作区 Makefile 的 ARCH 行，去掉 -fPIE（不提交子模块改动）
"""
import os
import shutil

root = os.path.dirname(os.path.abspath(__file__))
dkp = os.environ.get('DEVKITPRO', '/opt/devkitpro')

# 1. libnx 构建文件：主仓库副本覆盖安装目录
fix_dir = os.path.join(root, 'libs', 'libnx-fix')
for name in ('switch.specs', 'switch.ld'):
    src = os.path.join(fix_dir, name)
    dst = os.path.join(dkp, 'libnx', name)
    if os.path.isfile(src):
        shutil.copyfile(src, dst)

# 2. chesto switch Makefile（子模块工作区，临时）：ARCH 行去 -fPIE
chesto_mf = os.path.join(root, 'libs', 'chesto', 'helpers', 'Makefile.switch')
if os.path.isfile(chesto_mf):
    with open(chesto_mf) as f:
        content = f.read()
    fixed = content.replace('-mtune=cortex-a57 -fPIE', '-mtune=cortex-a57')
    if fixed != content:
        with open(chesto_mf, 'w') as f:
            f.write(fixed)
