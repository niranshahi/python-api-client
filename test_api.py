import argparse
import sys
import json
from utils.rest_api_client import RestApiClient  
default_api_url = "http://localhost:1400/api/"

def main(api_url,username,password):

    api_client = RestApiClient(api_url)
    
    done = api_client.login(username, password)
    if done:
        print(f"Successfully logged in.")
    else:
        print("Failed to log in!")
        print("  Please check the server connectivity or username/password")
        sys.exit()

    users=api_client.get_users()
    print( json.dumps(users,indent=4))

    dataResources=api_client.get_dataResources()
    print (json.dumps(dataResources,indent=4))

    # Upload Example usage


    shapefile_zip_path ="data/88ven01u2v.zip"
    imagefile_path="data/test1_3857.tif"
    datasourceInfo={
        "spatialReference":"EPSG:3857",
        "ext_west":50.5,
        "ext_south":33.5,
        "ext_east":55.5,
        "ext_north":35.5,
        "area":100000,
        "sensor_type":"ST",
        "country":"Iran",
        "state_province":"تهران",
        "pixel_size":10
    }

    uploadResults = api_client.register_datasource( shapefile_zip_path,imagefile_path,datasourceInfo)
    print( json.dumps(uploadResults,indent=4))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test api")

    parser.add_argument("-a", "--api_url", default=default_api_url, help="Server address. default is "+ default_api_url)
    parser.add_argument("-u", "--username", help="User name")
    parser.add_argument("-p", "--password", help="Password")

    args = parser.parse_args()
    username= args.username
    password= args.password
    if not username:
        parser.print_help()

        print("\033[94m" +"Please enter username and password." +"\033[0m")
        username = input("Username: ")
        password = input("Password: ")
    if not username:
        sys.exit()
    main(args.api_url,username,args.password)    