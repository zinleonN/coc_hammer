import pygetwindow as gw

# 获取所有打开的窗口
windows = gw.getWindowsWithTitle('部落冲突')

if windows:
    window = windows[0]
    window.activate()  # 切换到该窗口
else:
    print("窗口未找到")
