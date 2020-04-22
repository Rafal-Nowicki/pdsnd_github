import pandas as pd
import time
import calendar

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all_months" to apply no month filter
        (str) day - name of the day of week to filter by, or "all_days" to apply no day filter
    """

    print("Hello there! Let's explore some data!")

    legit_cities = ['chicago', 'new york city', 'washington'] # cities im gonna accept
    city = input("\nWhich city do you want to analyze? Chicago, New York City or Washington?\n").lower()
    while city not in legit_cities:
        print("There is no such city in database!")
        city = input("\nWhich city do you want to analyze?\n").lower()

    city = city.replace(" ", "_")

    possible_answers = ['month', 'day', 'both', 'none'] # answers im gonna accept - 4 possibilities
    answer = input("\nFilter by 'month','day' or 'both'? If you don't want to filter type 'none'\n").lower()
    while answer not in possible_answers:
        print("WAAT?!")
        answer = input("\nFilter by 'month','day' or 'both'? If you don't want to filter type 'none'\n").lower()


    legit_months = ['Jan', "Feb", "Mar", "Apr", "May", "Jun"]
    legit_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fry', 'Sat', 'Sun']
    month, day = 'all_months', 'all_days'

    if answer == 'both':
        month = input("\nWhich month do you want to analyze? Jan, Feb ,.., Jun\n").capitalize()
        while month not in legit_months:
            print('There is no such month! Try again.')
            month = input("\nWhich month do you want to analyze?\n").capitalize()
        day = input("\nChoose a day of interest - Mon, Tue, ...\n").capitalize()
        while day not in legit_days:
            print("There is no such day! Try again.")
            day = input("\nWhich day do you want to analyze? Mon, Tue, Wed...\n").capitalize()
    elif answer == "month":
        month = input("\nWhich month do you want to analyze? Jan, Feb, ..., Jun\n").capitalize()
        while month not in legit_months:
            print('There is no such month! Try again.')
            month = input("\nWhich month do you want to analyze?\n").capitalize()
    elif answer == 'day':
        day = input("\nChoose a day of interest - Mon, Tue, Wed...\n").capitalize()
        while day not in legit_days:
            print("There is no such day! Try again.")
            day = input("\nWhich day do you want to analyze?\n").capitalize()
    return city, month, day
    print('-'*40)


##############################################

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all_months" to apply no month filter
        (str) day - name of the day of week to filter by, or "all_days" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    data = pd.read_csv("{}.csv".format(city))
    data.drop(data.columns[0], axis = 1, inplace = True) #dropping this strange column

    data['Start Time'] =  pd.to_datetime(data['Start Time'], format='%Y-%m-%d %H:%M:%S')
    data['End Time'] =  pd.to_datetime(data['End Time'], format='%Y-%m-%d %H:%M:%S')

    data['weekday'] = data['Start Time'].dt.dayofweek #0 - monday
    data['month'] = data['Start Time'].dt.month #1 - january
    data['hour'] = data['Start Time'].dt.hour # 1 - hour 1

    day_dict = {"Mon":0, "Tue":1, "Wed":2, "Thu":3, "Fry":4, "Sat":5, "Sun":6}

    month_dict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6}

    if month == 'all_months' and day != 'all_days': # filter just by day
        day = day_dict.get(day)
        df = data[data['weekday'] == day]
    elif day == 'all_days' and month != 'all_months': # filter just by month
        month = month_dict.get(month)
        df = data[data['month'] == month]
    elif day == 'all_days' and month == 'all_months': # no filters
        df = data
    else: # filter both by day and month
        day = day_dict.get(day)
        month = month_dict.get(month)
        df = data[(data['weekday']== day) & (data['month']==month)]
    return df

###########################



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("="*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_freq_hour = str(df.groupby(['hour'])['Start Time'].count().idxmax())
    high_hour_qty = str(df.groupby(['hour'])['Start Time'].count().max())


    if len(df['weekday'].unique()) != 1 and len(df['month'].unique()) != 1: # if you dont filter im gonna show you month, day and hour
        most_freq_month = int(df.groupby(['month'])['Start Time'].count().idxmax())
        high_month_qty = str(df.groupby(['month'])['Start Time'].count().max())

        print("Hottest month was {}".format(calendar.month_name[most_freq_month]))
        print("Bikes were rented then for about {} times".format(high_month_qty))
        print()
        most_freq_day = int(df.groupby(['weekday'])['Start Time'].count().idxmax())
        high_day_qty = str(df.groupby(['weekday'])['Start Time'].count().max())

        print("Hottest day was {}".format(calendar.day_name[most_freq_day]))
        print("Bikes were rented then for about {} times".format(high_day_qty))
        print()
        print("Hottest hour was {} o'clock".format(most_freq_hour))
        print("Bikes were rented then for about {} times".format(high_hour_qty))


    elif len(df['month'].unique()) == 1 and len(df['weekday'].unique()) != 1: # if you filter just by month i will show you day and hour
        most_freq_day = int(df.groupby(['weekday'])['Start Time'].count().idxmax())
        high_day_qty = str(df.groupby(['weekday'])['Start Time'].count().max())

        print("Hottest day was {}".format(calendar.day_name[most_freq_day]))
        print("Bikes were rented then for about {} times".format(high_day_qty))
        print()
        print("Hottest hour was {} o'clock".format(most_freq_hour))
        print("Bikes were rented then for about {} times".format(high_hour_qty))

    elif len(df['month'].unique()) != 1 and len(df['weekday'].unique()) == 1: # if you filter only by day i will show you month and hour

        most_freq_month = int(df.groupby(['month'])['Start Time'].count().idxmax())
        high_month_qty = str(df.groupby(['month'])['Start Time'].count().max())

        print("Hottest month was {}".format(calendar.month_name[most_freq_month]))
        print("Bikes were rented then for about {} times".format(high_month_qty))
        print()
        print("Hottest hour was {} o'clock".format(most_freq_hour))
        print("Bikes were rented then for about {} times".format(high_hour_qty))


    else: # if you filter either just by day or by both day and month im gonna show you just hour
        print("Hottest hour was {} o'clock".format(most_freq_hour))
        print("Bikes were rented then for about {} times".format(high_hour_qty))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_high_freq = df.groupby(['Start Station'])['Start Time'].count().idxmax()
    start_station_high_qty = df.groupby(['Start Station'])['Start Time'].count().max()
    print("The hottest start station was {}".format(start_station_high_freq))
    print("Bikes were rented there around {}".format(start_station_high_qty), "times")
    print()
    # TO DO: display most commonly used end station
    end_station_high_freq = df.groupby(['End Station'])['Start Time'].count().idxmax()
    end_station_high_qty = df.groupby(['End Station'])['Start Time'].count().max()
    print("The hottest end station was {}".format(end_station_high_freq))
    print("Bikes were rented there around {}".format(end_station_high_qty), "times")
    print()
    # TO DO: display most frequent combination of start station and end station trip
    df_grouped = df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'}).sort_values(by = "count", ascending = False)
    print("Most frequent stations combination was:\n{} and {}".format(str(df_grouped.iloc[0,0]), str(df_grouped.iloc[0,1])))
    print("This route was accomplished {} times".format(int(df_grouped.iloc[0,2])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['time'] = df['End Time'] - df['Start Time']
    # TO DO: display total travel time
    print("Total travel time in that period of time: {}".format(df['time'].sum()))
    print("Average time of journey: {}".format(df['time'].mean()))
    # TO DO: display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['Start Time'].count()
    print(user_types.to_string())
    print()

    try:
        # TO DO: Display counts of gender
        gender = df.groupby(['Gender'])['Start Time'].count()
        print(gender.to_string())
        print()
    # TO DO: Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        common = int(df['Birth Year'].mode()[0]) # its very important to index it with 0 -> without it program crashes f.e. for june monday filter in NY
        recent = int(df['Birth Year'].max())

        print("The oldest person that rented a bicycle in that time was born in: {}".format(earliest))
        print("The most common birth year: {}".format(common))
        print("The youngest person: {}".format(recent))

    except KeyError:
        print("="*40)
        print("For Washington there is no data on Gender and Birth Year")
        print("="*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("="*40)


def show_entries(df): # Line 249 and 259 - is there a better way to do that?
    i = -1 # i find it kind of stupid i = -1 but it works! when i set to 0 it starts showing entries from 5th row up
    while True:
        i+=1
        curious = input("Do you want to see five entries of raw data? Type 'yes' or 'no' \n")
        if curious.lower() != 'yes':
            break
        else:
            print(str(df.iloc[0+5*i:5+5*i, :8].to_json(orient = 'records',date_format = 'iso')).replace('},{', "\n\n").replace(",", "\n").replace("[{", "").replace("}]", "").replace('"', '').replace(":", ": "), "\n")

# Line 257 - i guess that is not very pythonic syntax but it works
# Line 257 - i dont like that iso date format but i didnt find any better solution

def show_entries_washington(df): # no info on gender and age for washington
    i = -1
    while True:
        i+=1
        curious = input("Do you want to see five entries of raw data? Type 'yes' or 'no' \n")
        if curious.lower() != 'yes':
            break
        else:
            print(str(df.iloc[0+5*i:5+5*i, :6].to_json(orient = 'records',date_format = 'iso')).replace('},{', "\n\n").replace(",", "\n").replace("[{", "").replace("}]", "").replace('"', '').replace(":",": "), "\n")
# I guess the program would crash if 0+i > number of rows in the data and:
    #a) i think i could prevent it somehow handling IndexError but...
    #b) i find it unnecessary to do so


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        if city == 'washington':
            show_entries_washington(df)
        else:
            show_entries(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
