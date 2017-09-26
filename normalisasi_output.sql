CREATE TABLE "public"."master_outlet_jkt_cluster_final" (
"ID" bigserial,
"DayID" varchar(255) COLLATE "default",
"FSRCode" varchar(255) COLLATE "default",
"FSRName" varchar(255) COLLATE "default",
"cust_id" varchar(255) COLLATE "default",
"LNG" float8,
"LAT" float8,
"FSRArea" varchar(255) COLLATE "default",
"Cluster" varchar(255) COLLATE "default",
"di_id" varchar(255) COLLATE "default"
)

insert into master_outlet_jkt_cluster_final
("DayID", "FSRCode", "FSRName", cust_id, "LNG", "LAT", "ID")
select day, collector_id, collector_name, dest_id, dest_lon, dest_lat, id
from tb_routing_suggestion

create sequence master_outlet_sdn start 1;

update master_outlet_jkt_cluster_final
set "Cluster" = a.seq
from
(SELECT nextval('master_outlet_sdn') as seq, id, collector_name, collector_id, day
FROM (SELECT id, collector_name, collector_id, day,
ROW_NUMBER() OVER (partition BY collector_name, collector_id, day ORDER BY id) AS rnum
FROM tb_routing_suggestion) t
WHERE t.rnum = 1) a
where cast("FSRCode" as bigint) = a.collector_id
and "DayID" = a.day;

update master_outlet_jkt_cluster_final
set "FSRArea" = 'D312'