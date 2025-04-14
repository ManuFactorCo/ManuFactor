import argparse
import mysql.connector  
import json

def get_product_bp(company_id):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="manuDB"
        )
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT curr_Sales, next_Sales, twicenext_Sales, EI_Rate, DM_per_Unit, EI_DM_Rate, DM_Price
        FROM Product_BP
        WHERE comp_id = %s;
        """
        cursor.execute(query, (company_id,))
        result = cursor.fetchone()
        return result if result else None

    except mysql.connector.Error as err:
        print(json.dumps({"error": f"Database Error: {err}"}))
        return None
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

def update_product_bp(company_id, curr_Sales, next_Sales, twicenext_Sales, EI_Rate, DM_per_Unit, EI_DM_Rate, DM_Price):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="manuDB"
        )
        cursor = connection.cursor()

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

        message = "BP data updated successfully." if cursor.rowcount > 0 else "No rows updated. Check if company_id exists."
        print(json.dumps({"message": message}))

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

def calc_bp_summary(company_id)
        data = get_product_bp(company_id)

        if not data:
            return None
    
        curr_sales = data['curr_Sales']
        next_sales = data['next_Sales']
        twicenext_sales = data['twicenext_Sales']
        ei_rate = data['EI_Rate']
        dm_per_unit = data['DM_per_Unit']
        ei_dm_rate = data['EI_DM_Rate']
        dm_price = data['DM_Price']

        this_month_production = calc_production(curr_sales, next_sales, ei_rate)
        next_month_production = calc_production(next_sales, twicenext_sales, ei_rate)
        dm_purchases = calc_purchases(this_month_production, next_month_production, ei_dm_rate, dm_per_unit, dm_price)

        result = {
            "company_id": company_id,
            "production_required": round(this_month_production, 0),
            "dm_purchases_required": round(dm_purchases, 2)
        }

        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate production and DM purchases for a given company.")
    parser.add_argument("company_id", type=int)
    args = parser.parse_args()

    result = calculate_bp_summary(args.company_id)
    print(json.dumps(result, indent=2))
