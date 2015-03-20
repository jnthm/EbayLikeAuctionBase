-- description: <Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item>
PRAGMA foreign_keys = ON;
drop trigger if exists NextBidGtPrevBid;
