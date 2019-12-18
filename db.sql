create database knowyourneighbors;

use knowyourneighbors;

CREATE TABLE SignUp_Details
(
	uid int NOT NULL AUTO_INCREMENT,
    username varchar(20) NOT NULL UNIQUE,
    pwd varchar(50) NOT NULL,
    signuptime datetime NOT NULL,
    PRIMARY KEY (uid)
);

INSERT INTO SignUp_Details VALUES
(1, 'rayin11', 'tettete', '2018-10-31 23:59:59'),
(2, 'ringoStarr1', 'tettetesahcjls1', '2018-10-05 13:00:00'),
(3, 'paulMacca', 'ipoifwpoj2', '2018-10-06 13:00:00'),
(4, 'theJohnLennon', 'ueuueueueu3', '2016-01-31 23:51:59'),
(5, 'GeoHarrison', 'bvbvbvbv4', '2013-12-30 23:59:59'),
(6, 'NeetuforApoo', 'ygsjhcba5', '2018-12-26 23:59:59'),
(7, 'Suchu', 'yqudajcv6', '2018-12-25 23:59:59'),
(8, 'rinkia', 'eteyqquaa7', '2018-12-22 23:59:59'),
(9, 'anjuuuuu', 'dahasdad8', '2018-12-12 23:59:59'),
(10, 'gary11', 'adacsdfdsfs9', '2018-12-17 23:59:59'),
(11, 'masterBlaster69', 'sdcsjqdnskc10', '2018-12-1 23:59:59'),
(12, 'abba', 'akjcbksjc', '2018-12-3 23:59:59'),
(13, 'harmoniumVituoso', 'uywuueueue', '2018-06-17 23:59:59'),
(14, 'goodForNothing', 'yyyyyyyyy', '2018-11-11 23:59:59'),
(15, 'fmlXOXO', 'wewewewewe', '2018-11-14 23:59:59'),
(16, 'mistermaster', 'yyessss', '2018-10-14 23:59:59');

CREATE TABLE Neighborood_Details
(
	nid int NOT NULL AUTO_INCREMENT,
    nname varchar(100) NOT NULL,
    maxlat decimal(9,6) NOT NULL,
    maxlong decimal(9,6) NOT NULL,
    minlat decimal(9,6) NOT NULL,
    minlong decimal(9,6) NOT NULL,
    PRIMARY KEY(nid)
);

INSERT INTO Neighborood_Details VALUES 
	(10, 'Bay Ridge', '40.63', '-74.02', '40.61', '-74.01' ),
    (11, 'Hells Kitchen', '40.65', '-73.99', '40.77', '-73.98' ),
    (12, 'Jamaica', '40.66', '-73.80', '40.72', '-73.76' ),
    (13, 'Parkchester', '40.82', '-74.02', '40.83', '-73.87' ),
    (14, 'Flatbush', '40.65', '-73.95', '40.95', '-73.94' ),
    (15, 'Long Island City', '40.73', '-73.96', '40.76', '-73.90' );
    
CREATE TABLE Block_Details
(
bid int NOT NULL AUTO_INCREMENT,
    bname varchar(100) NOT NULL,
    pincode int NOT NULL,
    nid int NOT NULL,
    endlat decimal(9,6) NOT NULL,
    endlong decimal(9,6) NOT NULL,
    startlat decimal(9,6) NOT NULL,
    startlong decimal(9,6) NOT NULL,
    PRIMARY KEY (bid),
    FOREIGN KEY (nid)
	REFERENCES Neighborood_Details (nid)
        ON DELETE CASCADE
);

INSERT INTO Block_Details VALUE
	(101, '59-37 80th St', 11209, 10, '40.63', '-74.03', '40.62', '-74.03'),
    (102, '7600-7698 3rd Ave', 11209, 10, '40.63', '-74.02', '40.62', '-74.03'),
    (103, '398-334 W 57th St', 10019, 11, '40.76', '-73.98', '40.62', '-74.03'),
    (104, 'South Jamaica', 11436, 12, '40.67', '-73.79', '40.68', '-74.79'),
    (105, 'Parkchester', 10462, 13, '40.63', '-74.03', '40.62', '-74.03'),
    (106, '1916 Benedict Ave', 10462, 14, '40.64', '-73.94', '40.72', '-73.81'),
    (107, '1203 Jackson Ave', '11101', 15, '40.75', '-73.96', '40.72', '-73.81');
    
Create table User_Info
(
	uid int NOT NULL,
    Fname varchar(20) NOT NULL,
    Lname varchar(20) NOT NULL,
    email varchar(50) NOT NULL,
    phone_number varchar(10) NOT NULL,
    apt_num varchar(20) NOT NULL,
    street varchar(50) NOT NULL,
    city varchar(20) NOT NULL,
    state varchar(20) NOT NULL,
    zip_code int NOT NULL,
    block_id int DEFAULT NULL,
    intro varchar(50) NOT NULL,
    photo blob,
    logout_time datetime DEFAULT NULL,
    email_preference boolean DEFAULT 0,
    FOREIGN KEY (uid)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE,
FOREIGN KEY (block_id)
REFERENCES Block_Details (bid)
        ON DELETE CASCADE
);

INSERT INTO User_Info VALUES
(1, "Indraneel", "Ray", "ir944@nyu.edu", 3476529125, "5713", "58th Street", "New York", "New York", 11220, 101, "The OG", NULL, NULL, NULL),
(2, "Ringo", "Starr", "ringo@beatles.com", 34765125, "577", "58th Street", "New York", "New York", 11209, 101, "Drummer", NULL, NULL, NULL),
(3, "Paul", "Mccartney", "paul@beatles.com", 3476529122, "776", "59th Street", "New York", "New York", 11209, 102, "Bassist", NULL, NULL, NULL),
(4, "John", "Lenon", "john@beatles.com", 1234567890, "4678", "59th Street", "New York", "New York", 11221, 102, "Rhythm Guitars", NULL, NULL, NULL),
(5, "George", "Harrison", "george@beatles.com", 2134567809, "543", "69th Street", "New York", "New York", 11221, 102, "Lead Guitar", NULL, NULL, NULL),
(6, "Nits", "Shin", "neetu@abc.com", 5555555555, "890", "57th Street", "New York", "New York", 10019, 103, "jnsckskdc", NULL, NULL, NULL),
(7, "Su", "Chu", "suchu@abc.com", 4567812345, "12", "57th Street", "New York", "New York", 10019, 103, "cskjb ckjsc sc", NULL, NULL, NULL),
(8, "Rin", "Kia", "rinkia@abc.com", 9876543213, "632", "36th Street", "New York", "New York", 11436, 104, "jcsb. sdnc ", NULL, NULL, NULL),
(9, "An", "Jan", "anju@abc.com", 5627124538, "421", "34th Street", "New York", "New York", 11436, 104, "hwhvcs", NULL, NULL, NULL),
(10, "Gary", "Neville", "gnev@abc.com", 6231972439, "265", "43th Street", "New York", "New York", 10462, 105, "nbxcw sckjhs cscs", NULL, NULL, NULL),
(11, "Sachin", "Tendulkar", "st@abc.com", 6182438152, "172", "41th Street", "New York", "New York", 10462, 105, "hvsj skss", NULL, NULL, NULL),
(12, "Jen", "Doe", "jd@abc.com", 8243612376, "1298", "9th Street", "New York", "New York", 10462, 106, "hd dj wss", NULL, NULL, NULL),
(13, "Abi", "Tin", "at@abc.com", 6342512349, "1938", "119th Street", "New York", "New York", 11101, 107, "ospwjx wjw pins ", NULL, NULL, NULL),
(14, "Mad", "Donna", "donna@abc.com", 7241528489, "42", "58th Street", "New York", "New York", 11220, 101, "djwsx sk sksl", NULL, NULL, NULL),
(15, "Donny", "Darko", "donnie@abc.com", 6132436152, "176", "58th Street", "New York", "New York", 11220, 101, "djskbj skukjs sdcs", NULL, NULL, NULL),
(16, "Max", "Planck", "max@abc.com", 6231425397, "1769", "89th Street", "New York", "New York", 11220, 102, "dwkjhsm skhss", NULL, NULL, NULL);


Create table User_Locality
(
	bid int NOT NULL,
    uid int NOT NULL,
    starttime datetime NOT NULL,
    endtime datetime DEFAULT NULL,
FOREIGN KEY (bid)
REFERENCES Block_Details (bid)
        ON DELETE CASCADE,
FOREIGN KEY (uid)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE
        
);


insert into User_Locality values
(101,1,'2019-1-18 04:12:28','2019-11-20 04:12:28'),
(101,3,'2019-11-19 14:02:30',null),
(102,1,'2019-11-24 04:12:38',null),
(101,4,'2019-11-20 08:12:28',null),
(101,6,'2019-11-21 04:12:28',null),
(101,2,'2019-11-26 16:12:28',null),
(102,7,'2019-11-30 04:12:28',null);


Create table Locality_Access_Request
(
    uid int NOT NULL,
    bid int NOT NULL,
    Request_status Enum('Approved','Declined','Pending') DEFAULT 'Pending',
    IsActive boolean DEFAULT 1,
    FOREIGN KEY (uid)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE,
FOREIGN KEY (bid)
REFERENCES Block_Details (bid)
        ON DELETE CASCADE
);

insert into Locality_Access_Request values
(1,101,'Approved',0),
(3,101,'Approved',1),
(1,102,'Approved',1),
(4,101,'Approved',1),
(6,101,'Approved',1),
(2,101,'Approved',1),
(5,101,'Pending',1),
(7,102,'Approved',1),
(5,102,'Declined',0),
(7,101,'Declined',0);

#If user is first in neighborhood, they are approved
Create table Locality_Approval
(
	uid int NOT NULL,
    requestor_id int NOT NULL,
    bid int NOT NULL,
    Approval_Status Enum('Approved','Declined','Pending') DEFAULT 'Pending',
    FOREIGN KEY (uid)
		REFERENCES User_Locality (uid)
        ON DELETE CASCADE,
	FOREIGN KEY (requestor_id)
		REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE,
	FOREIGN KEY (bid)
		REFERENCES User_Locality (bid)
        ON DELETE CASCADE
);

insert into Locality_Approval values
(1,1,101,'Approved'),
(1,3,101,'Approved'),
(1,1,102,'Approved'),
(3,4,101,'Approved'),
(3,6,101,'Approved'),
(4,6,101,'Approved'),
(3,2,101,'Approved'),
(4,2,101,'Approved'),
(6,2,101,'Approved'),
(3,5,101,'Pending'),
(4,5,101,'Pending'),
(6,5,101,'Approved'),
(2,5,101,'Declined'),
(1,7,102,'Approved'),
(7,5,102,'Approved'),
(1,5,102,'Declined'),
(2,7,101,'Approved');

select * from Locality_Approval;

Create table Friend_Request
(
uid_requestor int NOT NULL,
    friendId int NOT NULL,
    Request_status Enum('Approved','Declined','Pending') DEFAULT 'Pending',
    FOREIGN KEY (uid_requestor)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE,
FOREIGN KEY (friendId)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE
);

insert into Friend_Request values 
(1, 2, 'Pending'),
(2, 3, 'Approved'),
(3, 4, 'Approved'),
(1, 4, 'Declined');

insert into Friend_Request values 
(11, 12, 'Pending');

select * from Friend_Request;

Create table Friendship
(
	uid int NOT NULL,
    FriendId int NOT NULL,
	starttime datetime NOT NULL,
    endtime datetime DEFAULT NULL,
    FOREIGN KEY (uid)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE,
FOREIGN KEY (FriendId)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE
);

INSERT INTO FRIENDSHIP VALUES
(2, 3, '2019-11-20 04:12:28', NULL),
(11, 13, '2019-11-20 04:12:28', NULL),
(12, 15, '2019-11-20 04:12:28', NULL),
(16, 9, '2019-11-20 04:12:28', NULL),
(7, 13, '2019-11-20 04:12:28', NULL),
(12, 13, '2019-11-20 04:12:28', '2019-11-22 04:12:28'),
(12, 13, '2019-11-24 04:12:28', NULL);
INSERT INTO FRIENDSHIP VALUES
(11, 12, '2019-11-27 04:12:28', NULL);

select * from FRIENDSHIP;


Create table Neighbors
(
uid int NOT NULL,
    NeighborId int NOT NULL,
    starttime datetime NOT NULL,
    endtime datetime DEFAULT NULL,
    FOREIGN KEY (uid)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE,
FOREIGN KEY (NeighborId)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE
);

INSERT INTO Neighbors VALUES
(1, 2, '2019-11-20 04:12:28', '2019-11-20 14:12:28'),
(3, 4, '2019-11-20 14:12:28', NULL);

select * from neighbors;

Create table MessageThreads
(
tid int AUTO_INCREMENT,
    Created_By int NOT NULL,
    Title varchar(50) NOT NULL,
    Description_Msg varchar(200),
    Created_Time datetime NOT NULL,
    Access_Level Enum('f','n','b','h'),
    PRIMARY KEY (tid),
    FOREIGN KEY (Created_By)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE
);

/*
f -> friend
n -> neighbor
b -> block
h -> hood
*/

insert into MessageThreads(Created_By,Title,Description_Msg,Created_Time,Access_Level) values (4,'Want to start a band','I am a guitarist looking for 3 more guys to make music.','2019-12-03 06:15:00','h');
insert into MessageThreads(Created_By,Title,Description_Msg,Created_Time,Access_Level) values (1,'Dirt on the roads','Kindly keep the streets clean.','2019-12-03 01:15:00','b');
insert into MessageThreads(Created_By,Title,Description_Msg,Created_Time,Access_Level) values (3,'Lets party','I just moved in. Lets catch up!','2019-12-13 16:15:00','n');
insert into MessageThreads(Created_By,Title,Description_Msg,Created_Time,Access_Level) values (2,'I am your friend','Lets talk like friends.','2019-11-03 04:15:00','n');
insert into MessageThreads(Created_By,Title,Description_Msg,Created_Time,Access_Level) values (5,'Lets go camping upstate','plan with me.','2019-11-23 04:15:00','f');


select * from MessageThreads;

Create table ThreadComments
(
	CommentId int AUTO_INCREMENT,
	tid int NOT NULL,
    Comment_Msg varchar(200) NOT NULL,
    Comment_By int NOT NULL,
    CommentTime datetime NOT NULL,
    PRIMARY KEY (CommentId),
    FOREIGN KEY (tid)
REFERENCES MessageThreads (tid)
        ON DELETE CASCADE,
FOREIGN KEY (Comment_By)
REFERENCES SignUp_Details (uid)
        ON DELETE CASCADE
);

insert into ThreadComments(CommentId,tid,Comment_Msg,Comment_By,CommentTime) values(1,1,'hi',3,'2019-12-03 05:13:00');
insert into ThreadComments(CommentId,tid,Comment_Msg,Comment_By,CommentTime) values(2,1,'Hello mister how do you do?',4,'2019-12-03 06:33:00');
insert into ThreadComments(CommentId,tid,Comment_Msg,Comment_By,CommentTime) values(3,1,'I am fine bro...',3,'2019-12-01 06:43:00');
insert into ThreadComments(CommentId,tid,Comment_Msg,Comment_By,CommentTime) values(4,2,'Happy thanksgiving',5,'2019-12-02 06:33:00');
insert into ThreadComments(CommentId,tid,Comment_Msg,Comment_By,CommentTime) values(5,3,'My random rant',6,'2019-12-04 06:33:00');

select * from ThreadComments;


#c11:
 #Sign up:
 Insert INTO SignUp_Details(uid,username,pwd,signuptime) VALUES (17,'jimmypage','abc@123',CURRENT_TIMESTAMP());
 
 select * from SignUp_Details;
 
# c13:
 #Create Profile : 
INSERT INTO User_Info VALUES (17, "Jimmy", "Page", "jimmy@ledzep.com", 930165125, "57", "18th Street", "New York", "New York", 11219, 106, "I am a new user", NULL, NULL, 1);
 
select * from User_Info;


# c14:
 #Edit Profile:
 UPDATE User_Info SET apt_num=2016 where uid=17;
 
 select * from user_info;
 
#c15
#Create a message thread.
insert into MessageThreads(Created_By,Title,Description_Msg,Created_Time,Access_Level) values (15,'Snow','I hate snow.','2019-11-23 04:15:00','f');

select * from  MessageThreads;
 
 
#c16
insert into ThreadComments(CommentId,tid,Comment_Msg,Comment_By,CommentTime) values(6,6,'Snow sucks',16,'2019-12-04 06:35:00');


#c17
select * from friendship;

select u.fname,u.lname from user_info u inner join neighbors n on u.uid= n.NeighborId where n.uid=1;

#c18

 select * from user_info;
 select * from user_locality;
 insert into user_locality values(102, 5, '2019-12-02 06:35:00', null);
 UPDATE User_Info SET logout_time='2019-12-04 06:35:00' where uid=5;
 
SET @Id := 5;
 create temporary table btemp (uid int);
 
 SELECT @logtime = logout_time from user_info where uid = @Id;
 insert into btemp
    select distinct uid from User_Locality u1 where bid=(select bid from User_Locality u2 where uid=@Id);
     
 select  t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.Comment_Msg,
 case when ( ifnull(t.Created_Time,0) >= ifnull(@logtime,0) or ifnull(c.CommentTime,0) >= ifnull(@logtime,0) ) 
 then 'New' ELSE 'Old' end as MsgType 
 from MessageThreads t 
 join btemp t1 on t.Created_By = t1.uid 
 left join ThreadComments c on t.tid = c.tid
 where t.Access_Level = 'b'
 order by 
 c.CommentTime desc, 
 t.Created_Time desc;
 
 select * from messageThreads;
 drop table btemp;
 

 
 create temporary table temp1 (bid int);
 insert into temp1
    select bid from User_Locality ul where uid=@ID;
	
 create temporary table temp2(hid int);
 
 insert into temp2
    select b.hid from temp1 t inner join Block_Details b on t.bid=b.bid;

 create temporary table temp3 (bid int);
 
 insert into temp3
	select b.bid from Block_Details b inner join temp2 on b.hid=temp2.hid;
	
 create temporary table temp4 (uid int);
	
 insert into temp4
	select ul.uid from User_Locality ul inner join temp3 on ul.bid=temp3.bid;
	

 
 
 
 create temporary table temp (tids int,starttime datetime, endtime datetime);

 insert into temp
    select distinct uid, starttime,endtime from friends where FriendId = @Id
    union 
    select distinct FriendId, starttime,endtime from friends where uid = @Id;
 
 (select t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.comment_msg,t2.endtime,commentID,commemtedBy, 
 from Thread t 
 join temp t5 on t.Created_By = t5.tids 
 left join Comments c on t.tid = c.tid
 where t.Access_Level = '2'
 and (case when t2.endtime is null then 1 else 
 (case when (t2.endtime >= t.Created_Time) then 1 else 0 end)
 end )= 1
 order by 
 c.CommentTime desc, 
 t.Created_Time desc) as ffeed;
 
 
 create temporary table temp (NeighborId int, starttime datetime, endtime datetime);
 insert into temp
    select distinct uid as NeighborId, starttime,endtime from Neighbors where NeighborId = @Id
    union 
    select distinct NeighborId,starttime,endtime from Neighbors where uid = @Id;
    
drop table temp;

create temporary table btemp (userid int);
 insert into btemp
    select distinct uid from User_Locality u1 where bid=(select bid from User_Locality u2 where uid=@Id);
    

 select * from btemp;
 
 
 create temporary table bfeed as (select  t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.comment_msg,commentID,comment_By
 from MessageThreads t 
 join btemp t1 on t.Created_By = t1.uid 
 left join ThreadComments c on t.tid = c.tid
 where t.Access_Level = 'b'
 order by 
 c.CommentTime desc, 
 t.Created_Time desc); 
 
 select * from bfeed;
 
 
 # friend
 SET @Id := 5;
create temporary table temp (tids int,starttime datetime, endtime datetime);
 SElECT @logtime = logout_time from User_Info where uid = @Id;

drop table temp;

 insert into temp
    select distinct uid, starttime,endtime from friendship where FriendId = @Id
    union 
    select distinct FriendId, starttime,endtime from friendship where uid = @Id;
    
    
select * from temp;
 
 select t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.comment_msg,t2.endtime,
 case when ( ifnull(t.Created_Time,0) >= ifnull(@logtime,0) or ifnull(c.CommentTime,0) >= ifnull(@logtime,0) ) 
 then 'New' ELSE 'Old' end as MsgType 
 from MessageThreads t 
 join temp t2 on t.Created_By = t2.tids 
 left join ThreadComments c on t.tid = c.tid
 where t.Access_Level = 'f'
 and (case when t2.endtime is null then 1 else 
 (case when (t2.endtime >= t.Created_Time) then 1 else 0 end)
 end )= 1
 order by 
 c.CommentTime desc, 
 t.Created_Time desc;
 drop table temp;

select t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.comment_msg
from MessageThreads t  join ThreadComments c on t.tid = c.tid
 where t.Access_Level = 'f';
 
 
 
 # hood
  SET @Id := 1;
create temporary table temp (tids int,starttime datetime, endtime datetime);
 SElECT @logtime = logout_time from User_Info where uid = @Id;
 
  insert into temp
    select distinct uid, starttime,endtime from friendship where FriendId = @Id
    union 
    select distinct FriendId, starttime,endtime from friendship where uid = @Id;
    
 select t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.comment_msg,t2.endtime,
 case when ( ifnull(t.Created_Time,0) >= ifnull(@logtime,0) or ifnull(c.CommentTime,0) >= ifnull(@logtime,0) ) 
 then 'New' ELSE 'Old' end as MsgType 
 from MessageThreads t 
 join temp t2 on t.Created_By = t2.tids 
 left join ThreadComments c on t.tid = c.tid
 where t.Access_Level = 'h'
 and (case when t2.endtime is null then 1 else 
 (case when (t2.endtime >= t.Created_Time) then 1 else 0 end)
 end )= 1
 order by 
 c.CommentTime desc, 
 t.Created_Time desc;
 drop table temp;
    
 select t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.comment_msg
from MessageThreads t  join ThreadComments c on t.tid = c.tid
 where t.Access_Level = 'h';
 
 
 create temporary table final  (
	select tid,title,description,created_at,comment_text,commentID,commemted_by
);
 
 
 create table t1(tid int,title varchar(20),description varchar(20),author int, comment_text varchar(20),comment_id int,comment_by int);
 
 insert into t1 values (1,'Accident','Flood',1,'oh my god!',6,1);
 
 select * from t1;
 

SET @Id := 1;
create temporary table temp (creator_id int,starttime datetime, endtime datetime);
 SElECT @logouttime = logout_time from User_Info where uid = @Id;
 
insert into temp
select distinct uid, starttime,endtime from friendship where FriendId = @Id
union     
select distinct FriendId, starttime,endtime from friendship where uid = 2;

 select t.tid,t.Title,t.Description_Msg,t.Created_Time,t.Access_Level,c.comment_msg,t2.endtime,
 case when ( ifnull(t.Created_Time,0) >= ifnull(@logtime,0) or ifnull(c.CommentTime,0) >= ifnull(@logtime,0) ) 
 then 'New' ELSE 'Old' end as MsgType 
 from MessageThreads t 
 join temp t2 on t.Created_By = t2.creator_id 
 left join ThreadComments c on t.tid = c.tid
 where t.Access_Level = 'f'
 and (case when t2.endtime is null then 1 else 
 (case when (t2.endtime >= t.Created_Time) then 1 else 0 end)
 end )= 1
 order by 
 c.CommentTime desc, 
 t.Created_Time desc;

 drop table temp;