select count(distinct I.SellerUserID) from UserInfo U, ItemInfo I where I.SellerUserID = U.UserID and U.Rating>1000;
