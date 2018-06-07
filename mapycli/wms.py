"""
This file is the base of the wms object
"""
import requests

class WMS:
	# This class implement the method necessary to do request to a wms server
	defaultVersion = "1.3.0"
	session = None

	def __int__(self):
		self.version = defaultVersion

	def getcapabilities(self,url,request="GetCapabilities",
						service="WMS",
						version=False,**kargs):
		# This method does a simple gercap request to a wms server

		# Check if a version karg as been passed to the method
		if version is False:
			# Place default value for version
			version = self.version

		# Add all parameters to a dict called params
		params = {"request":request,"service":service,"version":version}
		params.update(kargs)

		# Do a get request
		r = requests.get(url, params=params)

		# Send the responce in a new getCapabilitiesObject
		gco = getCapabilitiesObject(r)

		# Return the getCapabilitiesObject to the user
		return gco

class getCapabilitiesObject:
	def __init__(self,responce):
		self.responce = responce
