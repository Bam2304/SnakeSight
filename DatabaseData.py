
#pip install supabase
#througout used methods like .Select() which calls all data from that table
#.table() calls the table but requires a name, i.e. .table("Characteristics")
#.execute, executes the "sql" calls, and returns the column data off of the Databse table
from collections import defaultdict
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
#^supabase built in library for python
def DataFromDatabase():
    supabase_url: str = "https://lgvelnkhepuokjbacqqx.supabase.co" #os.getenv("SUPABASE_URL")
    supabase_key: str = "sb_publishable_VwY13z1yliMQ698Km0fNYA_tgpwqZab" #os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)


    #Gets Data From the Main Table in Supabase
    response = (supabase.from_("SnakeMain").select("*").execute() )
    data = response.data
    DataMain = response.data


    #Gets Data From the Habits Table in Supabase
    response = (supabase.from_("Habits").select("*").execute())
    DataHabits = response.data
 

    #only returns row where the values is not equal to NONE 
    CleanedRowsHabits = [
        {k: v for k, v in row.items() if v is not None}
        for row in response.data
    ]



    #gets data from the characteristics table
    response = ( supabase.from_("Characteristics").select("*").execute() )
    DataCharacteristics = response.data



    #only returns row where the values is not equal to NONE 
    CleanedRowsCharacteristics = [
        {k: v for k, v in row.items() if v is not None}
        for row in response.data
    ]





    #gets data from the OtherNames table
    response =( supabase.from_("OtherNames").select("*").execute())
    DataOtherNames = response.data


    #only returns row where the values is not equal to NONE 
    CleanedRowsOtherNames = [
        {k: v for k, v in row.items() if v is not None}
        for row in response.data
    ]



    #gets data from the SnakeImages table
    response = (supabase.from_("SnakeImages").select("*").execute())
    DataSnakeImages = response.data


    #only returns row where the values is not equal to NONE 
    CleanedRowsSnakeImages = [
        {k: v for k, v in row.items() if v is not None}
        for row in response.data
    ]



    
    BigFinalList = CleanedRowsCharacteristics + CleanedRowsHabits + CleanedRowsOtherNames + CleanedRowsSnakeImages

    merged = defaultdict(dict)


    #sorts ID, but does not properly store every data value, overwrites the previous value only holds last one
    #only an issue for otherNames which can be multiple, IE. snake 3. FUture Issue for Color and potentially other catogories
    # for item in BigFinalList:
    #     ID = item['ID']
    #     merged[ID].update(item)

    

    #goes into a combiation of every data point off of the database (List[{}]) returns it to be a Dict{} with key being 'ID'
    #and the value being a Dict of all info related to snake, including ID

    for item in BigFinalList:
        ID = item['ID']
        for key, value in item.items():
            if key == 'ID':
                continue
            if key in merged[ID]:
                existing = merged[ID][key]
                if not isinstance(existing, list):
                    if existing != value:
                        merged[ID][key] = [existing, value]
                elif value not in existing:
                    merged[ID][key].append(value)
            else:
                merged[ID][key] = value

    

    FullDict = dict(merged)
    # print(FullDict)
    return FullDict

DataFromDatabase()











