-- description: <The Current Price of an item must always match the Amount of the most recent bid for that item>
PRAGMA foreign_keys = ON;
drop trigger if exists CurrPriceEqMostRcntBidAfterInsert;
drop trigger if exists CurrPriceEqMostRcntBidAfterDeleteCase1;
drop trigger if exists CurrPriceEqMostRcntBidAfterDeleteCase2;
