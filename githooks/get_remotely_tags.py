import subprocess

def get_remotely_git_tags(remote_name='origin'):
    """
    Retrieves a list of remote tags from the specified remote repository.
    
    :param remote_name: The name of the remote repository (default is 'origin').
    :return: A list of unique tags from the remote repository or an empty list in case of an error.
    """
    try:
        # Execute the command to get the list of remote tags
        result = subprocess.run(
            ["git", "ls-remote", "--tags", remote_name],
            capture_output=True,
            text=True,
            check=True
        )

        tags = set()  # Use a set to automatically handle duplicates
        for line in result.stdout.splitlines():
            # Each line is formatted: commit_hash refs/tags/tag_name
            # Extract the tag_name
            parts = line.split('\t')
            if len(parts) > 1 and parts[1].startswith("refs/tags/"):
                tag_name = parts[1][len("refs/tags/"):]
                if tag_name.endswith("^{}"):
                    tag_name = tag_name[:-3]  # Remove ^{} from the tag
                tags.add(float(tag_name))
        
        tags
        return tags
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving remote tags: {e}")
        