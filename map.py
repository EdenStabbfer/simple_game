
def map_loader(file_name):
    map_mass = []
    file = open(file_name, 'r')
    for row in file.read().split('\n'):
        map_mass.append(row)
    return map_mass