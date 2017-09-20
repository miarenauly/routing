#   Point Model 

# Permutasi Titik
def point_permutation():
    sql = """
              INSERT  INTO tb_route_directions (ori_id, ori_lat, ori_lon, dest_id, dest_lat, dest_lon, cluster_code,
              distance, duration, polyline, flagging, bot_flags)
              SELECT a.outlet_id AS ori_id ,a.latitude AS ori_lat ,a.longitude AS ori_lon,
              b.outlet_id AS dest_id, b.latitude AS dest_lat ,b.longitude AS dest_lon ,
              a.sales_id AS cluster_code , NULL AS distance, NULL AS duration, NULL AS polyline, 'A' AS flagging, 'Q' AS bot_flags
              FROM tb_points AS a CROSS JOIN tb_points AS b
              WHERE a.sales_id =  b.sales_id  AND a.outlet_id != b.outlet_id
    """
    return sql

def del_depo_dest():
    sql = """
    DELETE from tb_route_directions
    WHERE dest_id = '1'
    """
    return sql

# Update Rute Balik menjadi B
def update_route_b():
    sql = """
          UPDATE tb_route_directions a
          SET flagging = 'B'
          FROM
          (
           SELECT  a.outlet_id AS ori_id,   b.outlet_id AS dest_id      
           FROM tb_points AS a     
           INNER JOIN tb_points AS b ON a.outlet_id < b.outlet_id 
           WHERE a.sales_id =  b.sales_id AND a.outlet_id != b.outlet_id           
           GROUP BY ori_id, dest_id
           ) b 
          WHERE a.ori_id = b.ori_id and a.dest_id = b.dest_id
    """
    return sql

# Update Rute Balik menjadi C
def update_route_c():
    sql = """
    UPDATE tb_route_directions AS r 
    SET distance = b.distance, duration = b.duration, polyline = b.polyline ,time_flags= b.time_flags, flagging = 'C' 
    FROM
          (
           SELECT ori_id,dest_id,distance,duration,polyline,time_flags 
           FROM tb_route_directions
           WHERE flagging = 'D'
           ) AS b  
    WHERE ((b.dest_id = r.ori_id) AND b.ori_id = r.dest_id) and r.flagging = 'B' 
    """
    return sql

# Update Rute To D
def update_route_d(data,ori,dest):
    sql = """
          UPDATE tb_route_directions
          SET distance = '%s',
          duration = '%s',
          polyline = '%s',
          flagging = 'D',
          time_flags='%s'
          WHERE ori_id = '%s'
          AND dest_id = '%s'
    """ %(data['distance'],data['duration'],data['polyline'],data['time'],ori,dest)
    return sql

# get data for crawling
def get_data_crawl(name):
    sql = """
       SELECT id,ori_id,ori_lat,ori_lon,dest_id,dest_lat,dest_lon
       FROM tb_route_directions
       WHERE distance is NULL
       AND duration is NULL
       AND polyline is NULL
       AND flagging = 'A'
       AND bot_flags = '%s'
       and cluster_code= '9'
       LIMIT 1000 
    """ %(name)
    return sql

# updating with bot_name
def updated_bot_name(name):
    sql = """
      UPDATE tb_route_directions
      SET bot_flags = '%s'
      WHERE
        id IN (
          SELECT
            id
          FROM
            tb_route_directions
          WHERE
            bot_flags = 'Q'
          LIMIT 1000
        )      
    """ %(name)
    return sql
