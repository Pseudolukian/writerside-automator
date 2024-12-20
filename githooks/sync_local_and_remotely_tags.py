import subprocess

def sync_tags(remote_name:str, local_tags_list:list[float],remotely_tags_list:list[float]):
    """Sync local and remote git tags."""
    local_tags = local_tags_list
    remote_tags = remotely_tags_list

    # Tags only in local
    to_push = local_tags - remote_tags
    # Tags only in remote
    to_fetch = remote_tags - local_tags

    if to_push:
        for tag in to_push:
            try:
                subprocess.run(["git", "push", remote_name, str(tag)], check=True)
                print(f"Pushed local tag '{tag}' to remote '{remote_name}'.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to push tag '{tag}' to remote '{remote_name}': {e}")
    
    if to_fetch:
        try:
            subprocess.run(["git", "fetch", remote_name, "--tags"], check=True)
            print(f"Fetched missing remote tags to local repository.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch tags from remote '{remote_name}': {e}")

    if not to_push and not to_fetch:
        print("Local and remote tags are synced.")