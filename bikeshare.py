import time
import pandas as pd
import numpy as np

#for file name extraction
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#for city name validation
cities = ['chicago', 'new york city', 'washington']
#for month validation and extracting number of month
month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
#for day validation
day_list= ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday' , 'all']#for day validation

i = 5#variable to access rows of the data frame

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # getting input for city (chicago, new york city, washington).
    city = input('Which City do you want to explore ?(chicago, new york city, washington) : ').lower()
    #validating city input
    while city not in cities:
        city = input('Enter a Valid City! (chicago, new york city, washington) : ').lower()

    #
    print('\n***Now Enter Month and Day you want to filter by***\n')

    # get user input for month (all, january, february, ... , june)
    month =input('Enter Month : (Note)-Enter Month\'s Name -Month Should be from "january" to "june" -For no Month Filter enter "all" \n').lower()
    while month not in month_list :#validating month
        month = input('Enter Valid Month!: ').lower()

    #getring user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter Day : (Note) -Enter Day\'s Name -For no Day Filter enter "all" \n').lower()
    while day not in day_list :#validating day
        day = input('Enter Valid Day! : ').lower()

    print('-'*40)
    #print( "preparing to filter by ",city, month, day)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #loading City's csv file
    df = pd.read_csv(CITY_DATA[city])

    #delete 'unnamed' column #dont's know why it exists!
    df = df.drop(['Unnamed: 0'], axis = 1)
    #print("df:\n",df.head())

    #converting Date to Datetime data-type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #making a new column for months
    df['months'] = df['Start Time'].dt.month

    #making a new column for day_name
    df['days'] = df['Start Time'].dt.day_name()

    #Applying month filter
    if month != 'all' :
        #testing#print("printing from if month != 'all'")
        #convertin month name to months's order
        month_num = month_list.index(month) + 1
        df = df[df['months'] == month_num]#only show data for chosen month

    #Applying day filter
    if day != 'all' :
        #testing#print("printing from if day != 'all'")
        df = df[df['days'] == day.title()] #only show data for chosen day

    #testing the DateFrame
    #print("testing data frame:\n",df.head())
    #print('the order of the month you chosed: ',month,'\n')
    #print('testing months column: \n',df['months'][:5])
    #print('testing days column: \n',df['days'][:5],'\n')
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    calc_time_stats = input('\nWould You like to Calculate The Most Frequent Times of Travel "yes" or Continue "no" ?\n').lower()
    while calc_time_stats != 'yes' and calc_time_stats != 'no' :
        calc_time_stats = input('\nWould you like to Calculate The Most Frequent Times of Travel "yes" or Continue "no" ?\n').lower()


    if calc_time_stats == 'yes':
        print('Calculating Most Frequent Times of Travel.......\n')
        start_time = time.time()
        # display the most common month only if no-month filter
        #clculate most common month
        if month == 'all':
            month_data = df['months'].value_counts()
            print('•"Month" that had most Trips : {}, count: {}\n'.format(month_list[month_data.idxmax() - 1], month_data.max() ))

        # display the most common day of week
        if day == 'all':
            most_common_day = df['days'].value_counts()
            print('•"Day" of week that had most Trips : {}, count: {}\n'.format(most_common_day.idxmax(), most_common_day.max() ))


        # display the most common start hour
        #print('testing dataframe before hour\n',df.head())
        df['hours'] = df['Start Time'].dt.hour
        #print('testing dataframe after hour\n',df.head())
        most_common_start_hour = df['hours'].value_counts()
        #print("testing most common start hour data:\n", most_common_start_hour)
        print('•"Hour" that had Most Trips : {}, count: {}'.format(most_common_start_hour.idxmax(), most_common_start_hour.max() ))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    calc_station_stats = input('\nWould You like to Calculate The Most Popular Stations and Most frequent Trip "yes" or Continue "no" ?\n').lower()
    while calc_station_stats != 'yes' and calc_station_stats != 'no' :
        calc_station_stats = input('\nWould you like to Calculate The Most Popular Stations and Most frequent Trip "yes" or Continue "no" ?\n').lower()


    if calc_station_stats == 'yes':
        print('\nCalculating The Most Popular Stations and Most frequent Trip\n')
        start_time = time.time()

        # display most commonly used start station
        start_station_data = df['Start Station'].value_counts()
        #print('start sttation data\n',start_station_data)#testing
        print('•Most common Start sation: {} ,Count : {}\n'.format(start_station_data.idxmax(), start_station_data.max() ))

        # display most commonly used end station
        end_station_data = df['End Station'].value_counts()
        #print("end station data:\n",end_station_data)#testing
        print('•Most common End sation: {} ,Count : {}\n'.format(end_station_data.idxmax(), end_station_data.max() ))


        # display most frequent combination of start station and end station trip
        #make a dataframe 'trip_data' for combination counts
        trip_data = df.groupby(['Start Station', 'End Station']).size().reset_index().rename(columns={0:'count'})
        #print(trip_data)#test it

        #reducing data frame into one row containing most frequent TRIP
        trip_data = trip_data[trip_data['count']==trip_data['count'].max()].reset_index()
        #print("most frequent trip:\n",freq_trip)
        print('•Most Frequent Trip: FROM "{}" >>> TO "{}" ,count: {}\n'.format(trip_data['Start Station'][0], trip_data['End Station'][0], trip_data['count'][0] ))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    calc_trip_stats = input('\nWould You like to Calculate statistics on Trip duration "yes" or Continue "no" ?\n').lower()
    while calc_trip_stats != 'yes' and calc_trip_stats != 'no' :
        calc_trip_stats = input('\nWould you like to Calculate statistics on Trip duration "yes" or Continue "no" ?\n').lower()


    if calc_trip_stats == 'yes':
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
        total = df['Trip Duration'].sum()
        print('•Total Travel Time: ', round(total, 2), 'S\n')

        # display mean travel time
        avarage = df['Trip Duration'].mean()
        print('•avarage trip Duration: ', round(avarage,2), 'S\n')


        print('\nThis took %s seconds.' % (time.time() - start_time))
        print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
       (str) city - name of the city to check if data is available for the city or not
    """
    calc_user_stats = input('\nWould You like to Calculate satistics on BikeShare users "yes" or Continue "no"? \n').lower()
    while calc_user_stats != 'yes' and calc_user_stats != 'no' :
        calc_user_stats = input('\nWould you like to Calculate statistics on BikeShare users "yes" or continue "no"\n').lower()


    if calc_user_stats == 'yes':
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_type = df['User Type'].value_counts()
        print("USER TYPES :\n•Subscribers : {}\n•Customer    : {}\n".format(user_type['Subscriber'],user_type['Customer']))

        # Display counts of gender
        if city == 'chicago' or city == 'new york city':
            gender = df['Gender'].value_counts()
            print('COUNTS OF GENDER :\n•male   : {} \n•female : {}\n'.format(gender['Male'], gender['Female']))
        else:
            print('*No gender data is available for Washington')

        # Display earliest, most recent, and most common year of birth
        if city == 'chicago' or city == 'new york city':
            print('YEAR OF BIRTH STATS :')
            print('•earliest year of birth    : ',df['Birth Year'].min())#,earliest_year)
            print('•most recent year of birth : ',df['Birth Year'].max())#,recent_year)
            print('•most common year of birth : ',(df['Birth Year'].mode())[0])#,common_year)
        else:
            print("*No Birth data is available for Washington")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def raw_data(df, i):
    """ displays 5 raw data from the dataframe"""
    while True:



        #get input to show raw data or not
        display_data = input('\nWould you like to see raw data? yes or no \n').lower()
        while display_data != 'yes' and display_data != 'no':#validate the input
            display_data = input('\nWould you like to see raw data? yes or no : \n').lower()

        if display_data == 'yes':
            print('raw data:\n',df.iloc[ i-5 : i ,:])
            i += 5

        elif display_data == 'no':
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df, i)

        restart = input('\nWould you like to restart the Program? Enter yes or no.\n').lower()
        while restart != 'yes' and restart != 'no' :
            restart = input('\nWould you like to restart the program? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
