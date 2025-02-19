#!/bin/bash

SOURCE_DIR="/Users/al/OneDrive/ADI/Covers"
DESTINATION_DIR=/Users/al/OneDrive/GITHUB/example42.github.io/AbnormalDevOpsIterations/img/

# Loop through each file in the directory
for FILE in "$SOURCE_DIR"/ADI*.png; do    # Check if the file is a regular file
    if [ -f "$FILE" ]; then
        SOURCE_FILE=$(basename "$FILE")
        DEST_FILE="${SOURCE_FILE#* }"

        # Check if the txt file already exists
        if [ ! -e "${DESTINATION_DIR}/${DEST_FILE}" ]; then
            # Execute the pippo command to generate the txt file
            sips --resampleHeight 140 "$FILE" -o "${DESTINATION_DIR}/${DEST_FILE}"
        else
            echo "Skipping, ${DESTINATION_DIR}/${DEST_FILE} already exists."
        fi
    fi
done

