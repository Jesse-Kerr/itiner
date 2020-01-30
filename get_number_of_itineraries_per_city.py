import pandas as pd
from src.VisitACity import VisitACity

if __name__ == "__main__":
    visit_a_city = VisitACity()
    top_cities = pd.read_csv("data/top_cities.csv") # Load list of 140 cities
    city_links = dict()
    for city in top_cities.cities:
        city_links[city] = visit_a_city.get_all_guides_for_a_city(city = city)
    
    no_dupes_city_links = visit_a_city.split_dupes_into_own_entry(city_links)

    cleaned_city_links = visit_a_city.clean_guide_dict(no_dupes_city_links)
        
    visit_a_city.driver.close()

    # Save the dict
    df = pd.Series(cleaned_city_links).to_frame()
    df.to_csv("data/guides_by_city.csv")
