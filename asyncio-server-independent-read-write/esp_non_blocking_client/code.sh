#!/bin/bash

# Run VSCode setup for ESP-IDF 5.4.0

# Last command should display no errors
export IDF_PATH=$HOME/esp/v5.4.0/esp-idf
export IDF_TOOLS_PATH=$IDF_PATH/.espressif
. $IDF_PATH/export.sh

# Change to example dir
cd non_blocking

# Comment out component path setting in main/idf_component.yml
    # Please comment the following line, if this example is installed by idf.py create-project-from-example.
    #override_path: "../../../components/mesh_lite"

# Start VSCode from example dir - CLOSE all popups when it opens!!
code .
