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
	layer = []
	for layerDict in layerDictList:
		layer.append(struct())
		# Get title (There can only be one)
		layer[-1].title = layerDict["Title"][0][2]
		# Add name Optional
		try:
			# Get name (There can only be one)
			layer[-1].name = layerDict["Name"][0][2]
		except KeyError:
			# If there is no name, do nothing
			pass
		# O CRS
		try:
			layer[-1].crs = [tup[2] for tup in layerDict["CRS"]]
		except KeyError:
			# If there is no crs, do nothing
			pass

		# O Abstract (0/1)
		try:
			layer[-1].abstract = layerDict["Abstract"][0][2]
		except KeyError:
			# If there is no abstract, do nothing
			pass

		# O KeywordList (0/1)
		try:
			layer[-1].keywordList = [tup[2] for tup in layerDict["KeywordList"][0][0]["Keyword"]]
		except KeyError:
			# If there is no keywords, do nothing
			pass

		# exGeographicBoundingBox
		layer[-1].exGeographicBoundingBox = struct()
		try:
			layer[-1].exGeographicBoundingBox.westBoundLongitude = float(  layerDict["EX_GeographicBoundingBox"][0][0]["westBoundLongitude"][0][2] )
			layer[-1].exGeographicBoundingBox.eastBoundLongitude = float( layerDict["EX_GeographicBoundingBox"][0][0]["eastBoundLongitude"][0][2] )
			layer[-1].exGeographicBoundingBox.southBoundLongitude = float( layerDict["EX_GeographicBoundingBox"][0][0]["southBoundLongitude"][0][2] )
			layer[-1].exGeographicBoundingBox.northBoundLongitude = float( layerDict["EX_GeographicBoundingBox"][0][0]["northBoundLongitude"][0][2] )
		except:
			pass

		# Add boundingBox
		# Create the list of struct
		layer[-1].boundingBox = []
		try:
			for bbox in layerDict["BoundingBox"]:
				# Create the structure
				layer[-1].boundingBox.append(struct())

				# Add crs from attributes to struct
				layer[-1].boundingBox[-1].crs = bbox[1]["CRS"]

				# Add minx, maxx, miny, maxy from attributes to struct
				layer[-1].boundingBox[-1].minx = float( bbox[1]["minx"] )
				layer[-1].boundingBox[-1].miny = float( bbox[1]["miny"] )
				layer[-1].boundingBox[-1].maxx = float( bbox[1]["maxx"] )
				layer[-1].boundingBox[-1].maxy = float( bbox[1]["maxy"] )

				# Try to add resx and resy
				try:
					layer[-1].boundingBox[-1].resx = float( bbox[1]["resx"] )
					layer[-1].boundingBox[-1].resy = float( bbox[1]["resy"] )
				except:
					# If you can't, don't create these variable
					pass
		except KeyError:
			pass


		# Add sub layers, if any, to the layers
		try:
			layer[-1].layer = addlayers([tup[0] for tup in layerDict["Layer"]])
		except KeyError as e:
			# If there is no layer, do nothing
			pass


	return layer

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

		# Retrive the values to create tuple associated with the tag

		# Get childs
		if len(list(tag)) > 0:
			# If the element has child add keep them in a dict
			child = explore(tag)
		else:
			# Create an empty dict
			child = {}

		# Get Attributes and remove namespace if needed
		attributes = {}
		for katt, vatt in tag.attrib.items():
			attributes[katt.split("}")[-1]] = vatt


		# Get text of tag
		text = tag.text

		# Create a tuple and add it to the list of this tag name
		theXML[name].append( (child,attributes,text) )

	# Return the dict containing the xml struc from this point
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

			# If the standard describe that a field can only be there once, The next part will just use the first one and ignore the rest

			# Create the GetCapabilities structure
			self.getCapStruct = struct()

			# Create the service variable
			self.getCapStruct.service = struct()
			# Create the capability variable
			self.getCapStruct.capability = struct()

			# Filling of the service metadata
			# Get name (There can only be one)
			self.getCapStruct.service.name = self.getCapDict["Service"][0][0]["Name"][0][2]
			# Get title (There can only be one)
			self.getCapStruct.service.title = self.getCapDict["Service"][0][0]["Title"][0][2]
			# O Get abstract (There can only be one)
			try:
				self.getCapStruct.service.abstract = self.getCapDict["Service"][0][0]["Abstract"][0][2]
			except KeyError:
				# If there is no abstract, do nothing
				pass

			# OnlineResource
			self.getCapStruct.service.onlineRessource = self.getCapDict["Service"][0][0]["OnlineResource"][0][1]["href"]

			# O keywordList
			try:
				self.getCapStruct.service.keywordList = []
				for keyword in self.getCapDict["Service"][0][0]["KeywordList"][0][0]["Keyword"]:
					self.getCapStruct.service.keywordList.append(keyword[2])
			except KeyError:
				# If there is no keywords, do nothing.
				pass

			# O Contact information
			try:
				# Check if there is a ContactInformation tag
				ci = self.getCapDict["Service"][0][0]["ContactInformation"][0][0]
				# Create a struct
				self.getCapStruct.service.contactInformation = struct()
				# Add contactPersonPrimary
				try:
					cip = ci["ContactPersonPrimary"][0][0]
					self.getCapStruct.service.contactInformation.contactPersonPrimary = struct()
					# Add contactPerson
					try:
						self.getCapStruct.service.contactInformation.contactPersonPrimary.contactPerson = cip["ContactPerson"][0][2]
					except KeyError:
						# If there is no contactperson, do nothing.
						pass
					# Add contactOrganisation
					try:
						self.getCapStruct.service.contactInformation.contactPersonPrimary.contactOrganization = cip["ContactOrganization"][0][2]
					except KeyError:
						# If there is no contactperson, do nothing.
						pass

				except KeyError:
					# If there is no contactPersonPrimary, do nothing.
					pass

				# Add contactPosition
				try:
					self.getCapStruct.service.contactInformation.contactPosition = ci["ContactPosition"][0][2]
				except KeyError:
					# If there is no ContactPosition, do nothing.
					pass

				# Add ContactAddress
				try:
					cia = ci["ContactAddress"][0][0]
					self.getCapStruct.service.contactInformation.contactAddress = struct()

					# Add addressType
					try:
						self.getCapStruct.service.contactInformation.contactAddress.addressType = cia["AddressType"][0][2]
					except KeyError:
						# If there is no AddressType, do nothing.
						pass

					# Add address
					try:
						self.getCapStruct.service.contactInformation.contactAddress.address = cia["Address"][0][2]
					except KeyError:
						# If there is no Address, do nothing.
						pass

					# Add city
					try:
						self.getCapStruct.service.contactInformation.contactAddress.city = cia["City"][0][2]
					except KeyError:
						# If there is no city, do nothing.
						pass

					# Add stateOrProvince
					try:
						self.getCapStruct.service.contactInformation.contactAddress.stateOrProvince = cia["StateOrProvince"][0][2]
					except KeyError:
						# If there is no city, do nothing.
						pass

					# Add postCode
					try:
						self.getCapStruct.service.contactInformation.contactAddress.postCode = cia["PostCode"][0][2]
					except KeyError:
						# If there is no city, do nothing.
						pass

					# Add country
					try:
						self.getCapStruct.service.contactInformation.contactAddress.country = cia["Country"][0][2]
					except KeyError:
						# If there is no country, do nothing
						pass

				except KeyError:
					# If there is no ContactAddress, do nothing.
					pass

				# Add contactVoiceTelephone
				try:
					self.getCapStruct.service.contactInformation.contactVoiceTelephone = ci["ContactVoiceTelephone"][0][2]
				except:
					# If there is no contactVoiceTelephone, do nothing.
					pass

				# Add contactElectronicMailAddress
				try:
					self.getCapStruct.service.contactInformation.contactElectronicMailAddress = ci["ContactElectronicMailAddress"][0][2]
				except:
					# If there is no contactElectronicMailAddress, do nothing.
					pass

			except KeyError:
				# if there is no contact information, do nothing.
				pass

			# O LayerLimit
			try:
				self.getCapStruct.service.layerLimit = int(self.getCapDict["Service"][0][0]["LayerLimit"][0][2])
			except KeyError:
				# If there is no LayerLimit, do nothing.
				pass

			# O MaxWidth
			try:
				self.getCapStruct.service.maxWidth = int(self.getCapDict["Service"][0][0]["MaxWidth"][0][2])
			except KeyError:
				# If there is no MaxWidth, do nothing.
				pass

			# O MaxHeight
			try:
				self.getCapStruct.service.maxHeight = int(self.getCapDict["Service"][0][0]["MaxHeight"][0][2])
			except KeyError:
				# If there is no MaxHeight, do nothing.
				pass

			# O Fees
			try:
				self.getCapStruct.service.fees = self.getCapDict["Service"][0][0]["Fees"][0][2]
			except KeyError:
				# If there is no Fees, do nothing.
				pass

			# O accessConstraints
			try:
				self.getCapStruct.service.accessConstraints = self.getCapDict["Service"][0][0]["AccessConstraints"][0][2]
			except KeyError:
				# If there is no AccessConstraints, do nothing.
				pass

			# Filling of the capability metadata
			# Lack of documentation in ogc for request and expception

			# O Fill layers arg with a list of layers
			try:
				self.getCapStruct.capability.layer = addlayers([tup[0] for tup in self.getCapDict["Capability"][0][0]["Layer"]])
			except KeyError:
				# If there is no layer, do nothing
				pass








		else:
			# End there since this unknow object should not be processed
			return

# REFS:
# [1] : https://bugs.python.org/issue18304
