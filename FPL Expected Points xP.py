import requests
import pandas as pd
import http.client
import json
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Dynamically generate a figure for gameweek
dynamic_number = 8  

# Set the date range dynamically
from_date = '2024-10-19'
to_date = '2024-10-21'

folder_name = f"Gameweek_{dynamic_number}"

# Create the folder
os.makedirs(folder_name, exist_ok=True)

# URL of the FPL API endpoint
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# Fetch data from the endpoint
response = requests.get(url)
data = response.json()

# Extract relevant data
players = data['elements']
teams = data['teams']
positions = data['element_types']

# Create a dictionary to map team IDs to team names
team_dict = {team['id']: team['name'] for team in teams}

# Create a dictionary to map position IDs to position names
position_dict = {position['id']: position['singular_name'] for position in positions}

# Extract player details and store them in a list of dictionaries
player_details = []
for player in players:
    player_info = {
        'Full Name': f"{player['first_name']} {player['second_name']}",  # Combine first and second names
        'Team': team_dict[player['team']],
        'Position': position_dict[player['element_type']],
        'Price': player['now_cost'] / 10.0,  # Price is in tenths of a million
        'Ownership (%)': player['selected_by_percent'],  # Ownership percentage
        'Injured': player['status'] == 'i'  # True if player is injured
    }
    player_details.append(player_info)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(player_details)

name_replacements = {
    "Álex Moreno Lopera": "Alex Moreno",
    "Abdoulaye Doucouré": "Abdoulaye Doucoure",
    "Ali Al-Hamadi": "Ali Al Hamadi",
    "Andreas Hoelgebaum Pereira": "Andreas Pereira",
    "Antony Matheus dos Santos": "Antony",
    "Benjamin White": "Ben White",
    "Benoît Badiashile": "Benoit Badiashile",
    "Bernardo Veiga de Carvalho e Silva": "Bernardo Silva",
    "Boubacar Traoré": "Boubacar Traore",
    "Boubakary Soumaré": "Boubakary Soumare",
    "Bruno Borges Fernandes": "Bruno Fernandes",
    "Bruno Guimarães Rodriguez Moura": "Bruno Guimaraes",
    "Carlos Alcaraz Durán": "Carlos Alcaraz",
    "Carlos Henrique Casimiro": "Casemiro",
    "Carlos Vinícius Alves Morais": "Carlos Vinicius",
    "Chadi Riad Dnanou": "Chadi Riad",
    "Cheick Doucouré": "Cheick Doucoure",
    "Christian Nørgaard": "Christian Norgaard",
    "Danilo dos Santos de Oliveira": "Danilo",
    "Darwin Núñez Ribeiro": "Darwin Nunez",
    "Diogo Dalot Teixeira": "Diogo Dalot",
    "Diogo Teixeira da Silva": "Diogo Jota",
    "Dominic Solanke-Mitchell": "Dominic Solanke",
    "Edson Álvarez Velázquez": "Edson Alvarez",
    "Emerson Palmieri dos Santos": "Emerson Palmieri",
    "Emiliano Buendía Stati": "Emiliano Buendia",
    "Endo Wataru": "Wataru Endo",
    "Enzo Fernández": "Enzo Fernandez",
    "Eric da Silva Moreira": "Eric Moreira",
    "Ezri Konsa Ngoyo": "Ezri Konsa",
    "Fábio Ferreira Vieira": "Fabio Vieira",
    "Fábio Freitas Gouveia Carvalho": "Fabio Carvalho",
    "Fabian Schär": "Fabian Schar",
    "Facundo Pellistri Rebollo": "Facundo Pellistri",
    "Francisco Jorge Tomás Oliveira": "Francisco Oliveira",
    "Gabriel dos Santos Magalhães": "Gabriel Magalhaes",
    "Gabriel Fernando de Jesus": "Gabriel Jesus",
    "Gabriel Martinelli Silva": "Gabriel Martinelli",
    "Gonçalo Manuel Ganchinho Guedes": "Manuel Goncalo Guedes",
    "Guido Rodríguez": "Guido Rodriguez",
    "Hugo Bueno López": "Hugo Bueno",
    "Hwang Hee-chan": "Hee-Chan Hwang",
    "Ibrahim Sangaré": "Ibrahim Sangare",
    "Ibrahima Konaté": "Ibrahima Konate",
    "Igor Julio dos Santos de Paulo": "Igor Julio",
    "Iliman Ndiaye": "Iliman-Cheikh Ndiaye",
    "Ismaïla Sarr": "Ismaila Sarr",
    "Jørgen Strand Larsen": "Jorgen Strand Larsen",
    "Jérémy Doku": "Jeremy Doku",
    "Jaden Philogene": "Jayden Philogene-Bidace",
    "Jean-Ricner Bellegarde": "Jeanricner Bellegarde",
    "Jefferson Lerma Solís": "Jefferson Lerma",
    "Jeffrey Schlupp": "Jeff Schlupp",
    "Jeremy Sarmiento Morante": "Jeremy Sarmiento",
    "Jhon Durán": "Jhon Duran",
    "Joško Gvardiol": "Josko Gvardiol",
    "João Pedro Junqueira de Jesus": "Joao Pedro",
    "João Victor Gomes da Silva": "Joao Gomes",
    "Joël Veltman": "Joel Veltman",
    "Joelinton Cássio Apolinário de Lira": "Joelinton",
    "Jorge Cuenca Barreno": "Jorge Cuenca",
    "Jorge Luiz Frello Filho": "Jorginho",
    "Juan Larios López": "Juan Larios",
    "Jurriën Timber": "Jurrien Timber",
    "Kim Ji-soo": "Ji-soo Kim",
    "Kosta Nedeljković": "Kosta Nedeljkovic",
    "Lisandro Martínez": "Lisandro Martinez",
    "Lucas Tolentino Coelho de Lima": "Lucas Paqueta",
    "Luis Díaz": "Luis Diaz",
    "Luis Guilherme Lira dos Santos": "dos Santos Luis Guilherme",
    "Mads Roerslev Rasmussen": "Mads Roerslev",
    "Marc Cucurella Saseta": "Marc Cucurella",
    "Marc Guéhi": "Marc Guehi",
    "Marc Guiu Paz": "Marc Guiu",
    "Marcus Myers-Harness": "Marcus Harness",
    "Martin Ødegaard": "Martin Odegaard",
    "Mateo Kovačić": "Mateo Kovacic",
    "Matheus Luiz Nunes": "Matheus Nunes",
    "Matheus Santos Carneiro Da Cunha": "Matheus Cunha",
    "Mathias Jorgensen": "Mathias Zanka Jorgensen",
    "Micky van de Ven": "Mickey van de Ven",
    "Miguel Almirón Rejala": "Miguel Almiron",
    "Mitoma Kaoru": "Kaoru Mitoma",
    "Murillo Santiago Costa dos Santos": "Murillo",
    "Nélson Cabral Semedo": "Nelson Semedo",
    "Nathan Aké": "Nathan Ake",
    "Niclas Füllkrug": "Niclas Fullkrug",
    "Nicolás Domínguez": "Nicolas Dominguez",
    "Nikola Milenković": "Nikola Milenkovic",
    "Pape Matar Sarr": "Pape Sarr",
    "Pedro Cardoso de Lima": "Cardoso Pedro Lima",
    "Pedro Lomba Neto": "Pedro Neto",
    "Pervis Estupiñán": "Pervis Estupinan",
    "Raúl Jiménez": "Raul Jimenez",
    "Radu Drăgușin": "Radu Dragusin",
    "Rúben Gato Alves Dias": "Ruben Dias",
    "Rayan Aït-Nouri": "Rayan Ait Nouri",
    "Renato Palma Veiga": "Renato Veiga",
    "Ricardo Barbosa Pereira": "Domingos Ricardo Pereira",
    "Richarlison de Andrade": "Richarlison",
    "Rodrigo Martins Gomes": "Martins Rodrigo Gomes",
    "Rodrigo Muniz Carvalho": "Rodrigo Muniz",
    "Rodrigo 'Rodri' Hernandez": "Rodri",
    "Roméo Lavia": "Romeo Lavia",
    "Sávio 'Savinho' Moreira de Oliveira": "Savio",
    "Séamus Coleman": "Seamus Coleman",
    "Sékou Mara": "Sekou Mara",
    "Saša Lukić": "Sasa Lukic",
    "Son Heung-min": "Heung-Min Son",
    "Sugawara Yukinari": "Yukinari Sugawara",
    "Tim Iroegbunam": "Timothy Iroegbunam",
    "Tino Livramento": "Valentino Livramento",
    "Tom Cannon": "Thomas Cannon",
    "Tomáš Souček": "Tomas Soucek",
    "Toti António Gomes": "Toti Gomes",
    "Valentín Barco": "Valentin Barco",
    "Victor Lindelöf": "Victor Lindelof",
    "Vitalii Mykolenko": "Vitaliy Mykolenko",
    "Vladimír Coufal": "Vladimir Coufal",
    "Wanya Marçal-Madivadua": "Wanya Marcal-Madivadua",
    "Wilfred Ndidi": "Onyinye Ndidi",
    "Will Smallbone": "William Smallbone",
    "Yehor Yarmoliuk": "Yegor Yarmolyuk"
}

team_replacements = {
    "Man City": "Manchester City",
    "Man Utd": "Manchester United",
    "Nott'm Forest": "Nottingham Forest",
    "Spurs": "Tottenham"
}

df['Full Name'] = df['Full Name'].replace(name_replacements)
df['Team'] = df['Team'].replace(team_replacements)

folder_path = os.path.join(r"C:\Users\conor\OneDrive\Desktop\FPL xP", f"Gameweek_{dynamic_number}")

# Save the DataFrame to a CSV file within the folder
file_path = os.path.join(folder_path, "fantasy.csv")
df.to_csv(file_path, index=False)

cleansheet_mapping = {
    'Defender': 4,
    'Goalkeeper': 4,
    'Midfielder': 1,
    'Forward': 0
}

df['CS Value'] = df['Position'].map(cleansheet_mapping)

anytime_mapping = {
    'Defender': 6,
    'Goalkeeper': 6,
    'Midfielder': 5,
    'Forward': 4
}

df['Anytime Value'] = df['Position'].map(anytime_mapping)

ormore_mapping = {
    'Defender': 12,
    'Goalkeeper': 12,
    'Midfielder': 10,
    'Forward': 8
}

df['2ormore Value'] = df['Position'].map(ormore_mapping)

df.head()

# Establish the connection
conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "YOUR_API_KEY",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

# Step 1: Get the fixture IDs
url = f"/v3/fixtures?league=39&season=2024&from={from_date}&to={to_date}"
conn.request("GET", url, headers=headers)
res = conn.getresponse()
data = res.read()
json_data = json.loads(data.decode("utf-8"))

# Step 2: Extract the fixture IDs (handle cases where response may be empty)
fixture_ids = [fixture['fixture']['id'] for fixture in json_data.get('response', [])]

# Define the bet IDs you want to query
bet_ids = [92, 95]

# Step 3: Initialize a list to hold all odds data
all_odds_data = []

# Step 4: Loop through each fixture ID and bet ID to get odds
for fixture_id in fixture_ids:
    for bet_id in bet_ids:
        conn.request("GET", f"/v3/odds?league=39&season=2024&fixture={fixture_id}&bookmaker=1&bet={bet_id}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))

        # Extract odds data for each bet type (handle cases where response may be empty)
        bookmakers = json_data.get('response', [])
        if bookmakers:
            bookmakers = bookmakers[0].get('bookmakers', [])
            for bookmaker in bookmakers:
                for bet in bookmaker.get('bets', []):
                    if bet.get('id') == bet_id:
                        bet_data = bet.get('values', [])
                        for item in bet_data:
                            item['bet_id'] = bet_id  # Add bet_id to each item
                            all_odds_data.append(item)

# Step 5: Create the DataFrame
df1 = pd.DataFrame(all_odds_data)
df1.head()

# Handle possible missing or improperly formatted data in 'odd' column
df1['odd'] = df1['odd'].apply(lambda x: x.split('.')[0] if isinstance(x, str) and '.' in x else x)

# Step 6: Remove duplicates and aggregate odds
duplicates = df1[df1.duplicated(subset=['value', 'bet_id'], keep=False)]
df1_aggregated = df1.groupby(['value', 'bet_id']).agg({'odd': 'mean'}).reset_index()

# Step 7: Pivot the DataFrame
df_pivot = df1_aggregated.pivot(index='value', columns='bet_id', values='odd').reset_index()

# Rename the columns for better readability
df_pivot.columns = ['Full Name', 'anytime', '2ormore']

df_pivot.head()

master = df.merge(df_pivot, on='Full Name', how='left')
master.fillna(0.1, inplace=True)
master.head()

#HOME AND AWAY ODDS

# Establish connection and set headers
conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "YOUR_API_KEY",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

# Make the request
endpoint = f"/v3/fixtures?from={from_date}&to={to_date}&league=39&season=2024"
conn.request("GET", endpoint, headers=headers)

# Get the response
res = conn.getresponse()
data = res.read()

# Decode the data to a string and then to JSON
json_data = json.loads(data.decode("utf-8"))

# Extract fixture IDs, home teams, and away teams
fixture_ids = [fixture['fixture']['id'] for fixture in json_data['response']]
home_teams = [fixture['teams']['home']['name'] for fixture in json_data['response']]
away_teams = [fixture['teams']['away']['name'] for fixture in json_data['response']]

# Create DataFrame
df = pd.DataFrame({
    'Fixture ID': fixture_ids,
    'Home Team': home_teams,
    'Away Team': away_teams
})

# Initialize lists to store the 'Yes' odds for both home and away teams
home_yes_odds = []
away_yes_odds = []

# Loop through each Fixture ID in the DataFrame
for fixture_id in df['Fixture ID']:
    # Reinitialize connection for home odds
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

    # API call to get home team odds (bet ID 27)
    endpoint_home = f"/v3/odds?fixture={fixture_id}&league=39&season=2024&bookmaker=1&bet=27"
    conn.request("GET", endpoint_home, headers=headers)
    res_home = conn.getresponse()
    data_home = res_home.read()
    decoded_data_home = json.loads(data_home.decode("utf-8"))
    
    # Extract the 'Yes' odds for home
    home_yes_value = None
    try:
        response_data_home = decoded_data_home.get('response', [])
        if response_data_home:
            bookmakers_home = response_data_home[0].get('bookmakers', [])
            if bookmakers_home:
                bets_home = bookmakers_home[0].get('bets', [])
                if bets_home:
                    values_home = bets_home[0].get('values', [])
                    home_yes_value = next((item['odd'] for item in values_home if item['value'] == 'Yes'), None)
    except (IndexError, KeyError):
        pass
    
    # Reinitialize connection for away odds
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

    # API call to get away team odds (bet ID 28)
    endpoint_away = f"/v3/odds?fixture={fixture_id}&league=39&season=2024&bookmaker=1&bet=28"
    conn.request("GET", endpoint_away, headers=headers)
    res_away = conn.getresponse()
    data_away = res_away.read()
    decoded_data_away = json.loads(data_away.decode("utf-8"))
    
    # Extract the 'Yes' odds for away
    away_yes_value = None
    try:
        response_data_away = decoded_data_away.get('response', [])
        if response_data_away:
            bookmakers_away = response_data_away[0].get('bookmakers', [])
            if bookmakers_away:
                bets_away = bookmakers_away[0].get('bets', [])
                if bets_away:
                    values_away = bets_away[0].get('values', [])
                    away_yes_value = next((item['odd'] for item in values_away if item['value'] == 'Yes'), None)
    except (IndexError, KeyError):
        pass
    
    # Append the 'Yes' odds to the lists
    home_yes_odds.append(home_yes_value)
    away_yes_odds.append(away_yes_value)

# Add the 'Yes' odds to the DataFrame
df['Home Yes Odds'] = home_yes_odds
df['Away Yes Odds'] = away_yes_odds
df.head()

# Create a new column in the master dataframe to store the CS odds
master['CS odds'] = None

# Iterate through each row in the master dataframe
for index, row in master.iterrows():
    team = row['Team']
    
    # Check if the team is in the Home Team column of df
    home_match = df[df['Home Team'] == team]
    if not home_match.empty:
        master.at[index, 'CS odds'] = home_match['Home Yes Odds'].values[0]
    else:
        # Check if the team is in the Away Team column of df
        away_match = df[df['Away Team'] == team]
        if not away_match.empty:
            master.at[index, 'CS odds'] = away_match['Away Yes Odds'].values[0]

file_path = os.path.join(folder_path, "odds.csv")
master.to_csv(file_path, index=False)
master.head()

master['anytime'] = pd.to_numeric(master['anytime'], errors='coerce')
master['2ormore'] = pd.to_numeric(master['2ormore'], errors='coerce')
master['CS odds'] = pd.to_numeric(master['CS odds'], errors='coerce')

# Optionally fill NaN values with a specific value and then convert to integer
master['anytime'] = master['anytime'].fillna(0).astype(int)
master['2ormore'] = master['2ormore'].fillna(0).astype(int)
master['CS odds'] = master['CS odds'].fillna(0).astype(int)

master['1 Goal Probability'] = (1 / master['anytime'])
master['2 Goal Probability'] = (1 / master['2ormore'])
master['CS Probability'] = (1 / master['CS odds'])

master['Anytime Expected'] = master['1 Goal Probability'] * master['Anytime Value']
master['2 Goal Expected'] = master['2 Goal Probability'] * master['2ormore Value']
master['CS Expected'] = master['CS Probability'] * master['CS Value']


master['Total xP'] = (master['CS Expected'] + master['Anytime Expected'] + master['2 Goal Expected'])
master['PPM'] = master['Total xP'] / master['Price']

# Replace all inf and -inf values with 0 in the dataframe
#master.replace([np.inf, -np.inf], 0, inplace=True)
master.head()

# Replace all inf and -inf values with NaN
master.replace([float('inf'), float('-inf')], float('nan'), inplace=True)

# Now, replace all NaN values (including the ones from inf) with 0.1
master.fillna(0.1, inplace=True)

columns_to_keep = ['Full Name', 'Team', 'Position', 'Price', 'Ownership (%)', 'Injured', 'Total xP', 'PPM']  # Adjust this list to your needs

# Create a new dataframe with only the specified columns
final = master[columns_to_keep]

file_path = os.path.join(folder_path, "final.csv")
final.to_csv(file_path, index=False)

# First, filter the dataframe to exclude players with injuries
filtered_df = master[master['Injured'] == False]

# Sort the dataframe to get the top 11 values based on 'Total xP'
top_11_df = filtered_df.nlargest(33, 'Total xP')

# Increase the figure size for better readability
plt.figure(figsize=(24, 16))

# Create the scatter plot using seaborn with customizations
scatter_plot = sns.scatterplot(data=top_11_df, x='Price', y='Total xP', s=50, marker='o', color='blue')

# Prepare a list to hold the text objects
texts = []
for i in range(top_11_df.shape[0]):
    texts.append(plt.text(top_11_df['Price'].iloc[i], top_11_df['Total xP'].iloc[i], 
                          top_11_df['Full Name'].iloc[i], fontsize=15, ha='right'))

# Visualise results
# Adjust the text to minimize overlap
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))

# Add title and labels to the axes with larger font sizes
plt.title('Top 33 Players xP', fontsize=16)
plt.xlabel('Price', fontsize=14)
plt.ylabel('Total xP', fontsize=14)

# Display grid for better readability
plt.grid(True)

# Save the plot as a JPEG image with the dynamic number in the file name
file_name = f"top_11_players_xP_{dynamic_number}.jpeg"
plt.savefig(os.path.join(folder_path, file_name), format='jpeg')

# Show the plot
plt.show()
