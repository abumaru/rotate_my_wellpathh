# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 03:07:09 2019

@author: GOGUT
script to rotate your well 
"""
# =============================================================================
# INPUT DATA:
# =============================================================================
from pathlib import Path, PureWindowsPath
# I've explicitly declared my path as being in Windows format, so I can use forward slashes in it.
data_folder = PureWindowsPath(r"Y:\ressim\lavani-deep\dg2\simu1\new_well_paths_ref_case_aquifer\include\well_paths\Rotated_wellpaths")
data_name = "LS1NW_NEW.xlsx"
# Convert path to the right format for the current operating system
correct_path = Path(data_folder / data_name)
# prints "source_data/text_files/raw_data.txt" on Mac and Linux
# prints "source_data\text_files\raw_data.txt" on Windows
data_name_lenght = len(data_name)
data_name_point = data_name.find('.')
rot_angle_degrees = -51
data_name_new = data_name[0:data_name_point]+str(rot_angle_degrees)+data_name[-5:]
data_name_new_txt = data_name[0:data_name_point]+str(rot_angle_degrees)+".dev"
new_file = Path(data_folder / data_name_new)
new_file2 = Path(data_folder / data_name_new_txt)
print(new_file)
print(new_file2)
#
#
# =============================================================================
# modules import 
# =============================================================================
#import numpy as np
import math 
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
#
#
# =============================================================================
# functions for rotation
# =============================================================================
def Rotatepointx(x,y,cx,cy,angl):
    xrot = math.cos(math.radians(angl))*(x-cx)-math.sin(math.radians(angl))*(y-cy)+cx
    return xrot
def Rotatepointy(x,y,cx,cy,angl): 
    yrot = math.sin(math.radians(angl))*(x-cx)+math.cos(math.radians(angl))*(y-cy)+cy
    return yrot
#
#
# =============================================================================
# reading from data from excel file to pandas 
# =============================================================================
df= pd.read_excel(correct_path)
'''
Columns in dataset: East_X	North_Y	TVDMSL	MDMS
'''
df['TVD_neg']=df['TVDMSL']*(-1) # negative TVD
df['MD_diff']= df['MDMSL'].diff() # delta MD
df['TVD_diff']= df['TVDMSL'].diff() # delta TVD
df['Disp']=((df['MD_diff']**2)-(df['TVD_diff']**2))**0.5 # Displacement
df['Cum.Disp']=df['Disp'].cumsum() # Cumulative displacement 
df['ratio Disp/MD_diff']= df['Disp']/df['MD_diff'] # ratio. intermediate calculation
df['Incl_degrees']= [math.degrees(math.asin(row)) for row in df['ratio Disp/MD_diff']] # Calculates the inclication at each survey.
df['Cum.Disp'].fillna(0,inplace=True) # replacing from nan values to cero.
df2= df[['East_X','North_Y','MDMSL','Cum.Disp','TVD_neg','Incl_degrees']] # final dataset df2
df2['xrot']=Rotatepointx(df2['East_X'],df2['North_Y'],df2['East_X'].iloc[31],df2['North_Y'].iloc[31],rot_angle_degrees) # East_x rotated arround first point.
df2['yrot']=Rotatepointy(df2['East_X'],df2['North_Y'],df2['East_X'].iloc[31],df2['North_Y'].iloc[31],rot_angle_degrees) # North_y rotated arround first point.
#
#
# =============================================================================
# Plotting data in 3D
# =============================================================================
'''
Data from initial well survey
'''
x = list(df2['East_X'])
y = list(df2['North_Y'])
z = list(df2['TVD_neg'])
'''
Data from rotated well survey
'''
x1 = list(df2['xrot'])
y1 = list(df2['yrot'])
z1 = list(df2['TVD_neg'])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z,color='b', marker='o') #initial well survey
ax.scatter(x1,y1,z1,color='r', marker='o')# rotated survey
ax.set_xlabel('East_X')
ax.set_ylabel('North_Y')
ax.set_zlabel('Z TVD')
#

# =============================================================================
# generates xlsx file with df2 as feed
# =============================================================================
df2.to_excel(new_file,index=False)
print("new wellpath:" ,new_file)
#
#
# =============================================================================
# generate a .dev file  with df3 as feed
# =============================================================================

df2['TVDMSL2']=df['TVDMSL'] 
df3 = df2[['xrot','yrot','TVDMSL2','MDMSL',]]
print(df3)
df3.to_csv(new_file2, index=None, sep=' ', mode='a')
print("new wellpath:" ,new_file2)
