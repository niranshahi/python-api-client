import requests
import json
import os

class RestApiClient:
    """
    This class provides methods for interacting with a REST API, including authentication, user retrieval, and file upload.
    """

    def __init__(self, base_url):
        """
        Initializes the client with the base URL of the REST API.

        Args:
            base_url: The base URL of the REST API.
        """
        self.base_url = base_url
        self.token = None  # Store token for authorized requests
    def login(self,username, password):
        """
        Args:
            username: نام کاربری
            password: رمز عبور

        Returns:
            توکن یا None در صورت بروز خطا
        """

        
        # داده های درخواست را به صورت JSON آماده کنید
        data = {
            "userName": username,
            "password": password
        }

        
        try:
            #headers =  {"Content-Type":"application/json"}
            #response = requests.post(base_url + "login", data=json.dumps(data), headers=headers)
            response = requests.post(self.base_url + "login", data=data)
            
            # بررسی کنید که آیا درخواست با موفقیت انجام شده است
            if response.status_code == 200:
                # داده های JSON را به یک شیء دیکشنری تبدیل کنید
                data = response.json()

                # توکن را از JSON استخراج کنید
                self.token = data["token"]

                # توکن را برگردانید
                return True
            else:
                #print(f"خطا: {response.status_code}")
                return False
        except  Exception as e:
            print("Error in login:", e)
            return False

    def get_users(self):
        """
        This function retrieves users list.

        Returns:
            List of users
        """

        

        try:
            # headers =  {"Content-Type":"application/json","Authorization": f"Bearer {token}"}
            headers =  {"Authorization": f"Bearer {self.token}"}
            response = requests.get(self.base_url + "users", headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return None
        except  Exception as e:
            print("Error in get_users:", e)
            return None

    def get_dataResources(self):
        """
        This function retrieves uploaded datasets list.

        Args:
           
        Returns:
            List of data sources.
        """

        

        try:
            #headers =  {"Content-Type":"application/json","Authorization": f"Bearer {token}"}
            headers =  {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(self.base_url + "dataResources", headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return None
        except  Exception as e:
            print("Error in get_dataResources:", e)
            return None            

    def register_datasource(self, shapefile_zip_path,imageFile_path,datasourceInfo):
        """
        This function register a a dataset .

        Args:
            shapefile_zip_path: Path to the zipped shapefile.
            imageFile_path: Path to image file.
            datasourceInfo: A dictionary containing other datasource info.

        Returns:
            The response object from the server.
        """
        if not os.path.exists(shapefile_zip_path):
            print(f"Error: Shapefile zip path '{shapefile_zip_path}' does not exist.")
            return None
        if not os.path.exists(imageFile_path):
            print(f"Error: Image file path '{imageFile_path}' does not exist.")
            return None
        
        try:
            with open(shapefile_zip_path, 'rb') as f1, open(imageFile_path, 'rb') as f2:
                files = {
                     'shapefile': (f1.name, f1, 'application/x-zip-compressed'),
                     'imagefile': (f2.name, f2, 'image/tiff')
                     }    
                headers =  {"Authorization": f"Bearer {self.token}"}
                response = requests.post(self.base_url + "dataResource/upload",files=files,data=datasourceInfo,  headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    return data
                else:
                    return None
        except Exception as e:
            print("Error in register_datasource:", e)
            return None

    def bulk_upload_datasources(self, zip_file_path, common_metadata):
        """
        Bulk upload multiple shapefile-image pairs from a single ZIP file.

        Args:
            zip_file_path: Path to the ZIP file containing multiple pairs
            common_metadata: Dictionary with common metadata for all resources

        Returns:
            Response from server with count and results
        """
        if not os.path.exists(zip_file_path):
            print(f"Error: ZIP file path '{zip_file_path}' does not exist.")
            return None

        try:
            with open(zip_file_path, 'rb') as f:
                files = {
                    'zipfile': (f.name, f, 'application/x-zip-compressed')
                }
                headers = {"Authorization": f"Bearer {self.token}"}
                response = requests.post(
                    self.base_url + "dataResource/bulkUpload",
                    files=files,
                    data=common_metadata,
                    headers=headers
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
        except Exception as e:
            print("Error in bulk_upload_datasources:", e)
            return None