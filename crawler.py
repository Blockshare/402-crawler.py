""" 402 Crawler

	Crawl endpoints, check socket connection, and
	check 402 headers.

"""

import datetime
import logging
import socket

from two1.wallet import Wallet
from two1.bitrequests import BitTransferRequests

class Crawler402():

	""" Crawl endpoints to check status.

		Check server socket connection and query endpoints for
		price and recipient address.

	"""
	def __init__(self, endpoint_list, log_file):4

		""" 
			Setting up logging and member vars

		"""

		# configure logging
		logging.basicConfig(level=logging.INFO,
							filename=log_file,
							filemode='a',
							format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
							datfmt='%m-%d-%H-%M')
		self.console = logging.StreamHandler()
		self.console.setLevel(logging.INFO)
		logging.getLogger('402-crawler').addHandler(self.console)
		self.logger = logging.getLogger('402-crawler')
		self.endpoint_list = endpoint_list

	def check_endpoints(self):

		"""
			Crawl 402 endpoints

		"""

		# create 402 client
		self.bitrequests = BitTransferRequests(Wallet())

		# crawl endpoints, check headers
		self.logger.info("\nCrawling machine-payable endpoints...")
		for endpoint in self.endpoint_list:

			# extract domain name
			name = endpoint.split('/', 1)[0].split('.', 1)[1]

			# get server IP address
			server_ip = socket.gethostbyname(name)

			self.logger.info("Checking {}...".format(endpoint))

			# configure socket module
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_state = sock.connect_ex((server_ip, 80))
			sock.close()

			if server_state == 0:
				try:
					self.logger.info("Server State: {} is up!".format(endpoint))
					response = self.bitrequests.get_402_endpoint('https://'+endpoint)
					self.logger.info("Price: {}".format(response['price']))
					self.logger.info("Address: {}".format(response['bitcoin-address']))
				except Exception:
					self.logger.info("Could not read 402 payment headers.")
			else:
				self.logger.info("Server State: {} is down!".format('https://'+endpoint))
			self.logger.info("Timestamp: {}".format(datetime.datetime.now()))

if __name__=='__main__':

	# endpoints to crawl
	endpoints_list = [
            'http://www.blockshar.es/bitcoin',
            'http://www.blockshar.es/ether',
	]

	crawler = Crawler402(endpoint_list, '402-crawler.log')
    crawler.check_endpoints()
