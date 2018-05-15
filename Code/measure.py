class Mesure:
    def __init__(self):
        pass

def get_id(data, anchor_id_keys):
    _id = ''
    for i in anchor_id_keys[:-1]:
        _id += str(data[i]) + ':'
    _id += str(data[anchor_id_keys[-1]])
    return _id
