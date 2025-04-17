# CSV-LLM Average Calculator

## Overview
This project demonstrates a basic integration of data processing and LLM (Large Language Model) capabilities using the Domino Data Lab platform. The script reads a CSV file containing integer values, calculates their average using an LLM through MLflow, and writes the result to a text file along with the current date and time.

## How It Works
1. The script looks for a specified CSV file in the `/mnt/data/csv-llm-pipeline` directory
2. It reads all integer values from the CSV, handling multiple values per row
3. The average calculation is performed by sending a prompt to an LLM via MLflow deployments
4. Results are written to a text file in the `/mnt/data/csv-output` directory, with the filename including a timestamp

## Usage
```bash
python average_calculator.py <csv_filename>
```

Example:
```bash
python average_calculator.py data.csv
```

## Key Features
- Automatic directory management for inputs and outputs
- Integration with MLflow for LLM inference
- Fallback to direct calculation if LLM response parsing fails
- Timestamped output files
- Error handling for file operations and non-integer values

## Dependencies
- Python 3.x
- MLflow
- Domino Data Lab environment with proper configuration

## Environment Variables
- `DOMINO_MLFLOW_DEPLOYMENTS`: Must be set to access the MLflow deployment client

## Project Structure
```
/
├── average_calculator.py    # Main Python script
├── README.md                # This file
└── /mnt/data/               # Data directories (mounted volumes)
    ├── csv-llm-pipeline/    # Input CSV files
    └── csv-output/          # Output text files
```

## Domino Data Lab Integration
This project serves as a demonstration of basic Domino Data Lab platform capabilities:
- File I/O with mounted volumes
- Environment variable configuration
- MLflow model deployment integration
- LLM inference for data processing

## Getting Started
1. Ensure you have access to a Domino Data Lab environment
2. Clone this repository to your workspace
3. Verify that the required environment variables are set
4. Place your CSV files in the input directory
5. Run the script with your CSV filename

## Fork This Project
If you'd like to fork this code and build on it, you can find the repository at:
[https://github.com/ddl-jim-coates/csv-llm-pipeline](https://github.com/ddl-jim-coates/csv-llm-pipeline)

