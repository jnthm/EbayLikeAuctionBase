-- description: <In every auction, the Number of Bids attribute corresponds to the actual number of bids for that particular item>
PRAGMA foreign_keys = ON;
drop trigger if exists NumBidsAfterInsert;
drop trigger if exists NumBidsAfterDel;
drop trigger if exists CheckNumBidsBeforeInsert;
