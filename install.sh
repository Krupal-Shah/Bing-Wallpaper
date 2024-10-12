# Check if python is available on the system
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found on the system. Please install python3 and try again."
    exit
fi

# Create a python environment
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Install the application
