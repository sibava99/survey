from serpapi import GoogleSearch

params = {
    "engine": "google_scholar",
    "q": "biology",
    "api_key": "547d24801ea6012fcdd4c9dfee999baecadcbfc3b9c46e9490035ae2d83522e0",
}

search = GoogleSearch(params)
results = search.get_dict()
organic_results = results["organic_results"]
print(organic_results)
