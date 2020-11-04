# -*- coding: utf-8 -*-

# Scrapy settings for zhihu_crawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html


# 参数
DATABASE_NAME_t1 = 'x'
DATABASE_NAME_t2 = 'x'
DATABASE_HOST = 'cdb-nran2q00.cd.tencentcdb.com'
DATABASE_USER = 'root'
DATABASE_PASS = 'Mimashi123'
BEFORE_STOP = 0


# using redis
REDIS_HOST = '129.28.28.203'
REDIS_PORT = 6379
REDIS_PARAMS = {'password': 'Mimashiredis1'}
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
REDIS_ENCODING = 'utf-8'


BOT_NAME = 'zhihu_crawl'
SPIDER_MODULES = ['zhihu_crawl.spiders']
NEWSPIDER_MODULE = 'zhihu_crawl.spiders'
LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the
# user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

FEED_EXPORT_ENCODING = 'UTF-8'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
CLOSESPIDER_TIMEOUT = 3500  # 单位：秒
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'zhihu_crawl.middlewares.Close_spider': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'zhihu_crawl.middlewares.Close_spider': 543,
}

MYEXT_ENABLED = True      # 开启扩展
IDLE_NUMBER = 360           # 配置允许的空闲时长，每5秒会增加一次IDLE_NUMBER，直到增加到360，程序才会close

# 在 EXTENSIONS 配置，激活扩展
EXTENSIONS = {
    'zhihu_crawl.extensions.RedisSpiderSmartIdleClosedExensions': 500,
    # 空闲30min自动退出
}
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'zhihu_crawl.pipelines.ZhihuCrawlPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
