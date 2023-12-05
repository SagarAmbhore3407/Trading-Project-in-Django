

import os
from django.shortcuts import render, HttpResponse
import csv
from django.http import JsonResponse, request
from .models import Candle
from datetime import datetime
from django.conf import settings
from django.http import FileResponse
from django.utils.encoding import smart_str

#Global variable to store the list of candles database obj...
candles = []
csv_file = None
time_frame = None
converted_filePath = None



#This function stores the data into Django database server...and creates the list of objects.                 
def store_csv(csv_file, timeframe):
    try:
        #The file will be splited in lines..
        #The first line will be of columns name
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        #Using DictReader which consider the column name as a key of dict..
        csv_data = csv.DictReader(decoded_file)
    
        #Iterating over the rows...and creating obj of candle model   
        for row in csv_data:
            #parcing date from file and coverting to date object
            csv_date = datetime.strptime(row['DATE'], '%Y%m%d').date()
            # Format the time according to the CSV format
            csv_time = datetime.strptime(row['TIME'], '%H:%M').time()
            
            candle = Candle(
                symbol=row['BANKNIFTY'],
                date=csv_date,
                time=csv_time,  
                open=row['OPEN'],
                high=row['HIGH'],
                low=row['LOW'],
                close=row['CLOSE'],
                volume=row['VOLUME']
            )
            candles.append(candle)
        
        #Execute the all objs in single query 
        Candle.objects.bulk_create(candles)
        return True
    
    except Exception as e:
        print(f"An Error occured while storing data..:{e}")
        return False




#Converts the candle into timeframe and then saves in temp file
def convert_to_timeframe(candles, time_frame):
    #Path of converted candles into dataframe within the app..
    file_path = os.path.join(settings.BASE_DIR, 'MainApp', 'TimeFrame_Candles.csv')  
    
    #Check whether the file exist or not, It will be deleted if it is..
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Write candle data to the file
    with open(file_path, 'w') as file:
        index = 0
        counter = 0
        while index+time_frame <= len(candles):
            counter += 1
            symbol = candles[index].symbol
            date = candles[index].date
            time = candles[index].time
            opening = candles[index].open
            high = max(candle.high for candle in candles[index:index + time_frame])
            low = min(candle.low for candle in candles[index:index + time_frame])
            close = candles[index + time_frame - 1].close
            volume = candles[index + time_frame - 1].volume

            candle_data = f"{counter}. Symbol: {symbol}, Date: {date}, Time: {time}, Open: {opening}, High: {high}, Low: {low}, Close: {close}, Volume: {volume}\n"
            file.write(candle_data)
            index += time_frame
        
        #Clears the candle obj list for reusing..    
        candles.clear()        
    return file_path





# Homepage static page route
def index(request):
    return render(request,"index.html")




#Action Route to take a input of csv file 
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        if csv_file:
            result = store_csv(csv_file, time_frame)
            if result:
                context = {
                    'message1':'File uploaded and stored to database Successfully....',
                    'message2':'Enter a timeframe number to convert those candles in respective timeframe..(Multiple to one Minute)'
                }
            else:
                context = {'message1':'The file upload process is Unsuccessful..',
                           'message2':'An error occurred in file storing Try again..'
                        }
        else:
            context = {
                    'message1':'Unable to find a file..',
                    'message2':'File not found in the request...'
                }
            
        return render(request,'gettimeframe.html',context = context)
    return render(request, 'index.html')




#Getting timeframe input        
def getTimeFrame(request):
    global time_frame  # Declare global variable
    global converted_filePath
    if request.method == 'POST':
        time_frame = request.POST.get('timeframeNo')
        converted_filePath = convert_to_timeframe(candles, int(time_frame))

        if converted_filePath:
            print(f"Printing from timeframe{converted_filePath}")
            context = {
                'message1': 'The file converted Successfully...',
                'message2': 'To Download the file click on Download button...'
            }
        else:
            context = {
                'message1': 'The file conversion Unsuccessful...',
                'message2': 'Try again later...'
            }
    else:
        return render(request, 'gettimeframe.html')

    return render(request, 'downloadfile.html', context=context)
   


#To download a file which is stored in system
def download_file(request):
    global converted_filePath

    if converted_filePath:
        
        try:
            with open(converted_filePath, 'rb') as file:
                response = HttpResponse(file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename={smart_str(os.path.basename(converted_filePath))}'
                return response
        except FileNotFoundError:
            return HttpResponse("File not found!", status=404)
    else:
        return HttpResponse("File path not set!", status=404)
  
    
 
            
                    
                      
           
                 
        
        
