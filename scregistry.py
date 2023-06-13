import boto3
from io import BytesIO
import pandas as pd
import os
from datetime import datetime
from math import ceil
import json
import requests
import logging
import dateutil
import re
from typing import List, Dict, Tuple, Union, Optional, Callable


class CatalogRegistry:
    """Use to work with the the global catalog (catalog of catalogs)."""
    
    def __init__(self, catalog_url: Optional[str] = None) -> None:
        """
        Parameters:
            catalog_url: either the environment variable `ROOT_CATALOG_REGISTRY_URL` if it exists
                         or the smce heliocloud global catalog by default, otherwise the explicitly passed in url.
        """
        # Set the catalog URL (env variable or default if not manually provided)
        if catalog_url is None:
            catalog_url = os.getenv('ROOT_CATALOG_REGISTRY_URL')
            if catalog_url is None:
                # TODO: Edit to real catalog
                catalog_url = 'https://git.mysmce.com/heliocloud/heliocloud-data-uploads/-/blob/main/catalog.json'
                # TODO: Remove ValueError
                raise ValueError('No environment variable ROOT_CATALOG_REGISTRY_URL nor was an explicit catalog_url passed in.')
        self.catalog_url = catalog_url

        # Load the content from json
        response = requests.get(self.catalog_url)
        if response.status_code == 200:
            self.catalog = response.json()
        else:
            raise requests.ConnectionError(f'Get Request for Global Catalog Failed. Catalog url: {self.catalog_url}')
        
        # Check global catalog format assumptions
        if 'registry' not in self.catalog:
            raise KeyError('Invalid catalog. Missing registry key.')
        for reg_entry in self.catalog['registry']:
            if 'endpoint' not in reg_entry or 'name' not in reg_entry or 'region' not in reg_entry:
                raise KeyError(f'Invalid registry entry in catalog. Missing endpoint or name or region key. Registry entry: {reg_entry}')
        

    def get_catalog(self) -> Dict:
        """
        Get the global catalog with all metadata and registry entries.

        Returns:
            The global catalog dict
        """
        return self.catalog
        
    def get_registry(self) -> List[Dict]:
        """
        Get the registry values in the global catalog.

        Returns:
            A list of catalog dicts, which are each entry in the registry.
        """
        return self.catalog['registry']
    
    def get_entries_name_region(self) -> List[Tuple[str, str]]:
        """
        Get the entry names and region of each entry in the registry.
        
        Returns:
            A list of tuples with the name and region from the global catalog registry.
        """
        # Get the name and region of each entry in the catalog
        return [(x['name'], x['region']) for x in self.catalog['registry']]

    def get_entries(self):
        """
        Get all data for a given registry
        
        Returns:
            A dictionary for that entry
        """
        # Get the name and region of each entry in the catalog
        myjson = [x for x in self.catalog['registry']]
        if myjson is not None:
            myjson = myjson[0]
        return myjson
        
    def get_endpoint(self, name: str, region_prefix: str = '', force_first: bool = False) -> str:
        """
        Get the s3 endpoint given the name and region.
        
        Parameters:
            name: Name of the endpoint.
            region_prefix (optional, str,): Prefix for a region.
            force_first (optional, defaults to False, bool): If True, returns the first entry regardless of name+region uniqueness.

        Returns:
            The URI of the endpoint.
        """
        # Find registries that match the specified name and region prefix
        registries = [x for x in self.catalog['registry'] if x['name'] == name and x['region'].startswith(region_prefix)]
        # Check to make sure all entries have unique names + prefixed region
        if not force_first and len(registries) > 1:
            if len(set(x['region'] for x in registries)) == 1:
                raise ValueError('Entries do not all have unique names. You may enable force_first to choose first option.')
            else:
                raise ValueError('Entries do not all have unique names but have different regions, please further specify region_prefix.')
        elif len(registries) == 0:
            raise KeyError('No endpoint found with given name and region_prefix.')
        return registries[0]['endpoint']


class FailedS3Get(Exception):
    """
    A custom exception for any errors relating to s3 that are not already thrown by boto.
    """
    pass


class UnavailableData(Exception):
    """
    A custom exception for when the catalog indicates the dataset is unavailable.
    """
    pass

    
class FileRegistry:
    """
    Use to work with a specific bucket (obtained from the global catalog) and
    the associated catalog in the bucket.
    """
    
    def __init__(self, bucket_name: str, cache_folder: Optional[str] = None, cache: bool = True, **client_kwargs) -> None:
        """
        Parameters: 
            bucket_name (str): The name of the s3 bucket.
            cache_folder (str): Folder to store the file registry cache, defaults to bucket_name + '_cache'.
            cache (optional, defaults to True, bool): Determines if any files should be cached so that S3 pulling
                                                      is not unnecessarily done. If a cache_folder is provided,
                                                      this is forced to true.
            client_kwargs: parameters for boto3.client: region_name, aws_acces_key_id, aws_secret_access_key, etc.
        """
        # Remove s3 uri info if provided
        if bucket_name.startswith('s3://'):
            bucket_name = bucket_name[5:]
        bucket_name = bucket_name.rstrip('/')
    
        # Store the bucket name for future use  
        self.bucket_name = bucket_name
        
        self.cache = cache
        
        # Create a client object with provided kwargs
        self.s3_client = boto3.client('s3', **client_kwargs)

        # Get catalog bytes from S3 
        # May through some errors, NoSuchBucket, ClientError (file may not exists or access denied)
        # If have ListBucket perms, no such key error will be raised instead of client error
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key='catalog.json')
        status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
        if 'Body' in response and status == 200:
            catalog_bytes = response['Body'].read()
        else:
            raise FailedS3Get(f'Failed to Get Catalog from Bucket. Status: {status}. Response: {response}')
        
        # Load the content from json
        self.catalog = json.loads(catalog_bytes)
        
        # Check catalog format assumptions
        if any([key not in self.catalog for key in ['status', 'catalog']]):
            raise KeyError(f'Invalid catalog. Missing either status or catalog key. Catalog: {self.catalog}')

        # Check status and rasie exception
        if self.catalog['status']['code'] == 1400:
            raise UnavailableData(self.catalog['status'])
            
        # Check catalog entries format assumptions
        for entry in self.catalog['catalog']:
            #if 'start' in entry:
            #    entry['start'] = entry.pop('start')
            #if 'stop' in entry:
            #    entry['stop'] = entry.pop('stop')
            #if 'modification' in entry:
            #    entry['modification'] = entry.pop('modification')
            missing_keys = [key for key in ['id', 'index', 'title', 'start', 'stop'] if key not in entry]
            if len(missing_keys) > 0:
                raise KeyError(f'Invalid catalog entry. Missing keys ({missing_keys}) in entry: {entry}')
            loc = entry['index']
            #if (not loc.startswith('s3://') and not loc.startswith(f'{bucket_name}/')) or loc[-1] != '/':
            if not (loc.startswith('s3://') and loc[-1] == '/'):
                raise ValueError(f'Invalid index in catalog entry. index: {loc}')
            # could check if start is less than stop here
        
        # Set and create the folder for caching
        self.cache_folder = None
        if cache:
            if cache_folder is None:
                cache_folder = self.bucket_name + '_cache'
            self.cache_folder = cache_folder
            if self.cache_folder is not None and not os.path.exists(self.cache_folder):
                os.mkdir(self.cache_folder)

            # Copy the content of the catalog to this file (overwrites)
            with open(os.path.join(cache_folder, 'catalog.json'), 'wb') as file:
                file.write(catalog_bytes)

    def get_catalog(self) -> Dict:
        """
        Gets the raw catalog downloaded from the bucket.

        Returns:
            The catalog dict.
        """
        return self.catalog
    
    def get_entries_id_title(self) -> List[Tuple[str, str]]:
        """
        Get just the entry id and title of each entry in the catalog.
        
        Returns:
            A list of tuples with the id and title from the global catalog registry.
        """
        # Get the name and region of each entry in the catalog
        return [(x['id'], x['title']) for x in self.catalog['catalog']]
    
    def get_entries_dict(self) -> List[Dict]:
        """
        Get all the items of each entry in the catalog.
        
        Returns:
            The json items from the catalog
        """
        return self.catalog['catalog']
    
    def get_entry(self, entry_id: str) -> Dict:
        """
        Get the entry (with full info) using the given entry_id.
        
        Returns:
            A list of tuples with the id and title from the global catalog registry.
        """
        entries = [x for x in self.catalog['catalog'] if x['id'] == entry_id]
        if len(entries) == 0:
            raise KeyError(f'No entries found with entry_id ({entry_id}).')
        elif len(entries) > 1:
            raise ValueError(f'Invalid catalog with multiple entries with the same ID. ID: {entry_id}')
        return entries[0]
            
    def request_file_registry(self, catalog_id: str, start_date: Optional[str] = None, stop_date: Optional[str] = None, overwrite: bool = False) -> pd.DataFrame:
        """
        Request the files in the file registry within the provided times from the s3 bucket. 

        Parameters: 
            catalog_id (str): The id of the catalog entry in the s3 bucket. 
            start_date (str): Start date for which file registry is needed (default None). ISO 8601 standard.
            stop_date (str): End date for which file registry is needed (default None). ISO 8601 standard.
            overwrite (bool): Overwrite files already cached if within request
                              cache in initilization must have been true.
                             
        Returns:
            A pandas Dataframe containing the requested file registry data.
        """
        # Make dates conform with Restricted ISO 8601 standard
        if start_date[-1] != 'Z':
            start_date += 'Z'
        if stop_date[-1] != 'Z':
            stop_date += 'Z'
        # Convert dates to datetime object
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}(:\d{2}(:\d{2}(\.\d+)?)?)?Z', start_date):
            raise ValueError('start_date must follow the format XXXX-XX-XXTXXZ with at least the year, month, day, and hour specified.')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}(:\d{2}(:\d{2}(\.\d+)?)?)?Z', stop_date):
            raise ValueError('stop_date must follow the format XXXX-XX-XXTXXZ with at least the year, month, day, and hour specified.')
        # dateutil.parser.parse
        start_date = dateutil.parser.parse(start_date[:-1])
        stop_date = dateutil.parser.parse(stop_date[:-1])
        
        # Check if start date is less or equal than end date
        if stop_date < start_date:
            raise ValueError(f'start_date ({start_date}) must be equal or less than stop_date ({stop_date}).')

        # Get the entry with given catalog id from the list of catalogs 
        entry = [catalog_entry for catalog_entry in self.catalog['catalog'] if catalog_entry['id'] == catalog_id]

        # Raises error if no matching entry is found 
        if len(entry) == 0:
            raise KeyError(f'No catalog entry found with id: {catalog_id}')
        elif len(entry) > 1:
            raise ValueError(f'No unique catalog entry found with id: {catalog_id}')
        else:
            entry = entry[0]

        # Get some necessary variables 
        eid, loc, catalog_start_date, catalog_stop_date = entry['id'], entry['index'], entry['start'], entry['stop']
        ndxformat = 'csv'  # entry['ndxformat']

        # If caching
        if self.cache_folder is None:
            path = None
        else:
            # Create the path for storing cached files and folder if does not exist
            path = os.path.join(self.cache_folder, catalog_id)
            if not os.path.exists(path):
                os.mkdir(path)

        # Compute minimum and maximum year from start and end date respectively
        
        # assuming Z ends date
        catalog_year_start_date = dateutil.parser.parse(catalog_start_date[:-1]).year
        year_start_date = catalog_year_start_date if start_date is None else max(catalog_year_start_date, start_date.year)

        def ceil_year(date):
            return ceil(date.year + (date - datetime(date.year, 1, 1)).total_seconds() * 3.17098e-8)

        # assuming Z ends date
        catalog_year_stop_date = ceil_year(dateutil.parser.parse(catalog_stop_date[:-1]))
        year_stop_date = catalog_year_stop_date if stop_date is None else min(catalog_year_stop_date, ceil_year(stop_date))
        
        # Local or different: Could be same bucket or different bucket
        # not enforcing being same bucket
        bucket_name = loc[5:].split('/', 1)[0]
        loc = loc[len(bucket_name)+6:]

        # Define empty array for storing data frames 
        frs = []

        # Loop through all the years 
        for year in range(year_start_date, year_stop_date):
            filename = f'{eid}_{year}.{ndxformat}'

            if path is None:
                filepath = None
            else:
                filepath = os.path.join(path, filename)

            # If file does not exist download it from s3
            # And save it to the given path 
            if not self.cache or overwrite or (filepath is not None and not os.path.exists(filepath)):
                # May through some errors, NoSuchBucket, ClientError (file may not exists or access denied)
                # If have ListBucket perms, no such key error will be raised instead of client error
                response = self.s3_client.get_object(Bucket=bucket_name, Key=loc + filename)
                status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
                if 'Body' in response and status == 200:
                    fr_bytes_file = BytesIO()
                    fr_bytes_file.write(response['Body'].read())
                    fr_bytes_file.seek(0)
                else:
                    raise FailedS3Get(f'Failed to get a file registry object. Status: {stats}. Response: {response}')

                if filepath is not None:
                    with open(filepath, 'wb') as file:
                        file.write(fr_bytes_file.read())
                    fr_bytes_file.seek(0)
                fr = pd.read_csv(fr_bytes_file)

            # If file exists, read from given path
            else:
                fr = pd.read_csv(filepath)
            
            # Handle # if used for the header
            if fr.columns.values[0][:2] == '# ':
                fr.columns.values[0] = fr.columns.values[0][2:] 
            
            # Make column names consistent since not enforcing this spec (as of now)
            fr.rename(columns={'start': 'start',
                               'stop': 'stop',
                               'modification': 'modification'}, inplace=True)
            
            # assume first column is start, second is key, and third is filesize
            # only assuming if not found in column names
            # no error will be thrown if one of these missing, but per spec they are required
            if 'start' not in fr.columns.values:
                fr.columns.values[0] = 'start'
            if 'datakey' not in fr.columns.values:
                fr.columns.values[1] = 'datakey'
            if 'filesize' not in fr.columns.values:
                fr.columns.values[2] = 'filesize'

            frs.append(fr)

        frs = pd.concat(frs)
        
        # Filter file registry dataframe to exact requested dates
        frs['start'] = pd.to_datetime(frs['start'], format='%Y-%m-%dT%H:%M:%SZ')
        frs = frs[(start_date <= frs['start']) & (frs['start'] < stop_date)]

        return frs
    
    @staticmethod
    def stream(file_registry: pd.DataFrame,
               process_func: Callable[[BytesIO, str, int], None], 
               ignore_faileds3get: bool = False) -> None:
        """
        Downloads files from S3 and passes them to a processing function.

        Parameters:
            file_registry (pd.DataFrame): A pandas DataFrame containing the file registry information.
            process_func (Callable): A function that takes a BytesIO object, a string representing the
                                     start date of the file, and an integer representing the file size
                                     as arguments.
            ignore_faileds3get (bool): A boolean that determines if the FailedS3Get is not thrown.
        """
        s3_client = boto3.client('s3')

        fr_bytes_file = None
        for _, row in file_registry.iterrows():
            # Get the S3 URL from the key in the dataframe
            s3_url = row['datakey']

            # Download the S3 file and read it into a BytesIO object
            response = s3_client.get_object(Bucket=s3_url.split('/')[2], Key='/'.join(s3_url.split('/')[3:]))
            status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
            if 'Body' in response and status == 200:
                fr_bytes_file = BytesIO()
                fr_bytes_file.write(response['Body'].read())
                fr_bytes_file.seek(0)
            elif not ignore_faileds3get:
                raise FailedS3Get(f'Failed to get a file registry object. Status: {stats}. Response: {response}')            

            # Pass the BytesIO object, start date, and file size to the processing function
            # start may be a date object so making a string just in case for consistency
            process_func(fr_bytes_file, str(row['start']), row['filesize'])
            
    @staticmethod
    def stream_uri(file_registry: pd.DataFrame,
                   process_func: Callable[[str, str, int], None]) -> None:
        """
        Sends S3 URLs to a processing function.

        Parameters:
            file_registry (pd.DataFrame): A pandas DataFrame containing the file registry information.
            process_func (Callable): A function that takes a string representing the S3 URL, a string
                                     representing the start date of the file, and an integer representing
                                     the file size as arguments.
        """
        for _, row in file_registry.iterrows():
            # Get the S3 URL from the key in the dataframe
            s3_url = row['datakey']

            # Pass the S3 URL, start date, and file size to the processing function
            # start may be a date object so making a string just in case for consistency
            process_func(s3_url, str(row['start']), row['filesize'])


class EntireCatalogSearch:
    """Use to search through all the catalogs by using the global catalog to get all the local catalogs."""
    
    def __init__(self, catalog_url: Optional[str] = None, **client_kwargs):
        """
        Parameters:
            catalog_url (str, optional): URL of the global catalog, default is None.
            client_kwargs: Keyword arguments passed to the FileRegistry object.
        """

        # Get the global catalog
        self.global_catalog = CatalogRegistry(catalog_url=catalog_url)

        # Combine the global catalog with local catalogs from each entry
        self.combined_catalog = []
        failed_entries = []
        entries = self.global_catalog.get_registry()
        for entry in entries:
            endpoint = self.global_catalog.get_endpoint(entry['name'], entry['region'])
            try:
                file_registry = FileRegistry(endpoint, cache=False, **client_kwargs)
                local_catalog = file_registry.get_catalog()
                self.combined_catalog.append(local_catalog)
            except Exception as e:
                logging.debug(f"Failed to fetch local catalog for entry {entry['name']} (Region: {entry['region']}; Endpoint: {entry['endpoint']}): {e}\n")
                failed_entries.append((entry['name'], entry['region']))
        if len(failed_entries) > 0:
            msg = f"Failed Local Catalog Fetches ({len(failed_entries)}/{len(entries)}): \n[\n"
            for entry in failed_entries:
                msg += f"    {entry[0]} ({entry[1]})\n"
            msg += ']'
            logging.warning(msg)

    def search_by_id(self, catalog_id_substr: str):
        """
        Search the combined catalog by ID.

        Parameters:
            catalog_id_substr (str): The catalog ID to search for. Can be an ID prefix.

        Returns:
            A list of matching catalog entries.
        """
        results = []
        catalog_id_substr = catalog_id_substr.lower()
        for catalog in self.combined_catalog:
            for entry in catalog['catalog']:
                if catalog_id_substr in entry['id'].lower():
                    results.append(entry)
        return results

    def search_by_title(self, title_substr: str):
        """
        Search the combined catalog by title substring.

        Parameters:
            title_substr (str): The substring to search for in catalog titles.

        Returns:
            A list of matching catalog entries.
        """
        results = []
        title_substr = title_substr.lower()
        for catalog in self.combined_catalog:
            for entry in catalog['catalog']:
                if title_substr in entry['title'].lower():
                    results.append(entry)
        return results

    def search_by_keywords(self, keywords: List[str]):
        """
        Search the combined catalog for keywords in ID, location, and title.

        Parameters:
            keywords (List[str]): A list of keywords to search for.

        Returns:
            A list of matching catalog entries, sorted by the most matching keywords.
        """
        entry_counts = []
        for catalog in self.combined_catalog:
            for entry in catalog['catalog']:
                count = 0
                for keyword in keywords:
                    keyword = keyword.lower()
                    count += entry['id'].lower().count(keyword)
                    count += entry['index'].lower().count(keyword)
                    count += entry['title'].lower().count(keyword)
                    if 'tags' in entry:
                        count += sum([keyword in tag.lower() for tag in entry['tags']])
                if count > 0:
                    entry_counts.append((entry, count))

        # Sort results by the most matching keywords
        sorted_results = sorted(entry_counts, key=lambda x: x[1], reverse=True)
        return [entry for entry, count in sorted_results if count > 0]
