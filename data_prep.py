from sklearn.cluster import KMeans
import sys
sys.path.append('core')
import pgsqlib
sys.path.append('models')
import prep_records

def create_table():
    sql = prep_records.create_tb_sales()
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.create_tb_points()
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.create_tb_route_directions()
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.create_tb_suggestion()
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.create_tb_route_sales()
    print (sql)
    pgsqlib.execScalar(sql)


def clustering():
	data_constraint = [357,305]

	n = 0
	while n <= 11:
		sql = prep_records.select_first_cluster_id()
		res = pgsqlib.fetch(sql)
		ori_id = res[0][0]

		if n == 5 or n == 11:
			limit_constraint = data_constraint[1]
		else:
			limit_constraint = data_constraint[0]

		sql = prep_records.update_cluster_table(n, ori_id, limit_constraint)
		print(sql)
		pgsqlib.execScalar(sql)

		sql = prep_records.insert_depo(n)
		print(sql)
		pgsqlib.execScalar(sql)

		n += 1


def data_prep(master_outlet_clean, area_branch, m_salesman):
    create_table()

    sql = prep_records.create_outlet_table(master_outlet_clean)
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.update_error_outlet(master_outlet_clean)
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.update_error_branch(master_outlet_clean, area_branch)
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.insert_tb_points(master_outlet_clean)
    print (sql)
    pgsqlib.execScalar(sql)

    clustering()

    sql = prep_records.insert_fsr(m_salesman)
    print (sql)
    pgsqlib.execScalar(sql)

    sql = prep_records.update_fsr_ori()
    print (sql)
    pgsqlib.execScalar(sql)
    
data_prep('master_outlet_clean', 'area_branch', 'm_salesman')

     
