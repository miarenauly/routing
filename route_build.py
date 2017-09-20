import sys
sys.path.append('core')
import pgsqlib
sys.path.append('models')
import route_records



def get_constraints(day):
    if day == 5 or day == 11:
        sql = route_records.get_constraints(2)
        print(sql)
        r = pgsqlib.fetch(sql)

        data = {
            "cons_dur": r[0][0],
            "cons_dis": r[0][2],
            "cons_rest": r[0][3],
            "cons_stop": r[0][4]
        }
    else:
        sql = route_records.get_constraints(1)
        print(sql)
        r = pgsqlib.fetch(sql)

        data = {
            "cons_dur": r[0][0],
            "cons_dis": r[0][2],
            "cons_rest": r[0][3],
            "cons_stop": r[0][4]
        }

    return data


def get_ori_id():
    sql = route_records.get_ori_id()
    print(sql)
    r = pgsqlib.fetch(sql)

    data = {
        "sales_id": r[0][0],
        "sales_name": r[0][1],
        "day": r[0][2],
        "ori_id": r[0][3]
    }

    return data


def get_ori(ori_id, day):
    ori = route_records.get_ori_dest(ori_id, day)
    print(ori)
    r = pgsqlib.fetch(ori)

    print(r)

    if len(r) == 0:
        data = {
        }
    else:
        data = {
            "id": r[0][0],
            "ori_id": r[0][1],
            "ori_lat": r[0][2],
            "ori_lon": r[0][3],
            "dest_id": r[0][4],
            "dest_lat": r[0][5],
            "dest_lon": r[0][6],
            "distance": r[0][7],
            "duration": r[0][8],
            "polyline": r[0][9]
        }

    return data


def check_sales(status):
    ori = route_records.check_sales(status)
    print(ori)
    res = pgsqlib.fetch(ori)
    if len(res) == 0:
        print("sales sudah ganti")
        sql = route_records.proc_sales_id()
        pgsqlib.execScalar(sql)
    else:
        pass


def get_sales():
    ori = route_records.check_sales('P')
    print(ori)
    r = pgsqlib.fetch(ori)

    data = {
        "sales_id": r[0][0],
        "sales_name": r[0][1],
        "ori_id": r[0][2]
    }

    return data


def update_sales_queue(dest_id, sales_id,day):
    ori = route_records.check_sales('Q')
    print(ori)
    res = pgsqlib.fetch(ori)
    print("len update sales %s" %len(res))
    if len(res) == 0:
        #update tb_route_fc
        sql = route_records.updatePointSales('dest_id', dest_id, 'D', sales_id, day)
        print(sql)
        pgsqlib.execScalar(sql)

        print ("all sales has been used")
    else:
        pass


def check_point_sales():
    sql = route_records.checkPointSales()
    data = pgsqlib.fetch(sql)
    print(data)
    data = data[0][1]
    if data == None:
        data = 0
    else:
        data = 1
    print(data)
    return data


def update_point_sales(dest_id, sales_id, day):
    # update last dest
    sql = route_records.updatePointSales('dest_id', dest_id, 'D', sales_id, day)
    print(sql)
    pgsqlib.execScalar(sql)

    if day <= 11:
        # get sales
        check_sales('P')

        sales = get_sales()

        new_sales_name = sales["sales_name"]
        new_sales_id = sales["sales_id"]
        new_ori_id = sales["ori_id"]
        print(new_sales_name, new_sales_id, new_ori_id)

        # insert point sales
        sql = route_records.insertionPointSales(
            new_sales_name, new_sales_id, day, new_ori_id)
        print(sql)
        pgsqlib.execScalar(sql)
    else:
        print("All day is done")


def get_diss(sales_id, day):
    sql = route_records.get_diss(sales_id, day)
    print(sql)
    data = pgsqlib.fetch(sql)
    diss = data[0][0]
    if diss == None:
        diss = 0
    else:
        pass
    print(diss)
    return diss


def get_durs(sales_id, day):
    sql = route_records.get_durs(sales_id, day)
    print(sql)
    data = pgsqlib.fetch(sql)
    durs = data[0][0]
    stop = data[0][1] * 600
    if durs == None:
        durs = 0
    else:
        durs += stop
    print("durs %s" % durs)
    return durs


def initiate_route(day):
    # update tb_sales status to process
    sql = route_records.proc_sales_id()
    print(sql)
    pgsqlib.execScalar(sql)

    sales = get_sales()
    sales_id = sales["sales_id"]
    sales_name = sales["sales_name"]
    ori_id = sales["ori_id"]

    sql = route_records.insertionPointSales(sales_name, sales_id, day, ori_id)
    print(sql)
    pgsqlib.execScalar(sql)

    recursive_extraction()


def recursive_extraction():
    #get sales detil
    sales = get_ori_id()

    sales_id = sales["sales_id"]
    sales_name = sales["sales_name"]
    ori_id = sales["ori_id"]
    day = sales["day"]

    if day <= 11:
        try:
            # get route suggestion
            route = get_ori(ori_id, day)

            ori_id = route["ori_id"]
            ori_lat = route["ori_lat"]
            ori_lon = route["ori_lon"]
            dest_id = route["dest_id"]
            dest_lat = route["dest_lat"]
            dest_lon = route["dest_lon"]
            distance = route["distance"]
            duration = route["duration"]
            polyline = route["polyline"]

            # check constraint
            durs = get_durs(sales_id, day)
            diss = get_diss(sales_id, day)

            durs += duration
            print("durs ditambah duration is %s" % durs)
            diss += distance

            cons = routes_constraint(durs, diss, day)

            enough = cons["enough"]
            print("enough is %s" % enough)
            durs = cons["durs"]
            print("durs ditambah stop is %s" % durs)
            diss = cons["diss"]

        except KeyError:
            print ("keyError")
            enough = "yes"

        if enough != "yes":
            print((sales_name, sales_id, day, ori_id, ori_lat,
                   ori_lon, dest_id, dest_lat, dest_lon, distance, duration, polyline))
            sql = route_records.insertionPoints(sales_name, sales_id, day, ori_id, ori_lat,
                                                ori_lon, dest_id, dest_lat, dest_lon, distance, duration, polyline)
            print(sql)
            pgsqlib.execScalar(sql)

            # update flag tb_route_direction
            sql = route_records.update_route_flags(ori_id)
            print(sql)
            pgsqlib.execScalar(sql)

            #update tb_route_sales
            sql = route_records.updatePointSales('dest_id', dest_id, 'D', sales_id, day)
            print(sql)
            pgsqlib.execScalar(sql)

            sql = route_records.updatePointSales('ori_id', dest_id, 'Q', sales_id, day)
            print(sql)
            pgsqlib.execScalar(sql)

            #repeat the process
            recursive_extraction()
        else:
            #update status one sales_id to done
            sql = route_records.update_sales_id(sales_id, 'D', 'P')
            print(sql)
            pgsqlib.execScalar(sql)

            #update flag tb_route_direction
            sql = route_records.update_route_flags(ori_id)
            print(sql)
            pgsqlib.execScalar(sql)

            #update bulk tb_sales status
            update_sales_queue(ori_id, sales_id, day)

            #insert new point
            update_point_sales(ori_id, sales_id, day)

            print("Done processing sales id %s, day %s" % (sales_id, day))
    else:
        print ("all day is done")


def routes_constraint(duration, distance, day):
    cons_max = get_constraints(day)

    hts = cons_max["cons_stop"]
    print ("hts is %s" %hts)
    hth = cons_max["cons_dur"]
    htd = cons_max["cons_dis"]

    enough = "no"

    tdur = 0 + duration
    print ("tdur is %s" %tdur)

    tdis = 0 + distance
    if hts > 0:
        tdur = duration + hts
        print ("tdur ditambah stop %s" %tdur)

    if hth > 0:
        if tdur > hth:
            enough = "yes"
        else:
            enough = "no"

    if htd > 0:
        if tdis > htd:
            enough = "yes"
        else:
            enough = enough

    objects = {
        "enough": enough,
        "durs": tdur,
        "diss": tdis,
        "stop": hts
    }
    return objects


def main():
    day = 0
    while day <= 11:
        print ("day is %s" %day)
        try:
            initiate_route(day) 
            while check_point_sales() > 0:
                recursive_extraction()
        except IndexError:
            pass
        day +=1
        #update tb_field_collector
        sql = route_records.update_sales_status()
        print(sql)
        pgsqlib.execScalar(sql)

main()