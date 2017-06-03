#!/usr/bin/python3
# Author: Claudio <3261958605@qq.com>
# Created: 2017-05-31 18:28:17
# Code:
'''
音乐播放脚本
'''
import itertools
import os
import os.path
import re
import subprocess
import sys
import tempfile
import time

from claudio_color import colorful

MUSIC_FILE_RE_OBJ = re.compile(r'.*\.(mp3|mp4|ogg)$')  # 匹配音乐文件名
HAN_RE_OBJ = re.compile(r'[\u4e00-\u9fa5]')             # 匹配汉字

# 资源获取


def is_music_file(path_string):
    '根据PATH_STRING的后缀判断是否为音乐文件'
    if MUSIC_FILE_RE_OBJ.match(path_string):
        return True
    return False


def is_contains_music_file(dirpath):
    'DIRPATH文件夹中是否存在音乐文件'
    if not os.path.exists(dirpath):
        return False
    if not os.path.isdir(dirpath):
        return False
    for _root, _dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if is_music_file(filename):
                return True
    return False


def get_music_dirs(root_dir):
    '获取ROOT_DIR路径下所有含音乐文件的子文件夹。'
    music_dirs = []
    for root, dirnames, _filenames in os.walk(root_dir):
        for dirname in dirnames:
            path = os.path.join(root, dirname)
            # print(path)
            if is_contains_music_file(path):
                music_dirs.append(path)
    return sorted(music_dirs)


def get_music_files(music_dir):
    '获取MUSIC_DIR文件夹中所有音乐文件'
    musics = []
    for file in os.listdir(music_dir):
        if is_music_file(file):
            musics.append(file)
    return sorted(musics)

# 开始播放


def play_music(music_file, player='mplayer'):
    '播放单个音频文件。'
    print('q)下一曲')
    # os.system(cmd)
    with tempfile.TemporaryFile() as fp:
        subprocess.run([player, music_file], stdout=fp, stderr=fp)


def play_musics(music_dir, player='mplayer'):
    '播放MUSIC_DIR文件夹中的所有音乐文件'
    music_files = get_music_files(music_dir)
    for filename in music_files:
        print('正在播放：{}'.format(filename))
        play_music(os.path.join(music_dir, filename), player=player)


def display_music_dirs_and_get_dir(music_dirs):
    '''打印含音乐文件的文件夹
    由于汉字在命令行占两个英语字母位置，所以单独成函数处理。
    '''
    # 打印菜单
    os.system('clear')

    print(colorful('播放列表：', color='light-blue'))
    print('-' * 80)
    columns = 30                # 打印文件夹名时所占宽度。
    for i, dirname in zip(itertools.count(0), music_dirs):
        basename = os.path.basename(dirname)
        han_chrs = len(HAN_RE_OBJ.findall(basename))  # 汉字数量
        print('{:<2}) {:<{columns}}'.format(
            i, colorful(basename, color='green'), columns=columns - han_chrs), end='')
        if i % 3 == 2:
            print()

    print('\n\nq ) 退出')
    print('-' * 80)

    # 获取文件夹
    music_dir = input(colorful('请选择： ', color='blue'))

    # 如果为退出选项
    if music_dir.lower() == 'q':
        print('再见')
        sys.exit()

    # 如果不能转换为数字
    try:
        music_dir = int(music_dir)
        if music_dir < 0 or music_dir >= len(music_dirs):
            # print('{} 范围错误，请重新输入'.format(music_dir))
            raise ValueError('返回错误')
        else:
            return music_dir
    except ValueError:
        print('无效，请重新输入')
        time.sleep(1)
        return display_music_dirs_and_get_dir(music_dirs)


def play(root_dir, player='mplayer'):
    '显示提示，根据用户输入播放ROOT_DIR中所有子文件夹中的音乐文件。'
    music_dirs = get_music_dirs(root_dir)
    music_dir = display_music_dirs_and_get_dir(music_dirs)
    # print(music_dirs[music_dir])
    play_musics(music_dirs[music_dir])

    # 循环
    play(root_dir, player=player)


if __name__ == '__main__':
    root_music_dir = '/home/claudio/Music'
    # print(is_contains_music_file(root_music_dir))
    # print(get_music_dirs(root_music_dir))
    # print(play_musics(os.path.join(root_music_dir, 'U2/')))
    play(root_music_dir)
    # print(display_music_dirs_and_get_dir(get_music_dirs(root_music_dir)))
