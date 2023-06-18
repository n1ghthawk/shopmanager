# shopmanager
Manages Shop

# Prerequisites
* User must maintain PriceListMaster.csv by exporting pricelist supplied by manufacturer in pdf format.
* User must ensure proper item maps is maintained, to ensure spelling mistakes are taken care of.
* User must ensure Tally scripts are sending periodic reports to designated email id.

# How it works?
* First generate map for every new version of pricelist from manufacturer wrt tally processed stocklist.
* Generate pricelist with both manufacturer item name and mapped item name, if any. pricelist shall have a field for indicating weather name is mapped name.
* for each new tally report mail, generate json containing both tally stock items and manufacturer items. This merge is done on tally item column and mapped item name column. On items where tally item is not found in pricelist price shall be NA. On items where stock item is not found in tally, quantity shall be NA.
* This generated json shall be the data for android app. App shall also have provision to display pricelist alone, tally stock non-zero data alone and mask data alone.
