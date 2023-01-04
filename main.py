import folium
from folium.plugins import MarkerCluster

amount_of_points = 5_583
distance_between_points=0.0006/10
start_location = [ (48.8566, 2.3522)]

paris_map = folium.Map( location=[48.8566, 2.3522], zoom_start=6 )

marker_cluster = MarkerCluster().add_to(paris_map)

# Add markers
for coord in start_location:
    for i in range(0,int(5_583)):
        long=coord[0]+(distance_between_points*i)
        lat= coord[1]+(distance_between_points*i)
        print(long, lat)
        folium.Marker( location=[ long, lat ], fill_color='#43d9de', radius=8 ).add_to( paris_map ).add_to(marker_cluster)

paris_map.save('map.html')