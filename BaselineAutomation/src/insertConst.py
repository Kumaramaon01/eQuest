import pandas as pd
import os
import re
import streamlit as st

def update_external_wall_roof_undergrnd(data):
    start_marker = "Floors / Spaces / Walls / Windows / Doors"
    end_marker = "Electric & Fuel Meters"

    # Finding start and end indices
    start_index = None
    end_index = None

    for i, line in enumerate(data):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break

    value_before_equal_wall = None
    value_before_equal_roof = None
    value_before_equal_under = None

    for line in data:
        if "BL Wall" in line:
            index = line.find('=')
            if index != -1:
                value_before_equal_wall = line[:index].strip()
        elif "Undergrd W" in line:
            index = line.find('=')
            if index != -1:
                value_before_equal_under = line[:index].strip()
        elif "BL Roof" in line:
            index = line.find('=')
            if index != -1:
                value_before_equal_roof = line[:index].strip()
    st.success(value_before_equal_wall)
    st.success(value_before_equal_roof)
    st.success(value_before_equal_under)
    
    if start_index is not None and end_index is not None:
        inside_exterior_wall = False
        inside_underground_wall = False

        for line_index in range(start_index + 3, end_index - 4):
            line = data[line_index]

            if "EXTERIOR-WALL" in line:
                inside_exterior_wall = True
                inside_underground_wall = False
        
            elif "UNDERGROUND-WALL" in line:
                inside_underground_wall = True
                inside_exterior_wall = False
            
            elif inside_exterior_wall:
                if ".." in line:
                    inside_exterior_wall = False
                elif "CONSTRUCTION" in line:
                    location_value = re.search(r'LOCATION\s*=\s*(\S+)', line).group(1)
                    construction_value = re.search(r'CONSTRUCTION\s*=\s*(\S+)', line).group(1)
                    if "TOP" not in location_value:
                        data[line_index] = '   CONSTRUCTION     = {}\n'.format(value_before_equal_wall)
                    elif "extroof" in construction_value or "Ext Roof" in construction_value or "Roof" in construction_value:
                        data[line_index] = '   CONSTRUCTION     = {}\n'.format(value_before_equal_roof)

            elif inside_underground_wall:
                if ".." in line:
                    inside_underground_wall = False
                elif "CONSTRUCTION" in line and value_before_equal_under is not None:
                    if "BOTTOM" not in data[line_index + 1]:
                        data[line_index] = '   CONSTRUCTION     = {}\n'.format(value_before_equal_under)

    return data
