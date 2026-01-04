import pandas as pd

def rank_weekend_getaways(source_city, dataset_path='data\Top Indian Places to Visit.csv'):
    # Load dataset
    df = pd.read_csv(dataset_path)
    
    # Identify Source City details
    city_info = df[df['City'].str.lower() == source_city.lower()]
    
    if city_info.empty:
        return f"City '{source_city}' not found in dataset."
    
    source_zone = city_info.iloc[0]['Zone']
    source_state = city_info.iloc[0]['State']
    
    # Filter destinations (exclude source city)
    destinations = df[df['City'].str.lower() != source_city.lower()].copy()
    
    # Calculate Proximity Score (Distance Proxy)
    def get_proximity_score(row):
        if row['State'] == source_state:
            return 10
        elif row['Zone'] == source_zone:
            return 5
        return 0
            
    destinations['Proximity_Score'] = destinations.apply(get_proximity_score, axis=1)
    
    # Rank Score = (Rating * 2) + (Popularity * 1.5) + Proximity_Score
    destinations['Rank_Score'] = (destinations['Google review rating'] * 2) + \
                                 (destinations['Number of google review in lakhs'] * 1.5) + \
                                 destinations['Proximity_Score']
    
    # Sort and return top 5
    return destinations.sort_values(by='Rank_Score', ascending=False).head(5)

if __name__ == "__main__":
    for city in ["Delhi", "Mumbai", "Bengaluru"]:
        print(f"\nTop 5 Getaways from {city}:")
        print(rank_weekend_getaways(city)[['Name', 'City', 'Rank_Score']])