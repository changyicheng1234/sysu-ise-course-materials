# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入并执行主脚本
from 移除学号重命名 import main

if __name__ == "__main__":
    main()
