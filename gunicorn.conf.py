import multiprocessing
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

from blog import settings

LOG_DIR = BASE_DIR.joinpath('log')

LOG_DIR.mkdir(mode=0o755, exist_ok=True)

# 绑定的ip与端口
bind = "127.0.0.1:8000"

# 以守护进程的形式后台运行
daemon = True

# 最大挂起的连接数，64-2048
backlog = 512

# 超时
timeout = 30

# 调试状态
debug = settings.DEBUG
reload = True

# gunicorn要切换到的目的工作目录
chdir = str(BASE_DIR)

# 工作进程类型(默认的是 sync 模式，还包括 eventlet, gevent, or tornado, gthread, gaiohttp)
worker_class = 'sync'

# 工作进程数
workers = multiprocessing.cpu_count()

# 指定每个工作进程开启的线程数
threads = multiprocessing.cpu_count() * 2

# 日志级别，这个日志级别指的是错误日志的级别(debug、info、warning、error、critical)，而访问日志的级别无法设置
loglevel = 'info'

# 日志格式
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 其每个选项的含义如下：
'''
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
'''

accesslog = str(LOG_DIR.joinpath('gunicorn_access.log'))
errorlog = str(LOG_DIR.joinpath('gunicorn_error.log'))
pidfile = str(LOG_DIR.joinpath('gunicorn_error.pid'))

proc_name = 'django_blog.pid'
