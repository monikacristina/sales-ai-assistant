import csv
from app.database import get_connection

CSV_FILE = "data/sales.csv"


def load_sales_data():
    connection = get_connection()
    cursor = connection.cursor()

    with open(CSV_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        records = []

        for row in reader:
            record = (
                row["Transaction_Id"],
                row["Order_date"],
                row["Product"],
                row["Category"],
                int(row["Quantity"]) if row["Quantity"] else None,
                float(row["Unit_price"]) if row["Unit_price"] else None,
                float(row["Discount_amount"]) if row["Discount_amount"] else 0,
                row["Region"],
                row["Sales_channel"],
                row["Status"]
            )

            records.append(record)

    cursor.executemany("""
        INSERT OR IGNORE INTO sales (
            transaction_id,
            transaction_date,
            product_name,
            category,
            quantity,
            unit_price,
            discount_amount,
            region,
            sales_channel,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]

    connection.close()

    print(f"Successfully loaded data. Total records: {count}")


if __name__ == "__main__":
    load_sales_data()
