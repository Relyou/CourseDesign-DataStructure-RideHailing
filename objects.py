from minheap import MinHeap
# ===订单节点===
class Orders:
    def __init__(self, pos_x, pos_y, id):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id = id
        self.next_order = None
        self.dispatch_time = 0
    
    def get_pos(self):
        return self.pos_x // 100, self.pos_y // 100
   
# ===订单队列=== 
class OrderQueue:
    def __init__(self):
        self.head_order = None
        self.tail_order = None
        self.total_order = 0
        self.cnt_order = [[0 for i in range(10)] for j in range(10)]
    
    def add_order(self, order):
        # ==第一个入队的，头和尾都是他==
        if self.head_order == None:
            self.head_order = order
            self.tail_order = order
        # ==不是的话直接接在尾节点后==
        else:
            self.tail_order.next_order = order
            order.next_order = None
            self.tail_order = order
        
        # ==统计对应地区顶单数==
        gx, gy = order.get_pos()
        self.cnt_order[gx][gy] += 1
        self.total_order += 1
        
    # ====删除对应订单====
    def del_order(self, order):
        # ==空了就不用删了==
        if self.head_order == None:
            return
        
        pre_order = self.head_order
        # ==如果第一个就是要删的，直接改头节点==
        if pre_order == order:
            self.head_order = order.next_order
            gx, gy = order.get_pos()
            self.cnt_order[gx][gy] -= 1
            self.total_order -= 1
            return
        
        # ==不是则找目标节点的前一个节点==
        while(pre_order.next_order != order):
            pre_order = pre_order.next_order
            if pre_order == None:
                return
            
        # ==如果刚好删的是尾节点，则前一节点变成尾节点==
        if pre_order.next_order == self.tail_order:
            self.tail_order = pre_order
            
        # ==报错修改懒得写了，就这么办吧，题目也没要求==
        pre_order.next_order = order.next_order
        
        # ==节点删完了，改数值==
        gx, gy = order.get_pos()
        self.cnt_order[gx][gy] -= 1
        self.total_order -= 1
        
    
    # ===获取订单个数===
    def size(self):
        return self.total_order
    
# ====司机节点，同时也是链表节点====
class Cars:
    def __init__(self, pos_x, pos_y, id, rating = 4.0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_idle = True
        self.id = id
        self.rating  = rating
        self.next = None
        
    def get_pos(self):
        return self.pos_x // 100, self.pos_y // 100
        
# ====司机链表管理器====
class CarList:
    def __init__(self):
        self.data = [[None for i in range(10)] for j in range(10)]
        self.cnt_car = [[0 for i in range(10)] for j in range(10)]
        self.total_car = 0
    
    # ===获取实际位置在10*10网格上的映射===
    def get_pos(self, x, y):
        gx = x // 100
        gy = y // 100
        return gx, gy
    
    # ===将指定车辆加入链表===
    def add_car(self, car):
        gx, gy = self.get_pos(car.pos_x, car.pos_y)
        car.next = self.data[gx][gy]
        self.data[gx][gy] = car
        self.cnt_car[gx][gy] += 1
        self.total_car += 1
        return car
    
    # ===从链表中移除指定司机===
    def remove_car(self, car):
        driver_id = car.id
        gx, gy = car.get_pos()
        
        prev = None
        current = self.data[gx][gy]
        while current is not None:
            if current.id == driver_id:
                if prev is None:
                    self.data[gx][gy] = current.next
                else:
                    prev.next = current.next
                    
                # ==找到了，更新数值==
                self.cnt_car[gx][gy] -= 1 
                self.total_car -= 1
                return True
            prev = current
            current = current.next
        
        return False
        
        
    # ===查找指定司机,待定，需要加===
    
    # ===获取指定网格的所有司机，待定，需要加===
        