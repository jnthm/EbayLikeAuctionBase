/* SELECT statement verifying Referential Integrity constraint #2 */
select 'Not Empty for Constraint2 ItemInfo' from ItemInfo where SellerUserID not in (select UserID from UserInfo);
select 'Not Empty for Constraint2 BidderInfo' from BidderInfo where BidderUserID not in (select UserID from UserInfo);

/* SELECT statement verifying Referential Integrity constraint #4 */
select 'Not Empty for Constraint4 BidInfo' from BidInfo where ItemID not in (select ItemID from ItemInfo);
select 'Not Empty for Constraint4 BidderInfo' from BidderInfo where ItemID not in (select ItemID from ItemInfo);

/* SELECT statement verifying Referential Integrity constraint #5 */
select 'Not Empty for Constraint5' from ItemCategory where ItemID not in (select ItemID from ItemInfo);

/*
 SELECT statement verifying Trigger constraint #8 
-- no need to submit this
select 'Loaded DB doesnot adhere to constraint 8' from 
       (select max(Amount) as maxAmount, Currently as Curr 
       from BidInfo Bid, BidderInfo Bidder where Bid.ItemID = Bidder.ItemID group by Bid.ItemID) where maxAmount <> Curr;
*/
