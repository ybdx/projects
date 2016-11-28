#!/bin/bash
CURRENT_FILE_DIR="$(cd "$(dirname "$0")";pwd)"
cd $CURRENT_FILE_DIR
file="../source_data/urlandcompanynameData"
if [ -f "$file" ]; then
    rm "$file"
fi
hadoop fs -text projects/address_to_gps/qichacha/online/AddressFinal/2016-11-23/part-* > ../source_data/urlandcompanynameData
python qichachaDataSplit.py ../source_data/urlandcompanynameData ../source_data/url_and_companyName/
