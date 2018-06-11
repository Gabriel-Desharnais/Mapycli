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
mapycli.wms.getcapabilities(*args,**kargs)
```
will translate to
``` python
se.getcapabilities(*args,**args)
```

---
**Note:**

It is important to note that since *mapycli* is using *requests* under the houd you can always add any parameters to your request (usefull for vendor support) and you force *mapycli* to not send a default parameter by explicitily setting it to `None`

---

#### GetCapabilities
usage
``` python
getCapRes = mapycli.wms.getcapabilities(url,service="WMS",request="GetCapabilities",version="1.3.0",format="application/vnd.ogc.se_xml",**kargs)
```
every kargs given to getcapabilities will be url encoded and passed directly to the server. The function returns a `getCapabilitiesObject` object. If the format of the server response is the default one (application/xml) mapycli will parse the response, otherwise the only functionality provided by `getCapabilitiesObject` will be the
``` python
Res = getCapRes.response
```
This will return you the **requests** response

If you want to go threw the basic parsing of the xml file you can use `getCapDict`. This variable is a dictionary that contains lists of every tags with their respective values. Therefore, the content of every tags with a given label at root level are assembled together in a list and placed in the dict with their label as key. If the tag contain other tags the content will be a dict of tags.

e.g.
``` python
dic = getCapRes.getCapDict
# Accessing all 'Service' tags
serv = dic['Service']
# Accessing the first Service tag
s = serv[0]
```


If you want to go threw a well parsed hierarchy using OGC standard you can use `getCapStruct`.

e.g.

``` python
val = getCapRes.getCapStruct.service.title
```
`val` will then have the value of the `<Title>` tag in `<service>` tag.
Here is a list of all the supported tags and their place in the `getCapStruct` object.

|             Link           |                   Tag                     |     Type    | Behavior note |
| -------------------------- | ----------------------------------------- | ----------- | ------------- |
|        service.name        |         &lt;Service&gt;&lt;Name&gt;       |     str     | Expception if no tag, if multiple first one kept. |
|        service.title       |        &lt;Service&gt;&lt;Title&gt;       |     str     | Exception if no tag, if multiple first one kept. |
|      service.abstract      |      &lt;Service&gt;&lt;Abstract&gt;      |     str     | Exception if no tag, if multiple first one kept. |
|   service.onlineResource   |   &lt;Service&gt;&lt;OnlineResource&gt;   |     str     | Will not be implemented in a while. |
|    service.keywordList     |    &lt;Service&gt;&lt;KeywordList&gt;     | list of str | Exception if no tag, if multiple first one kept. |
| service.contactInformation | &lt;Service&gt;&lt;ContactInformation&gt; |    struct   | Exception if no tag, if multiple first one kept. Will not be implemented in a wild. |
|     service.layerLimit     |     &lt;Service&gt;&lt;LayerLimit&gt;     |     int     | If multiple, first one kept. If none, layerLimit will not be created in service. |
|      service.maxWidth      |      &lt;Service&gt;&lt;MaxWidth&gt;      |     int     | If multiple, first one kept. If none, maxWidth will not be created in service. |
|      service.maxHeight     |      &lt;Service&gt;&lt;MaxHeight&gt;     |     int     | If multiple, first one kept. If none, maxHeight will not be created in service. |
|        service.fees        |        &lt;Service&gt;&lt;Fees&gt;        |     str     | If multiple, first one kept. If none, fees will not be created in service. |
|  service.accessConstrains  |  &lt;Service&gt;&lt;AcessConstrains&gt;   |     str     | If multiple, first one kept. If none, accessConstrains will not be created in service. |


If you want to have the list of the layer name you can call the `getLayers` method.

e.g.
``` python
getCapRes.getLayers()
```
#### GetMap
#### GetFeatureInfo
#### DescribeLayer
#### GetLegendGraphic



## Developement
This package is developed threw documentation driven developement (DDD). If you want to commit a change, the documentation should be the first thing you touch. No **pull request** without a change in the doc will be merged.

## Bibliography
Every document consulted to make this package will be listed here.
- [OWSLib](https://geopython.github.io/OWSLib/)
