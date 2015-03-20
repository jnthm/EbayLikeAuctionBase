-- description: <No auction may have a bid before its start time or after its end time>
PRAGMA foreign_keys = ON;
drop trigger if exists BidBeforeStart;
drop trigger if exists BidBeforeEnds;
