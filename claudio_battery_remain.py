#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-05-31 14:38:17
# Code:
'''
查看电池剩余情况
'''

import sys
from pathlib import Path


def main():
    '主函数'
    config_file_path = Path('/sys/class/power_supply/BAT1')  # 配置文件路径

    if not config_file_path.exists():
        sys.exit('没有电池')

    charge_full = float(config_file_path.joinpath('charge_full').read_text())
    charge_now = float(config_file_path.joinpath('charge_now').read_text())

    return charge_now / charge_full


if __name__ == '__main__':
    print('电池剩余：{:.2%}'.format(main()))
    sys.exit()
