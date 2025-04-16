#!/bin/bash

# Set the year for processing
YEAR="2023"

DATA_DIR="DATA"


# Name of the monthly processing script
MONTHLY_SCRIPT="./process-complete-ERA5.sh"

# Define final output file
FINAL_FILE="${DATA_DIR}/2023-ERA5-Complete-SEA.grib"

# Temporary list to store monthly output files
OUTPUT_FILES=()

# Loop over all 12 months
for MONTH in {1..12}; do
    # Format the month with leading zero and ensure it's passed as a string
    FORMATTED_MONTH=$(printf "%02d" $MONTH)
    echo -e "\033[0;36mProcessing month: $YEAR-$FORMATTED_MONTH...\033[0m"

    # Run the monthly processing script with the correctly formatted month
    $MONTHLY_SCRIPT $YEAR $FORMATTED_MONTH $DATA_DIR

    # Check if the output file was created
    MONTHLY_FILE="${DATA_DIR}/${FORMATTED_MONTH}-${YEAR}_pres.grib"
    if [ -f "$MONTHLY_FILE" ]; then
        OUTPUT_FILES+=("$MONTHLY_FILE")
    else
        echo -e "\033[0;31mError: Monthly file $MONTHLY_FILE not found! Skipping...\033[0m"
    fi
done

# Merge all monthly files into the final output file
if [ ${#OUTPUT_FILES[@]} -gt 0 ]; then
    echo -e "\033[0;36mMerging all monthly files into $FINAL_FILE...\033[0m"
    cdo mergetime "${OUTPUT_FILES[@]}" "$FINAL_FILE"

    # Check if the final file was created successfully
    if [ -f "$FINAL_FILE" ]; then
        echo -e "\033[0;32mFinal file $FINAL_FILE created successfully!\033[0m"
    else
        echo -e "\033[0;31mError: Failed to create final file $FINAL_FILE!\033[0m"
    fi
else
    echo -e "\033[0;31mError: No monthly files to merge!\033[0m"
fi

cdo -f nc copy "${$DATA_DIR}/${YEAR}-ERA5-Complete-SEA.grib" "${DATA_DIR}/${YEAR}-ERA5-Complete-SEA.nc"

# Cleanup intermediate files
#echo -e "\033[0;36mCleaning up intermediate monthly files...\033[0m"
#for FILE in "${OUTPUT_FILES[@]}"; do
#    rm -v "$FILE"
#done
#
