import json

def augment_json_data(file_name, method="h", path="./"):
    # read json
    with open(f"{path}{file_name}", 'r') as f:
        json_data = json.load(f)

    # get image scale
    width = json_data['label_info']['image']['width']
    height = json_data['label_info']['image']['height']

    # new points
    new_points = []

    # augment data
    if method == "h":
        for i in range(len(json_data['label_info']['shapes'])):
            new_points.append([[width - point[0], point[1]] for point in json_data['label_info']['shapes'][i]['points']])
    elif method == "v":
        for i in range(len(json_data['label_info']['shapes'])):
            new_points.append([[point[0], height - point[1]] for point in json_data['label_info']['shapes'][i]['points']])
        
    for i in range(len(new_points)):
        json_data['label_info']['shapes'][i]['points'] = new_points[i]
    
    # create new Json file
    file_base, file_extension = file_name.split(".")[0], file_name.split(".")[-1]
    with open(f'{path}{file_base}-{method}.{file_extension}', 'w') as f:
        json.dump(json_data, f)

    return json_data
