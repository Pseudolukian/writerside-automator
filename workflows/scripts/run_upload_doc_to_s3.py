from upload_doc_to_s3 import S3_doc_upload, sys

if __name__ == "__main__":
    s3_upload = S3_doc_upload(endpoint_url = sys.argv[1], 
                          region_name = sys.argv[2],
                          bucket_name = sys.argv[3],
                          access_key_id = sys.argv[4],
                          access_key = sys.argv[5],
                          path_to_doc_folder = sys.argv[6],
                          S3_upload_dir =sys.argv[7],
                          current_tag = sys.argv[8],
                          S3_exclude_folders = sys.argv[9]
                          )
    
    s3_session = s3_upload.get_s3_session()
    s3_actual_version_dir = s3_upload.S3_dir_worker(s3_session = s3_session)
    upload_doc_to_s3_version_folder = s3_upload.upload_doc_s3(s3_session = s3_session, S3_actual_version_tag_folder = s3_actual_version_dir)
    upload_doc_to_s3_root = s3_upload.upload_doc_to_s3_root(s3_session = s3_session)


