import subprocess

def get_local_git_tags():
    """Get local git tags
    Function get the list of git tags.
    """
    try:
        # Run the git tag command and capture the output
        result = subprocess.run(["git", "tag"], capture_output=True, text=True, check=True)
        
        # Split the output into a list based on newline characters
        tags = result.stdout.strip().split('\n')
        tags = {float(tag) for tag in tags}
        
        if len(tags) == 0:
            raise Exception("You are dont have local tags")
        
        return tags
    except subprocess.CalledProcessError as e:
        # Handle errors if the git command fails
        print(f"An error occurred while getting git tags: {e}")
        return {}
