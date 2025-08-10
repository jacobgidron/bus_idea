import requests
import json
from csv import DictWriter
from pyproj import Transformer
import argparse


CRS_FROM = 'epsg:3857'
CRS_TO = 'epsg:4326'
GOVMAP_BUS_INFO_URL = "https://www.govmap.gov.il/apps/data/public-transportation/routes/{}.json"

# Create a Transformer object for the conversion
# always_xy=True ensures output is always (x, y) or (longitude, latitude)
transformer = Transformer.from_crs(CRS_FROM, CRS_TO, always_xy=True)

# transformer.transform(3886611.373224132,3820674.3162589082)

def bus_data_from_govmap_id(bus_id):
    resp = requests.get(GOVMAP_BUS_INFO_URL.format(bus_id)).json()
    

    #resp = requests.get("https://www.govmap.gov.il/apps/data/public-transportation/routes/12246.json").json()
    _, trip = resp["trips"].popitem()
    stops = []
    line_corditates = []
    for i in trip["stop_times"]:
        lon,lat = transformer.transform(i["stop_lon"],i["stop_lat"])
        stops.append({
            "name": i["stop_name"]["en"],
            "WKT": f"POINT({lon} {lat})"
            })
        line_corditates.append(f"{lon} {lat}")
        line_info = {
            "name" : resp["route_short_name"],
            "from" : resp["originStationName"],
            "to" : resp["destinationCityName"]
        }
    
    return stops, line_corditates, line_info

def write_buss_info_to_csv(stops,line_corditates,line_ident,id,path=None):
    if path is None:
        path = "line_{}_info.csv".format(id)
    import csv

    with open(path, 'w', newline='') as csvfile:
        fieldnames = ["WKT","name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for x in stops:
            writer.writerow(x)
        
        line = {"name": f"line {line_ident['name']}: {line_ident['from']} -> to {line_ident['to']}",
            "WKT": "LINESTRING(" + ", ".join(line_corditates) + ")"
            }
        writer.writerow(line)        
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(  
                    prog='ProgramName',
                    description='generate csv to upload to google maps',
                    epilog='Text at the bottom of help')  
    parser.add_argument(  
    '--line-id',
    metavar='line id',dest="line_id", nargs='+', type=int,
    help='an integer to be summed')  
    parser.add_argument(  
    "-o",'--output',dest="path", type=str,  
    help='the file where the sum should be written')  
    args = parser.parse_args()
    print(args.line_id)
    print(args.path)
    print(args)

    for id in args.line_id:
        stops_info, line_info, line_ident = bus_data_from_govmap_id(id)
        print(write_buss_info_to_csv(stops_info, line_info,line_ident,id,args.path))