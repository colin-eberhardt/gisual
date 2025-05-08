import zipfile 

from fastkml import KML, Placemark
from fastkml.utils import find, find_all
from bs4 import BeautifulSoup

def extract_kml_file(kmz_path:str) -> str:
    """
        Extracts KML file from the provided KMZ file.

        Parameters:
        -------------
            kmz_path: string
                Path to the KMZ file provided.

        Reponse:
        -------------
            output_path: string
                Path to the KML file that was extracted
    """
    with zipfile.ZipFile(kmz_path, 'r') as kmz_file:
        for file in kmz_file.namelist():
            content = kmz_file.read(file)

            output_path = f'./data/{file}'
            with open(output_path, 'wb') as kml_file:
                kml_file.write(content)
            print(f'Extracted KML file: {output_path}')
            return output_path

    # Handle an error here

def convert_kml(kml_path:str) -> list:
    """
        Converts the KML content into a list of station dicts.

        Parameters:
        -------------
            kml_path: string
                Path to the KML file to convert.

        Reponse:
        -------------
            stations: list
                A list of station dicts 
                e.g.: {"line":"Manayunk Norristown Line", "station":"Elm Street", "lat": 40, "long":-75}
    """
    stations=[]
    # Parse the KML file with fastkml 
    kml_parsed = KML.parse(kml_path)
    
    # Find all Placemarks
    placemarks = list(find_all(kml_parsed, of_type=Placemark))

    # Iterate through placemarks to find all rows 
    for placemark in placemarks:
        soup = BeautifulSoup(placemark.description, 'html.parser')
        rows = soup.find_all('tr')

        # Iterate through rows to create station dict for each stop
        for row in rows:
            cells = row.find_all('td')
            if(cells[0].string == 'Station_Na'):
                station_name = cells[1].string
                stations.append({'line': placemark.name, 'station': station_name, 'lat': float(placemark.geometry.y), 'long': float(placemark.geometry.x)})
    
    return stations


