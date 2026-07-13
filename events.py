import random
import numpy as np
import objects as obj
import config as cfg
from scipy.stats import truncnorm
from dispatcher import DispatchEngine
# ===模拟订单产生状况的变量=====
test_option = 0 


class EventGenerator:
    def __init__(self):
        # 订单相关变量
        self.order_queue = obj.OrderQueue()
        self.next_order_id = 1
        
        # 司机相关变量
        self.car_list = obj.CarList()
        self.next_driver_id = 1
        
        #订单分配机
        self.dispatcher = DispatchEngine(self.car_list, self.order_queue)
        
    def add_to_min_heap(self, car):
        gx, gy = car.get_pos()
        if gx > 0:
            self.order_queue.car_min_heap[gx - 1][gy].push(abs(car.pos_x - gx * 100 ), car)
        if gx < 9:
            self.order_queue.car_min_heap[gx + 1][gy].push(abs(car.pos_x - gx * 100 + 100) , car)
        if gy > 0:
            self.order_queue.car_min_heap[gx][gy - 1].push(abs(car.pos_y - gy * 100 ), car)
        if gy < 9:
            self.order_queue.car_min_heap[gx][gy + 1].push(abs(car.pos_y - gy * 100 + 100) , car)
        
    # ===创建一辆车===
    def create_car(self, pos_x = None, pos_y = None, rating = None):
        # ==无参数时，就是随机生成==
        if pos_x is None:
            pos_x = random.randint(10, 990)
        if pos_y is None:
            pos_y = random.randint(10, 990)
        if rating is None:
            rating = round(random.uniform(3.5, 5.0), 1)
            
        car = obj.Cars(pos_x, pos_y, self.next_driver_id, rating)
        self.next_driver_id += 1
        
        self.car_list.add_car(car)
        
        print(f"[生成车辆] 司机 #{car.id} 位置({car.pos_x},{car.pos_y}), 评分{car.rating}")
        
        # ==这个小根堆只在需要调度时有用==
        if cfg.IS_OPEN_ORDER_BALANCE:
            self.add_to_min_heap(car)
            
        return car
    
    # ===创建一个订单，接受确切坐标，未指定则随机生成===
    def create_order(self, pos_x = None, pos_y = None):
        if pos_x is None:
            pos_x = random.randint(10, 990)
        if pos_y is None:
            pos_y = random.randint(10, 990)
            
        order = obj.Orders(pos_x, pos_y, self.next_order_id)
        self.next_order_id += 1
        
        self.order_queue.add_order(order)
        
        print(f"[生成订单] 订单id #{order.id} 位置({order.pos_x},{order.pos_y})")
        return order
        
    # ===负责批量随机生成车辆===
    def create_car_bash(self, count):
        for i in range(count):
            self.create_car()
        
    # ===负责批量随机生成订单===    
    def create_order_bash(self, count):
        # == ORDER_CREATE_POS为（0，0）时表示随机生成==
        if cfg.ORDER_CREATE_POS == (0, 0):
            for i in range(count):
                self.create_order()
            return 
        
        #  ==以ORDER_CREATE_POS为中心正态分布生成==
        for i in range(count):
            mid_x = cfg.ORDER_CREATE_POS[0]
            mid_y = cfg.ORDER_CREATE_POS[1]
            sigma = cfg.ORDER_CREATE_SCLAE
            x = int(truncnorm.rvs((0 - mid_x) / sigma, (999 - mid_x) / sigma, loc = mid_x, scale = sigma))
            y = int(truncnorm.rvs((0 - mid_y) / sigma, (999 - mid_y) / sigma, loc = mid_y, scale = sigma))
            self.create_order(x, y)
        
            
            






"""
def create_order(pos_x, pos_y, No):
    one_order = obj.orders(pos_x, pos_y, No)
    refe_x, refe_y = pos_x / 10, pos_y / 10
    one_order.next = obj.car_list.data[refe_x][refe_y]
    obj.cat_list.data[refe_x][refe_y] = one_car 

def create_cars(pos_x, pos_y, No):
    one_car = obj.cars(pos_x, pos_y, No)
    refe_x, refe_y = pos_x / 10, pos_y / 10
    one_car.next = obj.car_list.data[refe_x][refe_y]
    obj.cat_list.data[refe_x][refe_y] = one_car 

def create_line():
    vehicle_generation :float = 0
    middle_x, middle_y :int = 0,0
    if test_option == 1:
        # 订单和车辆生成地址平均，其中车辆生成几率更大，模拟车辆充足。
        vehicle_generation = 0.6
    elif test_option == 2:
        # 订单和车辆生成地址平均，其中订单生成几率更大，模拟订单高峰
        vehicle_generation = 0.4
    elif test_option == 3:
        # 车辆生成地址平均，订单生成存在高峰，模拟早高峰之类订单群聚集的情况
        middle_x = random.randint(50,950)
        middle_y = random.randint(50,950)
        sigma = 100
        
    if random.randrange(0,1) < vehicle_generation:
        create_cars(random.randint(0,999), random.randint(0, 999))
    else:
        if test_option == 3:
            x ,y = 1, 1
            while True:
                x = random.gauss(middle_x, sigma)   # 正态分布生成 x
                y = random.gauss(middle_y, sigma)   # 正态分布生成 y
                # 限制在 [0, 999] 范围内
                if 0 <= x <= 999 and 0 <= y <= 999:
                    break
            create_order(x, y)
        else :
            create_order(random.randint(0,999), random.randint(0, 999))
        
"""