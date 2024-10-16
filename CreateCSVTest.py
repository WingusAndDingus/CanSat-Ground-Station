import csv
data = [
    ['Name', 'Length', 'Girth'],
    ['Bernie', 5, 3],
    ['Test', 10, 3]
]

csv_file_path = 'test.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)