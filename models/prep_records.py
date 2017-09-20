def create_tb_points():
	sql = '''CREATE TABLE tb_points (
	point_id serial,
	sales_id varchar(255),
	outlet_id varchar(255),
	latitude float,
	longitude float,
	score int
	)'''
	return sql


def create_tb_sales():
	sql = '''CREATE TABLE tb_field_collector (
	br_id varchar (10),
	fc_id serial,
	employee_id varchar(255),
	employee_name varchar(255),
	employee_address varchar(255),
	employee_ori_id varchar(100) DEFAULT '1'::character varying,
	employee_lat float,
	employee_lng float,
	pr_id int,
	di_id int,
	su_id int,
	status varchar(1) DEFAULT 'Q'::character varying
	)'''
	return sql

def create_tb_route_sales():
	sql = ''' CREATE TABLE tb_route_fc
	(br_id varchar(10),
	employee_name varchar(35),
	employee_id varchar (35),
	day int,
	ori_id varchar(50),
	dest_id varchar(50),
	flags VARCHAR(1) DEFAULT 'Q'::VARCHAR,
	id bigserial
	);'''
	return sql


def create_tb_suggestion():
	sql = '''CREATE TABLE tb_routing_suggestion (
	collector_name varchar(35),
	collector_id bigint,
	day int,
	ori_id varchar(50),
	dest_id varchar(50),
	ori_lat float,
	ori_lon float,
	dest_lat float,
	dest_lon float,
	distance float,
	duration float,
	polyline text,
	plan_date_from date,
	plan_date_to date,
	flags timestamp(6) DEFAULT now(),
	id bigserial
	);'''
	return sql

def create_tb_route_directions():
	sql = '''CREATE TABLE tb_route_directions (
		id bigserial,
		ori_id varchar(255),
		ori_lat double precision,
		ori_lon double precision,
		ori_score int,
		dest_id varchar(255),
		dest_lat double precision,
		dest_lon double precision,
		dest_score int,
		cluster_code varchar(20),
		distance double precision,
		duration double precision,
		polyline text,
		flagging varchar (1) DEFAULT 'A'::character varying,
		route_flags varchar (1) DEFAULT 'Q'::character varying,
		time_flags timestamp(6) DEFAULT now(),
		bot_flags varchar(20) DEFAULT 'Q'::character varying
		)'''
	return sql


def create_outlet_table(master_outlet_clean):
	sql = '''CREATE TABLE %s as
		select *, 'Q'::varchar(1) as flag
		from %s;
		''' % (master_outlet_clean + '_cluster', master_outlet_clean)
	return sql


def update_error_outlet(master_outlet_clean):
	sql = """update %s
		set flag = 'E'
		WHERE longitude is null or latitude is null
		or longitude = 0 or latitude = 0;
		""" % (master_outlet_clean + '_cluster')
	return sql

def update_error_branch(master_outlet_clean, area_branch):
	sql = """
		UPDATE {0}
		SET flag = 'E'
		WHERE customer_id not in (
		SELECT customer_id
		FROM {0} a
		JOIN {1} b
		ON ST_Intersects(b.geom_br,
		ST_SetSRID(st_makepoint(a.longitude, a.latitude), 4326))
		AND b.m_br_id = a.branch_id
		)
		and flag = 'Q';
		""" .format(master_outlet_clean + '_cluster', area_branch)
	return sql


def insert_tb_points(master_outlet_clean):
	sql = """
		INSERT INTO tb_points (outlet_id, longitude, latitude)
		select customer_id, longitude, latitude
		from %s
		where flag = 'Q';
		""" % (master_outlet_clean + '_cluster')
	return sql

def select_first_cluster_id():
	sql = """
	SELECT a.outlet_id as ori_id, a.longitude as ori_lon, a.latitude as ori_lat, 
	b.outlet_id as dest_id, b.longitude as dest_lon, b.latitude as dest_lat,
	ST_Distance(CAST(ST_SetSRID(ST_Point(a.longitude,a.latitude),4326) AS geography),
	CAST(ST_SetSRID(ST_Point(b.longitude,b.latitude),4326) AS geography)) AS air_distance
	FROM  tb_points a CROSS JOIN tb_points b
	WHERE a.outlet_id != b.outlet_id
	and a.sales_id is NULL
	and b.sales_id is null
	order by air_distance desc
	limit 1
	"""
	return sql

def update_cluster_table(cluster_code, ori_id, limit_constraint):
	sql = """ UPDATE tb_points
	set sales_id = %s
	where outlet_id in
	(select b.outlet_id
	from tb_points a,
	tb_points b
	where a.outlet_id = '%s'
	and a.sales_id is null
	and b.sales_id is null
	order by ST_Distance(CAST(ST_SetSRID(ST_Point(a.longitude,a.latitude),4326) AS geography),
	CAST(ST_SetSRID(ST_Point(b.longitude,b.latitude),4326) AS geography)) asc
	limit %s)
	""" % (cluster_code, ori_id, limit_constraint)
	return sql

def insert_depo(cluster_code):
	sql = """insert into tb_points (sales_id, outlet_id, latitude, longitude)
	        select %s, depo_id, depo_lat, depo_lng from tb_depo
	      """ % (cluster_code)
	return sql

def insert_fsr(m_salesman):
    sql = """
    insert into tb_field_collector (br_id, employee_id, employee_name)
    select m_br_id as br_id, m_slm_id as employee_id, m_slm_name as employee_name
    from %s
    where active = 1
    and type_name = 'FARMER'
    and m_br_id = 'D312'
    group by m_br_id, m_slm_id, m_slm_name
    """ % (m_salesman)
    return sql

def update_fsr_ori():
    sql = """
    UPDATE tb_field_collector
    SET employee_lat = a.depo_lat,
    employee_lng = a.depo_lng
   	FROM tb_depo a
    """ % ()
    return sql