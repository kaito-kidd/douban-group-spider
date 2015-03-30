# 说明
用于爬取`豆瓣小组`的爬虫。<br/>
此爬虫我主要用于了爬取`豆瓣租房小组`的帖子，支持`关键字搜索`以及`发帖`、`更新时间排序`。 

# 依赖
- `gevent`
- `pymongo`
- `requests`
- `lxml`
- `Flask`
-  `boostrap`
<br/>
具体版本参见`requirements.txt`<br/>

# 特别说明
- 由于豆瓣有防抓机制，故此爬虫使用了代理爬取，防止被封IP。<br/>
- 可从网上收集代理IP，放在项目路径下`proxy_list.txt`。
- 每个一行，程序会自动加载，且可以自动定时加载新代理。<br/>
- 或者参考我的[代理采集器](https://github.com/kaito-kidd/proxy-fetcher)，自动采集代理。
- 如果程序运行发现总是出现超时或者403，请更换`proxy_list.txt`下的代理。

# 使用
- 安装`MongoDB`，具体参考安装文档。
- 建议使用`virtualenv`环境<br/>
    `pip install -r requirements.txt`
- 启动爬虫<br/>
    `nohup python spider.py >> douban_spider.log &`
- 启动web服务<br/>
    `nohup python app.py >> app.log &`
- 查看页面<br/>
    `http://localhost:5000`

# 配置
参数配置见`config.py`，例如`MongoDB地址`、`并发数`、`爬取页数`等。
