#!/bin/bash

echo "***********************************"
echo "This software requires Python 3.10. Please install it first"
echo "For Debian (Ubuntu)"
echo "sudo apt-get update"
echo "sudo apt-get install python3"
echo "***********************************"
echo "Activate Python virtual environment"
./venv/Scripts/activate
echo "Install pip package to virtual environment"
pip install requirements.txt
echo "Run FHIR Transformer"
python -m fhir_transformer
echo "Leave Python virtual environment"
deactivate