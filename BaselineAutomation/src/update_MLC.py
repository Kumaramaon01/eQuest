import json
import os
import streamlit as st

def get_climate_path(climate_zone, building_type):
    with open('config.json', 'r', encoding='utf-8') as f:  # Specify the encoding
        data = json.load(f)
    for entry in data:
        if entry['climate'] == str(climate_zone) and building_type == 1:
            return entry['construction_library_path']
        elif entry['climate'] == str(climate_zone) and building_type == 0:
            return entry['construction_library_path_residential']
    return None

def get_system_path(building_type, heat_type, area, floor):
    area = int(area)
    floor = int(floor)
    with open('config.json', 'r', encoding='utf-8') as f:  # Specify the encoding
        data = json.load(f)
    construction_library_systems_paths = [entry["construction_library_systems"] for entry in data]
    if building_type == 0:
        if heat_type == 0:
            return construction_library_systems_paths[0]
        else:
            return construction_library_systems_paths[1]
    elif building_type == 1:
        if area <= 25000 and floor <= 3:
            if heat_type == 0:
                return construction_library_systems_paths[2]
            else:
                return construction_library_systems_paths[3]
        elif area < 150000:
            if floor <= 5:
                if heat_type == 0:
                    return construction_library_systems_paths[4]
                else:
                    return construction_library_systems_paths[5]
            elif floor == 4 or floor == 5:
                if heat_type == 0:
                    return construction_library_systems_paths[4]
                else:
                    return construction_library_systems_paths[5]
        else:
            if floor > 5:
                if heat_type == 0:
                    return construction_library_systems_paths[6]
                else:
                    return construction_library_systems_paths[7]
    return None

def insert_material_data(climate_zone_file, amenity_file):
    start_marker1 = "= MATERIAL"
    end_marker1 = ".."
    try:
        with open(climate_zone_file, 'r', encoding='utf-8', errors='ignore') as file:
            data_climate_zone = file.readlines()
    except UnicodeDecodeError as e:
        st.error(f"Error reading {climate_zone_file}: {e}")
        return []

    start_indices1 = [i for i, line in enumerate(data_climate_zone) if start_marker1 in line]
    end_indice1 = [i for i, line in enumerate(data_climate_zone) if end_marker1 in line]
    end_indices1 = []
    for i in range(0, len(start_indices1)):
        end_indices1.append(end_indice1[i])

    try:
        with open(amenity_file, 'r', encoding='utf-8', errors='ignore')) as file:  # Specify the encoding
            amenity_data = file.readlines()
    except UnicodeDecodeError as e:
        st.error(f"Error reading {amenity_file}: {e}")
        return []

    layer_index = None
    for i, line in enumerate(amenity_data):
        if "= LAYERS" in line:
            layer_index = i
            break

    if layer_index is not None:
        for start_idx, end_idx in zip(start_indices1, end_indices1):
            material_data = data_climate_zone[start_idx:end_idx+1]
            amenity_data = amenity_data[:layer_index] + material_data + amenity_data[layer_index:]

    return amenity_data

def insert_layers_data(climate_zone_file, mat_data):
    start_marker2 = "= LAYERS"
    strt_mrk1 = "TYPE             = LAYERS"
    end_marker2 = ".."
    try:
        with open(climate_zone_file, 'r', encoding='utf-8') as file:  # Specify the encoding
            data_climate_zone = file.readlines()
    except UnicodeDecodeError as e:
        st.error(f"Error reading {climate_zone_file}: {e}")
        return []

    start_indices2 = [i for i, line in enumerate(data_climate_zone) if start_marker2 in line and strt_mrk1 not in line]
    end_indice2 = [i for i, line in enumerate(data_climate_zone) if end_marker2 in line]
    end_indicee2 = [x for x in end_indice2 if x > start_indices2[0]]

    end_indices2 = []
    for i in range(0, len(start_indices2)):
        end_indices2.append(end_indicee2[i])

    construction_index = None
    for i, line in enumerate(mat_data):
        if "= CONSTRUCTION" in line:
            construction_index = i
            break  

    if construction_index is None:
        construction_index = len(mat_data)
    else:
        for start_idx, end_idx in zip(start_indices2, end_indices2):
            layer_data = data_climate_zone[start_idx:end_idx+1]
            mat_data = mat_data[:construction_index] + layer_data + mat_data[construction_index:]

    return mat_data

def insert_const_data(climate_zone_file, lyr_data):
    start_marker3 = "= CONSTRUCTION"
    end_marker3 = ".."
    try:
        with open(climate_zone_file, 'r', encoding='utf-8') as file:  # Specify the encoding
            data_climate_zone = file.readlines()
    except UnicodeDecodeError as e:
        st.error(f"Error reading {climate_zone_file}: {e}")
        return []

    start_indices3 = [i for i, line in enumerate(data_climate_zone) if start_marker3 in line]
    end_indice3 = [i for i, line in enumerate(data_climate_zone) if end_marker3 in line]
    end_indicee3 = [x for x in end_indice3 if x > start_indices3[0]]

    end_indices3 = []
    for i in range(0, len(start_indices3)):
        end_indices3.append(end_indicee3[i])

    construction_index = None
    for i, line in enumerate(lyr_data):
        if "Glass Types" in line:
            construction_index = i - 2
            break

    if construction_index is None:
        construction_index = len(lyr_data)

    for start_idx, end_idx in zip(start_indices3, end_indices3):
        material_data = data_climate_zone[start_idx:end_idx+1]
        lyr_data = lyr_data[:construction_index] + material_data + lyr_data[construction_index:]

    return lyr_data
