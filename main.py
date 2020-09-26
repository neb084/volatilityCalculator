import requests
import sys
import datetime as dt
# API key
key = 'key left out'


def get_price_history(**kwargs):
    # Method/function to call to website and upload parameters and return results
    # **kwargs means it can handle many arguments that are defined by a keyword in which the method can handle

    # URL address for API, pulling 'symbol' key from kwargs
    url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(kwargs.get('symbol'))

    # Initialize dictionary
    user_params = {}
    # Add 'apikey' to "user_params" dictionary
    user_params.update({'apikey': key})

    # for every argument ("arg") in kwargs, add it to the "user_params" dictionary
    for arg in kwargs:
        user_params.update({arg: kwargs.get(arg)})

    # Return the results by sending "url" and the supplied "params" (params is a keyword on the API), json is the format it is being received in
    return requests.get(url, params=user_params).json()


# Loop for user input and running program
keep_processing = True

while keep_processing:
    # get user input
    user_input = input("Input symbol (exit with 0): ")
    # check for exit command
    if user_input.isnumeric() and int(user_input) == 0:
        # exit system
        sys.exit(0)
    else:
        # convert to uppercase
        user_input = user_input.upper()

    # call API with criteria
    data_dict = get_price_history(symbol=user_input, period=2,  periodType='month', frequency=1, frequencyType='daily', needExtendedHoursData='false')

    # initialize lists
    date = []
    period_high = []
    period_low = []
    period_range = []
    five_day_range = []
    ten_day_range = []
    twenty_day_range = []

    # loop for size of dictionary
    for i in range(len(data_dict['candles'])):
        # format date... requires //1000 & adding 2 hours (+7200)... %a is Day, %b is Month, %d is numeric date
        date.append(dt.date.fromtimestamp(data_dict['candles'][i]['datetime']//1000+7200).strftime('%a, %b %d'))

        # get the high, low & calculate the range
        period_high.append(float(data_dict['candles'][i]['high']))
        period_low.append(float(data_dict['candles'][i]['low']))
        period_range.append((period_high[i]/period_low[i])-1)

        # print gathered info
        print(date[i], f"High: {period_high[i]:<7.2f}", f"Low: {period_low[i]:<7.2f}",
              f"Range: {period_range[i]:<6.2%}", end=' ')

        # check if 5 day average is availible, if so print info
        print('5 day:', end=' ')
        if i >= 4:
            five_day = 0
            for j in range(i-4, i+1):
                five_day = five_day + period_range[j]
            five_day_range.append(five_day / 5)
            print(f"{five_day_range[i]:<6.2%}", end=' ')
        else:
            print('      ', end=' ')
            five_day_range.append(-1) # means no data

        # check if 10 day average is availible, if so print info
        print('10 day:', end=' ')
        if i >= 9:
            ten_day = 0
            for j in range(i - 9, i + 1):
                ten_day = ten_day + period_range[j]
            ten_day_range.append(ten_day / 10)
            print(f"{ten_day_range[i]:<6.2%}", end=' ')
        else:
            print('      ', end=' ')
            ten_day_range.append(-1)  # means no data

        # check if 20 day average is availible, if so print info
        print('20 day:', end=' ')
        if i >= 19:
            twenty_day = 0
            for j in range(i - 19, i + 1):
                twenty_day = twenty_day + period_range[j]
            twenty_day_range.append(twenty_day / 20)
            print(f"{twenty_day_range[i]:<6.2%}")
        else:
            print('      ')
            twenty_day_range.append(-1)  # means no data

    # Calculate max of each range for 10 last days
    print("\nMax Ranges of", user_input, "in each Category within the last 10 days")
    print("=========================================================")

    # Max of 5 day
    max_five_day = 0
    for i in range(len(five_day_range) - 10, len(five_day_range)):
        if five_day_range[i] > max_five_day:
            max_five_day = five_day_range[i]
    print(f'Max of 5 day:    {max_five_day:<6.2%}')

    # Max of 10 day
    max_ten_day = 0
    for i in range(len(ten_day_range) - 10, len(ten_day_range)):
        if ten_day_range[i] > max_ten_day:
            max_ten_day = ten_day_range[i]
    print(f'Max of 10 day:   {max_ten_day:<6.2%}')

    # Max of 20 day
    max_twenty_day = 0
    for i in range(len(twenty_day_range) - 10, len(twenty_day_range)):
        if twenty_day_range[i] > max_twenty_day:
            max_twenty_day = twenty_day_range[i]
    print(f'Max of 20 day:   {max_twenty_day:<6.2%}')

    # Max of 5, 10, & 20 day
    max_all = 0
    if max_five_day > max_all:
        max_all = max_five_day
    if max_ten_day > max_all:
        max_all = max_ten_day
    if max_twenty_day > max_all:
        max_all = max_twenty_day
    print(f'Max of all days: {max_all:<6.2%}')




