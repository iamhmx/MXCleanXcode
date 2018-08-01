# coding=utf-8

import os
import plistlib as pl
import shutil

# Mac瘦身：http://www.th7.cn/system/mac/201610/184480.shtml

archives_path = '%s/Library/Developer/Xcode/Archives' % os.environ['HOME']
derivedData_path = '%s/Library/Developer/Xcode/DerivedData' % os.environ['HOME']
products_path = '%s/Library/Developer/Xcode/Products' % os.environ['HOME']

simulator_path = '%s/Library/Developer/CoreSimulator/Devices' % os.environ['HOME']
device_set_plist_path = '%s/Library/Developer/CoreSimulator/Devices/device_set.plist' % os.environ['HOME']

device_plist_name = 'device.plist'


class Simulator(object):
    """模拟器对象"""
    def __init__(self, path, udid, devicetype, name, runtime):
        self.path = path
        self.udid = udid
        self.devicetype = devicetype
        self.name = name
        self.runtime = runtime

    def print_simulator(self):
        print('\nPath:%s\nUDID:%s\nDeviceType:%s\nName:%s\nRuntime:%s\n' %
              (self.path, self.udid, self.devicetype, self.name, self.runtime))


def size_of_folder(path):
    """文件目录大小"""
    size = 0.0
    for (root, dirs, files) in os.walk(path):
        for name in files:
            try:
                size += os.path.getsize(os.path.join(root, name))
            except BaseException as e:
                print('统计异常：%s' % e)
                continue
    # 返回MB
    return size / (1024**2)


def delete_folder(path):
    """删除"""
    file_list = os.listdir(path)
    for f in file_list:
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print('%s 文件已删除！' % file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path, True)
            print('%s 目录已删除！' % file_path)


def find_all_simulator(path):
    """查找所有模拟器文件"""
    folders = os.listdir(path)
    return [f for f in folders if '-' in f]


# 读取plist
def read_device_plist():
    with open(device_set_plist_path, 'rb') as fp:
        set_plist = pl.load(fp)
    return set_plist


def clean_garbage():
    """清理垃圾"""
    size = 0.0
    paths = [archives_path, derivedData_path, products_path]
    print('要清理的目录：')
    for path in paths:
        print(path)
        size += size_of_folder(path)
        delete_folder(path)
    if size / 1024 > 1:
        print('大小：%.2f GB' % (size / 1024))
    else:
        print('大小：%.2f MB' % size)


def clean_simulator():
    """清理模拟器"""
    simulator_folders = find_all_simulator(simulator_path)
    device_array = []
    for f in simulator_folders:
        # 模拟器文件目录
        file_path = os.path.join(simulator_path, f)
        # 模拟器文件中plist文件路径
        plist_path = os.path.join(file_path, device_plist_name)
        # 读取plist
        # plist = pl.readPlist(plist_path)
        with open(plist_path, 'rb') as fp:
            plist = pl.load(fp)
        device_udid = plist.get('UDID')
        device_devicetype = plist.get('deviceType')
        device_name = plist.get('name')
        device_runtime = plist.get('runtime')
        # 存放模拟器对象
        s = Simulator(file_path, device_udid, device_devicetype, device_name, device_runtime)
        # s.print_simulator()
        device_array.append(s)
    print('包含的所有模拟器：')
    for d in [s.name for s in device_array]:
        print(d)

    target_path = {}
    deleted_device = []

    need_device = input('\n请输入您需要保留的模拟器设备名称，以逗号,分隔：\n')
    device = need_device.split(',')

    size = 0.0

    for s in device_array:
        if s.name not in device:
            size += size_of_folder(s.path)
            # 要删除的模拟器，key为路径用于删除，value为名称用于显示
            target_path[s.path] = s.name
            deleted_device.append(s)

    if len(target_path) > 0:
        res = input('是否要删除%s模拟器(共：%.2f MB)？（y/n）\n' % (list(target_path.values()), size))
        if res.lower() == 'y':
            for folder_path in target_path.keys():
                shutil.rmtree(folder_path)
                # TODO 清理device.plist
    else:
        print('未找到需要删除的模拟器')


def clean_xcode():
    clean_garbage()
    go_on = input('是否继续清理模拟器？（yes/no）\n')
    if go_on.lower() == 'yes':
        clean_simulator()
    else:
        print('程序结束，欢迎下次再来~')
    # read_device_plist()


if __name__ == '__main__':
    clean_xcode()

