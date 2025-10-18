#pip install nbimporter, not this one
#pip install import-ipynb
 
#import import_ipynb
import DatabaseData
Data = DatabaseData.DataFromDatabase(); #Dict{int:Dict{str:any}} why print????????????? why output??? 
# {'ID': 1, 'Venomous': False, 'SnakeDailyActivity': 'MostlyDiurnal', 'OtherName': ['PantherophisAlleghanie', 'CentralRatsnake', 'EasternRatsnake'], 'SnakeImage': ['https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/BlackRatSnake/P.-alleghaniensis-1-Nick-Arms.jpg', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/BlackRatSnake/black_rat_snake_web-1024x683.jpg', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/BlackRatSnake/blackrat2.jpg']}
# {'ID': 2, 'Venomous': False, 'SnakeDailyActivity': 'Diurnal', 'OtherName': ['ThamnophisSirtalis', 'CommonGarter'], 'SnakeImage': ['https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/EasternGarter/images-2.jpeg\n', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/EasternGarter/images.jpeg', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/EasternGarter/images-3.jpeg']}

#result = Dict{int:float}

result = {1:10.0, 2:9.0 , 3:8.0 , 4:7.0 , 5:6.0}
snake_dict = {'1': 'BlackRat',
    '2': 'EasternGarter',
    '3': 'EasternHognose',
    '4': 'EasternMassuga',
    '5': 'NorthernWater',
    '6': 'EasternMilk',
    '7': 'EasternWorm',
     '8': 'NorthernBlackRacer',
    '9': 'NorthernBrown',
    '10': 'NorthernCopperhead',
    '11': 'Redbelly',
    '13': 'Ring-Necked',
    '14': 'Queen',
    '15': 'SmoothGreen',
    '16': 'RoughSnake',
    '17': 'TimberRattle',
    '18': 'EasternRibbon'
}



def ChangeIntoSeprateInfo(ResultInput):
    #print(ResultInput)
    ResultResult = list(ResultInput.keys())
    ResultResultResult = []
    for item in ResultResult:
      
       
        ResultResultResult.append(Data[item])
    
    return ResultResultResult
    




def FormatSnakeResults(snake_data):
    """
    Safely formats each snake dictionary into a readable string and 
    returns a list of formatted entries.
    Includes the snake name from snake_dict after the number.
    """
    snake_dict = {
        '1': 'BlackRat',
        '2': 'EasternGarter',
        '3': 'EasternHognose',
        '4': 'EasternMassuga',
        '5': 'NorthernWater',
        '6': 'EasternMilk',
        '7': 'EasternWorm',
        '8': 'NorthernBlackRacer',
        '9': 'NorthernBrown',
        '10': 'NorthernCopperhead',
        '11': 'Redbelly',
        '13': 'Ring-Necked',
        '14': 'Queen',
        '15': 'SmoothGreen',
        '16': 'RoughSnake',
        '17': 'TimberRattle',
        '18': 'EasternRibbon'
    }

    formatted_snakes = []

    for i, snake in enumerate(snake_data, start=1):
        # Get snake name from snake_dict, fallback to "Unknown" if not found
        snake_name = snake_dict.get(str(snake.get("ID", i)), "Unknown")

        venom_status = "Venomous" if snake.get("Venomous") else "Non-venomous"
        activity = snake.get("SnakeDailyActivity", "Unknown Activity")

        # Handle OtherName being either list or single string
        other_names = snake.get("OtherName", [])
        if isinstance(other_names, list):
            other_names = " , ".join(other_names)
        else:
            other_names = str(other_names)

        formatted_snake = (
            f"#{i} {snake_name}  "
            f"Status: {venom_status} "
            f"Daily Activity: {activity} "
            f"Other Names: {other_names}"
            # f"  Images: {image_urls}"  # uncomment if you want images
        )

        formatted_snakes.append(formatted_snake)

    return formatted_snakes

def GetFormattedSnakeInfo(result):
    snake_output = ChangeIntoSeprateInfo(result)
    return FormatSnakeResults(snake_output)


# output = GetFormattedSnakeInfo(result)
# for item in output:
#     print(item)





