BEGIN TRANSACTION;
INSERT INTO customers VALUES(1,'John','Doe','john.doe@localhost.com','2018-10-11 08:16:18');
INSERT INTO customers VALUES(2,'Jean','Cousin','jean.cousin@localhost.com','2018-10-11 08:16:37');
INSERT INTO customers VALUES(3,'Tech','Master','tech.master@localhost.com','2018-10-11 08:17:37');
INSERT INTO zones VALUES(1,'Paris','[[48.52525,2.7114799999999377],[48.48635241323575,2.528786386718707],[48.471445041412174,2.3406225634764724],[48.49113,2.2197499999999764],[48.59989,1.9438499999999976],[48.836933955300736,1.9165120214843228],[48.95804986457497,1.885591552734354],[49.008659310870186,1.8766437402343854],[49.07825,2.0139299999999594],[49.07448395036218,2.215759746093795],[49.072516942721066,2.361284560546892],[49.068525885837325,2.447802724609346],[49.07713,2.563160000000039],[49.01694,2.6812600000000657],[48.87827,2.8048599999999624],[48.73830645398122,2.7368765087890097]]','2018-10-11 08:18:33');
INSERT INTO zones VALUES(2,'Lille','[[50.56339488780267,3.2145309448242188],[50.551943935854055,3.061237335205078],[50.62861220151879,2.9564380645751953],[50.679056768285434,3.0356597900390625],[50.72895820522394,3.100719451904297],[50.72542662601523,3.131532669067383],[50.73604772589882,3.1356096267700195],[50.73927975658645,3.1685256958007812],[50.69689257335114,3.2310104370117188],[50.5652485897902,3.2157325744628906],[50.56339488780267,3.2145309448242188]]','2018-10-11 08:20:29');
INSERT INTO drivers VALUES(1,'Jean','Michel','jean.michel@localdriver.com',1,'2018-10-11 08:21:24');
INSERT INTO drivers VALUES(2,'Xavier','Fine','xavier.fine@localdriver.com',1,'2018-10-11 08:22:03');
INSERT INTO drivers VALUES(3,'Mick','John','mick.john@localdriver.com',2,'2018-10-11 08:23:14');
INSERT INTO drivers VALUES(4,'Pope','Will','pope.will@localdriver.com',2,'2018-10-11 08:25:27');
INSERT INTO products VALUES(1,'Gasoil','2018-10-11 08:32:19');
INSERT INTO products VALUES(2,'SP 95','2018-10-11 08:32:34');
INSERT INTO products VALUES(3,'SP 98','2018-10-11 08:32:40');
INSERT INTO products_prices VALUES(1,1,1.5200000000000000177,'2018-10-11 08:32:19');
INSERT INTO products_prices VALUES(2,2,1.5500000000000000444,'2018-10-11 08:32:34');
INSERT INTO products_prices VALUES(3,3,1.580000000000000071,'2018-10-11 08:32:40');
INSERT INTO products_prices VALUES(4,1,1.5,'2018-10-11 08:33:47');
INSERT INTO products_prices VALUES(5,1,1.5300000000000000266,'2018-10-11 08:33:51');
INSERT INTO products_prices VALUES(6,1,1.5200000000000000177,'2018-10-11 08:33:58');
INSERT INTO products_prices VALUES(7,1,1.5400000000000000355,'2018-10-11 08:34:03');
INSERT INTO products_prices VALUES(8,2,1.5400000000000000355,'2018-10-11 08:34:49');
INSERT INTO products_prices VALUES(9,2,1.5100000000000000088,'2018-10-11 08:34:56');
INSERT INTO products_prices VALUES(10,2,1.580000000000000071,'2018-10-11 08:35:00');
INSERT INTO products_prices VALUES(11,2,1.5600000000000000532,'2018-10-11 08:35:05');
INSERT INTO products_prices VALUES(12,3,1.5700000000000000621,'2018-10-11 08:35:37');
INSERT INTO products_prices VALUES(13,3,1.6000000000000000888,'2018-10-11 08:35:40');
INSERT INTO products_prices VALUES(14,3,1.5900000000000000799,'2018-10-11 08:35:50');
INSERT INTO deliveries VALUES(1,1,1,1,'38 rue des gravilliers',48.86400059999999712,2.3562400000000001121,'2018-10-11 15:00:00',NULL,NULL,'2018-10-11 14:14:58');
INSERT INTO deliveries VALUES(2,2,1,1,'4 rue du temple',48.857480700000003536,2.3527301000000000463,'2018-10-11 15:00:00',NULL,NULL,'2018-10-11 14:15:18');
INSERT INTO deliveries VALUES(3,1,2,1,'12 rue franc sergent marly le roi',48.867710099999996488,2.0936878999999999351,'2018-10-12 10:00:00',NULL,NULL,'2018-10-11 14:15:59');
INSERT INTO deliveries VALUES(4,3,3,2,'36 rue augustin bourdon',50.666911800000001163,3.0716766999999998155,'2018-10-12 10:00:00',NULL,NULL,'2018-10-11 14:17:49');
INSERT INTO deliveries VALUES(5,3,3,2,'7 rue du touquet Marquette-lez-Lille',50.680497899999998878,3.0667002999999999346,'2018-10-15 13:00:00',NULL,NULL,'2018-10-11 14:21:26');
INSERT INTO deliveries_products VALUES(1,1,1,'Gasoil',1.5400000000000000355,'2018-10-11 14:14:58');
INSERT INTO deliveries_products VALUES(2,1,2,'SP 95',1.5600000000000000532,'2018-10-11 14:14:58');
INSERT INTO deliveries_products VALUES(3,1,3,'SP 98',1.5900000000000000799,'2018-10-11 14:14:58');
INSERT INTO deliveries_products VALUES(4,2,1,'Gasoil',1.5400000000000000355,'2018-10-11 14:15:18');
INSERT INTO deliveries_products VALUES(5,2,2,'SP 95',1.5600000000000000532,'2018-10-11 14:15:18');
INSERT INTO deliveries_products VALUES(6,2,3,'SP 98',1.5900000000000000799,'2018-10-11 14:15:18');
INSERT INTO deliveries_products VALUES(7,3,1,'Gasoil',1.5400000000000000355,'2018-10-11 14:15:59');
INSERT INTO deliveries_products VALUES(8,3,2,'SP 95',1.5600000000000000532,'2018-10-11 14:15:59');
INSERT INTO deliveries_products VALUES(9,3,3,'SP 98',1.5900000000000000799,'2018-10-11 14:15:59');
INSERT INTO deliveries_products VALUES(10,4,1,'Gasoil',1.5400000000000000355,'2018-10-11 14:17:49');
INSERT INTO deliveries_products VALUES(11,4,2,'SP 95',1.5600000000000000532,'2018-10-11 14:17:49');
INSERT INTO deliveries_products VALUES(12,4,3,'SP 98',1.5900000000000000799,'2018-10-11 14:17:49');
INSERT INTO deliveries_products VALUES(13,5,1,'Gasoil',1.5400000000000000355,'2018-10-11 14:21:26');
INSERT INTO deliveries_products VALUES(14,5,2,'SP 95',1.5600000000000000532,'2018-10-11 14:21:26');
INSERT INTO deliveries_products VALUES(15,5,3,'SP 98',1.5900000000000000799,'2018-10-11 14:21:26');
INSERT INTO deliveries_vehicles VALUES(1,1,1,'BMW Z3 Bleu - AS-123-TY',0.0,'2018-10-11 14:22:56');
INSERT INTO deliveries_vehicles VALUES(2,1,1,'Audi A6 Gris - AD-567-TV',0.0,'2018-10-11 14:23:19');
INSERT INTO deliveries_vehicles VALUES(3,2,5,'Audi TT Jaune - FG-127-DF',0.0,'2018-10-11 14:23:58');
INSERT INTO deliveries_vehicles VALUES(4,3,8,'Mini Cooper Noir - HH-627-SQ',0.0,'2018-10-11 14:24:43');
INSERT INTO deliveries_vehicles VALUES(5,3,8,'Dodge Challenger Noir - OI-712-LM',0.0,'2018-10-11 14:28:21');
INSERT INTO deliveries_vehicles VALUES(6,3,7,'Ford Ranger Blanc - TY-444-LF',0.0,'2018-10-11 14:28:52');
INSERT INTO deliveries_vehicles VALUES(7,4,10,'Ford Transit Blanc - GG-456-QX',0.0,'2018-10-11 14:30:20');
INSERT INTO deliveries_vehicles VALUES(8,4,11,'Peugeot 206 Gris - PE-206-OT',0.0,'2018-10-11 14:31:31');
INSERT INTO deliveries_vehicles VALUES(9,4,12,'Ford Mustang Jaune - FO-609-RD',0.0,'2018-10-11 14:32:26');
INSERT INTO deliveries_vehicles VALUES(10,4,12,'Chevrolet Camaro Rouge - CH-111-CA',0.0,'2018-10-11 14:32:56');
COMMIT;