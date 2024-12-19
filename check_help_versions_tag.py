import json

def check_help_version_json(path:str, local_tags_set:set[float], url_template:str):
    latest_tag = max(local_tags_set)
    lat_version_url = "/"
    last_version_json_row = {"version": str(latest_tag), "url": lat_version_url, "isCurrent": True}
    
    with open(path, "r") as file:
        versions = json.load(file) 

    if float(versions[-1]["version"]) < latest_tag and versions[-1]["url"] == "/":
        versions[-1]["url"] = url_template + str(versions[-1]["version"]) + "/"
        versions[-1]["isCurrent"] = False
        versions.append(last_version_json_row)
        
        with open(path, "w", encoding='utf-8') as file:
            json.dump(versions, file, ensure_ascii=False, indent=4)
        return f"Last tag added to version switcher."
    
    elif float(versions[-1]["version"]) == latest_tag and versions[-1]["url"] == "/":
        print(f"In the switcher using latest tag.")
    elif float(versions[-1]["version"]) > latest_tag and versions[-1]["url"] == "/":
        print(f"Error! The last tag in the version switcher is {versions[-1]["version"]} but latest local tag is {latest_tag}.")    

    print(versions)             
        

