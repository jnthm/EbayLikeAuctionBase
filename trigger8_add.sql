-- description: <The Current Price of an item must always match the Amount of the most recent bid for that item>
PRAGMA foreign_keys = ON;
drop trigger if exists CurrPriceEqMostRcntBidAfterInsert;
drop trigger if exists CurrPriceEqMostRcntBidAfterDeleteCase1;
drop trigger if exists CurrPriceEqMostRcntBidAfterDeleteCase2;

create trigger CurrPriceEqMostRcntBidAfterInsert
         after insert ON BidderInfo
         for each row
         begin
 	      update BidInfo set Currently = New.Amount where BidInfo.ItemID = New.ItemID and not exists 
	      -- making sure the new.amount is > all of the existing bids
	      (select * from BidderInfo Bidder where Bidder.ItemID = New.ItemID and Bidder.Amount > New.Amount);
	 end;	 

create trigger CurrPriceEqMostRcntBidAfterDeleteCase1
         after delete ON BidderInfo
         for each row
         -- sub-query for Number_of_Bids > 0
	 when ((select count(B.ItemID) from BidderInfo B where B.ItemID = Old.ItemID)>0)
         begin
	 -- two cases on a delete
	 -- case1: at least one bid remaining after the deletion, and so maxBid is the Currently value.
	   update BidInfo set Currently = 
	   (select max(Amount) from BidderInfo where (ItemID = Old.ItemID)) where BidInfo.ItemID = Old.ItemID;
	 end;
	      
create trigger CurrPriceEqMostRcntBidAfterDeleteCase2
         after delete ON BidderInfo
         for each row
	 when ((select count(B.ItemID) from BidderInfo B where B.ItemID = Old.ItemID)=0)
         begin

   	 -- whenever a deletion happens, not relying on the update of Number of Bids. 
	 -- So, calculating the NumberOfBids myself.
	 -- case2: no bids remaining, and so the FirstBid value is the currently value.
	   update BidInfo set Currently = (select FirstBid from ItemInfo where ItemID = Old.ItemID) where BidInfo.ItemID = Old.ItemID;
	 end;
