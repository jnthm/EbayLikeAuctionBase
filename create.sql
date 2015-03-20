drop table if exists ItemCategory;
drop table if exists ItemInfo;
drop table if exists BidInfo;
drop table if exists BidderInfo;
drop table if exists UserInfo;
drop table if exists CurrentTime;

create table ItemCategory(ItemID int, Category text, UNIQUE(ItemID, Category), FOREIGN KEY (ItemID) REFERENCES ItemInfo(ItemID));
create table ItemInfo(ItemID int PRIMARY KEY, Name text, Description text, SellerUserID int, Started text, Ends text, BuyPrice real, FirstBid real, FOREIGN KEY (SellerUserID) REFERENCES UserInfo(UserID), CHECK(Started < Ends));
create table BidInfo(ItemID int, Currently real, Number_of_Bids int, FOREIGN KEY (ItemID) REFERENCES ItemInfo(ItemID));
create table BidderInfo(ItemID int, BidderUserID, Time text, Amount real, UNIQUE(ItemID, Time), UNIQUE(ItemID, Amount), FOREIGN KEY (BidderUserID) REFERENCES UserInfo(UserID), FOREIGN KEY (ItemID) REFERENCES ItemInfo(ItemID));
create table UserInfo(UserID int PRIMARY KEY, Location text, Country text, Rating int);

create table CurrentTime(CurrTime text);
insert into CurrentTime values("2001-12-20 00:00:01");
select CurrTime from CurrentTime;
