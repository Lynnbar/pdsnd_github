import pandas as pd
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# This function asks for the user for the city and returns the name of the csv file
# to read
def ask_city():
    '''Asks the user for a city and returns the filename for 
    that city's bike share data.
    Args:
        none.
    Returns:
        City name (str) that a user selected.
    '''
    city = ''
    while city not in ('chicago', 'new york', 'washington'):
        city = input('Please enter your city choice Chicago, New York, Washington:\n')
        city = city.lower()
        if city in ('chicago', 'new york', 'washington'):
            return city
        else:
            print('Sorry this is an invalid input\n')

            
# Ask the user for the time frame to perform analysis
def ask_time():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        Month and Day (str) period selected by the user.
    '''
    
    time_frame = ''
    
    while time_frame not in ['month', 'day', 'none']:
        time_frame = input('Would you like to filter the data by Month, Day, None:\n')
        time_frame = time_frame.lower()
        
        # Ask user for the month
        if time_frame == 'month':
          month = ''
          while month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            month = input('Which month? January, February, March, April, May, or June?:\n')
            month = month.lower()
            if month in ['january', 'february','march', 'april','may','june']:
              day = 'all'
            else:
              print('Sorry this is an invalid input\n')

        # Ask user for the day
        elif time_frame == 'day':
          day = ''
          while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday'):
            day = input('Which Day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?:\n')
            day = day.lower()
            if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
              month = 'all'
            else:
              print('Sorry this is an invalid input\n')
          
        
        elif time_frame == 'none':
          month = 'all'
          day = 'all'

        else:
          print('Sorry, invalid input\n')
    
    return month, day


# Load data that will return filter data frame
def load_data(city, month, day):
    '''Filters a dataframe based on selections by the user.
    Args:
        city - string
        month - string
        day - string
    Returns:
        df - Filtered pandas dataframe.
    '''

    df = pd.read_csv(CITY_DATA[city])
   # print(df.head())

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1\

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        df: pandas dataframe.
    Returns:
        None
    Output:
        Prints out most popular month, day and hour for trips in the dataframe
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day Of Week: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    print("\nThis took {}s seconds.".format(time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        df: pandas dataframe.
    Returns:
        None
    Output:
        Prints out total trip duration and average trip durations
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The Total Travel Time (sec): ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average Travel Time (sec): ', mean_travel_time)


    print("\nThis took {}s seconds.".format(time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        df: pandas dataframe.
    Returns:
        None
    Output:
        Prints out most popular start,end and most frequent combination of start station and end station trip 
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station: ', popular_end_station)


    # display most frequent combination of start station and end station trip
    
    df['trip'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    popular_trip = df['trip'].mode()[0]
    print('Most Common Trip Taken:',popular_trip)
    

    print("\nThis took {}s seconds.".format(time.time() - start_time))
    print('-'*40)

def user_stats(df, city ):
    """Displays statistics on bikeshare users.
    Args:
        df: pandas dataframe
        city: city name (str) selected by the user        
    Returns:
        None
    Output:
        pandas series with counts for each user type ,counts of gender,
        earliest, latest, and most frequent year of birth
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('The Counts By User Type Are:\n',count_user_types)


    # TO DO: Display counts of gender
    if city != "washington":
        count_gender_types = df['Gender'].value_counts()
        print('The Counts By Gender Type Are:\n', count_gender_types)
        earliest_bday = df['Birth Year'].min()
        print('The earliest Birthday was: ', earliest_bday)
    
        most_recent_bday = df['Birth Year'].max()
        print('The Most Recent Birthday was:\n ', most_recent_bday)
    
        most_common_bday = df['Birth Year'].mode()[0]
        print('The Most Common Birthday was:\n ', most_common_bday)


    print("\nThis took {}s seconds.".format(time.time() - start_time))
    print('-'*40)
    
    
def display_data(df):
    """Displays 5 rows at a time for the filtered data frame.
    Args:
        df: pandas dataframe.
    Returns:
        None
    Output:
        Prints out 5 rows of the dataframe at a time 
    """

    i = 0
    user_input = input('\n Would you like to see individual trip data? Type Yes or No:\n')
    user_input = user_input.lower()
    
    while user_input != 'no':
        print(df[i:i+5])
        print('-'*40)
        i = i+5
        user_input = input('\n Would you like to see more data? Type Yes or No:\n')
        user_input = user_input.lower()

        
def main(): 
    """Calculates and prints out the descriptive statistics about a city
    and time period specified by the user.
    
    Args:
        df: pandas dataframe.
    Returns:
        None
    Output:
        Asks user if they want to restart the program again 
    """
    
    final_question = 'yes'
    
    while final_question != 'no':
        city = ask_city()
        result = ask_time()
        month = result[0]
        day = result[1]
        data_frame = load_data(city, month, day)
    
        time_stats(data_frame)
        trip_duration_stats(data_frame)
        station_stats(data_frame)
        user_stats(data_frame, city)
        display_data(data_frame)
    
        final_question = input('\n Would you like to restart? Type Yes or No:\n')
        final_question = final_question.lower()
 
    print('Thank you for using the Bike Share Exploration Program!')


if __name__ == "__main__":
    main()


  