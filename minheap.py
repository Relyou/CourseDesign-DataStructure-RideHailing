class MinHeap:
    def __init__(self, capacity=100):
        self.heap = [None] * capacity
        self.size = 0
        
    def is_empty(self):
        return self.size == 0
    
    # ===插入车辆===
    def push(self, score, driver):
        if self.size >= len(self.heap):
            self.resize()
        self.heap[self.size] = (score, driver)
        self.size += 1
        self.shift_up(self.size - 1)
        
    # ===弹出堆顶===
    def pop(self):
        temp = self.heap[0]
        self.heap[0], self.heap[self.size - 1] = self.heap[self.size - 1], self.heap[0]
        self.size -= 1
        self.shift_down(0)
        return temp
    
    # ===获取堆顶元素===
    def top(self):
        if self.size == 0:
            return None
        return self.heap[0]
    
    # ===清空堆===
    def clear(self):
        self.size = 0
    
    # ===插入数据后上浮===
    def shift_up(self, index):
        while(index != 0):
            fa = (index - 1) // 2
            if self.heap[fa][0] > self.heap[index][0]:
                self.heap[fa], self.heap[index] = self.heap[index], self.heap[fa]
                index = fa
            else:
                break
    
    # ==取出堆顶后下沉===
    def shift_down(self, index):
        while 1:
            smallest = index
            # ==判断当前节点，左节点，右节点三者中哪个最小，顺便判断是否有左右子节点
            ls = index * 2 + 1
            rs = index * 2 + 2
            if ls < self.size and self.heap[ls][0] < self.heap[smallest][0]:
                smallest = ls
            if rs < self.size and self.heap[rs][0] < self.heap[smallest][0]:
                smallest = rs
            if smallest == index:
                break
            # 交换父子节点，递归处理更小的子节点
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest
    
    # ===检查是否为空===
    def empty(self):
        if self.size == 0:
            return True
        return False
            
        
    # ===空间不足时扩容===
    def resize(self):
        new_capacity = len(self.heap) * 2
        new_heap = [None] * new_capacity
        for i in range(self.size):
            new_heap[i] = self.heap[i]
        self.heap = new_heap