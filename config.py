# coding: utf8

"""配置
"""

# User-Agent
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.3; WOW64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/40.0.2214.93 Safari/537.36"
)

# mongo config
DB_URI = "mongodb://127.0.0.1:27017"
DB_NAME = "douban_group"

# 豆瓣小组URL
GROUP_LIST = [
    # 北京租房豆瓣
    "http://www.douban.com/group/26926/",
    # 北京租房（非中介）
    "http://www.douban.com/group/279962/",
    # 北京租房房东联盟(中介勿扰)
    "http://www.douban.com/group/257523/",
    # 北京租房
    "http://www.douban.com/group/beijingzufang/",
    # 通州租房
    "http://www.douban.com/group/369658/",
    # 北京租房小组
    "http://www.douban.com/group/xiaotanzi/",
    # 北京无中介租房
    "http://www.douban.com/group/zhufang/",
    # 北漂爱合租
    "http://www.douban.com/group/aihezu/",
    # 北京租房
    "http://www.douban.com/group/370806/"
    # 北京同志们来租房
    "http://www.douban.com/group/325060/",
    # 北京个人租房
    "http://www.douban.com/group/opking/",
    # 北京租房小组!
    "http://www.douban.com/group/374051/",
]

# 后缀
SUFFIX = "discussion?start=%d"

# 抓取前多少页
MAX_PAGE = 10

# 并发数
POOL_SIZE = 3

# 监控周期(秒),默认5分钟
WATCH_INTERVAL = 5 * 60
