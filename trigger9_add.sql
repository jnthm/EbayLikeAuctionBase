-- description: <A user may not bid on an item he or she is also selling>
PRAGMA foreign_keys = ON;
drop trigger if exists SellerCantBidOnHisOwn;


create trigger SellerCantBidOnHisOwn
         after insert ON BidderInfo
         for each row
	 when New.BidderUserID = (select SellerUserID from ItemInfo I where I.ItemID = New.ItemID)
         begin
	      select raise(rollback, 'Constraint violated - Inserted bidder is also a seller on the same item');
	 end;	 
