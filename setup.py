# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='zhihu_crawl_slaver',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=zhihu_crawl.settings']},
)