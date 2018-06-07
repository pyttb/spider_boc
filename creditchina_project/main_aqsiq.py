from scrapy import cmdline
name = 'aqsiq'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())