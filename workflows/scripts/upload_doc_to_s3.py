import boto3
import sys
import os
import zipfile
from botocore.exceptions import BotoCoreError, NoCredentialsError, ClientError


class S3_doc_upload:

    def __init__(self, 
                 endpoint_url: str, 
                 access_key_id:str, 
                 access_key:str, 
                 region_name:str, 
                 bucket_name:str,
                 path_to_doc_folder:str,
                 S3_upload_dir: str,
                 current_tag: str,
                 S3_exclude_folders: list[str]
                   ) -> None:
        self.endpoint_url = endpoint_url
        self.access_key_id = access_key_id
        self.access_key = access_key
        self.region_name = region_name
        self.bucket_name = bucket_name
        self.path_to_doc_folder = path_to_doc_folder
        self.S3_upload_dir = S3_upload_dir
        self.current_tag = current_tag
        self.S3_exclude_folders = S3_exclude_folders

    def get_s3_session(self):
        try:
            session = boto3.Session(
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.access_key,
                region_name=self.region_name,
            )
            s3 = session.client("s3", endpoint_url=self.endpoint_url)
            
            # Попытка вызова метода клиента, чтобы убедиться, что сессия работает
            s3.list_buckets()
            
            print("S3 session obtained successfully")
            return s3

        except (BotoCoreError, NoCredentialsError, ClientError) as e:
            raise RuntimeError("Cannot connect to S3: {}".format(e))

    def S3_dir_worker(self, s3_session: get_s3_session) -> str:
        prefix = f"{self.S3_upload_dir}/{self.current_tag}/"
        
        # Check if the folder already exists
        response = s3_session.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, Delimiter='/')
        
        if 'Contents' in response:
            print("Folder is found.")
            return prefix
        else:
            print("Folder does not exist, creating the folder.")
            # Create a new folder (by creating an empty object with a trailing slash)
            s3_session.put_object(Bucket=self.bucket_name, Key=prefix)
            return prefix        

    def upload_doc_s3(self, s3_session:get_s3_session, S3_actual_version_tag_folder: str) -> str:
        for root, dirs, files in os.walk(self.path_to_doc_folder):
            relative_root = os.path.relpath(root, self.path_to_doc_folder)
            if relative_root != '.':
                s3_folder_path = os.path.join(S3_actual_version_tag_folder, relative_root).replace('\\', '/') + '/'
                s3_session.put_object(Bucket=self.bucket_name, Key=s3_folder_path)

            # Upload files
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(local_file_path, self.path_to_doc_folder)
                s3_key = os.path.join(S3_actual_version_tag_folder, relative_file_path).replace('\\', '/')

                # Upload files to S3
                s3_session.upload_file(local_file_path, self.bucket_name, s3_key)
                print(f"Uploaded {local_file_path} to s3://{self.bucket_name}/{s3_key}")

        return "All files successfully uploaded."
    
    def upload_doc_to_s3_root(self, s3_session:get_s3_session) -> str:
        # List all objects in the bucket
        response = s3_session.list_objects_v2(Bucket=self.bucket_name)
        keys_to_delete = []

        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                # Check if object should be excluded from deletion
                if not any(key.startswith(folder) for folder in self.S3_exclude_folders):
                    keys_to_delete.append({'Key': key})

        # Delete unwanted objects
        if keys_to_delete:
            s3_session.delete_objects(Bucket=self.bucket_name, Delete={'Objects': keys_to_delete})
            print(f"Deleted files: {keys_to_delete}")

        # Upload new files to the root of the S3 bucket
        for root, dirs, files in os.walk(self.path_to_doc_folder):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(local_file_path, self.path_to_doc_folder)
                s3_key = relative_file_path.replace('\\', '/')

                # Upload files to S3 root
                s3_session.upload_file(local_file_path, self.bucket_name, s3_key)
                print(f"Uploaded {local_file_path} to s3://{self.bucket_name}/{s3_key}")

        return "All files successfully uploaded to S3 root."