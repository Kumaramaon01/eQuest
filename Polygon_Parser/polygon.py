import pandas as pd
import re

def extract_polygons(inp_file):
    with open(inp_file) as f:
        # Read all lines from the file and store them in a list named flist
        flist = f.readlines()
        
        # Initialize an empty list to store line numbers where 'Polygons' occurs
        polygon_count = [] 
        # Iterate through each line in flist along with its line number
        for num, line in enumerate(flist, 0):
            if 'Polygons' in line:
                polygon_count.append(num)
            if 'Wall Parameters' in line:
                numend = num
        # Store the line number of the first occurrence of 'Polygons'
        numstart = polygon_count[0] if polygon_count else None
        if not numstart:
            print("No 'Polygons' section found in the file.")
            return pd.DataFrame()  # Return an empty dataframe if no polygons section is found
        
        # Slice flist from the start of 'Polygons' to the line before 'Wall Parameters'
        polygon_rpt = flist[numstart:numend]
        
        # Initialize an empty dictionary to store polygon data
        polygon_data = {}
        current_polygon = None
        vertices = []
        
        # Iterate through the lines in polygon_rpt
        for line in polygon_rpt:
            if line.strip().startswith('"'):  # This indicates a new polygon
                if current_polygon:
                    polygon_data[current_polygon] = vertices
                current_polygon = line.split('"')[1].strip()  # Extract the polygon name
                vertices = []
            elif line.strip().startswith('V'):  # This is a vertex line
                try:
                    vertex = line.split('=')[1].strip()
                    vertex = tuple(map(float, vertex.strip('()').split(',')))
                    vertices.append(vertex)
                except ValueError:
                    pass  # Handle any lines that don't match the expected format
        if current_polygon:
            polygon_data[current_polygon] = vertices  # Add the last polygon

        # Debugging: Print the extracted polygon data
        print("Extracted Polygon Data:")
        print(polygon_data)
        
        # If polygon_data is empty, return an empty DataFrame
        if not polygon_data:
            print("No polygons data extracted.")
            return pd.DataFrame()
        
        # Get the maximum number of vertices in any polygon
        max_vertices = max(len(vertices) for vertices in polygon_data.values())

        # Create a DataFrame to store the polygon data
        result = []
        for polygon_name, vertices in polygon_data.items():
            # Fill missing vertex data with blanks
            vertices = list(vertices) + [''] * (max_vertices - len(vertices))
            result.append([polygon_name] + vertices)
        
        # Create the DataFrame and assign column names
        polygon_df = pd.DataFrame(result)
        column_names = ['Polygon'] + [f'V{i+1}' for i in range(max_vertices)]
        polygon_df.columns = column_names

    return polygon_df

# Path to the .inp file
inp_file_path = input("Enter the path to the .inp file: ")
polygon_df = extract_polygons(inp_file_path)
polygon_df.to_csv("Polygon.csv")
print(polygon_df)


# Add new column SH2 (after Space column)
# 
