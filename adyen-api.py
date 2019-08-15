import Adyen 
### NOTE! This libr import should be added to the Dev Resources pg listed below
### -- the code from referencing libr only works if you've imported the
### Adyen libr, of course. The pg overviews how to download, but doesn't 
### demonstrate/explicitly call out the importing of the libr

#From https://docs.adyen.com/development-resources/libraries#python
ady = Adyen.Adyen()
client = ady.client
client.xapikey = "TBD"
client.platform = "test"
