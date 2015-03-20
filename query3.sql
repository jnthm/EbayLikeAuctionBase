select count(ItemID) from (select ItemID, count(*) as Cnt from ItemCategory group by ItemID having Cnt=4);
