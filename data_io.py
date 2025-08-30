import json 
import os

def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return None

def write_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

# User management functions
def create_user(email, password, name, birthday="", gender=""):
    users = load_json("data/users.json")
    if users is None:
        users = []
    
    users.append({
        "id": len(users) + 1,
        "email": email,
        "password": password,
        "name": name,
        "birthday": birthday,
        "gender": gender,
        "avatar": "img/avatar.jpg"  # Default avatar
    })
    write_json("data/users.json", users)

def get_user_by_id(id):
    users = load_json("data/users.json")
    if users is None:
        return None
    
    for user in users:
        if user["id"] == id:
            return user
    return None

def get_user_by_email(email):
    users = load_json("data/users.json")
    if users is None:
        return None
    
    for user in users:
        if user["email"] == email:
            return user
    return None

def get_user_by_email_and_password(email, password):
    users = load_json("data/users.json")
    if users is None:
        return None
    
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user
    return None

def update_user(id, name, birthday="", gender="None"):
    users = load_json("data/users.json")
    if users is None:
        return
    
    for user in users:
        if user["id"] == id:
            user["name"] = name
            user["birthday"] = birthday
            user["gender"] = gender
            break
    write_json("data/users.json", users)

def update_user_avatar(id, avatar):
    users = load_json("data/users.json")
    if users is None:
        return
    
    for user in users:
        if user["id"] == id:
            user["avatar"] = avatar
            break
    write_json("data/users.json", users)

# Film management functions
def load_films():
    """Load all films from film.json"""
    films = load_json("data/film.json")
    if films is None:
        return []
    return films.get("movies", [])

def get_film_by_id(film_id):
    """Get film by ID"""
    films = load_films()
    for film in films:
        if film["id"] == film_id:
            return film
    return None

def get_film_by_name(name):
    """Search films by name (case-insensitive)"""
    films = load_films()
    if not name.strip():
        return films
    
    matching_films = []
    search_name = name.lower().strip()
    
    for film in films:
        if search_name in film["title"].lower():
            matching_films.append(film)
    
    return matching_films

def get_films_by_genre(genre):
    """Get films by genre"""
    films = load_films()
    matching_films = []
    
    for film in films:
        if genre.lower() in [g.lower() for g in film["genre"]]:
            matching_films.append(film)
    
    return matching_films

def get_films_by_country(country):
    """Get films by country"""
    films = load_films()
    matching_films = []
    
    for film in films:
        if country.lower() in film["country"].lower():
            matching_films.append(film)
    
    return matching_films

def get_recent_films(limit=10):
    """Get recent films (sorted by release date)"""
    films = load_films()
    # Sort by release date (newest first)
    sorted_films = sorted(films, key=lambda x: x["release_date"], reverse=True)
    return sorted_films[:limit]

def get_films_by_year(year):
    """Get films by release year"""
    films = load_films()
    matching_films = []
    
    for film in films:
        if film["release_date"].startswith(str(year)):
            matching_films.append(film)
    
    return matching_films

# Favorite management functions
def load_favorites():
    """Load user favorites from favorites.json"""
    favorites = load_json("data/favorites.json")
    if favorites is None:
        return {}
    return favorites

def save_favorites(favorites):
    """Save user favorites to favorites.json"""
    write_json("data/favorites.json", favorites)

def add_to_favorites(user_id, film_id):
    """Add film to user favorites"""
    favorites = load_favorites()
    
    if str(user_id) not in favorites:
        favorites[str(user_id)] = []
    
    if film_id not in favorites[str(user_id)]:
        favorites[str(user_id)].append(film_id)
        save_favorites(favorites)
        return True
    return False

def remove_from_favorites(user_id, film_id):
    """Remove film from user favorites"""
    favorites = load_favorites()
    
    if str(user_id) in favorites and film_id in favorites[str(user_id)]:
        favorites[str(user_id)].remove(film_id)
        save_favorites(favorites)
        return True
    return False

def is_favorite(user_id, film_id):
    """Check if film is in user favorites"""
    favorites = load_favorites()
    
    if str(user_id) in favorites:
        return film_id in favorites[str(user_id)]
    return False

def get_user_favorites(user_id):
    """Get all favorite films for a user"""
    favorites = load_favorites()
    
    if str(user_id) not in favorites:
        return []
    
    favorite_films = []
    all_films = load_films()
    
    for film_id in favorites[str(user_id)]:
        film = get_film_by_id(film_id)
        if film:
            favorite_films.append(film)
    
    return favorite_films

# Utility functions
def normalize_path(path):
    """Normalize file path for cross-platform compatibility"""
    if path:
        return os.path.normpath(path)
    return path

def get_film_poster_path(film):
    """Get the poster/banner path for a film"""
    if "img" in film:
        return film["img"]
    else:
        return "img/default_poster.jpg"

def get_film_video_path(film):
    """Get the video path for a film"""
    if "trailer" in film:
        return film["trailer"]
    else:
        return None