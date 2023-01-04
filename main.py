import folium
import haversine as hs
from folium.plugins import MarkerCluster
import xml.etree.ElementTree as ET
import math   
import numpy


stripped_cords = []
tree = ET.parse('paris_marathon.kml')
for elem in tree.iter():
    if 'coordinates' in elem.tag:
        cords = elem.text
        chunks = cords.split('\n')
        print(len(chunks))
        if len(chunks) > 3:
            for c in chunks:
                cord_str = c.strip()
                cord_str=cord_str.split(",")
                # print(cord_str)
                if len(cord_str) == 3:
                    stripped_cords.append(tuple([float(cord_str[1]),float(cord_str[0])]))
            # for c in stripped_cords:
            #     print(c)


amount_of_points = 5_583 
distance_between_points=0.0006/10
start_location = [ (48.8566, 2.3522)]

paris_map = folium.Map( location=[48.8566, 2.3522], zoom_start=6 )

marker_cluster = MarkerCluster().add_to(paris_map)

points = []

loc1 = (48.8566, 2.3522)

loc2=(28.394231,77.050308)
# Add markers
for coord in start_location:
    for i in range(0,int(5_583)):
        long=coord[0]+(distance_between_points*i)
        lat= coord[1]+(distance_between_points*i)
        loc2=(long,lat)
        points.append(tuple([long,lat]))
        # print(long, lat)
        # folium.Marker( location=[ long, lat ], fill_color='#43d9de', radius=8 ).add_to( paris_map ).add_to(marker_cluster)


distance = hs.haversine(loc1,loc2)
print(distance)
folium.PolyLine(stripped_cords, color="red", weight=2.5, opacity=1).add_to(paris_map)

sum = 0
for i in range (1, len(stripped_cords)):
    distance = hs.haversine(stripped_cords[i],stripped_cords[i-1])
    # print(stripped_cords[i],stripped_cords[i-1],hs.haversine(stripped_cords[i],stripped_cords[i-1]), sum)
    sum = sum + distance

points_per_meter = sum/amount_of_points

def getEquidistantPoints(p1, p2, parts):
    return zip(numpy.linspace(p1[0], p2[0], parts+1),
               numpy.linspace(p1[1], p2[1], parts+1))

sum = 0
points_added = 0
markers_sum = 0
last_marker_endpoint = stripped_cords[0]
for i in range (1, len(stripped_cords)):
    last_cord = stripped_cords[i-1]
    current_cord = stripped_cords[i]
    distance = hs.haversine(current_cord,last_cord)
    markers_so_far = math.ceil(sum/points_per_meter)
    difference_in_markers = markers_so_far - points_added
    if difference_in_markers > 0:
        points_added = markers_so_far

        markers = getEquidistantPoints(current_cord,last_marker_endpoint,difference_in_markers-1)
        last_marker_endpoint = last_cord

        for c in markers:
            markers_sum += 1
            # print(c)
            # folium.Marker( location=[ c[0],c[1] ], fill_color='#43d9de', radius=1 ).add_to( paris_map ).add_to(marker_cluster)
            folium.Marker( location=[ c[0],c[1] ], fill_color='#43d9de', radius=1 ).add_to( marker_cluster )

    print(current_cord,last_cord,distance, sum, markers_so_far, difference_in_markers)



    sum = sum + distance

print(len(stripped_cords))

# for i in range(0,amount_of_points):
#     print(i*points_per_meter)

print(points_added)
print(markers_sum)


paris_map.save('map.html')
