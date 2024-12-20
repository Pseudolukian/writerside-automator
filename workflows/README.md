# About Writerside GitHub's Workflows

The workflows in this repository help you create a CI/CD production and preview-ready pipeline more quickly. For preview builds, the build_test_doc.yaml is used. This workflow is based on GitHub Pages for previewing the latest build of the documentation. For production documentation, build_prod_docs.yaml is used. This workflow uses boto3 to upload documentation to S3-compatible storage (AWS, Azure, Yandex Cloud, etc.).

## How the Production Deploy Workflow Works

The production deploy workflow is based on [JetBrains' Writerside GitHub Action](https://github.com/JetBrains/writerside-github-action) and uses Python 3 scripts (boto3) to upload documentation to S3.

Main steps and settings of the workflow:
1. The workflow is triggered in two ways:
    * When pushing local files to the main branch;
    * When merging any branch into the master branch;

    ```yaml
    on:
      push:
        branches:
          - main
    ```
    
2. In the build phase, the workflow creates an artifact and names it docs.
3. In the production phase, the workflow downloads the artifact, unzips it, and runs run_upload_doc_to_s3.py.

You can find information about the logic of the Python scripts in the scripts folder.