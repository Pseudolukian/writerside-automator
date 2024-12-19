import subprocess

def get_local_git_tags():
    try:
        # Run the git tag command and capture the output
        result = subprocess.run(["git", "tag"], capture_output=True, text=True, check=True)
        
        # Split the output into a list based on newline characters
        tags = result.stdout.strip().split('\n')
        tags = {float(tag) for tag in tags}
        
        # Return the list of tags
        return tags
    except subprocess.CalledProcessError as e:
        # Handle errors if the git command fails
        print(f"An error occurred while getting git tags: {e}")
        return {}
