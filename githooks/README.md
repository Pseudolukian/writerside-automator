# Writerside git hooks

This set of Git hooks is needed for automatically syncing tags in local and remote repositories. The synced tags are the basis for multi-version documentation deployment. In this case, you do not need to have many branches with different versions of the documentation—you have only one current version with a history of previous versions.

To deploy Writerside multi-version documentation, you can use GitHub workflows in this repository.

## How to use Writerside git hooks

1. Open the folder <path_of_your_doc_project>/.git/hooks/.
2. Find the pre-commit.sample file and delete the extension.
3. Open the pre-commit file and add:

    ```
    #!/bin/bash
    remote_main_branch="origin"
    help_versions_json_path="./help-versions.json"
    version_uri="/versions/"
    ws_instance_cfg="./Writerside/writerside.cfg"

    python3 <path_to_ws_git_hooks_folder>/main.py $remote_main_branch $help_versions_json_path $version_uri $ws_instance_cfg
    ```

    - remote_main_branch — this is the master branch in your repository. By default, it's `origin`.
    - help_versions_json_path — this is the path to the JSON file for version switcher URLs. By default, `help-versions.json` is located in the root of your documentation project.
    - version_uri — this is the part of the version URL in `help-versions.json`.
    - ws_instance_cfg — this is the path to the `writerside.cfg` file in your documentation instance.

    In the main run command, like python3 `<path_to_ws_git_hooks_folder>/main.py ...`, replace the placeholder with the real path to the Writerside Git hooks folder.

4. Save the file.

## How it works

When you make a commit, the pre-commit action starts, and the Python code runs:

1. Checking local tags: If local tags are not found, an error message is raised.
2. Checking remote tags: If remote tags are not found, an error message is raised.
3. Two-way sync of local and remote tags: This ensures both tag lists are consistent.
4. Checking the version tag in `help-versions.json`: If the file is using an outdated tag, the hook updates it to the latest tag used in the local repository. The hook does not create `help-versions.json`.
5. Checking the version tag in `writerside.cfg`: If the file is using an outdated tag, the hook updates it to the latest tag used in the local repository. The hook does not create `writerside.cfg`.