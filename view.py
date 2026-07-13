import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import time

# ====解决中文乱码=====
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

class RealtimeHeatmap:
    def __init__(self, max_logs=10):
        self.max_logs = max_logs
        self.logs = []
        self.stats = {
            'queue_length': 0,
            'success_rate': 0.0,
            'avg_time': 0.0,
            'round_num': 0,
            'total_success': 0,
            'total_fail': 0
        }
        
        plt.ion()
        self.fig = plt.figure(figsize=(10, 10))
        gs = GridSpec(3, 1, height_ratios=[5, 1, 2], figure=self.fig)
        
        self.ax_heatmap = self.fig.add_subplot(gs[0])
        self.ax_heatmap.set_title('网约车区域供需热力图', fontsize=14)
        
        self.ax_stats = self.fig.add_subplot(gs[1])
        self.ax_stats.axis('off')
        
        self.ax_log = self.fig.add_subplot(gs[2])
        self.ax_log.axis('off')
        
        self.data = np.zeros((10, 10))
        self.im = self.ax_heatmap.imshow(
            self.data,
            cmap='RdYlGn',
            vmin=-1,
            vmax=1,
            interpolation='nearest'
        )
        
        self.ax_heatmap.set_xticks(np.arange(-0.5, 10, 1), minor=True)
        self.ax_heatmap.set_yticks(np.arange(-0.5, 10, 1), minor=True)
        self.ax_heatmap.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
        
        self.cbar = self.fig.colorbar(self.im, ax=self.ax_heatmap, shrink=0.8)
        self.cbar.set_label('供需差值（绿=车多，红=单多）')
        
        self._update_stats_text()
        self._update_log_text()
        
        plt.subplots_adjust(hspace=0.3)
        
        plt.show(block=False)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def _update_stats_text(self):
        s = self.stats
        text = (
            f"订单队列: {s['queue_length']}  |  "
            f"成功率: {s['success_rate']:.1f}%  |  "
            f"平均耗时: {s['avg_time']:.1f}ms  |  "
            f"轮次: {s['round_num']}  |  "
            f"(成功: {s['total_success']}, 失败: {s['total_fail']})"
        )
        self.ax_stats.clear()
        self.ax_stats.axis('off')
        self.ax_stats.text(
            0.02, 0.5, text,
            fontsize=12,
            verticalalignment='center',
            horizontalalignment='left',
            fontfamily='sans-serif',
            transform=self.ax_stats.transAxes
        )
    
    def _update_log_text(self):
        self.ax_log.clear()
        self.ax_log.axis('off')
        
        self.ax_log.text(
            0.02, 0.92, '实时派单日志',
            fontsize=11,
            fontweight='bold',
            transform=self.ax_log.transAxes
        )
        
        if self.logs:
            display_logs = self.logs[-self.max_logs:]
            display_logs = reversed(display_logs)
            
            y_pos = 0.85
            step = 0.12
            max_lines = self.max_logs
            
            for i, log in enumerate(display_logs):
                if i >= max_lines:
                    break
                if len(log) > 100:
                    log = log[:97] + '...'
                self.ax_log.text(
                    0.02, y_pos, f' {log}',
                    fontsize=9,
                    verticalalignment='top',
                    transform=self.ax_log.transAxes
                )
                y_pos -= step
        else:
            self.ax_log.text(
                0.02, 0.85, '等待派单...',
                fontsize=10,
                color='gray',
                transform=self.ax_log.transAxes
            )
    
    def update_heatmap(self, new_data):
        self.im.set_data(new_data)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.01)
    
    def update_stats(self, queue_length, success_count, fail_count, total_time_ms, round_num):
        
        
        self.stats['queue_length'] = queue_length
        self.stats['round_num'] = round_num
        self.stats['total_success'] = success_count
        self.stats['total_fail'] = fail_count
        total_all = success_count + fail_count
        
        if total_all > 0:
            self.stats['success_rate'] = success_count / total_all * 100
        else:
            self.stats['success_rate'] = 0.0
        
        self.stats['avg_time'] = total_time_ms
        
        self._update_stats_text()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.01)
    
    def add_log(self, log_msg):
        timestamp = time.strftime('%H:%M:%S')
        self.logs.append(f'[{timestamp}] {log_msg}')
        
        if len(self.logs) > self.max_logs * 3:
            self.logs = self.logs[-self.max_logs * 3:]
        
        self._update_log_text()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.01)
    
    def close(self):
        plt.ioff()
        plt.close()