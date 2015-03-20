-- description: <All new bids must be placed at the time which matches the current time of your AuctionBase system>
PRAGMA foreign_keys = ON;
drop trigger if exists NewBidsAtCurrTimeOnly;
