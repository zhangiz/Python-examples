import re

# Function to replace even occurrences with "pathetic" and odd occurrences with "marvellous"
def replace_even_odd(match):
    global count
    count += 1
    if count % 2 == 0:
        return "pathetic"
    else:
        return "marvellous"

# Read the content from file_to_read.txt
with open('file_to_read.txt', 'r') as file:
    file_content = file.read()

# Calculate the total times "terrible" appears
count = 0
terrible_count = len(re.findall(r'\bterrible\b', file_content, re.IGNORECASE))
print("Total occurrences of 'terrible':", terrible_count)

# Replace even and odd occurrences and write to result.txt
modified_content = re.sub(r'\bterrible\b', replace_even_odd, file_content, flags=re.IGNORECASE)
with open('result.txt', 'w') as result_file:
    result_file.write(modified_content)

print("Modified content has been written to result.txt")