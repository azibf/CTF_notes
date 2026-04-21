import csv
import sys

def main():
    # Read input from CSV file
    csv_filename = "./5.csv"  # Change to your CSV file path
    
    try:
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
    except FileNotFoundError:
        print("CSV file not found!")
        return

    try:
        for I in range(39): 
            S = int(data[138][26 + I])
            V = int(data[99 + I][26 + S])
            
            print(chr(V), end='')
    except (IndexError, ValueError, TypeError) as e:
        print("Incorrect: Data error -", str(e))
        return


if __name__ == "__main__":
    main()