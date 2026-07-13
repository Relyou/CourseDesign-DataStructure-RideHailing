from view import RealtimeHeatmap
from events import EventGenerator
import config as cfg
import time
import matplotlib.pyplot as plt
import numpy as np
def main():
    
    # 创建城市抽象表格
    order_car_situation = [[0 for i in range(10)] for j in range(10)]
    # 创建事件生成器
    events = EventGenerator()
    
    # 初始条件，先加入100个司机
    events.create_car_bash(100)
    events.create_order_bash(30)
    # ===模拟伦次===
    test_num = cfg.SUM_TEST_NUM
    
    while(test_num >= 1):
        test_num -= 1
        # 添加司机，模拟送客完成后回归的以及刚上班的司机
        events.create_car_bash(cfg.CAR_TEST_NUM)
        # 添加订单，模拟接受派单
        events.create_order_bash(cfg.ORDER_TEST_NUM)
        # 对前十个订单进行分配
        events.dispatcher.dispatch_order_bash(10)

        time.sleep(1) # 模拟运行中的暂停，防止热力图变化太快

    events.dispatcher.heatmap.close()
        
if __name__ == "__main__":
    main()
    