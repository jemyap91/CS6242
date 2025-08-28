########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error, Connection
import csv
from typing import Any
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

############### DO NOT MODIFY THIS SECTION ###########################
######################################################################
def create_connection(path: str) -> Connection:
    connection = None
    try:
        connection = sqlite3.connect(path)
        connection.text_factory = str
    except Error as e:
        print("Error occurred: " + str(e))

    return connection


def execute_query(connection: Connection, query: str) -> str:
    cursor = connection.cursor()
    try:
        if query == "":
            return "Query Blank"
        else:
            cursor.execute(query)
            connection.commit()
            return "Query executed successfully"
    except Error as e:
        return "Error occurred: " + str(e)


def execute_query_and_get_result(connection: Connection, query: str) -> Any:
    cursor = connection.execute(query)
    return cursor.fetchall()
######################################################################
######################################################################


def GTusername() -> str:
    gt_username = "jyap36"
    return gt_username


def part_1_a_i() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
        CREATE TABLE IF NOT EXISTS incidents (
                report_id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                date TEXT NOT NULL
        );
            """
    ######################################################################
    return query


def part_1_a_ii() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
        CREATE TABLE IF NOT EXISTS details (
                report_id TEXT PRIMARY KEY,
                subject TEXT,
                transport_mode TEXT,
                detection TEXT
        );
            """
    ######################################################################
    return query


def part_1_a_iii() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
        CREATE TABLE IF NOT EXISTS outcomes (
                report_id TEXT PRIMARY KEY,
                outcome TEXT,
                num_ppl_fined INTEGER,
                fine REAL,
                num_ppl_arrested INTEGER,
                prison_time REAL,
                prison_time_unit TEXT
        );
            """
    ######################################################################
    return query


def part_1_b_i(connection: Connection, path: str) -> None:
    ############### CREATE IMPORT CODE BELOW ###########################
    # csv_path = f"{path}/incidents.csv"

    with open(path, 'r') as file:
        contents = csv.reader(file)
        next(contents)
        insert_records = "INSERT INTO incidents (report_id, category, date) VALUES (?, ?, ?)"
        cursor = connection.cursor()
        cursor.executemany(insert_records, contents)
        connection.commit()
    pass
    ######################################################################


def part_1_b_ii(connection: Connection, path: str) -> None:
    ############### CREATE IMPORT CODE BELOW ############################
    # csv_path = f"{path}/details.csv"
    with open(path, 'r') as file:
        contents = csv.reader(file)
        next(contents)
        insert_records = "INSERT INTO details (report_id, subject, transport_mode, detection) VALUES (?, ?, ?, ?)"
        cursor = connection.cursor()
        cursor.executemany(insert_records, contents)
        connection.commit()
    pass
    ######################################################################


def part_1_b_iii(connection: Connection, path: str) -> None:
    ############### CREATE IMPORT CODE BELOW ############################
    # csv_path = f"{path}/outcomes.csv"
    with open(path, 'r') as file:
        contents = csv.reader(file)
        next(contents)
        insert_records = "INSERT INTO outcomes (report_id, outcome, num_ppl_fined, fine, num_ppl_arrested, prison_time, prison_time_unit) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor = connection.cursor()
        cursor.executemany(insert_records, contents)
        connection.commit()
    pass
    ######################################################################


def part_2_a() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "CREATE UNIQUE INDEX incident_index ON incidents (report_id)"
    ######################################################################
    return query


def part_2_b() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "CREATE UNIQUE INDEX detail_index ON details (report_id)"
    ######################################################################
    return query


def part_2_c() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "CREATE UNIQUE INDEX outcomes_index ON outcomes (report_id)"
    ######################################################################
    return query


def part_3() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "SELECT ROUND((SUM(CASE WHEN date BETWEEN '2018-01-01' AND '2020-12-31' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS percentage FROM incidents"
    ######################################################################
    return query


def part_4() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "SELECT transport_mode, COUNT(report_id) AS count FROM details WHERE detection = 'Intelligence' AND NULLIF(transport_mode, '') IS NOT NULL GROUP BY transport_mode ORDER BY count DESC LIMIT 3"
    ######################################################################
    return query


def part_5() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
        SELECT d.detection, COUNT(d.report_id) AS count, ROUND(AVG(o.num_ppl_arrested), 2) AS avg_ppl_arrested
        FROM details AS d
        INNER JOIN outcomes AS o
        ON d.report_id = o.report_id
        WHERE NULLIF(d.detection, "") IS NOT NULL AND o.num_ppl_arrested >= 1
        GROUP BY d.detection
        HAVING COUNT(d.report_id) >= 100
        ORDER BY avg_ppl_arrested DESC
        LIMIT 3
    """
    ######################################################################
    return query


def part_6() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
        SELECT i.category, COUNT(i.report_id) AS count, 
        ROUND(AVG(
            CASE WHEN o.prison_time_unit = 'Years' THEN o.prison_time * 365
            WHEN o.prison_time_unit = 'Months' THEN o.prison_time * 30
            WHEN o.prison_time_unit = 'Weeks' THEN o.prison_time * 7  
            WHEN o.prison_time_unit = 'Days' THEN o.prison_time ELSE 0 END
        ), 2) AS avg_prison_time_days
        FROM incidents AS i
        INNER JOIN outcomes AS o
        ON i.report_id = o.report_id
        GROUP BY i.category
        HAVING count > 50
        ORDER BY avg_prison_time_days DESC
    """
    ######################################################################
    return query


def part_7_a() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
        CREATE VIEW fines AS
        SELECT i.report_id, i.date, o.num_ppl_fined, o.fine
        FROM incidents AS i
        INNER JOIN outcomes AS o
        ON i.report_id = o.report_id
        WHERE o.num_ppl_fined >= 1 
    """
    ######################################################################
    return query


def part_7_b() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = """
        SELECT strftime('%Y', date) AS year, 
                SUM(num_ppl_fined) AS total_ppl_fined,
                ROUND(SUM(fine), 2) AS total_fine_amount
        FROM fines
        GROUP BY year
        ORDER BY total_fine_amount DESC
        LIMIT 3
    """
    ######################################################################
    return query


def part_8_a() -> str:
    ############### EDIT SQL STATEMENT ###################################
    query = "CREATE VIRTUAL TABLE incident_overviews USING fts5(report_id, subject)"
    ######################################################################
    return query


def part_8_b() -> str:
    ############### EDIT SQL STATEMENT ############################
    query = """
        INSERT INTO incident_overviews (report_id, subject)
        SELECT report_id, subject
        FROM details
    """
    ######################################################################
    return query

    
def part_8_c():
    ############### EDIT SQL STATEMENT ###################################
    query = """
        SELECT COUNT(report_id) AS count
        FROM incident_overviews
        WHERE incident_overviews MATCH 'NEAR("dead" "pangolin", 2)'
    """
    ######################################################################
    return query


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    try:
        conn = create_connection("Q2")
    except Exception as e:
        print("Database Creation Error:", e)

    try:
        conn.execute("DROP TABLE IF EXISTS incidents;")
        conn.execute("DROP TABLE IF EXISTS details;")
        conn.execute("DROP TABLE IF EXISTS outcomes;")
        conn.execute("DROP VIEW IF EXISTS fines;")
        conn.execute("DROP TABLE IF EXISTS incident_overviews;")
    except Exception as e:
        print("Error in Table Drops:", e)

    try:
        print('\033[32m' + "part 1.a.i: " + '\033[m' + execute_query(conn, part_1_a_i()))
        print('\033[32m' + "part 1.a.ii: " + '\033[m' + execute_query(conn, part_1_a_ii()))
        print('\033[32m' + "part 1.a.iii: " + '\033[m' + execute_query(conn, part_1_a_iii()))
    except Exception as e:
         print("Error in part 1.a:", e)

    try:
        part_1_b_i(conn,"data/incidents.csv")
        print('\033[32m' + "Row count for Incidents Table: " + '\033[m' + str(execute_query_and_get_result(conn, "select count(*) from incidents")[0][0]))
        part_1_b_ii(conn, "data/details.csv")
        print('\033[32m' + "Row count for Details Table: " + '\033[m' + str(execute_query_and_get_result(conn,"select count(*) from details")[0][0]))
        part_1_b_iii(conn, "data/outcomes.csv")
        print('\033[32m' + "Row count for Outcomes Table: " + '\033[m' + str(execute_query_and_get_result(conn,"select count(*) from outcomes")[0][0]))
    except Exception as e:
        print("Error in part 1.b:", e)

    try:
        print('\033[32m' + "part 2.a: " + '\033[m' + execute_query(conn, part_2_a()))
        print('\033[32m' + "part 2.b: " + '\033[m' + execute_query(conn, part_2_b()))
        print('\033[32m' + "part 2.c: " + '\033[m' + execute_query(conn, part_2_c()))
    except Exception as e:
        print("Error in part 2:", e)

    try:
        print('\033[32m' + "part 3: " + '\033[m' + str(execute_query_and_get_result(conn, part_3())[0][0]))
    except Exception as e:
        print("Error in part 3:", e)

    try:
        print('\033[32m' + "part 4: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_4()):
            print(line[0],line[1])
    except Exception as e:
        print("Error in part 4:", e)

    try:
        print('\033[32m' + "part 5: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_5()):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part 5:", e)

    try:
        print('\033[32m' + "part 6: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_6()):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part 6:", e)
    
    try:
        execute_query(conn, part_7_a())
        print('\033[32m' + "part 7.a: " + '\033[m' + str(execute_query_and_get_result(conn,"select count(*) from fines")[0][0]))
        print('\033[32m' + "part 7.b: " + '\033[m')
        for line in execute_query_and_get_result(conn, part_7_b()):
            print(line[0],line[1], line[2])
    except Exception as e:
        print("Error in part 7:", e)

    try:   
        print('\033[32m' + "part 8.a: " + '\033[m'+ execute_query(conn, part_8_a()))
        execute_query(conn, part_8_b())
        print('\033[32m' + "part 8.b: " + '\033[m' + str(execute_query_and_get_result(conn, "select count(*) from incident_overviews")[0][0]))
        print('\033[32m' + "part 8.c: " + '\033[m' + str(execute_query_and_get_result(conn, part_8_c())[0][0]))
    except Exception as e:
        print("Error in part 8:", e)

    conn.close()
    #################################################################################
    #################################################################################
  