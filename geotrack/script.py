import json
import time
import requests
import psycopg2
import logging

db_params = {
'dbname': 'geotrak',
'user': 'postgres',
'password': 'postgres',
'host': 'geo.cdetqdxx15hj.ap-south-1.rds.amazonaws.com',
'port': '5432'
}


conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Configure the logger
logging.basicConfig(filename='script.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
# logger.warning("This is a warning log")
# logger.error("This is an error log")

def count_max_api_hits(api_url, username, password, timeout):
    start_time = time.time()
    count = 0
    try:
        response = requests.get(api_url, auth=(username, password), timeout=timeout)
        if response.status_code == 200:
            content = [response.content, count]
            logger.info("the logger info from success response: %s", content)
            print("the response value is ", content)
            print("###########################")
            if username == 'ashokvts':
                apiref = 1
                # print("i m from first")
            else:
                apiref = 2
                # print("i m from second")
            # count += 1
            status_code, headers, content = response.status_code, response.headers, response.content
            response = json.loads(content)

            # Get all the keys of the JSON response
            keys = response.keys()

            # Print all the keys
            for key in keys:
                systime = response[key][0]['systime']
                exceptionBM = response[key][0]['exceptionBM']
                virtualName = response[key][0]['virtualName']
                speed = response[key][0]['speed']
                direction = response[key][0]['direction']
                haltedSince = response[key][0]['haltedSince']
                elevation = response[key][0]['elevation']
                timestamp = response[key][0]['timestamp']
                distance = response[key][0]['distance']
                locStr = response[key][0]['locStr']
                noDataSince = response[key][0]['noDataSince']
                lattitude = response[key][0]['lattitude']
                movingSince = response[key][0]['movingSince']
                longitude = response[key][0]['longitude']
                regNo = response[key][0]['regNo']
                bmStr = response[key][0]['bmStr']

                insert_query = """INSERT INTO dev_detail (reg_device, systime, exceptionbm, virtualname, speed, direction, haltedsince, elevation, timestamps, distance, locstr, nodatasince, lattitude, movingsince, longitude, regno, bmstr, countt, apiref) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                data_to_insert = (key, systime, exceptionBM, virtualName, speed, direction, haltedSince, elevation, timestamp,
                distance, locStr, noDataSince, lattitude, movingSince, longitude, regNo, bmStr, count, apiref)


                cursor.execute(insert_query, data_to_insert)
                conn.commit()
        else:
            errorlst = [response.status_code, response.headers, response.content, count]
            logger.info("An exception occurred: %s", errorlst)
            print("the error list is ", errorlst)
            insert_query = """INSERT INTO errors (api_ref, error) VALUES (%s, %s);"""
            error_to_insert = (count, errorlst)
            cursor.execute(insert_query, error_to_insert)
            conn.commit()

    except requests.exceptions.Timeout:
        logger.info("Timeout Error exception coming from logger ")
        print("Timeout Error is coming")
        insert_query = """INSERT INTO errors (api_ref, error) VALUES (%s, %s);"""
        error_to_insert = (count, "Timeout Error")

        cursor.execute(insert_query, error_to_insert)
        conn.commit()
    except Exception as e:
        logger.error("Unhandled exception occurred from logger: ", e)
        print("Unhandled exception occurred from logger: ", e)
        insert_query = """INSERT INTO errors (api_ref, error) VALUES (%s, %s);"""
        error_to_insert = (count, e)
        cursor.execute(insert_query, error_to_insert)
        conn.commit()


        # time.sleep(10)


count_max_api_hits(
            "http://blazer7.geotrackers.co.in/GTWS/gtWs/LocationWs/getUsrLatestLocation",
            "ashokvts", "naresh@7014", 120)

count_max_api_hits(
            "http://blazer7.geotrackers.co.in/GTWS/gtWs/LocationWs/getUsrLatestLocation",
            "artravels", "trackit", 120)

