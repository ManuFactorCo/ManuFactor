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

def calc_production(curr_sales, next_sales, EI_rate):
    EI = EI_rate * next_sales
    BI = EI_rate * curr_sales
    return curr_sales + EI - BI

def calc_purchases(curr_production, next_production, EI_DM_Rate, DM_per_Unit, DM_price):
    EI = next_production * EI_DM_Rate
    BI = curr_production * EI_DM_Rate
    Use = curr_production * DM_per_Unit
    return DM_price * (Use + EI - BI)


    
