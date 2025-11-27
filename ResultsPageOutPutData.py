#pip install nbimporter, not this one
#pip install import-ipynb

#import import_ipynb
import DatabaseData

database = DatabaseData.DB()
Data = database.DataFromDatabase(); #Dict{int:Dict{str:any}} why print????????????? why output??? 
# {'ID': 1, 'Venomous': False, 'SnakeDailyActivity': 'MostlyDiurnal', 'OtherName': ['PantherophisAlleghanie', 'CentralRatsnake', 'EasternRatsnake'], 'SnakeImage': ['https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/BlackRatSnake/P.-alleghaniensis-1-Nick-Arms.jpg', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/BlackRatSnake/black_rat_snake_web-1024x683.jpg', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/BlackRatSnake/blackrat2.jpg']}
# {'ID': 2, 'Venomous': False, 'SnakeDailyActivity': 'Diurnal', 'OtherName': ['ThamnophisSirtalis', 'CommonGarter'], 'SnakeImage': ['https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/EasternGarter/images-2.jpeg\n', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/EasternGarter/images.jpeg', 'https://lgvelnkhepuokjbacqqx.supabase.co/storage/v1/object/public/SnakeImages/EasternGarter/images-3.jpeg']}
import random
#result = Dict{int:float}

class OutPutData:
    def __init__(self):
        self.resultNumberForm = {15: 10.0, 16: 10.0, 1: 0.0, 
                                 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 
                                 7: 0.0, 8: 0.0, 9: 0.0, 10: 0.0, 11: 0.0, 13: 0.0, 
                                 14: 0.0, 17: 0.0, 18: 0.0}
        self.snake_dict = {'1': 'BlackRat',
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
        '18': 'EasternRibbon'}



    def ChangeIntoSeprateInfo(self,ResultInput):
        #print(ResultInput)
        ResultResult = list(ResultInput.keys())[:5]
        #print(ResultResult)

        ResultResultResult = []
        for item in ResultResult:
            ResultResultResult.append(Data[item])
        

        #print(ResultResultResult)
        for item in ResultResult:
            d = Data[item]
            d["ID"] = item   # ← FIX
        ResultResultResult.append(d)
        return ResultResultResult

    #print(ChangeIntoSeprateInfo(resultNumberForm))
    # print(resultNumberForm)
    # ChangeIntoSeprateInfo(resultNumberForm)
        

    #picks a url randomly from the listen url from the datbase 
    #depricated
    # def getUrlFromDatabase():
    #     urls = ChangeIntoSeprateInfo(resultNumberForm)
    #     listOfChosenUrls = []
    #     for item in urls:
        
    #         ChosenUrl = random.randint(1,len(item['SnakeImage']))
    #         listOfChosenUrls.append(item['SnakeImage'][ChosenUrl-1])

    #     return listOfChosenUrls


    #resultNumberForm = {15: 10.0, 16: 10.0, 1: 0.0, 2: 0.0, 3: 0.0}
    """need to rewrite to work. Currenlty displaying all the wrong."""
    def FormatSnakeResults(self):
        
        
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
    ##
        for i, snake in enumerate(self.snake_data, start=1):
            #print(i)
            #print(snake)

            #print(snake_data.key())

            # Get snake name from snake_dict, fallback to "Unknown" if not found
            snake_name = snake_dict.get(str(snake.get("ID")), "Unknown")

            venom_status = "Venomous" if snake.get("Venomous") else "Non-venomous"
            activity = snake.get("SnakeDailyActivity", "Unknown Activity")

            # Handle OtherName being either list or single string
            other_names = snake.get("OtherName", [])
            if isinstance(other_names, list):
                other_names = " , ".join(other_names)
            else:
                other_names = str(other_names)

            formatted_snake = (
                f"#{i} {snake_name} "
                f"Status: {venom_status} "
                #f"Daily Activity: {activity} "
                f"OtherNames: {other_names} "
                
                # f"  Images: {image_urls}"  # uncomment if you want images
            )

            
            formatted_snakes.append(formatted_snake)

        return formatted_snakes

    def GetFormattedSnakeInfo(self,result):
    # print(result.keys())
        snake_output = self.ChangeIntoSeprateInfo(result)
        return self.FormatSnakeResults(snake_output)


output = OutPutData()
output.GetFormattedSnakeInfo(output.resultNumberForm)
#print(output)
# for item in output:
#     print(item)





