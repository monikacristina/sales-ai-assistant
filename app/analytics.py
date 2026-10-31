from app.database import get_connection


def get_total_revenue():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(
            (quantity * unit_price) - discount_amount
        ) AS total_revenue
        FROM sales
        WHERE status = 'Completed'
        AND quantity IS NOT NULL
        AND quantity > 0
        AND unit_price IS NOT NULL
        AND unit_price > 0
    """)

    result = cursor.fetchone()

    connection.close()

    return result["total_revenue"] or 0

def get_top_product():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_name,
            SUM((quantity * unit_price) - discount_amount)
            AS total_revenue
        FROM sales
        WHERE status = 'Completed'
        AND quantity IS NOT NULL
        AND quantity > 0
        AND unit_price IS NOT NULL
        AND unit_price > 0
        GROUP BY product_name
        ORDER BY total_revenue DESC
        LIMIT 1
    """)

    result = cursor.fetchone()
    connection.close()

    if result:
        return {
            "product": result["product_name"],
            "revenue": result["total_revenue"]
        }

    return None

def get_monthly_revenue():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUBSTR(transaction_date, 4, 7) AS month,
            SUM((quantity * unit_price) - discount_amount)
            AS total_revenue
        FROM sales
        WHERE status = 'Completed'
        AND quantity IS NOT NULL
        AND quantity > 0
        AND unit_price IS NOT NULL
        AND unit_price > 0
        GROUP BY SUBSTR(transaction_date, 4, 7)
        ORDER BY SUBSTR(transaction_date, 7, 4),
                 SUBSTR(transaction_date, 4, 2)
    """)

    results = cursor.fetchall()
    connection.close()

    return [
        {
            "month": row["month"],
            "revenue": row["total_revenue"]
        }
        for row in results
    ]

def get_top_region():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            region,
            SUM((quantity * unit_price) - discount_amount)
            AS total_revenue
        FROM sales
        WHERE status = 'Completed'
        AND quantity IS NOT NULL
        AND quantity > 0
        AND unit_price IS NOT NULL
        AND unit_price > 0
        GROUP BY region
        ORDER BY total_revenue DESC
        LIMIT 1
    """)

    result = cursor.fetchone()
    connection.close()

    if result:
        return {
            "region": result["region"],
            "revenue": result["total_revenue"]
        }

    return None

def compare_months(month1, month2):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            SUM((quantity * unit_price) - discount_amount)
            AS total_revenue
        FROM sales
        WHERE status = 'Completed'
        AND quantity IS NOT NULL
        AND quantity > 0
        AND unit_price IS NOT NULL
        AND unit_price > 0
        AND SUBSTR(transaction_date, 4, 7) = ?
    """

    cursor.execute(query, (month1,))
    revenue1 = cursor.fetchone()["total_revenue"] or 0

    cursor.execute(query, (month2,))
    revenue2 = cursor.fetchone()["total_revenue"] or 0

    connection.close()

    difference = revenue2 - revenue1

    return {
        "month1": month1,
        "revenue1": revenue1,
        "month2": month2,
        "revenue2": revenue2,
        "difference": difference
    }
