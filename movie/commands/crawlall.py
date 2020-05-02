# -*- coding: utf-8 -*-

from scrapy.commands import ScrapyCommand
import os
from twisted.internet import defer, protocol, reactor
from logger import spider_logger as logger
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from movie.commands.process import SpiderRunnerProtocol


class Command(ScrapyCommand):
    requires_project = True

    def short_desc(self):
        return "Run all spiders"

    def crawl(self, queue, spider):
        logger.info(f"spider = {spider}")
        # settings = Settings()
        # settings.set("PROJECT", {"movie"})
        settings = get_project_settings()
        crawler = CrawlerProcess(settings)
        crawler.crawl(spider, queue=queue)
        crawler.start()

    def run_spider(self, cmd, *args, **kwargs):
        d = defer.Deferred()
        pipe = SpiderRunnerProtocol(d)
        args = [cmd] + list(args)
        env = os.environ.copy()
        x = reactor.spawnProcess(pipe, cmd, args=args, env=env)
        print(x.pid)
        print(x)
        return d

    def run(self, args, opts):
        # spider_list = self.crawler_process.spiders.list()
        # queue = Queue()
        # logger.error(f"inside run that queue = {type(queue)}")
        # process_list = []
        # for spider in spider_list:
        #     logger.error(f"inside run that spider = {type(spider)}")
        #     p = Process(target=self.crawl, args=(queue, spider,))
        #     p.start()
        #     process_list.append(p)
        #
        # map(lambda x: x.join(), process_list)
        # for i in queue.get():
        #     print(i)
        d = self.run_spider("scrapy", "crawl", "boxOffice")
        # d.addCallback(lambda _: reactor.stop())
        reactor.run()
