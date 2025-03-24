import argparse
import mysql.connector  
import json

def get_product_bp(company_id):
    """
    Retrieves product BP data from the database for the given company_id.
    """

    try:
        # Database connection setup 
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="manuDB"
        )

        cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries

        # SQL Query get data 
        query = """
        SELECT curr_Sales, next_Sales, twicenext_Sales, EI_Rate, DM_per_Unit, EI_DM_Rate, DM_Price
        FROM Product_BP
        WHERE comp_id = %s;
        """

        cursor.execute(query, (company_id,))
        result = cursor.fetchone()  # Expecting one row per company_id

        return result if result else None  # Return None if no data

    except mysql.connector.Error as err:
        print(json.dumps({"error": f"Database Error: {err}"}))
        return None
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

def update_product_bp(company_id, curr_Sales, next_Sales, twicenext_Sales, EI_Rate, DM_per_Unit, EI_DM_Rate, DM_Price):
    """
    Updates product BP data in the database for the given company_id.
    """

    try:
        # Database connection setup 
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="manuDB"
        )

        cursor = connection.cursor()

        # SQL query to update existing BP data
        query = """
        UPDATE Product_BP
        SET 
            curr_Sales = %s,
            next_Sales = %s,
            twicenext_Sales = %s,
            EI_Rate = %s,
            DM_per_Unit = %s,
            EI_DM_Rate = %s,
            DM_Price = %s
        WHERE comp_id = %s;
        """

        values = (
            curr_Sales,
            next_Sales,
            twicenext_Sales,
            EI_Rate,
            DM_per_Unit,
            EI_DM_Rate,
            DM_Price,
            company_id
        )

        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount == 0:
            print(json.dumps({"message": "No rows updated. Check if company_id exists."}))
        else:
            print(json.dumps({"message": "BP data updated successfully."}))

    except mysql.connector.Error as err:
        print(json.dumps({"error": f"Database Error: {err}"}))

    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

def calc_production(curr_sales, next_sales, EI_rate):
    EI = EI_rate * next_sales
    BI = EI_rate * curr_sales
    return curr_sales + EI - BI

def calc_purchases(curr_production, next_production, EI_DM_Rate, DM_per_Unit, DM_price):
    EI = next_production * EI_DM_Rate
    BI = curr_production * EI_DM_Rate
    Use = curr_production * DM_per_Unit
    return DM_price * (Use + EI - BI)


    
