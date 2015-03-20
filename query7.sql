select count(distinct Category) from ItemCategory I where I.ItemID in (select ItemID from BidderInfo where Amount>100);
