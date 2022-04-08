#!/bin/bash
cd /home/ubuntu/healthtag/healthtag-hospital-api/csop
python3 transform_fhir.py
mkdir `date +%Y%m%d`
mv uploads/* `date +%Y%m%d`
python3 update_patient.py