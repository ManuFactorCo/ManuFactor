import argparse
import mysql.connector  
import json

def get_product_cvp(company_id):
    """
    Retrieves product CVP data from the database for the given company_id.
    """
    try:
        # Database connection setup (Get actual Creds from William)
        connection = mysql.connector.connect(
            host="",
            user="",
            password="",
            database=""
        )

        cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries

        # SQL Query get data 
        query = """
        SELECT fixed_cost, variable_cost_per_unit, selling_price_per_unit, target_income
        FROM Product_CVP
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


def calculate_breakeven_and_target_sales(data):
    """
    Calculates breakeven sales and target sales based on database values.
    Returns a dictionary with results.
    """
    if not data:
        return {"error": "No data found for the given company ID."}

    try:
        fixed_cost = float(data["fixed_cost"])
        vc_per_unit = float(data["variable_cost_per_unit"])
        price_per_unit = float(data["selling_price_per_unit"])
        target_income = float(data["target_income"])

        # cant sell for less than unit price
        if price_per_unit <= vc_per_unit:
            return {"error": "Selling price per unit must be greater than variable cost per unit."}

        # Breakeven
        breakeven_units = fixed_cost / (price_per_unit - vc_per_unit)
        breakeven_dollars = breakeven_units * price_per_unit

        # Target
        target_units = (fixed_cost + target_income) / (price_per_unit - vc_per_unit)
        target_dollars = target_units * price_per_unit

        # Return results in JSON format
        return {
            "breakeven_units": round(breakeven_units, 2),
            "breakeven_dollars": round(breakeven_dollars, 2),
            "target_units": round(target_units, 2),
            "target_dollars": round(target_dollars, 2)
        }

    except (TypeError, ValueError) as e:
        return {"error": f"Calculation error: {str(e)}"}


if __name__ == "__main__":
    # Use argparse for better argument handling
    parser = argparse.ArgumentParser(description="Calculate breakeven and target sales for a company.")
    parser.add_argument("company_id", type=int, help="Company ID to fetch CVP data for.")

    args = parser.parse_args()
    company_id = args.company_id

    # Get data
    product_data = get_product_cvp(company_id)

    # Compute breakeven and target sales
    result = calculate_breakeven_and_target_sales(product_data)

    # Print result as JSON
    print(json.dumps(result, indent=4))