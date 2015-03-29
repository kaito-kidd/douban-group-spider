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
# DB_URI = "mongodb://192.168.6.7:27017"
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
    # 北京租房小组
    "http://www.douban.com/group/xiaotanzi/",
    # 北京无中介租房
    "http://www.douban.com/group/zhufang/",
    # 北漂爱合租
    "http://www.douban.com/group/aihezu/",
    # 北京同志们来租房
    "http://www.douban.com/group/325060/",
    # 北京个人租房
    "http://www.douban.com/group/opking/",
    # 北京租房小组!
    "http://www.douban.com/group/374051/",
]

# 后缀
GROUP_SUFFIX = "discussion?start=%d"

# 抓取前多少页
MAX_PAGE = 5

# 匹配规则
RULES = {
    # 每个帖子项
    "topic_item": "//table[@class='olt']/tr",
    "url_list": "//table[@class='olt']/tr/td[@class='title']/a/@href",
    # 列表元素
    "title": "td[@class='title']/a/@title",
    "author": "td[@nowrap='nowrap'][1]/a/text()",
    "reply": "td[@nowrap='nowrap'][2]/text()",
    "last_reply_time": "td[@class='time']/text()",
    "url": "td[@class='title']/a/@href",
    # 帖子详情
    "detail_title_sm": "//td[@class='tablecc']/text()",
    # 完整标题
    "detail_title_lg": "//div[@id='content']/h1/text()",
    "create_time": "//span[@class='color-green']/text()",
    "detail_author": "//span[@class='from']/a/text()",
    "content": "//div[@class='topic-content']/p/text()",
}

# 并发数
POOL_SIZE = 20

# 监控周期(秒),默认10分钟
WATCH_INTERVAL = 10 * 60

# 重载代理周期
PROXY_INTERVAL = 30 * 60
