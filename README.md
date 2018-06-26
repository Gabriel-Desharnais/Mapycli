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

If you want to go threw the basic parsing of the xml file you can use `getCapDict`. This variable is a dictionary that contains lists of every tags with their respective values. Therefore, the content of every tags with a given label at root level are assembled together in a list and placed in the dict with their label as key.

The value stored in the list paired with the key is a tuple of lenght 3. The first element is a dict of tags, if the tag has children, they will be stored in this element. The second element is a dict of the attributes, the key is the name of the attribute and the value is the value of the attribute. The third element of the tuple is the value stored in the tag.

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

|             Link           |                   Tag                     |      Type      | Behavior note |
| -------------------------- | ----------------------------------------- | -------------- | ------------- |
|        service.name        |         &lt;Service&gt;&lt;Name&gt;       |       str      | Expception if no tag. If multiple, first one kept. |
|        service.title       |        &lt;Service&gt;&lt;Title&gt;       |       str      | Exception if no tag. If multiple, first one kept. |
|      service.abstract      |      &lt;Service&gt;&lt;Abstract&gt;      |       str      | If none, name will not be created. If multiple first one kept. |
|   service.onlineRessource   |   &lt;Service&gt;&lt;OnlineRessource&gt;   |       str      | Exception thrown if no tag. If multiple, first one kept. Attribute **xlink:href** in **OnlineRessource** |
|    service.keywordList     |    &lt;Service&gt;&lt;KeywordList&gt;     |  list of str   | If none, name will not be created. If multiple, first one kept. |
| service.contactInformation | &lt;Service&gt;&lt;ContactInformation&gt; |     struct     | If none, name will not be created. If multiple, first one kept. |
| ...contactInformation.contactPersonPrimary | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactPersonPrimary&gt; |     struct     | If none, name will not be created. If multiple, first one kept. |
| ...contactPersonPrimary.contactPerson | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactPersonPrimary&gt;&lt;ContactPerson&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactPersonPrimary.contactOrganization | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactPersonPrimary&gt;&lt;ContactOrganization&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactInformation.contactPosition | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactPosition&gt; |     str     | If none, name will not be created. If multiple, first one kept. |
| ...contactInformation.contactAddress | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactAddress&gt; |     struct     | If none, name will not be created. If multiple, first one kept. |
| ...contactAddress.addressType | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactAddress&gt;&lt;AddressType&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactAddress.address | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactAddress&gt;&lt;Address&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactAddress.city | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactAddress&gt;&lt;City&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactAddress.stateOrProvince | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactAddress&gt;&lt;StateOrProvince&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactAddress.postCode | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactAddress&gt;&lt;PostCode&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactAddress.country | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactAddress&gt;&lt;Country&gt; |       str      | If none, name will not be created. If multiple, first one kept. |
| ...contactInformation.contactVoiceTelephone | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactVoiceTelephone&gt; |     str     | If none, name will not be created. If multiple, first one kept. |
| ...contactInformation.contactElectronicMailAddress | &lt;Service&gt;&lt;ContactInformation&gt;&lt;ContactElectronicMailAddress&gt; |     str     | If none, name will not be created. If multiple, first one kept. |
|     service.layerLimit     |     &lt;Service&gt;&lt;LayerLimit&gt;     |       int      | If multiple, first one kept. If none, layerLimit will not be created in service. |
|      service.maxWidth      |      &lt;Service&gt;&lt;MaxWidth&gt;      |       int      | If multiple, first one kept. If none, maxWidth will not be created in service. |
|      service.maxHeight     |      &lt;Service&gt;&lt;MaxHeight&gt;     |       int      | If multiple, first one kept. If none, maxHeight will not be created in service. |
|        service.fees        |        &lt;Service&gt;&lt;Fees&gt;        |       str      | If multiple, first one kept. If none, fees will not be created in service. |
|  service.accessConstraints  |  &lt;Service&gt;&lt;AccessConstraints&gt;   |       str      | If multiple, first one kept. If none, accessConstraints will not be created in service. |
|    capability.exception    |    &lt;Capability&gt;&lt;Exception&gt;    |  list of str   | Exception if no tag, if multiple first one kept. |
|      capability.layer      |       &lt;Capability&gt;&lt;Layer&gt;     | list of struct | Exception if no tag. |
|       ...layer[n].queryable       | &lt;Capability&gt;&lt;Layer&gt; | bool | If none, queryable will be set to default (False). Using attribute **queryable**. |
|       ...layer[n].cascaded       | &lt;Capability&gt;&lt;Layer&gt; | int | If none, cascaded will be set to default (0). Using attribute **cascaded**. |
|       ...layer[n].opaque       | &lt;Capability&gt;&lt;Layer&gt; | bool | If none, opaque will be set to default (false). Using attribute **cascaded**. |
|       ...layer[n].noSubsets       | &lt;Capability&gt;&lt;Layer&gt; | bool | If none, noSubsets will be set to default (false). Using attribute **noSubsets**. |
|       ...layer[n].fixedWidth       | &lt;Capability&gt;&lt;Layer&gt; | int | If none, fixedWidth will be set to default (0). Using attribute **fixedWidth**. |
|       ...layer[n].fixedHeight       | &lt;Capability&gt;&lt;Layer&gt; | int | If none, fixedHeight will be set to default (0). Using attribute **fixedHeight**. |
|       ...layer[n].layer       | &lt;Capability&gt;&lt;Layer&gt;&lt;Layer&gt; | list of struct | If none, layer will not be created in service. |
|       ...layer.title       | &lt;Capability&gt;&lt;Layer&gt;&lt;Title&gt; | str | Exception if no tag, if multiple first one kept. |
|       ...layer.name       | &lt;Capability&gt;&lt;Layer&gt;&lt;Name&gt; | str | If none, name will not be created, if multiple first one kept. |
|       ...layer.abstract       | &lt;Capability&gt;&lt;Layer&gt;&lt;Abstract&gt; | str | If none, name will not be created, if multiple first one kept. |
|       ...layer.keywordList       | &lt;Capability&gt;&lt;Layer&gt;&lt;KeywordList&gt; | list of str | If none, name will not be created, if multiple first one kept. |
|       ...layer.style       | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt; |  list of struct  | If none, name will not be created. |
|       ...style[n].name       | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;Name&gt; | str | Exception if no tag, if multiple first one kept. |
|       ...style[n].title       | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;Title&gt; | str | Exception if no tag, if multiple first one kept. |
|       ...style[n].abstract       | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;Abstract&gt; | str | Exception if no tag, if multiple first one kept. |
|       ...style[n].legendUrl      | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;LegendURL&gt; | struct | If multiple first one kept. |
|       ...legendUrl.width      | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;LegendURL&gt; | int | If multiple first one kept. attribute **width** |
|       ...legendUrl.height      | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;LegendURL&gt; | int | If multiple first one kept. attribute **height** |
|       ...legendUrl.format      | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;LegendURL&gt;&lt;Format&gt; | str | If multiple first one kept. |
|       ...legendUrl.onlineRessource      | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;LegendURL&gt;&lt;OnlineRessource&gt; | str | If multiple first one kept. use value in **xlink:href** attribute |
|       ...style[n].styleSheetURL       | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;StyleSheetURL&gt; | struct | If multiple, first one kept. |
|       ...styleSheetURL.format       | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;StyleSheetURL&gt;&lt;Format&gt; | str | If multiple, first one kept. |
|       ...styleSheetURL.onlineRessource       | &lt;Capability&gt;&lt;Layer&gt;&lt;Style&gt;&lt;StyleSheetURL&gt;&lt;OnlineRessource&gt; | str | If multiple, first one kept. **Attribute xlink:href** |
|       ...layer.crs       | &lt;Capability&gt;&lt;Layer&gt;&lt;CRS&gt; | list of str | If none, name will be created with an empty list. |
|       ...layer.exGeographicBoundingBox       | &lt;Capability&gt;&lt;Layer&gt;&lt;EX_GeographicBoundingBox&gt; | struct | If none, name will be created with an empty struct. If multiple, first one kept. |
|       ...exGeographicBoundingBox.westBoundLongitude       | &lt;Capability&gt;&lt;Layer&gt;&lt;EX_GeographicBoundingBox&gt;&lt;westBoundLongitude&gt; | float | If none, exception thrown. If multiple, first one kept. |
|       ...exGeographicBoundingBox.eastBoundLongitude       | &lt;Capability&gt;&lt;Layer&gt;&lt;EX_GeographicBoundingBox&gt;&lt;eastBoundLongitude&gt; | float | If none, exception thrown. If multiple, first one kept. |
|       ...exGeographicBoundingBox.southBoundLatitude       | &lt;Capability&gt;&lt;Layer&gt;&lt;EX_GeographicBoundingBox&gt;&lt;southBoundLatitude&gt; | float | If none, exception thrown. If multiple, first one kept. |
|       ...exGeographicBoundingBox.northBoundLatitude       | &lt;Capability&gt;&lt;Layer&gt;&lt;EX_GeographicBoundingBox&gt;&lt;northBoundLatitude&gt; | float | If none, exception thrown. If multiple, first one kept. |
|       ...layer.boundingBox       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | list of struct | If none, exception thrown. |
|       ...boundingBox[n].crs       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | str | If none, exception thrown. Attribute CRS from &lt;BoundingBox&gt; |
|       ...boundingBox[n].minx       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | float | If none, exception thrown. Attribute minx from &lt;BoundingBox&gt; |
|       ...boundingBox[n].miny       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | float | If none, exception thrown. Attribute miny from &lt;BoundingBox&gt; |
|       ...boundingBox[n].maxx       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | float | If none, exception thrown. Attribute maxx from &lt;BoundingBox&gt; |
|       ...boundingBox[n].maxy       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | float | If none, exception thrown. Attribute maxy from &lt;BoundingBox&gt; |
|       ...boundingBox[n].resx       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | float | Attribute resx from &lt;BoundingBox&gt; |
|       ...boundingBox[n].resy       | &lt;Capability&gt;&lt;Layer&gt;&lt;BoundingBox&gt; | float | Attribute resy from &lt;BoundingBox&gt; |
|       ...layer[n].attribution       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt; | struct | If multiple, first one used. |
|       ...attribution.title       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt;&lt;Title&gt; | str | If multiple, first one used. |
|       ...attribution.onlineRessource       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt;&lt;OnlineRessource&gt; | str | If multiple, first one used. using attribute **xlink:href**. |
|       ...attribution.logoURL       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt;&lt;LogoURL&gt; | struct | If multiple, first one used. |
|       ...logoURL.width       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt;&lt;LogoURL&gt; | int | If multiple, first one used. Using attribute **width**. |
|       ...logoURL.height       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt;&lt;LogoURL&gt; | int | If multiple, first one used. Using attribute **height**. |
|       ...logoURL.format       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt;&lt;LogoURL&gt;&lt;Format&gt; | str | If multiple, first one used. |
|       ...logoURL.onlineRessource       | &lt;Capability&gt;&lt;Layer&gt;&lt;Attribution&gt;&lt;LogoURL&gt;&lt;OnlineRessource&gt; | str | If multiple, first one used. using attribute **xlink:href**. |
|       ...layer[n].authorityURL       | &lt;Capability&gt;&lt;Layer&gt;&lt;AuthorityURL&gt; | struct list |  |
|       ...authorityURL[n].name       | &lt;Capability&gt;&lt;Layer&gt;&lt;AuthorityURL&gt; | str | If multiple, first one used. Using attribute **name**. |
|       ...authorityURL[n].onlineRessource       | &lt;Capability&gt;&lt;Layer&gt;&lt;AuthorityURL&gt;&lt;OnlineRessource&gt; | str | If multiple, first one used. |
|       ...layer[n].identifier       | &lt;Capability&gt;&lt;Layer&gt;&lt;Identifier&gt; | struct list |  |
|       ...identifier[n].id       | &lt;Capability&gt;&lt;Layer&gt;&lt;Identifier&gt; | str | Actual value enclosed in **Identifier** tag  |
|       ...identifier[n].authority       | &lt;Capability&gt;&lt;Layer&gt;&lt;Identifier&gt; | str | If multiple, first one used. Using attribute **authority**.  |
|       ...layer[n].metadataURL       | &lt;Capability&gt;&lt;Layer&gt;&lt;MetadataURL&gt; | struct list |  |
|       ...metadataURL.type       | &lt;Capability&gt;&lt;Layer&gt;&lt;MetadataURL&gt; | str | If multple, first one used. Using attribute **type** |
|       ...metadataURL.format       | &lt;Capability&gt;&lt;Layer&gt;&lt;MetadataURL&gt;&lt;Format&gt; | str | If multple, first one used. |
|       ...metadataURL.onlineRessource       | &lt;Capability&gt;&lt;Layer&gt;&lt;MetadataURL&gt;&lt;OnlineRessource&gt; | str | If multple, first one used. Using attribute **xlink:href**. |
|       ...layer[n].dataURL       | &lt;Capability&gt;&lt;Layer&gt;&lt;DataURL&gt; | struct | If multple, first one used. |
|       ...dataURL.format       | &lt;Capability&gt;&lt;Layer&gt;&lt;DataURL&gt;&lt;Format&gt; | str | If multple, first one used. |
|       ...dataURL.onlineRessource       | &lt;Capability&gt;&lt;Layer&gt;&lt;DataURL&gt;&lt;OnlineRessource&gt; | str | If multple, first one used. Using attribute **xlink:href**. |
|       ...layer[n].featureListURL       | &lt;Capability&gt;&lt;Layer&gt;&lt;FeatureListURL&gt; | struct | If multple, first one used. |
|       ...featureListURL.format       | &lt;Capability&gt;&lt;Layer&gt;&lt;FeatureListURL&gt;&lt;Format&gt; | str | If multple, first one used. |
|       ...featureListURL.onlineRessource       | &lt;Capability&gt;&lt;Layer&gt;&lt;FeatureListURL&gt;&lt;OnlineRessource&gt; | str | If multple, first one used. Using attribute **xlink:href**. |
|       ...layer[n].minScaleDenominator       | &lt;Capability&gt;&lt;Layer&gt;&lt;MinScaleDenominator&gt; | float | If multple, first one used. |
|       ...layer[n].maxScaleDenominator       | &lt;Capability&gt;&lt;Layer&gt;&lt;MaxScaleDenominator&gt; | float | If multple, first one used. |
|       ...layer[n].dimension       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | struct list |  |
|       ...dimension[n].name       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using **name** attribute. |
|       ...dimension[n].units       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using **units** attribute. |
|       ...dimension[n].unitSymbol       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using **unitSymbol** attribute. |
|       ...dimension[n].default       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using **default** attribute. |
|       ...dimension[n].multipleValues       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using **multipleValues** attribute. |
|       ...dimension[n].nearestValue       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using **nearestValue** attribute. |
|       ...dimension[n].current       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using **current** attribute. |
|       ...dimension[n].extent       | &lt;Capability&gt;&lt;Layer&gt;&lt;Dimension&gt; | str | If multiple, first one used. Using value of **Dimension** tag. |

Inheritance of layers properties is manage with the folowing:

| Element | Inheritance |
| ------- | ----------- |
| Layer   | No          |
| Name    | No          |
| Title   | No          |
| Abstract | No         |
| KeywordList | No      |
| Style   | Add         |
| CRS     | Add         |
| EX_GeographicBoundingBox| Replace |
| BoundingBox | Replace |
| Dimension | Replace   |
| Attribution | Replace |
| AuthorityURL | Add    |
| Identifier | No       |
| MetadataURL | No      |
| DataURL | No          |
| FeatureListURL | No   |
| MinScaleDenominator | Replace |
| MaxScaleDenominator | Replace |
| Layer attributes | Replace |


If you want to have the list of the layer name you can call the `getLayers` method.

e.g.
``` python
layers = getCapRes.getLayers()
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
