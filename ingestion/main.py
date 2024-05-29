import clickhouse_connect
import string
import time
import random

client: clickhouse_connect.driver.Client


def insert_data():
    i = 0
    while True:
        data = []
        for i in range(0, 10000):
            # -14300000000000
            data.append([time.time_ns(),''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=10))])
        client1.insert('test', data,
                  column_names=['timestamp', 'data'],
                  column_type_names=['UInt64', 'String'])
        client2.insert('test', data,
                  column_names=['timestamp', 'data'],
                  column_type_names=['UInt64', 'String'])
        print("inserting: "+ str(i))
        i +=1
        time.sleep(0.001)

def main():
    global client1, client2  # pylint:  disable=global-statement
    client1 = clickhouse_connect.get_client(port=8123)
    client2 = clickhouse_connect.get_client(port=8124)
    insert_data()

if __name__ == '__main__':
    main()