#!/bin/bash
# main.sh
# This script checks if Python is available (using python or python).
# If a virtual environment in the "venv" directory doesn't exist, it creates one.
# Then, it activates the environment, runs main.py with any provided arguments,
# and finally deactivates the virtual environment.

 
# Check for a Python executable.
if command -v python &>/dev/null; then
    PYTHON_CMD=python
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python is not installed or not found in PATH."
    exit 1
fi

# Check if the virtual environment directory exists.
if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' not found. Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

#!/bin/bash
# run_traceroute.sh
# This script runs the main.py implementation of the ICMP Traceroute Lab.
# For each target host, it executes the traceroute program and saves the output to a separate text file.

# Check if main.py exists.
if [ ! -f main.py ]; then
    echo "Error: main.py not found in the current directory."
    exit 1
fi

# Activate the Python virtual environment (if it exists).
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Virtual environment activated."
fi

# Define target hosts.
declare -A targets
targets=( 
    ["google"]="google.com"
    ["facebook"]="facebook.com"
    ["yahoo"]="yahoo.com"
    ["bing"]="bing.com"
)



# For each target host, save the output.
# Remove previous output files.
 echo "Remove old files $host..."
rm -f traceroute_*.txt

# For each target host, run the traceroute program and save the output.
for key in "${!targets[@]}"; do
    host=${targets[$key]}
    output_file="traceroute_${key}.txt"
    
    echo "Running traceroute to $host..."
    python main.py "$host" > "$output_file" 2>&1
    echo "Output for $host saved in $output_file"
done

# Deactivate the virtual environment if it was activated.
if type deactivate >/dev/null 2>&1; then
    deactivate
    echo "Virtual environment deactivated."
fi

echo "Traceroute demonstration complete."

