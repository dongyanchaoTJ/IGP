import psycopg2 as ps2


#######################
# PostgresSQL wrapper #
#######################
class PGWrapper(object):
    def __init__(self):
        ''' Constructor for this class. '''
        self.conn = None
        self.curr = None
        self.conn_string = None

    def connect_pg(self, path):
        """
        Connect to postgres
        :param path: path to the csv with the connection string
        :return: 0: success, -1 failed
        """

        self.read_conn_string(path)

        try:
            self.conn = ps2.connect(self.conn_string)
        except ps2.Error as e:
            print "I am unable to connect to the database"
            print e
            print e.pgcode
            print e.pgerror
            return False

        self.curr = self.conn.cursor()

        return True

    def execute_multiple_query(self, query, values):
        """
        Execute multiple queries for values
        :param query: query to execute multiple times
        :param values: list of values to process
        :return: rowcount
        """

        try:
            self.curr.executemany(query, values)
        except ps2.Error as e:
            print "Cant execute the query"
            print e
            print e.pgcode
            print e.pgerror
            return -1

        return self.curr.rowcount

    def execute_query(self, query):
        """
        Execute a query
        :param query: query to execute
        :return: rowcount
        """

        try:
            self.curr.execute(query)
        except ps2.Error as e:
            print "Cant execute the query"
            print e
            print e.pgcode
            print e.pgerror

            return -1

        return self.curr.rowcount

    def execute_query_params(self, query, data):
        """
        Execute a query with parameters given by data field
        :param query: query to execute
        :param data: data to be converted by psycopg
        :return: rowcount
        """

        try:
            self.curr.execute(query, data)
        except ps2.Error as e:
            print "Cant execute the query"
            print e
            print e.pgcode
            print e.pgerror

            return -1

        return self.curr.rowcount

    def commit(self):
        """
        Commits the last transaction
        :return:
        """
        self.conn.commit()

    def roolback(self):
        """
        Rollback the last transaction
        :return:
        """
        self.conn.rollback()

    def fetch_all(self):
        """
        Fetch the results of the last query
        :return: dictionary with the result
        """

        a = self.curr.fetchall()
        return a

    def fetch_one(self):
        """
        Fetch one result from the last query
        :return:
        """

        a = self.curr.fetchone()
        return a

    def read_conn_string(self, path):
        """
        Reads the connection string from a csv file
        Format: host,post,database,user
        :param path: File path to csv
        :return:
        """

        f = open(path, "r")

        v = f.readline().split(',')

        f.close()

        self.conn_string = "host=" + v[0] + " port=" + v[1] + " dbname=" + v[2] + " user=" + v[3]
