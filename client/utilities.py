def string_response(files_response):
    message = f""
    for fr in range(len(files_response)):
        filename = files_response[fr].get("filename")
        message = message + f"{fr + 1}) {filename} \n"
    return message


def get_newname(filename, list_dir):
    name, ext = filename.rsplit(".", 1)
    same_names = list()
    for l_d in list_dir:
        if name in l_d:
            same_names.append(l_d)
    for sm in range(len(same_names)):
        new_name = f"{name}({sm+1}).{ext}"
        if not new_name in same_names:
            return new_name
