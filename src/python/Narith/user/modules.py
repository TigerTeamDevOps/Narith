"""
[Narith]
File: modules.py
Author: Saad Talaat
Date: 17th August 2013
brief: help representation of provided modules
########################
# Disclaimer:
# part of this code is part of webhandler software
# author: Ahmed Shawky aka lnxg33k
########################
"""
from Narith.user.termcolor import cprint

class Modules(object):
    """
    The following class contains the used
    modules by br and some info about them
    """

    def __init__(self):
	self.high_modules = {}
	self.base_modules = {}
	self.core_modules = {'pcap': self.pcap_module,
	 'local': self.local_module,
	 'domain': self.domain_module,
	 'browse': self.browse_module}
	self.all_modules = {}
	all_modules = [ x for x in self.core_modules ] + [ x for x in self.base_modules ] + [ x for x in self.high_modules ]
	for module in all_modules:
	    self.all_modules[module] = None

    def pcap_module(self):
	print ''
	cprint('Pcap file module', 'green')
	print '=======================\n'
	print '    read <filename>              Reads a pcap file into narith from given filename'
	print '    count                        provides the number of packets in read pcap file'
	print '    interface                    provides the used interface in the on recorded session'

    def domain_module(self):
	print ''
	cprint('Domains module', 'green')
	print '=======================\n'
	print '     www                         prints out all remote hostnames'
	print '     all                         prints all occurances of all hostnames during session'
	print '     search <infix>              reads a substring and searches for domains that match'
    def browse_module(self):
	print ''
	cprint('Domains module', 'green')
	print '=======================\n'
	print '     www                         prints out all remote hostnames'
	print '     all                         prints all occurances of all hostnames during session'
	print '     search <infix>              reads a substring and searches for domains that match'

	# def browse_module(self):
	# 	print ''
	# 	cprint ('HTTP MODULE', 'green')

    def local_module(self):
	print ''
	cprint('Local information module', 'green')
	print '=======================\n'
	print '     info                        Lists all information obtained about local host'
	print '     host                        Prints both the local ip and hostname if exists'
	print '     dns-servers                 Prints all dns servers used by local host'
	print '     mac-addr                    Prints the local host mac address'

    def session_module(self):
	print ''
	cprint('Session information module','green')
	print '=======================\n'
	print '     all                         Lists all sessions information'
	print '     search <infix>              Searches for sessions with hosts which contain the infix'
	print '     www                         Lists all sessions with www domain name'
	print '     protocol                    Lists sessions which uses certain protocol'
    def core(self):
	print ''
	cprint('List of core modules', 'red')
	print '====================='
	print '    pcap                         Specialized in extracting data from pcap'
	print '    local                        Specialized in extracting data about local user'
	print '    domain                       Specialized in extracting data about domain names'
	print '    session                      Specialized in extracting sessions  information'

    def base(self):
	print ''
	cprint('List of base modules', 'red')
	print '=========================='
	print '    NOT YET                      No low level modules yet defined'

    def high(self):
	print ''
	cprint('List of high modules', 'red')
	print '==========================='
	print '    NOT YET                      No High level modules yet defined'


'''
Module interfaces definitions, each module with own executer.
'''
from Narith.base.Pcap.Pcap import Pcap

class PcapInterface(object):
	__interfaces = \
	{
	0 : 'Undefined',
	1 : 'Ethernet'
	}
	def __init__(self):
		self.__commands = \
		{
		'read' : self.read,
		'count' : self.count,
		'interface' : self.interface,
		}
		self.__pcap = None

	def executer(self, commands):
		if commands[0] not in self.__commands:
			return
		self.__commands[commands[0]](commands[1:])

	def read(self, files):
		p = []
		for f in files:
			pp = Pcap(f)
			p.append(pp)
			if pp.length:
			    cprint(('[*] file %s read' % f),'green')
		self.__pcap = p

	def count(self, files):
		for p in self.__pcap:
			if p.file and p.length:
				cprint('[*] file %s: %d packets' % (p.file,p.length),'green')
			else:
				cprint('[!] Invalid file','red')

	def interface(self, files):
		for p in self.__pcap:
			try:
				cprint('[*] file %s: %s' %(p.file, self.__interfaces[p.interface]),'green')
			except:
				cprint('[!] Invalid file','red')
	def has(self, f):
		for p in self.__pcap:
			if p.file == f:
				return True
			else:
				False
	@property
	def pcap(self):
		return self.__pcap
class DomainInterface(object):

	def __init__(self, pcap, packets):
		from Narith.base.Analysis.Classifier import Classifier
		from Narith.core.Extraction.Domains import DomainExtractor

		self.__commands = \
		{
		'www'	: self.www,
		'all'	: self.all,
		'search': self.search,
		}
		self.__domain = None
		self.__pcap = pcap
		self.__packets = packets
		self.__de = DomainExtractor(self.__packets)

	def executer(self, commands):
		if commands[0] not in self.__commands:
			return
		self.__commands[commands[0]](commands[1:])

	def www(self, commands):
		for domain,ip in self.__de.wwwExtract():
			cprint("[*] " + domain + " -> " + ip,'green')

	def all(self, commands):
		for domain,ip in self.__de.domains(''):
			cprint("[*] " + domain + " -> " + ip,'green')

	def search(self, commands):
		for domain,ip in  self.__de.domains(commands[0]):
			cprint("[*] " + domain + " -> " + ip, 'green')
	@property
	def pcap(self):
		return self.__pcap

	@property
	def extractor(self):
		return self.__de
class LocalInterface(object):

	def __init__(self, pcap, packets, extractor):
		from Narith.base.Analysis.Classifier import Classifier
		from Narith.core.Extraction.Local import LocalInfo

		self.__commands = \
	        {
	        'dns-servers'   : self.dns,
	        'info'   : self.info,
	        'host': self.host,
		'mac': self.mac,
	        }
	        self.__local = None
	        self.__pcap = pcap
	        self.__li = LocalInfo(packets,extractor)

	def executer(self, commands):
		if commands[0] not in self.__commands:
			return
		self.__commands[commands[0]](commands[1:])

	def dns(self, commands):
		cprint('[*] DNS Servers:','green')
		for server in self.__li.dns_servers:
			cprint('\tServer: %s' % server, 'green')

	def host(self, commands):
		cprint('[*] Host: %s' % self.__li.host, 'green')

	def mac(self, commands):
		cprint('[*] Mac address: %s' % self.__li.mac_address, 'green')

	def info(self, commands):
		self.dns(commands)
		self.mac(commands)
		self.host(commands)
	@property
	def pcap(self):
		return self.__pcap

class SessionInterface(object):

	def __init__(self, pcap, packets, extractor):
		from Narith.base.Analysis.Classifier import Classifier
		from Narith.core.Extraction.Session import SessionExtractor
		self.__commands = \
		{
		'all'    : self.all,
		'search' : self.search,
		'www'    : self.www,
		'protocol': self.protocol
		}
		self.__pcap =  pcap
		self.__se = SessionExtractor(packets,pcap.records, extractor)

	def executer(self, commands):
		if commands[0] not in self.__commands:
			cprint("[!] Command not found",'red')
			return
		self.__commands[commands[0]](commands[1:])

	def all(self, commands):
		count = 0
		for host,session in self.__se.sessions.iteritems():
			cprint ("Host:\t\t"+session.hostname,'green')
			cprint ("Packets no.:\t"+str(session.count),'green')
			cprint ("Date:\t\t"+session.start+" ~ "+session.end,'green')
			cprint ("Bytes:\t\t"+str(session.bytes),'green')
			print ""
			count +=1
		cprint("Total sessions: "+str(count),'magenta')
	def search(self, commands):
		count = 0
		for session in self.__se.search(commands[0]):
			cprint ("Host:\t\t"+session.hostname,'green')
			cprint ("Packets no.:\t"+str(session.count),'green')
			cprint ("Date:\t\t"+session.start+" ~ "+session.end,'green')
			cprint ("Bytes:\t\t"+str(session.bytes),'green')
			print ""
			count +=1
		cprint("Total sessions: "+str(count),'magenta')

	def www(self, commands):
		count = 0
		for session in self.__se.prefix("www"):
			cprint ("Host:\t\t"+session.hostname,'green')
			cprint ("Packets no.:\t"+str(session.count),'green')
			cprint ("Date:\t\t"+session.start+" ~ "+session.end,'green')
			cprint ("Bytes:\t\t"+str(session.bytes),'green')
			print ""
			count +=1
		cprint("Total sessions: "+str(count),'magenta')


	def protocol(self, commands):
			pass

class BrowseInterface(object):

	def __init__(self, pcap, packets):
		from Narith.base.Analysis.Classifier import Classifier
		from Narith.core.Extraction.Browse import BrowseExtractor

		self.__commands = \
		{
		'requests'	: self.requests,
		'host'	: self.requestSelect,
		
		# 'search': self.search,
		}
		# self.__domain = None
		self.__pcap = pcap
		self.__packets = packets
		self.__http = BrowseExtractor(self.__packets)
		r = 0
		for i, j in self.__http.requests.iteritems():
			r += 1
			self.__http.requests[i]['index'] = r


	def executer(self, commands):
		if commands[0] not in self.__commands:
			return
		self.__commands[commands[0]](commands[1:])

	def requests(self, c):
		import time
		cprint ('[+] Found %s requests to %s hosts...' % ( str(sum(x['times'] for x in self.__http.requests.values())), str(len(self.__http.requests.keys()))), 'blue') 
		time.sleep(1)
		# r = 0
		for i, j in self.__http.requests.iteritems():
			# r += 1
			# self.__http.requests[i]['index'] = r
			cprint ('[%s]' % j['index'] + i, 'green')
			h = '  %s request(s)' % str(j['times'])
			nonVerbalKeys = ['times', 'index']
			for v in j:
				if v in nonVerbalKeys:
					continue
				h += ' | '
				h += v + ': ' + str(j[v])
			cprint(h, 'yellow')

	def requestSelect(self, commands):
		import time
		# print commands
		host = commands[0]
		# print host
		for i, j in self.__http.requests.iteritems():
			if j['index'] == int(host):
				key = i
				break
		try:
			key
		except:
			cprint ('Invalid host index', 'red')
			return

		cprint ('[+] %s request(s) to %s' % (self.__http.requests[key]['times'], key), 'blue')
		nonVerbalKeys = ['times', 'index']
		h = '[+] '
		for v in self.__http.requests[key]:
			if v in nonVerbalKeys:
				continue
			# h += ' | '
			h += v + ': ' + str(self.__http.requests[key][v])
			h += ' | '

		cprint (h, 'green')



