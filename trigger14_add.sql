-- description: <Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item>
PRAGMA foreign_keys = ON;
drop trigger if exists NextBidGtPrevBid;

create trigger NextBidGtPrevBid
         before insert ON BidderInfo
         for each row
	 when (New.Amount <= (select Amount from BidderInfo where ItemID = New.ItemID and Time in (select max(Time) from BidderInfo where ItemID = New.ItemID)))
         begin	
	 	select raise(rollback, 'Inserton Failed - Inserted Bid Amount is not greater than the existing highest bid amount');
	 end;	 

-- the following insert must fail.
-- insert into BidderInfo values (1043495702, 'mrwvh', '2001-12-10 12:40:08', 27.00);


