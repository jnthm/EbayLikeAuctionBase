-- description: <The current time of your AuctionBase system can only advance forward in time, not backward in time>
PRAGMA foreign_keys = ON;
drop trigger if exists CurrTimeOnlyFrwrdUpdate;
drop trigger if exists CurrTimeOnlyFrwrdInsert;
drop trigger if exists CurrTimeOnlyFrwrdDel;

create trigger CurrTimeOnlyFrwrdUpdate
         after update ON CurrentTime
         for each row
	 when (New.CurrTime < Old.CurrTime)
         begin	
	 	select raise(rollback, 'Update Failed - CurrentTime can not move backward in time');
	 end;	 

-- the following update must fail
-- update CurrentTime set CurrTime = '2001-12-20 00:00:00';

create trigger CurrTimeOnlyFrwrdInsert
         after insert ON CurrentTime
         for each row
         begin	
	 	select raise(rollback, 'Insert Failed - CurrTime can not have multiple values');
	 end;	 

-- the following insert must fail
-- insert into CurrentTime values('2001-12-20 00:00:02');

create trigger CurrTimeOnlyFrwrdDel
         after delete ON CurrentTime
         for each row
         begin	
	 	select raise(rollback, 'Delete Failed - CurrTime can not be deleted');
	 end;	 

-- the following delete must fail
-- delete from CurrentTime where CurrTime = '2001-12-20 00:00:02';
