from lxml import etree

def check_ws_instance_cfg_tag(path_to_instance_cfg: str, local_tags_list: set[float]) -> str:
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(path_to_instance_cfg, parser)
    root = tree.getroot()
    current_version = float(root.find("instance").attrib["version"])
    local_tags = sorted(local_tags_list)

    def update_version():
        root.find("instance").attrib["version"] = str(max(local_tags))

    if current_version in local_tags and current_version == max(local_tags):
        return "In the instance configuration using actual local tag"
    elif current_version in local_tags and current_version != max(local_tags):
        print(f"Warning! In the instance configuration using not actual local tag!")
        update_version()
        message = "Updated the instance configuration to the actual local tag"
    elif current_version in local_tags and current_version > max(local_tags):
        print(f"Warning! In the instance configuration using wrong tag!")
        update_version()
        message = "Corrected the instance configuration to the maximum local tag"
    else:
        return f"Error! In the configuration instance file using {current_version} tag. This tag not included in local tags."

    with open(path_to_instance_cfg, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(etree.tostring(tree, pretty_print=True, xml_declaration=False, encoding='UTF-8'))

    return message