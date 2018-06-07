from scrapy import cmdline
name = 'bxjg'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())