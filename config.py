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

# 搜索入口
ENABLE_ENTRY = True
ENTRY = "https://www.douban.com/group/search"
ENTRY_MAX_PAGE = 5
ENTRY_BLACKLIST = []
ENTRY_CATALOG = 1019
ENTRY_QUERY = u"家居"

# 豆瓣小组URL
GROUP_LIST = [
    # 爱生活！爱家居！爱艺术！
    "http://www.douban.com/group/sheyii/",
    # 家居党—家居知识NO.1小组
    "http://www.douban.com/group/household/",
    # 我爱我家（家电&家居&数码）
    "http://www.douban.com/group/532638/",
    # 软装配饰设计|家居软装饰设计
    "http://www.douban.com/group/DECORATIONS/",
    # DIY家居生活馆
    "http://www.douban.com/group/DIY-jiaju/",
    # 智能硬件 智能家居有多机智？
    "http://www.douban.com/group/538230/",
]

# 后缀
GROUP_SUFFIX = "discussion?start=%d"

# 抓取前多少页
MAX_PAGE = 25

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
    # 搜索入口
    "group_list": "//div[@class='title']/h3/a/@href"
}

# 并发数
POOL_SIZE = 20

# 监控周期(秒),默认10分钟
WATCH_INTERVAL = 10 * 60

# 重载代理周期
PROXY_INTERVAL = 30 * 60
