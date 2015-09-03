from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class MultiSwitchTopo(Topo):
    def build(self, n=2,m=2):
        switch=[]
        for s in range(m):
            switch.append(self.addSwitch('s%s'%(s+1)))
            for h in range(s*n, (s+1)*n):
                if (h%2==0):
                    host = self.addHost('h%s'%(h+1),
                        cpu=.5/n, ip="11.0.1."+str(h+1)+'/24')
                    self.addLink(host, switch[s], bw=1, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
                else:
                    host = self.addHost('h%s'%(h+1),
                        cpu=.5/n, ip="11.0.0."+str(h+1)+'/24')
                    self.addLink(host, switch[s], bw=2, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
            if(s>0):
                self.addLink(switch[s],switch[s-1])
        
def perfTest():
    topo = MultiSwitchTopo(n,m)
    net = Mininet(topo=topo, 
                  host=CPULimitedHost, link=TCLink)
    net.start()
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    n = int(raw_input("Enter number of hosts on each switch: "))
    m = int(raw_input("Enter number of switches: "))
    setLogLevel('info')
    perfTest()