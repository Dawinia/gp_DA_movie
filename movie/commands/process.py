# -*- coding: utf-8 -*-

from twisted.internet import defer, protocol, reactor

import os


class ProcessProtocol(protocol.ProcessProtocol):
    def __init__(self):
        pass

    def connectionMade(self):
        pass

    def outReceived(self, data):
        pass


class SpiderRunnerProtocol(protocol.ProcessProtocol):
    def __init__(self, d, inputt=None):
        self.deferred = d
        self.inputt = inputt
        self.output = ""
        self.err = ""

    def connectionMade(self):
        if self.inputt:
            self.transport.write(self.inputt)
        self.transport.closeStdin()

    def outReceived(self, data):
        self.output += data

    def processEnded(self, reason):
        print(reason.value)
        print(self.err)
        self.deferred.callback(self.output)

    def errReceived(self, data):
        # self.err += data
        pass


def run_spider(cmd, *args, **kwargs):
    # d = defer.Deferred()
    # pipe = SpiderRunnerProtocol(d)
    # args = [cmd] + list(args)
    # env = os.environ.copy()
    # x = reactor.spawnProcess(pipe, cmd, args, env=env)
    # print(x.pid)
    # print(x)
    # return d
    pass


def print_out(result):
    print(result)


# d = run_spider("scrapy", "crawl", "reddit")
# d = run_spider("scrapy", "crawl", "dmoz")
# d.addCallback(print_out)
# d.addCallback(lambda _: reactor.stop())
# reactor.run()
