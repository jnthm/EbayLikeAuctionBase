-- description: <The current time of your AuctionBase system can only advance forward in time, not backward in time>
PRAGMA foreign_keys = ON;
drop trigger if exists CurrTimeOnlyFrwrdUpdate;
drop trigger if exists CurrTimeOnlyFrwrdInsert;
drop trigger if exists CurrTimeOnlyFrwrdDel;
