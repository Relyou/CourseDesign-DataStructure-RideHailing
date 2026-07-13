import time
import matplotlib.pyplot as plt

class RealtimeHeatmap:
    def __init__(self):
        # 初始化窗口 
        plt.ion()
            
        # 创建画布和坐标轴
        self.fig, self.ax = plt.subplots(figsize = (8, 6))
        
        time.sleep(2000)
    
def main():
    heapmap = RealtimeHeatmap()
    
    
    
if __name__ == "__main__":
    main()
