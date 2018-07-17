"""
This file is the base of the session object
"""

def session(inheritance):
	# This function is made to dinamically inherite the session object.
	# This is important becanse sessions are supposed to support every
	# method supported by the service that's calling it

	class Session(inheritance):
		def __init__(self,url=None):
			# This method should have two behavior if an url is given,
			# Do a GetCapabilities at this url, else just create the object

			# Go fetch the service default version and use it as the default
			# in the new session
			self.version = self.defaultVersion

			# Create a dict that will contain all the sources and their
			# respective informations
			self.sources = {}

			# Check to see if an url arguments was passed
			if url:
				# Go request a GetCapabilities and store valuable informations
				# at the right place
				getCapRes = self.getcapabilities(url)

				# Add the GetCapabilities to the dictionary of sources
				self.sources[url] = getCap
		def update(self):
			# This method update information about layers with new
			# GetCapabilities
			pass

		def reset(self):
			# This method erase old information about layers and reload it with
			# a new GetCapabilities
			pass
	return Session
