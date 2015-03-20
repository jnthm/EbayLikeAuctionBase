-- description: <No auction may have a bid before its start time or after its end time>
PRAGMA foreign_keys = ON;
drop trigger if exists BidBeforeStart;
drop trigger if exists BidBeforeEnds;

create trigger BidBeforeStart
         after insert ON BidderInfo
         for each row
	 when New.Time < (select Started from ItemInfo where ItemID = New.ItemID)
         begin
	      select raise(rollback, 'Constraint violated - Inserted bid is before the start time');
	 end;	 

create trigger BidAfterEnds
         after insert ON BidderInfo
         for each row
	 when New.Time > (select Ends from ItemInfo where ItemID = New.ItemID)
         begin
	      select raise(rollback, 'Constraint violated - Inserted bid is after the end time');
	 end;	 
