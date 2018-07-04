# MXCleanXcode
Xcode清理工具
## 工作
* **(清理操作不可逆，请谨慎)**
* 清理冗余数据
* 清理多余模拟器

## 清理目录
* */Library/Developer/Xcode/Archives*
* */Library/Developer/Xcode/DerivedData*
* */Library/Developer/Xcode/Products*
* */Library/Developer/CoreSimulator/Devices*

## 包
```
import os
import plistlib as pl
import shutil
```
## 使用
```
git clone git@github.com:iamhmx/MXCleanXcode.git
cd MXCleanXcode
python cleanxcode.py
```
## 效果
![](https://github.com/iamhmx/MXCleanXcode/blob/master/screenshots/1.png?raw=true)

## 引用
[Xcode清理说明](http://www.th7.cn/system/mac/201610/184480.shtml)
## 
