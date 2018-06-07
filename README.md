# Mapycli
Python 3 package to do client operations on web service respecting Open Geospatial Consortium (OGC) standard.

## How to install
Sometime in the future the package will be on pypi and there will be a *.deb* or *.rpm* package, but for now you will need to do
``` bash
python3 setup.py install
```
## Compatibilitie
This package is develloped and tested on a linux machine it should work on other platform, but there are no guaranties and no support for it. This is a python3 package since python2 end of life is supposed to be on January the first 2020, I will neighter devellope nor support for python2 (python2 needs to die and thus I don't believe in it anymore).

## Dependencies
This is a list of package that **Mapycli** relies on.

## License
This package is under MIT license, for more information look in **LICENSE** file.

## User manual
This is a complete and exaustiv documentation of how to use the package.
### Importing the package
To import the package in your program use:
``` python
import mapycli
```
### Session
**Not available yet**
Although the creation of a session is not mandatory to do requests, it is highly recommanded to use them because it add a lot of functionality and they can make your life easier. A session is an object that will keep in memory some parameters and most importantly the information about ressource available on the server. Session are service specific ('WMS','WFS','WCS','WPS','CWS')
#### Creating a session
To create a session you should do:
``` python
se = mapycli.service.session()
```
Here `service` should be replaced by the name of the service *e.g.* `mapycli.WMS.session()`.
This opperation will create an empty session.

If you want to create a session and to a getcapabilities at the same time:
``` python
se = mapycli.service.session(URL)
```

#### Action on session
Sessions allow 2 type of opperation to control it.

##### Update
The update opperation enalbles you to update the informations about the layers. You can do an update on every layers by doing
``` python
se.update()
```
In this case the session will go threw every layer and do a getcapabilities on every different source available. You can also add all arguments allowed by a the getcapabilities requests (including vendor extention) (for more information go see [getcapabilities](#getcapabilities) to do an update on somme of the layers.
``` python
se.update(url)
```
The update opperation only add layers and replace the one that already exist with new ones, it will not erase the ones that aren't provided anymore by the server. Therefor, it might not be consistent with the state of the server. If you want full consistency with the server use [reset](#reset)

##### reset
This opperation will remove the old information about layers in the session and reload the new information. You can reset every layer in the session by doing
``` python
se.reset()
```
If you want to do a reset on a specific source you can pass all the getcapabilities parameters. e.g.
``` python
se.reset(url)
```

This opperation will not touch other parameters set in session.

#### Session variable

If you want to change the default version tag used to communicate with the web service you can change the version variable e.g.
``` python
se.version = "1.3.0"
```

The default values are:

| service | default version |
| ------- | --------------- |
| WMS | 1.3.0 |
| WFS | 2.0.2 |
| WCS | 2.0 |
| WPS | 2.0 |


### WMS
**not available yet**
This section will list every WMS supported opperations available. Note that wms session object support all of these opperations e.g.
The function call
``` python
mapycli.wms.getcapabilities(*args)
```
will translate to
``` python
se.getcapabilities(*args)
```
#### GetCapabilities
usage
``` python
getCapRes = mapycli.wms.getcapabilities(url,[service="WMS",request="GetCapabilities",version="1.3.0",format="application/vnd.ogc.se_xml",**kargs])
```
every kargs given to getcapabilities will be url encoded and passed directly to the server. The function returns a getcapabilitiesResponse object. If the format is the default one mapycli will parse the responce otherwise you the only functionality provided by the getcapabilitiesResponse object will be the
``` python
Res = getCapRes.Responce
```
This will return you the **requests** responce

If you want to go threw the hierarchy of the responce you can
``` python
val = getCapRes.Capabilities.Service.Title
```

If you want to have the list of the layer name you can
``` python
getCapRes.layers
```
#### GetMap
#### GetFeatureInfo
#### DescribeLayer
#### GetLegendGraphic



## Devellopement
This package is develloped threw documentation driven devellopement (DDD). If you want to commit a change The documentation should be the first thing you touch. No **pull request** without a change in the doc will be merged.

## Bibliography
Every document consulted to make this package will be listed here.
- [OWSLib](https://geopython.github.io/OWSLib/)
