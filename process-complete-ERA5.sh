#!/bin/bash

# Validate input arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <YEAR> <MONTH> <DATA_DIR>"
    exit 1
fi

# Get YEAR and MONTH from command-line arguments
YEAR="$1"
MONTH="$2"
# Define a base directory for data storage (relative or absolute path)
DATA_DIR="$3"  

# Pad the month if doesn't have leading 0's.
MONTH=$(printf "%02d" "$MONTH")

# Create the directory if it doesn't exist
mkdir -p "$DATA_DIR"

# Debugging: Print the arguments
echo "YEAR=$YEAR"
echo "MONTH=$MONTH"

# Define file names with directory prefix
TQ_ML_FILE="${DATA_DIR}/${MONTH}-${YEAR}-tq_ml.grib"
ZLNSP_ML_FILE="${DATA_DIR}/${MONTH}-${YEAR}-zlnsp_ml.grib"
Z_FILE="${DATA_DIR}/${MONTH}-${YEAR}-z.grib"
LNSP_FILE="${DATA_DIR}/${MONTH}-${YEAR}-lnsp.grib"
MERGED_FILE="${DATA_DIR}/${MONTH}-${YEAR}-merged.grib"
PRES_TEMP_FILE="${DATA_DIR}/${MONTH}-${YEAR}_pres_temp.grib"
PRES_FILE="${DATA_DIR}/${MONTH}-${YEAR}_pres.grib"

# Define Python scripts
DOWNLOAD_SCRIPT="download_Complete_ERA5.py"
COMPUTE_GEOPOTENTIAL_SCRIPT="compute_geopotential_on_ml_updated.py"

# Define color codes
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 1. Download relevant data files
echo -e "${CYAN}Step 1: Downloading relevant data files for ${YEAR}-${MONTH}...${NC}"
python3 $DOWNLOAD_SCRIPT --year $YEAR --month $MONTH --output_dir "$DATA_DIR"

# 2. Compute geopotential
echo -e "${CYAN}Step 2: Computing geopotential from ${TQ_ML_FILE} and ${ZLNSP_ML_FILE}...${NC}"
python3 $COMPUTE_GEOPOTENTIAL_SCRIPT $TQ_ML_FILE $ZLNSP_ML_FILE -o $Z_FILE

# 3. Remove 'z' from zlnsp_ml to avoid conflicts
echo -e "${CYAN}Step 3: Removing 'z' from ${ZLNSP_ML_FILE}...${NC}"
cdo delname,z $ZLNSP_ML_FILE $LNSP_FILE

# 4. Merge tq_ml, z, and lnsp into a full monthly dataset
echo -e "${CYAN}Step 4: Merging files into ${MERGED_FILE}...${NC}"
cdo merge $TQ_ML_FILE $Z_FILE $LNSP_FILE $MERGED_FILE

# 5. Convert to new pressure levels
echo -e "${CYAN}Step 5: Converting to pressure levels...${NC}"
#Original ERA5 pressure levels for comparison
#cdo ml2pl,100000,97500,95000,92500,90000,87500,85000,82500,80000,77500,75000,70000,65000,60000,55000,50000,45000,40000,35000,30000,25000,22500,20000,17500,15000,12000,10000,7000,5000,3000,2000,1000,700,500,300,200,100 \
#new, higher fidelity pressure levles
cdo ml2pl,15000,14500,14000,13500,13000,12500,12000,11500,11000,10500,10000,9500,9000,8500,8000,7500,7000,6500,6000,5500,5000,4750,4500,4250,4000,3750,3500,3250,3000,2800,2600,2400,2200,2000,1875,1750,1625,1500,1375,1250,1125,1000  \
    $MERGED_FILE $PRES_TEMP_FILE

# 6. Remove unnecessary variables
echo -e "${CYAN}Step 6: Removing unnecessary variables from ${PRES_TEMP_FILE}...${NC}"
cdo delname,q,t,lnsp $PRES_TEMP_FILE $PRES_FILE

# 7. Cleanup intermediate files
echo -e "${CYAN}Step 7: Cleaning up intermediate files...${NC}"
rm -v $MERGED_FILE $PRES_TEMP_FILE $Z_FILE $LNSP_FILE

# Final message
echo -e "${CYAN}Processing for ${YEAR}-${MONTH} completed. Final file: ${PRES_FILE}${NC}"
