-- description: <In every auction, the Number of Bids attribute corresponds to the actual number of bids for that particular item>
PRAGMA foreign_keys = ON;
drop trigger if exists NumBidsAfterInsert;
drop trigger if exists NumBidsAfterDel;
drop trigger if exists CheckNumBidsBeforeInsert;

create trigger NumBidsAfterInsert
         after insert ON BidderInfo
         for each row
         begin
 	      update BidInfo set Number_of_Bids = (select count(B.ItemID) from BidderInfo B where B.ItemID = New.ItemID) where BidInfo.ItemID = New.ItemID;
	 end;

create trigger NumBidsAfterDel
         after delete ON BidderInfo
         for each row
         begin
 	      update BidInfo set Number_of_Bids = (select count(B.ItemID) from BidderInfo B where B.ItemID = Old.ItemID) where BidInfo.ItemID = Old.ItemID;
	 end;
/*
-- checking before inserting bids whether the NumBids matches correctly with the outstanding bids.
-- this probably is not necessary for submission purposes.
create trigger CheckNumBidsBeforeInsert
         before insert ON BidderInfo
         for each row
	 when ((select count(B.ItemID) from BidderInfo B where B.ItemID = New.ItemID) <> (select Number_of_Bids from BidInfo))
         begin
 	      select raise(abort, 'NumOfBids attribute does not tally');
	 end;
-- following INSERT must fail.
-- insert into BidderInfo values(1043495702,'watchdenmark','2001-12-08 07:20:08',22.01);
*/
