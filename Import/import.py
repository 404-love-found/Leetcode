'''
写法	                 使用方式	     适用场景
import math	             math.sqrt()	最常用，清晰不冲突
from math import sqrt	 sqrt()	        某个函数用得特别多
import math as m	     m.sqrt()	    模块名太长时
'''

'''
模块	           用途	        典型函数/类
math	          数学函数	    sqrt、gcd、inf、ceil/floor
collections	      高级容器	    deque、defaultdict、Counter
heapq	          堆操作	    heappush、heappop
bisect	          二分查找	    bisect_left、bisect_right
itertools	      迭代器工具	permutations、combinations
functools	      函数工具	    lru_cache、cmp_to_key
sys	              系统相关	    sys.stdin（快读）、sys.maxsize

'''
#再提醒一下：list、dict、set、str、int 等内置类型，以及 len、range、sorted、max/min、sum、abs 等内置函数，不需要导入，直接用就行


'''
my_project/
├── main.py
└── utils/
    ├── __init__.py      # 标记 utils 是一个包
    ├── math_utils.py    # 数学工具模块
    └── string_utils.py  # 字符串工具模块
'''
# 导入包中的特定模块
from utils.math_utils import factorial

# 或者导入整个模块
import utils.math_utils as mu