import objects as obj
import config as cfg
import numpy as np
import time
from view import RealtimeHeatmap
from minheap import MinHeap

class DispatchEngine:
    def __init__(self, car_list, order_queue):
        # ==需要的变量==
        self.car_list = car_list # 司机列表
        self.order_queue = order_queue # 订单列表
        self.dispatch_success = 0 # 成功匹配次数
        self.dispatch_defeat = 0 # 失败匹配次数
        self.total_time_ms = 0 # 系统总撮合耗时
        self.round_num = 0 # 系统运行伦次
        self.scale = cfg.TANH_SACLE # tanh映射时的缩放因子
        
        # ==建立小根堆==
        self.min_heap = MinHeap()
        # 创建热力图窗口
        self.heatmap = RealtimeHeatmap()
    
    # ===生成热力图需要的参数，以当前区域车辆数-订单数为x值===
    def generate_heat_map(self):
        heat_map = [[0 for i in range(10)] for j in range(10)]
        for i in range(10):
            for j in range(10):
                heat_map[i][j] = np.tanh((self.car_list.cnt_car[i][j] - self.order_queue.cnt_order[i][j]) / self.scale)
        return heat_map
    
    # ===计算撮合函数===
    def get_score(self, order, car):
        return (order.pos_x - car.pos_x) ** 2 + (order.pos_y - car.pos_y) ** 2 - (car.rating ** 2) * cfg.COEF_JUDEG 
    
    # ===分配一个订单===
    def dispatch_order(self, order):
        print(f"正在匹配订单：{order.id}")
        start_time = time.time() # 查找开始时间
        
        # ==每个订单的小根堆独立，所以清空==
        self.min_heap.clear()
        
        # ==遍历九格==
        mid_x, mid_y = order.get_pos()
        for i in range(-1, 2, 1):
            # == x轴坐标边界条件判断==
            if mid_x + i < 0 or mid_x + i > 9:
                continue
            for j in range(-1, 2, 1):    
                # == y轴坐标边界条件判断==
                if mid_y + j < 0 or mid_y + j > 9:
                    continue
                # 获取目标格子链表首个司机
                one_car = self.car_list.data[mid_x + i][mid_y + j]
                while(one_car != None):
                    self.min_heap.push(self.get_score(order, one_car), one_car)
                    one_car = one_car.next
                    
        # ==非空则取堆顶==
        if self.min_heap.size != 0:
            # ==获取目标车辆==
            aim_car = self.min_heap.pop()[1]
            self.dispatch_success += 1
            
            # 从链表中取出司机
            self.car_list.remove_car(aim_car)
            aim_car.is_idle = False
            
            # ==添加成功日志，同时更新数据==
            log_msg=(f"[派单成功] 订单#{order.id} (位置：({order.pos_x}, {order.pos_y})) 已成功匹配司机#{aim_car.id}(评分：{aim_car.rating}，距离：{((order.pos_x - aim_car.pos_x) ** 2 + (order.pos_y - aim_car.pos_y) ** 2) ** 0.5:.1f})，耗时：{(time.time() - start_time) * 1000 : .1f}ms")
            self.total_time_ms += time.time() - start_time
            self.heatmap.add_log(log_msg)
            
            # ==弹出司机==
            self.min_heap.pop()
            return True
        else:
            self.dispatch_defeat += 1
            
            # ==添加失败日志，同时更新数据==
            log_msg = (f"[派单失败] 订单#{order.id} (位置：({order.pos_x}, {order.pos_y})) 未能够匹配司机，尝试次数:{order.dispatch_time}")
            self.heatmap.add_log(log_msg)
            
            return False
    
    # ====更新视图的都放着了====
    def update_heapmap_info(self):
        # ==更新热力图==
        self.heatmap.update_heatmap(self.generate_heat_map())
        
        # ==更新统计信息==
        self.heatmap.update_stats(
            queue_length=self.order_queue.total_order,
            success_count=self.dispatch_success,
            fail_count=self.dispatch_defeat,
            total_time_ms=self.total_time_ms,
            round_num=self.round_num
        )
        
        self.heatmap._update_log_text()
        
    # ====动态调度时用的距离====
    def get_distance_score(self, car, gx, gy):
        return abs(car.pos_x - gx * 100 - 50) + abs(car.pos_y - gy * 100 - 50)
        
    # ====动态调度====
    def dynamic_schedule(self):
        for gx in range(10):
            for gy in range(10):
                # ==第一部分：先判断该格子是否是热点区域==
                cnt_car = self.car_list.cnt_car[gx][gy] 
                cnt_order = self.order_queue.cnt_order[gx][gy]
                
                # ==显然车比订单多时就不用调度了==
                if cnt_car >= cnt_order:
                    continue
                
                # ==第二部分，建小根堆找那些车能调度==
                # ==每个订单的小根堆独立，所以清空==
                self.min_heap.clear()
                
                # ==遍历九格==
                mid_x, mid_y = gx, gy
                for i in range(-1, 2, 1):
                    # == x轴坐标边界条件判断==
                    if mid_x + i < 0 or mid_x + i > 9:
                        continue
                    for j in range(-1, 2, 1):    
                        # == y轴坐标边界条件判断==
                        if mid_y + j < 0 or mid_y + j > 9:
                            continue
                        
                        # ==这里比之前多了一点，如果对方格子车本来就不够，那就不要调配了==
                        if self.car_list.cnt_car[i][j] <= self.order_queue.cnt_order[i][j]:
                            continue
                        
                        # 获取目标格子链表首个司机
                        one_car = self.car_list.data[mid_x + i][mid_y + j]
                        while(one_car != None):
                            self.min_heap.push(self.get_distance_score(one_car, i, j), one_car)
                            one_car = one_car.next
                
                # ==第三部分：开始调度==
                # ==最多将该格子补满为止==
                max_move_car = cnt_order - cnt_car
                while(self.min_heap.empty() == False and max_move_car > 0):
                    one_car = self.min_heap.pop()[1]
                    
                    # ==检验是否能移动,车辆比订单小就不能移==
                    if self.car_list.cnt_car[i][j] <= self.order_queue.cnt_order[i][j]:
                        continue
                    
                    # ==能移，开始移动==
                    print(f"开始调度司机，id：{one_car.id},位置：({one_car.pos_x},{one_car.pos_y})")
                    self.car_list.remove_car(one_car)
                    one_car.pos_x = 100 * gx + 50
                    one_car.pos_y = 100 * gy + 50
                    self.car_list.add_car(one_car)
                    print(f"调度司机到达，id：{one_car.id},位置：({one_car.pos_x},{one_car.pos_y})")
                    
                    # ==完成移动，最大移动数量-1==
                    max_move_car -= 1
                    
        
    # ====订单分配过程====
    def dispatch_order_bash(self, count):
        one_order = self.order_queue.head_order
        # ==伦次+1==
        self.round_num += 1
        for i in range(count):
            # ==找完全部订单，直接返回==
            if one_order == None: # 订单派完就返回
                return 
            
            # ==订单寻找次数加一==
            one_order.dispatch_time += 1
            
            # ==尝试分配当前订单==
            if self.dispatch_order(one_order) == True:
                self.order_queue.del_order(one_order)
                one_order = one_order.next_order
            else:
                # ==不行就把寻找次数达到上限的订单去掉，排队尾去==
                if one_order.dispatch_time >= cfg.MAX_DISPATCH_TIME:
                # ==注意add_order会改变next_order,所以要存==
                    tem_order = one_order
                    one_order = one_order.next_order
                    self.order_queue.del_order(tem_order)
                    self.order_queue.add_order(tem_order)
                else:
                    one_order = one_order.next_order
            
            # ==更新视图相关数据==
            self.update_heapmap_info()
            
        # ==动态调度过程==
            if cfg.IS_OPEN_ORDER_BALANCE:
                self.dynamic_schedule()
            
        