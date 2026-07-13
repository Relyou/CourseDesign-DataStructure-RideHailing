# ====模拟派单参数====
SUM_TEST_NUM = 3 # 派单接单模拟伦次
CAR_TEST_NUM = 10 # 每轮加入司机数量
ORDER_TEST_NUM = 10 # 每轮加入订单数量

# ====订单生成相关参数====
ORDER_CREATE_POS = (650, 250) # 随机生成订单以该坐标为中心，（0，0）则为随机
ORDER_CREATE_SCLAE = 200 # 随机函数标准差，越小越集中

# ====派单过程相关====
COEF_JUDEG = 200 # 撮合函数中司机评价的权值系数
MAX_DISPATCH_TIMES = 10 # 每个订单最多试图匹配车辆次数
TANH_SACLE = 5.0 # tanh映射时的缩放因子
MAX_DISPATCH_TIME = 5 # 每个单子最多寻找次数，多了就排队尾

# ====图表显示相关====
MAX_LOGS = 10 # 日志区最多显示日志数量
IS_OPEN_ORDER_BALANCE = True # 是否启用车辆调度功能