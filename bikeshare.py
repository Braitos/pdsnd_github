import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv',
              'ca': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'wa': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\nI will need some information to understand your needs')
    # Get user input for city (chicago, new york city, washington).
    city = input('\nFirst, what is the city you want to analyse?\nChoose one of these cities CA, NY or WA (enter the full name if you like): ').lower()

    # Get user input for month (all, january, february, ... , june)
    month = input('\nNow, about the date.\nOur base has 6 months (january to june) \nTell me the specific month (complete name: january, february, ..., june)\nor simply type \'all\' if want all months:').lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nLast, what day of week you are looking for?\nTell me the specific day (complete name: monday, tuesday, ...)\nor simply type \'all\' if want all days of the week:').lower()

    print('-'*40)
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

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time AND End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month =  months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def display_raw_data(df):
    """
    Display for user 5 lines or more of raw data based in his the needs.

    Args:
        (str) raw_data - yes or no if the user wants the first five lines of data to analyse
        (str) more_raw_data - yes or no if the user wants more 5 lines of data to analyse

    Returns:
        table - Pandas DataFrame containing lines from the raw data of city data filtered by month and day
    """

    print('\nAwesome!\n')
    raw_data = input('Before your research summary,\nwould like to see the first lines of your raw data?\nEnter yes or no:')
    if raw_data.lower() == 'yes':
        line = 0
        index = df.index
        number_of_rows = len(index)
        while True:
            start_time = time.time()
            line += 5
            if line > number_of_rows:
                print('Sorry, there is no more data stored')
                print('-'*40)
                break
            else:
                table = df.head(line)
                print(table)
                print("\n(This took %s seconds to run)" % (time.time() - start_time))
                more_raw_data = input('\nWould you like to see more 5 lines? Enter yes or no.\n')
                if more_raw_data.lower() != 'yes':
                    break

    print('\nThank you for your inputs! See Below your search results\n')
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n1.The Most Frequent Times of Travel:\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('- The Most common month is: {}'.format(popular_month))

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('- The Most common day is: {}'.format(popular_day))

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('- The Most common start hour is: {}'.format(popular_hour))

    # Display function runtime
    print("\n(This took %s seconds to run)" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n2.The Most Popular Stations and Trip:\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('- The Most common Start Station is: {}'.format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('- The Most common End Station is: {}'.format(popular_end_station))

    # Display most frequent combination of start station and end station trip
    df['Station Combination'] = '  .start station: ' + df['Start Station'] + '\n' + '  .end station: ' + df['End Station']
    popular_station_combination = df['Station Combination'].mode()[0]
    print('- The Most common frequent combination of start station and end station trip is:\n{}'.format(popular_station_combination))

    # Display function runtime
    print("\n(This took %s seconds to run)" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n3.Trip Duration:\n')
    start_time = time.time()

    # Display total travel time
    df['travel time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['travel time'].sum()
    print('- The total travel time is: {}'.format(total_travel_time))

    # Display mean travel time
    mean_travel_time = df['travel time'].mean()
    print('- The mean travel time is: {}'.format(mean_travel_time))

    # Display function runtime
    print("\n(This took %s seconds to run)" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n4.User Stats:\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('- The counts of user types are:\n{}'.format(user_types))

    # Display counts of gender
    gender_exist = 'Gender' in df
    if gender_exist == False:
        print('\n- There are no data for gender of users')
    else:
        user_genders = df['Gender'].value_counts()
        print('\n- The counts of user genders are:\n{}'.format(user_genders))

    # Display earliest, most recent, and most common year of birth
    birth_exist = 'Birth Year' in df
    if gender_exist == False:
        print('\n- There are no data for Birth Year of users')
    else:
        most_recent_birth = df['Birth Year'].iloc[0]
        print('\n- The most recent year of birth is: {}'.format(most_recent_birth))
        most_common_birth = df['Birth Year'].mode()[0]
        print('\n- The most common year of birth is: {}'.format(most_common_birth))

    # Display function runtime
    print("\n(This took %s seconds to run)" % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Get user input to choose whether to restart analysis
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
