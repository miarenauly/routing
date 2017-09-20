#   Constraints
def get_constraints(id_constraint):
    sql = """
          SELECT constraint_max_duration,
          constraint_max_route,
          constraint_max_distance,
          constraint_rest,
          constraint_stop
          FROM tb_constraint
          WHERE constraint_id = '%s'
    """ % (id_constraint)
    return sql

#GET ORI_ID
def get_ori_id():
    sql = """
        SELECT employee_id, employee_name, day, ori_id
        FROM tb_route_fc
        where flags = 'Q'
        limit 1
  """
    return sql

# GET ori & destination
def get_ori_dest(ori_id, day):
    sql = """
        SELECT 
         id,ori_id,ori_lat,ori_lon,
         dest_id,dest_lat,dest_lon,
         distance,duration,polyline
        FROM 
        (
         SELECT 
         id,ori_id,ori_lat,ori_lon,
         dest_id,dest_lat,dest_lon,
         distance,duration,polyline
         FROM tb_route_directions
         WHERE ori_id = '%s'
         AND route_flags = 'Q'
         AND duration is not null
         AND cluster_code = '%s'
         LIMIT 20
        ) t 
        ORDER BY duration ASC
        LIMIT 1
  """ % (ori_id, day)
    return sql

# Insert Point
def insertionPoints(employee_name, employee_id, day, ori_id, ori_lat, ori_lon, dest_id, dest_lat, dest_lon, distance, duration, polyline):
    sql = """
    INSERT INTO tb_routing_suggestion
    (collector_name,collector_id,day,ori_id,ori_lat,ori_lon,dest_id,dest_lat,dest_lon,distance,duration,polyline)
    VALUES('%s','%s',%s,'%s',%s,%s,'%s',%s,%s,%s,%s,'%s')
  """ % (employee_name, employee_id, day, ori_id, ori_lat, ori_lon, dest_id, dest_lat, dest_lon, distance, duration, polyline)
    return sql

# Insert Point Sales
def insertionPointSales(employee_name, employee_id, day, ori_id):
    sql = """
    INSERT INTO tb_route_fc
    (employee_name, employee_id, day, ori_id)
    VALUES('%s','%s','%s',%s)
  """ % (employee_name, employee_id, day, ori_id)
    return sql

#Update Point Sales
def updatePointSales(column, dest_ori, flag, employee_id, day):
    sql = """
    UPDATE tb_route_fc
    SET %s = '%s',
    flags = '%s'
    WHERE employee_id = '%s'
    and day = %s
  """ % (column, dest_ori, flag, employee_id, day)
    return sql

#Update Point Sales
def checkPointSales():
    sql = """
    SELECT * from tb_route_fc
    WHERE flags = 'Q'
  """
    return sql

# Update tb_route_directions destination flag
def update_route_flags(dest_id):
    sql = """
        UPDATE tb_route_directions
        SET route_flags = 'D' 
        WHERE dest_id = '%s'
  """ % (dest_id)
    return sql

#check duration
def get_durs(employee_id, day):
    sql = """
    SELECT sum(duration), count(*) 
    FROM tb_routing_suggestion
    WHERE collector_id=%s
    AND day = %s
  """ % (employee_id, day)
    return sql

#check distance
def get_diss(employee_id, day):
    sql = """
    SELECT sum(distance) 
    FROM tb_routing_suggestion
    WHERE collector_id=%s
    AND day = %s
  """ % (employee_id, day)
    return sql

#HANDLE tb_field_collector
def check_sales(status):
    sql = """
    SELECT employee_id, employee_name, employee_ori_id
    FROM tb_field_collector
    WHERE status='%s'
  """ % (status)
    return sql

def proc_sales_id():
    sql = """
    UPDATE tb_field_collector
    SET status = 'P'
    WHERE employee_id
    IN
    ( SELECT employee_id 
    FROM tb_field_collector
    WHERE status = 'Q'
    LIMIT 1)
  """ % ()
    return sql

def update_sales_status():
    sql = """
    UPDATE tb_field_collector
    SET status = 'Q'
    where status = 'D'
  """ % ()
    return sql

def update_sales_id(sales_id, sts_a, sts_b):
    sql = """
        UPDATE tb_field_collector
        SET status='%s'
        WHERE employee_id = '%s'
        AND status = '%s'
  """ % (sts_a, sales_id, sts_b)
    return sql

def len_sales():
    sql = """
        select count(*)
        from tb_field_collector
        where status = 'Q'
        """
    return sql