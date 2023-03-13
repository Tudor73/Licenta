import os 
from lib import load_signal, find_notes

files = os.listdir("C:/projects/final/inputs")


expected_results = [(25, ["E5", "D5", "C5", "B4", "A4", "B4", "C5", "C5", "C5", "C5", "C5", 
                          "B4", "B4", "B4", "B4", "B4", "B4", "E5", "E5", "E5", "E5", "E5", "E5", "E5", "E5"]),
                          (11, ["A3", "B3", "C4", "C4", "B3", "A3", "A3", "B3", "C4", "C4", "A3"]), (1, ["G3"]), 
                          (6, ["E3", "G2", "A2", "B2", "D3", "E3"]), 
                          (16, ["G4", "F4", "E5", "D4", "G4","F4", "A4", "F4","G4", "F4", "E5", "D4", "G4", "F4", "A4", "F4"])]

def calculate(expected, actual):
    correct = 0
    for i in range(len(expected)):
        if i > len(actual) - 1:
            break
        if expected[i] == actual[i]:
            correct += 1
    return correct/len(expected)


total_percentage = 0

for idx, filename in enumerate(files):
    y, fs = load_signal(f"C:/projects/final/inputs/{filename}")
    notes = find_notes(y, fs)
    percentage = calculate(expected_results[idx][1], notes)
    total_percentage += percentage
    print("File: ", filename, "Expected_number_of_notes: ", expected_results[idx][0], "Actual: ", len(notes))
    print("File: ", filename, "Expected_notes: ", expected_results[idx][1], "Actual: ", notes)

print("Total percentage: ", total_percentage/len(files))