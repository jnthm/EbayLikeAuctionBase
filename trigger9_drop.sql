-- description: <A user may not bid on an item he or she is also selling>
PRAGMA foreign_keys = ON;
drop trigger if exists SellerCantBidOnHisOwn;

