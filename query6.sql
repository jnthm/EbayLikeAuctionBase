select count(distinct U.UserID) from BidderInfo B, UserInfo U, ItemInfo I where U.UserID = B.BidderUserID and U.UserID = I.SellerUserID;
