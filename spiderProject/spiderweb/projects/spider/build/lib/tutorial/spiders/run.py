# -*- coding: utf-8 -*-

from scrapy import cmdline, Spider
import time


if __name__ == '__main__':
    cmdline.execute(("scrapy crawl zhilian").split()) 