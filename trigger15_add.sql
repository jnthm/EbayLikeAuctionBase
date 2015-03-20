-- description: <All new bids must be placed at the time which matches the current time of your AuctionBase system>
PRAGMA foreign_keys = ON;
drop trigger if exists NewBidsAtCurrTimeOnly;

create trigger NewBidsAtCurrTimeOnly
         after insert ON BidderInfo
         for each row
	 when (New.Time <> (select CurrTime from CurrentTime))
         begin	
	 	select raise(rollback, 'Inserton Failed - Inserted Bid Time is did not match the current time of the AuctionBase system');
	 end;	 

-- the following insert must fail.
-- insert into BidderInfo values (1043495702, 'mrwvh', '2001-12-20 00:00:00', 29.00);


