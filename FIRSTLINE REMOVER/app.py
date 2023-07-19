import os

# Define the directory path where your Java files are located
directory = r''

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.java'):  # Process only Java files
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove the first line
        lines = lines[1:]

        with open(file_path, 'w') as file:
            file.writelines(lines)
            file.truncate()
