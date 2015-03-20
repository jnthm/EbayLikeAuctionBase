select ItemID from BidInfo where Currently in (select max(Currently) from BidInfo);
