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

]

# 监控周期(秒),默认5分钟
WATCH_INTERVAL = 5 * 60
