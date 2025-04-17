import csv
import os
import sys
from datetime import datetime
from mlflow.deployments import get_deploy_client

# Define input and output directories
INPUT_DIR = "/mnt/data/csv-llm-pipeline"
OUTPUT_DIR = "/mnt/artifacts"

def calculate_average_with_llm(numbers):
    """
    Calculate the average of a list of numbers by using an LLM through MLflow
    
    Args:
        numbers (list): List of integers to average
        
    Returns:
        float: The calculated average
    """
    # Prepare the prompt for the LLM
    numbers_str = ', '.join(map(str, numbers))
    prompt = f"Calculate the average of these numbers: {numbers_str}"
    
    # Call the LLM through MLflow
    client = get_deploy_client(os.environ['DOMINO_MLFLOW_DEPLOYMENTS'])
    response = client.predict(
        endpoint="chat-gpt4-ja",
        inputs={"messages": [{"role": "user", "content": prompt}]}
    )
    
    # Extract the average from the response
    try:
        # Simple extraction - you may need to implement more robust parsing
        response_text = response.get('choices', [{}])[0].get('message', {}).get('content', '')
        # Extract the number from the response
        import re
        average_match = re.search(r'(\d+(\.\d+)?)', response_text)
        if average_match:
            return float(average_match.group(1))
        else:
            # Fallback to calculating average directly if parsing fails
            return sum(numbers) / len(numbers)
    except (KeyError, IndexError, ValueError, ZeroDivisionError) as e:
        print(f"Error parsing LLM response: {e}")
        # Fallback to calculating average directly
        return sum(numbers) / len(numbers) if numbers else 0

def process_csv_and_output_result(csv_filename):
    """
    Read integers from a CSV file, calculate the average using an LLM,
    and write it to a text file with the current date/time.
    
    Args:
        csv_filename (str): Base filename of the CSV file (without path)
    """
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get full paths
    input_path = os.path.join(INPUT_DIR, csv_filename)
    
    # Get current date/time for both the filename and content
    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    output_filename = f"average_{current_datetime.strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Read integers from CSV
    numbers = []
    try:
        with open(input_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                # Convert each value in the row to an integer and add to numbers list
                for value in row:
                    if value.strip():  # Skip empty values
                        try:
                            numbers.append(int(value.strip()))
                        except ValueError:
                            print(f"Warning: Skipping non-integer value: '{value}'")
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Check if we have numbers to average
    if not numbers:
        print("No valid numbers found in the CSV file.")
        return
    
    # Calculate average using LLM
    try:
        average = calculate_average_with_llm(numbers)
    except Exception as e:
        print(f"Error calculating average with LLM: {e}")
        # Fallback to direct calculation
        average = sum(numbers) / len(numbers)
        print(f"Falling back to direct calculation: {average}")
    
    # Write result to output file
    try:
        with open(output_path, 'w') as output_file:
            output_file.write(f"Date: {date_str}\n")
            output_file.write(f"Average: {average}")
        print(f"Results written to {output_path}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_filename>")
        print("Example: python script.py data.csv")
        print(f"The script will look for the file in {INPUT_DIR}")
        print(f"and write the output to {OUTPUT_DIR}")
        sys.exit(1)
    
    csv_filename = sys.argv[1]
    process_csv_and_output_result(csv_filename)