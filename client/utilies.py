def string_response(files_response):
    message = f""
    for fr in range (len(files_response)):
        filename = files_response[fr].get('filename')
        message = message + f"{fr + 1}) {filename} \n"
    return message