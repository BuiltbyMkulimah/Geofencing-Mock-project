import h3

def normal_to_h3(lat:float ,lng :float , resolution:int=9):
    try:
        return h3.latlng_to_cell(lat,lng,resolution)
    except Exception as e:
        print(f"Error converting to h3 ,{e}")
        return None 