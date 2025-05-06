import zipfile 

from fastkml import KML, Placemark
from fastkml.utils import find, find_all
from bs4 import BeautifulSoup

def extract_kml_file(kmz_path:str) -> str:
    """
        Docstring here
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

def kml_to_dict(kml_path:str) -> list:
    """
        Docstring here
    """
    stations=[]
    kml_parsed = KML.parse(kml_path)
    
    placemarks = list(find_all(kml_parsed, of_type=Placemark))

    for placemark in placemarks:
        soup = BeautifulSoup(placemark.description, 'html.parser')
        rows = soup.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if(cells[0].string == 'Station_Na'):
                station_name = cells[1].string
                stations.append({'line': placemark.name, 'station': station_name, 'lat': placemark.geometry.y, 'long': placemark.geometry.x})
    
    return stations


