import pyodbc
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# SQL Server configuration
server = 'RIFAT-2741'
database = 'GAZIGROUP'
username = 'sa'
password = '123456'
driver = '{ODBC Driver 17 for SQL Server}'  # Adjust driver version if needed

# Connection string
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"


def get_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        logger.error("Error connecting to SQL Server: %s", e)
        return None


def fetch_sales_data():
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()

        query = """
        SELECT top 1000 xitem AS product, xitem AS product_name, xqtyord AS quantity_sold,
        xrate AS price, xvatrate AS vat_rate, xvatamt AS vat_amount, xlineamt AS line_amount
        FROM opdodetail
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        logger.info("Fetched rows: %s", rows)

        sales_data = []
        for row in rows:
            data_dict = {
                "product": str(row.product),
                "product_name": str(row.product_name),
                "quantity_sold": str(row.quantity_sold),
                "price": str(row.price),
                "vat_rate": str(row.vat_rate),
                "vat_amount": str(row.vat_amount),
                "line_amount": str(row.line_amount)
            }
            sales_data.append(data_dict)

        cursor.close()
        conn.close()

        return sales_data

    except Exception as e:
        logger.error("Error fetching sales data: %s", e)
        return []
