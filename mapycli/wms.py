"""
This file is the base of the wms object
"""
# python included package
import xml.etree.ElementTree as ET

# Third party package
import requests

# Usefull class and functions

class struct(object):
	# This class will be used to contain variable
	pass

def addlayers(layerDictList):
	# This fuction returns a list of layers and sublayers and fill the
	# information in a struct class
	layers = []
	for layerDict in layerDictList:
		layers.append(struct())
		# Get title (There can only be one)
		layers[-1].title = layerDict["Title"][0]
		# Add name Optional
		try:
			# Get name (There can only be one)
			layers[-1].name = layerDict["Name"][0]
		except KeyError:
			# If there is no name, do nothing
			pass
		# O CRS
		try:
			layers[-1].crs = layerDict["CRS"]
		except KeyError:
			# If there is no crs, do nothing
			pass

		# O Abstract (0/1)
		try:
			layers[-1].abstract = layerDict["Abstract"][0]
		except KeyError:
			# If there is no abstract, do nothing
			pass

		# O KeywordList (0/1)
		try:
			layers[-1].keywordlist = layerDict["KeywordList"][0]["Keyword"]
		except KeyError:
			# If there is no keywords, do nothing
			pass
		# Add sub layers, if any, to the layers
		try:
			layers[-1].layers = addlayers(layerDict["Layer"])
		except KeyError:
			# If there is no layer, do nothing
			pass


	return layers
	pass
def explore(root):
	# This function will explore the xml and return a dictionary
	theXML = {}
	# Go threw the tags at root level
	for tag in list(root):
		# Get name tag and remove the namespace
		name = tag.tag.split("}")[-1]

		# Check if that name is registered in the dictionary
		try:
			theXML[name]
		except KeyError:
			# If it is not registered, do it
			theXML[name] = []

		# Add the element in the registered tag
		# if the element as no child add the text
		if len(list(tag)) == 0:
			theXML[name].append(tag.text)
		else:
			theXML[name].append(explore(tag))

	return theXML
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

		# Do a get request to the url, send it the params in the url and
		# download content right away (stream), do not wait for r.text
		r = requests.get(url, params=params, stream=False)

		# TODO: We should do something to accelarate the parsing of text in
		#		requests to detect encoding faster.

		# Send the response in a new getCapabilitiesObject
		gco = getCapabilitiesObject(r)

		# Return the getCapabilitiesObject to the user
		return gco

class getCapabilitiesObject:
	def __init__(self,response):
		self.response = response

		# Get text from the response
		text = self.response.text

		# Verify that the response is of type xml before trying to parse it
		type = self.response.headers['content-type'] # Get type of document
		# test type
		if type == 'application/xml':
			# Parse the xml
			self.root = ET.fromstring(text)

			# Since etree is a piece of garbage maintened poorly [1], I'll use
			# a filling strategy so I'm expecting a few fields but instead of
			# looking for them they'll look for me.

			# This dict will contain every variable and list every child
			self.getCapDict=explore(self.root)

			# If there is the standard describe that a field can only be there once, The next part will just use the first one and ignore the rest

			# Create the GetCapabilities structure
			self.getCapStruct = struct()

			# Create the service variable
			self.getCapStruct.service = struct()
			# Create the capability variable
			self.getCapStruct.capability = struct()

			# Filling of the service metadata
			# Get name (There can only be one)
			self.getCapStruct.service.name = self.getCapDict["Service"][0]["Name"][0]
			# Get title (There can only be one)
			self.getCapStruct.service.title = self.getCapDict["Service"][0]["Title"][0]
			# Get abstract (There can only be one)
			self.getCapStruct.service.abstract = self.getCapDict["Service"][0]["Abstract"][0]
			# No OnlineResource
			# Contact information should be added
			# Optional info
			# O LayerLimit
			# O MaxWidth
			# O MaxHeight
			# O Fees

			# Filling of the capability metadata
			# Lack of documentation in ogc for request and expception

			# O Fill layers arg with a list of layers
			try:
				self.getCapStruct.capability.layers = addlayers(self.getCapDict["Capability"][0]["Layer"])
			except KeyError:
				# If there is no layer, do nothing
				pass









		else:
			# End there since this unknow object should not be processed
			return

# REFS:
# [1] : https://bugs.python.org/issue18304
