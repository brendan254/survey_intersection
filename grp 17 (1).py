import pandas as pd
import math
import tkinter as tk
from tkinter import filedialog


def parse_bearing(value):
    try:
        return float(value)
    except:
        d, m, s = map(float, str(value).split())
        return d + m/60 + s/3600


def bearing_intersection(xA, yA, bA, xB, yB, bB):

    print("\n--- Step 1: Convert Bearings to Radians ---")

    bA_rad = math.radians(bA)
    bB_rad = math.radians(bB)

    print("Bearing A (deg):", bA)
    print("Bearing B (deg):", bB)

    print("Bearing A (rad):", bA_rad)
    print("Bearing B (rad):", bB_rad)


    print("\n--- Step 2: Direction Vectors ---")

    dAx = math.sin(bA_rad)
    dAy = math.cos(bA_rad)

    dBx = math.sin(bB_rad)
    dBy = math.cos(bB_rad)

    print("Direction A:", dAx, dAy)
    print("Direction B:", dBx, dBy)


    print("\n--- Step 3: Solve Intersection ---")

    denom = (dAx * dBy - dAy * dBx)

    if denom == 0:
        raise ValueError("Lines are parallel")

    t = ((xB-xA)*dBy - (yB-yA)*dBx)/denom

    print("Intersection parameter t:", t)


    xP = xA + t*dAx
    yP = yA + t*dAy

    return xP, yP


def main():

    print("\n===================================")
    print("SURVEY BEARING INTERSECTION TOOL")
    print("===================================")

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select CSV Survey Data",
        filetypes=[("CSV files","*.csv")]
    )

    if not file_path:
        print("No file selected")
        return

    print("\nReading:", file_path)

    df = pd.read_csv(file_path)

    print("\n--- Step 0: Raw Survey Data ---")
    print(df)

    df["Northing"] = df["Northing"].astype(float)
    df["Easting"] = df["Easting"].astype(float)
    df["Bearing"] = df["Bearing"].apply(parse_bearing)

    print("\n--- Step 1: Bearings Converted to Decimal Degrees ---")
    print(df[["Station","Bearing"]])


    xA = df.loc[0,"Easting"]
    yA = df.loc[0,"Northing"]
    bA = df.loc[0,"Bearing"]

    xB = df.loc[1,"Easting"]
    yB = df.loc[1,"Northing"]
    bB = df.loc[1,"Bearing"]


    print("\n--- Step 2: Stations Used for Intersection ---")
    print("Station A:", xA, yA)
    print("Station B:", xB, yB)


    xP, yP = bearing_intersection(xA, yA, bA, xB, yB, bB)


    print("\n===================================")
    print("FINAL INTERSECTION COORDINATES")
    print("===================================")

    print("Easting :", round(xP,3))
    print("Northing:", round(yP,3))


if __name__ == "__main__":
    main()