try:
    VERSION = __import__('pkg_resources').get_distribution('fabric-bolt').version
except Exception, e:
    VERSION = 'unknown'