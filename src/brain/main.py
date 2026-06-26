from fastapi import FastAPI,BackgroundTasks
from pydantic import BaseModel
import os 
import csv
from datetime import datetime
from src.brain.h3converter import normal_to_h3

app =FastAPI()

class Location:
    lat:float
    lng:float
    accuracy:float =0.0
    
def log_to_csv(data:dict):
    filepath='data/raw/location_log.csv'
    os.makedirs(os.path.dir(filepath),exist_ok=True)
    file_exists=os.path.isfile(filepath)
    with open(filepath,'a', newline='') as f :
        writer= csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp","lat",'lng',"h3"])
        writer.writerow([data['timestamp'],data['lat'],data['lng'],data['h3']])
app.post('/update-location')
async def updated_location(loc:Location,background_tasks:BackgroundTasks):
    h3_idx=normal_to_h3(loc.lng,loc.lat)
    
    log_data={
        "timestamp":datetime.now().isoformat(),
        "h3":h3_idx,
        "lat":loc.lat,
        "lng":loc.lng
        }
    background_tasks.add_task(log_data,log_to_csv)
    
    return {"status": "received", "h3_index": h3_idx}
        
            
            
    