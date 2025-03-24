import argparse
import mysql.connector  
import json

def calc_production(curr_sales, next_sales, EI_rate):
    EI = EI_rate * next_sales
    BI = EI_rate * curr_sales
    return curr_sales + EI - BI

def calc_purchases(curr_production, next_production, EI_DM_Rate, DM_per_Unit, DM_price):
    EI = next_production * EI_DM_Rate
    BI = curr_production * EI_DM_Rate
    Use = curr_production * DM_per_Unit
    return DM_price * (Use + EI - BI)


    
