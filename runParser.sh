rm -f UserInfo.Dat ItemCategory.Dat BidderInfo.Dat BidInfo.Dat ItemInfo.Dat
python myparser.py /usr/class/cs145/project/ebay_data/items-*.json

sort UserInfo.Dat | uniq >| UserInfo_temp.Dat
mv UserInfo_temp.Dat UserInfo.Dat

sort BidderInfo.Dat | uniq >| BidderInfo_temp.Dat
mv BidderInfo_temp.Dat BidderInfo.Dat

sort BidInfo.Dat | uniq >| BidInfo_temp.Dat
mv BidInfo_temp.Dat BidInfo.Dat

sort ItemInfo.Dat | uniq >| ItemInfo_temp.Dat
mv ItemInfo_temp.Dat ItemInfo.Dat

sort ItemCategory.Dat | uniq >| ItemCategory_temp.Dat
mv ItemCategory_temp.Dat ItemCategory.Dat
