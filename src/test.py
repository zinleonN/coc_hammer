import logging
import asyncio
import time
import pyautogui as pa
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from common.image_utils import ImageLocator
from common.mouse_utils import MouseUtils
from tasks.attack import AttackManager
from tasks.donate import DonationManager

# 设置日志
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 创建文件处理器
    log_file = Path(__file__).parent / 'app.log'
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    logging.info("Logging setup complete")

# 测试图像定位功能
def test_image_locator():
    logging.info("\n" + "="*50)
    logging.info("测试图像定位功能")
    logging.info("="*50)
    
    locator = ImageLocator()
    
    # 测试图像路径获取
    test_images = ["attack_1", "donate_start", "nonexistent_image"]
    for img in test_images:
        path = locator.image_path(img)
        logging.info(f"图像 '{img}' 的路径: {path}")
    
    # 测试图像定位
    test_cases = [
        ("基本定位", ["attack_1", "attack_2"], False),
        ("颜色敏感定位", ["donate_army_giant"], True),
        ("多图像测试", ["attack_1", "donate_start"], False),
        ("不存在的图像", ["nonexistent_image"], False)
    ]
    
    for name, images, color_sensitive in test_cases:
        logging.info(f"\n测试: {name}")
        location = locator.locate_images(*images, color_sensitive=color_sensitive)
        if location:
            logging.info(f"找到图像: {images} 位置: {location}")
        else:
            logging.info(f"未找到图像: {images}")
    
    logging.info("图像定位测试完成\n")

# 测试鼠标功能
def test_mouse_utils():
    logging.info("\n" + "="*50)
    logging.info("测试鼠标功能")
    logging.info("="*50)
    
    # 测试坐标转换
    test_points = [(0.5, 0.5), (0.25, 0.75), (0.8, 0.2)]
    for point in test_points:
        actual = MouseUtils.radio_to_actual(*point)
        logging.info(f"相对坐标 {point} -> 实际坐标 {actual}")
    
    # 测试移动功能
    logging.info("\n测试基本移动")
    start_pos = pa.position()
    target_pos = MouseUtils.radio_to_actual(0.5, 0.5)
    MouseUtils.move(target_pos)
    end_pos = pa.position()
    logging.info(f"从 {start_pos} 移动到 {end_pos}")
    
    # 测试曲线移动
    logging.info("\n测试曲线移动")
    start_pos = pa.position()
    target_pos = MouseUtils.radio_to_actual(0.7, 0.3)
    MouseUtils.move(target_pos)
    end_pos = pa.position()
    logging.info(f"从 {start_pos} 曲线移动到 {end_pos}")
    
    # 测试点击图像功能
    logging.info("\n测试图像点击功能")
    click_results = MouseUtils.click_image("attack_1", "attack_2")
    logging.info(f"点击攻击按钮结果: {'成功' if click_results else '失败'}")
    
    # 测试拖拽功能
    logging.info("\n测试拖拽功能")
    start_point = (0.3, 0.3)
    end_point = (0.7, 0.7)
    MouseUtils.move_from_to(start_point, end_point)
    logging.info(f"从 {start_point} 拖拽到 {end_point}")
    
    logging.info("鼠标功能测试完成\n")

# 测试攻击功能
def test_attack_manager():
    logging.info("\n" + "="*50)
    logging.info("测试攻击管理器")
    logging.info("="*50)
    
    manager = AttackManager()
    
    # 测试选择攻击目标（模拟）
    logging.info("测试选择攻击目标（模拟）")
    async def mock_choose_target():
        logging.info("模拟检测最佳方向...")
        await asyncio.sleep(1)  # 模拟异步操作
        return MouseUtils.move_to_left_up, [(500, 300), (600, 400)]
    
    # 替换实际方法
    manager.choose_suitable_attack_target = mock_choose_target
    
    # 测试放置军队
    logging.info("测试放置军队")
    manager.place_armies(MouseUtils.move_to_left_up, [(500, 300), (600, 400)])
    
    # 测试放置英雄
    logging.info("测试放置英雄")
    manager.place_heroes([(500, 300), (600, 400)])
    
    # 测试完整攻击流程（模拟）
    logging.info("测试完整攻击流程（模拟）")
    original_execute = manager.execute_attack
    def mock_execute_attack():
        logging.info("模拟攻击流程...")
        logging.info("点击攻击按钮")
        logging.info("点击搜索按钮")
        logging.info("选择目标")
        logging.info("放置军队和英雄")
        logging.info("等待攻击完成...")
        time.sleep(2)
        logging.info("点击返回按钮")
        return True
    
    manager.execute_attack = mock_execute_attack
    attack_result = manager.execute_attack()
    logging.info(f"攻击结果: {'成功' if attack_result else '失败'}")
    
    # 恢复原始方法
    manager.execute_attack = original_execute
    
    logging.info("攻击管理器测试完成\n")

# 测试捐赠功能
def test_donation_manager():
    logging.info("\n" + "="*50)
    logging.info("测试捐赠管理器")
    logging.info("="*50)
    
    manager = DonationManager()
    
    # 测试随机捐赠
    logging.info("测试随机捐赠")
    manager.random_donate()
    
    # 测试完整捐赠流程（模拟）
    logging.info("测试完整捐赠流程（模拟）")
    original_process = manager.process_donation
    def mock_process_donation():
        logging.info("模拟捐赠流程...")
        logging.info("点击捐赠开始按钮")
        logging.info("找到捐赠请求")
        logging.info("执行随机捐赠")
        logging.info("点击返回按钮")
        return True
    
    manager.process_donation = mock_process_donation
    donation_result = manager.process_donation()
    logging.info(f"捐赠结果: {'需要资源' if donation_result else '不需要资源'}")
    
    # 恢复原始方法
    manager.process_donation = original_process
    
    logging.info("捐赠管理器测试完成\n")

# 测试方向检测功能
async def test_direction_detection():
    logging.info("\n" + "="*50)
    logging.info("测试方向检测功能")
    logging.info("="*50)
    
    logging.info("开始检测最佳方向...")
    move_func, projected_points = await MouseUtils.detect_best_direction()
    
    if move_func:
        logging.info(f"最佳移动函数: {move_func.__name__}")
        logging.info(f"投影点数量: {len(projected_points)}")
        if projected_points:
            logging.info(f"示例投影点: {projected_points[0]}")
    else:
        logging.info("未找到合适的方向")
    
    logging.info("方向检测测试完成\n")

# 主测试函数
def main():
    setup_logging()
    logging.info("开始测试重构后的代码")
    
    try:
        # 测试基础功能
        test_image_locator()
        test_mouse_utils()
        
        # 测试任务功能
        test_attack_manager()
        test_donation_manager()
        
        # 测试异步功能
        asyncio.run(test_direction_detection())
        
        logging.info("所有测试完成！")
    except Exception as e:
        logging.exception("测试过程中发生错误: ")
        print(f"测试失败: {e}")
    finally:
        # 确保鼠标回到安全位置
        MouseUtils.move(MouseUtils.radio_to_actual(0.1, 0.1))
        logging.info("鼠标已移动到安全位置")

if __name__ == "__main__":
    main()