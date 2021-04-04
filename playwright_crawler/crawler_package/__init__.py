# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
# https://unix.stackexchange.com/questions/164025/exclude-one-pattern-from-glob-match
# https://stackoverflow.com/questions/20638040/glob-exclude-pattern
from os.path import dirname, basename, isfile, join
import glob
from importlib import import_module


# 抓取所有非 __init__.py 的 py檔之絕對路徑
modules = glob.glob(join(dirname(__file__), "[!_]*.py"))
# 只取 module names
modules = [basename(f)[:-3] for f in modules]

# 取得套件名
pck_dir = basename(dirname(__file__))

# 把所有模組的物件及其名稱取出
objects = []
for f in modules:
    # 如果要用對路徑, package arg. 要定義
    m = import_module("%s." % pck_dir + f)
    for n in m.__objname__:
        objects.append([n, m.__dict__[n]])

# globals() 如果放在函式裡，回傳的名稱空間是定義的空間而不是呼叫的空間
# 把物件放進 package object 的名稱空間裡
globals().update(objects)

# debug
if __name__ == '__main__':
    print(modules)
    print(objects)
