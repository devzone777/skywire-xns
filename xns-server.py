"""
Skywire XNS requires zmq
"""
from twisted.names import dns, server, client, cache
from twisted.application import service, internet
from twisted.python import log
import zmq
import time
from twisted.internet import defer

skywire_xns_server_ip = "localhost"
skywire_xns_server_port = 8002

class CacheEntry(object):
    def __init__(self, ip, ttl):
        self.ip = ip
        self.ttl = int(ttl)
        self.valid_till = time.time() + int(ttl)
    def is_valid(self):
        return time.time() < self.valid_till
    def get_ip(self):
        return self.ip
    def get_ttl(self):
        return self.ttl

class MapResolver(client.Resolver):
    """
    Resolves names by looking in a mapping. 
    If `name in mapping` then mapping[name] should return an IP
    else the next server in servers will be asked for name    
    """
    def __init__(self, servers):
        self.cache = { }
        client.Resolver.__init__(self, servers=servers)
        self.ttl = 10
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://%s:%d" % (skywire_xns_server_ip,
                                             skywire_xns_server_port) )
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def lookupAddress(self, name, timeout = None):
        # find out if this is a .sky. request
        if name in self.cache and self.cache[name].is_valid():
            ip = self.cache[name].get_ip() # get the result
            
            if ip == "0.0.0.0":
                # doesn't exist
                return self._lookup(name, dns.IN, dns.A, timeout)
            
            return defer.succeed([
                    (dns.RRHeader(name,
                                  dns.A,
                                  dns.IN,
                                  self.ttl,
                                  dns.Record_A(ip, self.ttl)),),
                    (),()
                    ])
        else:
            try:
                self.socket.send(name)
                # our XNS server should answer within 5 ms
                socks = dict(self.poller.poll(timeout=5))

                if self.socket in socks and socks[self.socket] == zmq.POLLIN:
                    # format is "IP TTL"
                    msg = self.socket.recv().split(' ')
                    self.cache[name] = CacheEntry(msg[0], msg[1])
                    if msg[0] == "0.0.0.0":
                        # entry doesn't exist
                        return self._lookup(name, dns.IN, dns.A, timeout)
                    return self.lookupAddress(name)
            except zmq._zmq.ZMQError:
                log.msg("please start skywire-xns server")
            return self._lookup(name, dns.IN, dns.A, timeout)


## this sets up the application


application = service.Application('dnsserver', 1, 1)

# set up a resolver that uses the mapping or a secondary nameserver
xnsresolver = MapResolver(servers=[('8.8.8.8', 53)])


# create the protocols
f = server.DNSServerFactory(caches=[cache.CacheResolver()],
                            clients=[xnsresolver])
p = dns.DNSDatagramProtocol(f)
f.noisy = p.noisy = False


# register as tcp and udp
ret = service.MultiService()
PORT=53

for (klass, arg) in [(internet.TCPServer, f), (internet.UDPServer, p)]:
    s = klass(PORT, arg)
    s.setServiceParent(ret)


# run all of the above as a twistd application
ret.setServiceParent(service.IServiceCollection(application))


# run it through twistd!
if __name__ == '__main__':
    import sys
    print "Usage: twistd -y %s" % sys.argv[0]
