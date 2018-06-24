import geopandas as gpd
from fiona.crs import from_epsg
from pyproj import Proj, transform
from shapely.geometry import Point
import matplotlib.pyplot as plt
import os
import shutil

# Read original files
ptopo = gpd.read_file('PTOPO18.shp')
lamp = gpd.read_file('LAMP18.shp')
reg = gpd.read_file('REG18.shp')

# Define Projection as Lambert Conformal Conique Morocco Zone 1
ptopo.crs = from_epsg(26191)
lamp.crs = from_epsg(26191)
reg.crs = from_epsg(26191)

# Making a backup of the original files
if not os.path.exists('Backup'):
	os.makedirs('Backup')

	for f in os.listdir():
		# if not f.endswith('py'):
		path = os.path.join('Backup', f)
		if not os.path.exists(path):
			shutil.move(f, 'Backup')	

# Exporting the projected shapefile
if not os.path.exists('PTOPO18.shp'):
    ptopo.to_file('PTOPO18.shp')
    lamp.to_file('LAMP18.shp')
    reg.to_file('REG18.shp')
else:
    print('File already exists')

# Defining source and target projection
inProj = Proj(init='epsg:26191')
outProj = Proj(init='epsg:4326')

# Making empty geodataframes for the wgs projection
ptopo_wgs = gpd.GeoDataFrame()
lamp_wgs = gpd.GeoDataFrame()
reg_wgs = gpd.GeoDataFrame()

# Populating the geodataframes

# PTOPO18
design_ptopo = []
empl_ptopo = []
xy_ptopo = []

for key, row in ptopo.iterrows():
    design_ptopo.append(row[0])
    empl_ptopo.append(row[1])
    xy_ptopo.append(Point(transform(inProj, outProj, row[2].x, row[2].y)))

ptopo_wgs['DESIGN'] = design_ptopo
ptopo_wgs['EMPL'] = empl_ptopo
ptopo_wgs['geometry'] = xy_ptopo

# LAMP18
num_lamp = []
type_lamp = []
etat_lamp = []
xy_lamp = []

for key, row in lamp.iterrows():
	num_lamp.append(row[0])
	type_lamp.append(row[1])
	etat_lamp.append(row[2])
	xy_lamp.append(Point(transform(inProj, outProj, row[3].x, row[3].y)))

lamp_wgs['NUM'] = num_lamp
lamp_wgs['TYPE'] = type_lamp
lamp_wgs['ETAT'] = etat_lamp
lamp_wgs['geometry'] = xy_lamp

# REG18
num_reg = []
type_reg = []
situation_reg = []
xy_reg = []
for key, row in reg.iterrows():
	num_reg.append(row [0])
	type_reg.append(row[1])	
	situation_reg.append(row[2])
	xy_reg.append(Point(transform(inProj, outProj, row[3].x, row[3].y)))

reg_wgs['NUM'] = num_reg
reg_wgs['TYPE'] = type_reg
reg_wgs['SITUATION'] = situation_reg
reg_wgs['geometry'] = xy_reg

#Defining projections for geodataframes
ptopo_wgs.crs = from_epsg(4326)
lamp_wgs.crs = from_epsg(4326)
reg_wgs.crs = from_epsg(4326)

# Exporting projected geodataframes
if not os.path.exists('WGS'):
	os.makedirs('WGS')

ptopo_wgs.to_file(r'WGS\PTOPO18_WGS.shp')
lamp_wgs.to_file(r'WGS\LAMP18_WGS.shp')
reg_wgs.to_file(r'WGS\REG18_WGS.shp')

# Plotting

# Lambert Conformal Conique Morocco Zone 1
base = ptopo.plot(marker='+', color='red', label='Point Topo')
lamp.plot(ax=base, marker='o', color='yellow', label='Lampe')
reg.plot(ax=base, marker='x', color='blue', label='Regard')
plt.title('Lambert Conformal Conique\nMorocco Zone 1\n')
plt.legend()

# WORLD WGS 1984
base2 = ptopo_wgs.plot(marker='+', color='red', label='Point Topo')
lamp_wgs.plot(ax=base2, marker='o', color='yellow', label='Lampe')
reg_wgs.plot(ax=base2, marker='x', color='blue', label='Regard')
plt.title('WGS 1984\n')
plt.legend()


# TO DO IGNORE INTERVAL AND FILL WHITE SPACE

plt.show()
