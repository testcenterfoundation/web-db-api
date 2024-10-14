import os
import re

def convert_fitnesse_to_robot(fitnesse_dir, output_dir):
    for root, dirs, files in os.walk(fitnesse_dir):
        for file in files:
            if file.endswith('.wiki'):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, fitnesse_dir)
                output_path = os.path.join(output_dir, relative_path.replace('.wiki', '.robot'))
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
                    content = infile.read()
                    robot_content = convert_content(content)
                    outfile.write(robot_content)

def convert_content(content):
    # Basisstructuur voor Robot Framework
    robot_content = "*** Settings ***\n"
    robot_content += "Library    Browser\n\n"
    robot_content += "*** Variables ***\n\n"
    robot_content += "*** Test Cases ***\n"

    # Converteer FitNesse tabellen naar Robot Framework syntax
    tables = re.findall(r'\|(.*?)\|\n', content, re.DOTALL)
    for table in tables:
        rows = table.strip().split('\n')
        if rows[0].strip().lower().startswith('test'):
            robot_content += f"\n{rows[0].strip()}\n"
            for row in rows[1:]:
                cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                if cells:
                    robot_content += f"    {cells[0]}    {'    '.join(cells[1:])}\n"

    return robot_content

# Gebruik het script
fitnesse_dir = '/pad/naar/fitnesse/tests'
output_dir = '/pad/naar/robot/framework/tests'
convert_fitnesse_to_robot(fitnesse_dir, output_dir)
