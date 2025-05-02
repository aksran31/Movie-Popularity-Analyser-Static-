import folium
from folium.plugins import Search

# Create base map centered on India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Indian states coordinates (lat, lon format for folium.Polygon)
indian_states = {
    "Maharashtra": [[16.0, 72.5], [17.0, 76.0], [20.0, 77.0], [21.0, 73.0], [16.0, 72.5]],
    "Delhi": [[28.4, 76.8], [28.4, 77.4], [28.8, 77.4], [28.8, 76.8], [28.4, 76.8]],
    "Uttar Pradesh": [[25.0, 77.0], [26.0, 82.0], [28.0, 84.0], [30.0, 79.0], [25.0, 77.0]],
    "Telangana": [[16.0, 77.5], [17.5, 79.5], [19.5, 80.0], [18.5, 78.0], [16.0, 77.5]],
    "Andhra Pradesh": [[14.0, 78.0], [14.5, 80.0], [18.0, 83.0], [19.0, 79.0], [14.0, 78.0]],
    "Tamil Nadu": [[8.5, 77.0], [10.0, 80.0], [13.0, 80.3], [13.5, 77.5], [8.5, 77.0]],
    "Kerala": [[8.5, 75.0], [8.5, 77.0], [12.0, 77.0], [12.5, 75.0], [8.5, 75.0]],
    "Karnataka": [[12.0, 74.0], [13.0, 77.0], [16.0, 78.0], [15.0, 74.5], [12.0, 74.0]],
    "Gujarat": [[20.0, 69.0], [21.0, 73.0], [24.5, 73.0], [23.0, 68.5], [20.0, 69.0]],
    "Punjab": [[30.0, 74.0], [30.5, 76.5], [32.0, 76.0], [31.5, 73.5], [30.0, 74.0]]
}

# 2024 Indian movies data
movies_data = [
   {"title": "Pushpa 2: The Rule", "language": "Telugu", "gross": 1755.4, 
     "states": ["Andhra Pradesh", "Telangana", "Tamil Nadu"]},
    {"title": "Kalki 2898 AD", "language": "Telugu", "gross": 1052.5, 
     "states": ["Andhra Pradesh", "Telangana", "Karnataka", "Maharashtra"]},
    {"title": "Stree 2", "language": "Hindi", "gross": 857.15, 
     "states": ["Maharashtra", "Delhi", "Uttar Pradesh"]},
    {"title": "Devara - Part 1", "language": "Telugu", "gross": 443.8, 
     "states": ["Andhra Pradesh", "Telangana"]},
    {"title": "Bhool Bhulaiyaa 3", "language": "Hindi", "gross": 396.7, 
     "states": ["Maharashtra", "Delhi", "Uttar Pradesh"]},
    {"title": "Singham Again", "language": "Hindi", "gross": 378.4, 
     "states": ["Maharashtra", "Gujarat", "Delhi"]},
    {"title": "The Greatest of All Time", "language": "Tamil", "gross": 457.12, 
     "states": ["Tamil Nadu", "Kerala"]},
    {"title": "Amaran", "language": "Tamil", "gross": 333.67, 
     "states": ["Tamil Nadu"]},
    {"title": "Fighter", "language": "Hindi", "gross": 358.89, 
     "states": ["Maharashtra", "Delhi", "Punjab"]},
    {"title": "Hanuman", "language": "Telugu", "gross": 295.29, 
     "states": ["Andhra Pradesh", "Telangana"]},
    {"title": "Maharaja", "language": "Tamil", "gross": 190.5, 
     "states": ["Tamil Nadu"]},
    {"title": "Shaitaan", "language": "Hindi", "gross": 150.2, 
     "states": ["Maharashtra", "Gujarat"]},
    {"title": "Manjummel Boys", "language": "Malayalam", "gross": 136.2, 
     "states": ["Kerala", "Tamil Nadu"]}
]
movies_data = []
with open("movies_2024.txt", "r", encoding="utf-8") as f:
    for line in f:
        title, language, gross, regions = line.strip().split("|")
        states = [s.strip() for s in regions.split(",")]
        movies_data.append({
            "title": title,
            "language": language,
            "gross": float(gross),
            "states": states
        })

# Create a feature group for each movie (all hidden by default)
movie_layers = {}
for movie in movies_data:
    movie_layer = folium.FeatureGroup(name=movie["title"], show=False)
    
    # Color based on gross collection
    if movie["gross"] > 1000:
        color = "red"  # Blockbuster
    elif movie["gross"] > 500:
        color = "orange"  # Super Hit
    else:
        color = "green"  # Hit
    
    # Add state polygons for this movie
    for state_name in movie["states"]:
        if state_name in indian_states:
            coords = indian_states[state_name]
            folium.Polygon(
                locations=coords,
                color="black",
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                tooltip=f"{movie['title']} - {state_name}<br>₹{movie['gross']} Cr"
            ).add_to(movie_layer)
    
    # Add layer to map
    movie_layer.add_to(m)
    movie_layers[movie["title"]] = movie_layer

# Create a search group to hold searchable points
search_group = folium.FeatureGroup(name="Search", control=False).add_to(m)

# Add points for search functionality
for movie in movies_data:
    # Use the first state as the marker position
    first_state = movie["states"][0]
    coords = indian_states[first_state]
    # Calculate center point
    lat = sum(c[0] for c in coords) / len(coords)
    lon = sum(c[1] for c in coords) / len(coords)
    
    folium.Marker(
        [lat, lon],
        tooltip=movie["title"],
        popup=f"<b>{movie['title']}</b><br>Language: {movie['language']}<br>Box Office: ₹{movie['gross']} Cr",
        icon=folium.Icon(color="blue")
    ).add_to(search_group)

# Add search control
Search(
    layer=search_group,
    geom_type="Point",
    placeholder="Search 2024 Indian movies...",
    collapsed=False,
    search_label="tooltip"
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map
m.save("top10_movies_2024_regions.html")
print("Map created! Open 'top10_movies_2024_regions.html' in your browser.")
