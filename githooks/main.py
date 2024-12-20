import sys
from get_local_tags import get_local_git_tags
from get_remotely_tags import get_remotely_git_tags
from sync_local_and_remotely_tags import sync_tags
from check_help_versions_tag import check_help_version_json
from check_ws_instance_cfg_tag import check_ws_instance_cfg_tag

def run(help_versions_json_path:str, vers_url_temp:str, ws_instance_cfg_path:str, remote_main_branch = 'origin'):

    local_tags = get_local_git_tags()
    remote_tags = get_remotely_git_tags(remote_name=remote_main_branch)    
    
    sync_tags(remote_name = remote_main_branch, 
            local_tags_list = local_tags, 
            remotely_tags_list = remote_tags)
    
    local_tags = get_local_git_tags()
    remote_tags = get_remotely_git_tags(remote_name=remote_main_branch)

    check_help_version_json(path=help_versions_json_path,local_tags_set = local_tags, url_template = vers_url_temp)
    check_ws_instance_cfg_tag(path_to_instance_cfg=ws_instance_cfg_path, local_tags_list = local_tags)

if __name__ == "__main__":
    run(remote_main_branch = sys.argv[1], 
        help_versions_json_path = sys.argv[2], 
        vers_url_temp = sys.argv[3],
        ws_instance_cfg_path = sys.argv[4])