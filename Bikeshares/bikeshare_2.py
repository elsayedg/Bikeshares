import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


# defining two function to make  DRY code
def Get_Month():
    """
    this function take no arrguments 
    Returns:
        (str) month - name of the month to filter by
    """
    Month_flag = True
    while Month_flag:
        Months_Dict = {1: 'January',
                       2: 'February',
                       3: 'March',
                       4: 'April',
                       5: 'May',
                       6: 'June'}

        Month_input = input("Enter Number of the Month you want, choose from 1 to 6\nwhich 1 for January\n")
        # check the input of month
        while Month_input not in ['1', '2', '3', '4', '5', '6']:
            Month_input = input("Please choose from 1 to 6\n")

        Month = Months_Dict[int(Month_input)]
        if Month in Months_Dict.values():
            Month_flag = False
    return Month


def Get_Day():
    """
    take no arrguments
    Returns:
        (str) day - name of the day of week to filter by
    """
    Day_flag = True
    while Day_flag:
        Days_Dict = {1: 'Monday',
                     2: 'Tuesday',
                     3: 'Wednesday',
                     4: 'Thursday',
                     5: 'Friday',
                     6: 'Saturday',
                     7: 'Sunday'}

        Day_input = input("Enter Number of the Day you want, choose from 1 to 7\nwhich 1 for Monday\n")
        # check the input of day
        while Day_input not in ['1', '2', '3', '4', '5', '6', '7']:
            Day_input = input("Please ente a number from 1 to 7\n")

        Day = Days_Dict[int(Day_input)]

        if Day in Days_Dict.values():
            Day_flag = False
    return Day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    City_flag = True
    while City_flag:
        City_Dict={ 1 :'Chicago',
                    2 :'New york city',
                    3 :'Washington'}

        city_input = input(
            "Which City are you intersted in\n"
            "Type the Number of Ctiy\n"
            "1- Chicago, 2- New york city, 3- Washington\n")

        # Check if user enter any other input

        while city_input not in ['1','2','3']:
            city_input = input("please enter a number from 1 to 3\n")

        city = City_Dict[int(city_input)]
        # if the City is valid exit the while loop
        if city in City_Dict.values():
            City_flag = False


    # Let User Choose his/her own Filters
    print('you have Choose {} '.format(city.capitalize()))
    Filter_flag = True
    while Filter_flag:
        Filter_Type = input('Would you like to Filter the Data \n'
                            'by month, day, both or not at all? type "none" for no filter\n').lower()
        if Filter_Type in ['day','month','both','none']:
            Filter_flag = False

        if Filter_Type == 'both':
            # get user input for month and Day
            month = Get_Month()
            day = Get_Day()
        elif Filter_Type == 'month':
            month = Get_Month()
            day = "all"
        elif Filter_Type == 'day':
            month = "all"
            day = Get_Day()
        elif Filter_Type == 'none':
            month = "all"
            day = "all"

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time  column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month , day of week and start hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour']= df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df.query("month == @month",inplace=True)

    # filter by day of week if applicable
    if day != 'all':
        df.query('day_of_week == @day',inplace=True)

    df.reset_index(inplace=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if len(df['month'].unique())>2:
        # display the most common month
        month = df['month'].mode()[0]
        print("the most common month {}".format(month))
    if len(df['day_of_week'].unique()) > 2:
        # display the most common day of week
        day = df['day_of_week'].mode()[0]
        print('the most common Day is {}'.format(day))
    # display the most common start hour
    start_hour = df['start_hour'].mode()[0]
    print('the most common start hour is {}'.format(start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('most commonly used start station is {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('most commonly used end station is {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    # make new column that has the start and the end as the same string
    # then take most frequant in that columns
    df['start_end'] = df['Start Station']+' ===> ' +df['End Station']
    Popular_Trip = df['start_end'].mode()[0]
    print('most Popular Trip\n{}'.format(Popular_Trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time in Hours {}'.format(round(df['Trip Duration'].sum() / 120),2))
    # display mean travel time
    print('Mean Travel Time in Hours {}'.format(round(df['Trip Duration'].mean() / 120),2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types\n{}".format(df['User Type'].value_counts()))
    # Display number of Users
    Num_Users = df['User Type'].count()
    print('\nTotal Number of Users in this Data set\n {}'.format(Num_Users))
    # Display counts of gender
    if 'Gender' in df:
        print("\nCounts of Gender \n{}".format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        youngest = int(df['Birth Year'].max())
        oldest = int(df['Birth Year'].min())
        comman_brith_date = int(df['Birth Year'].mode())
        print("\nthe oldest User Birth Year {},\nthe youngest User Birth Year {},\nand most common Birth date {}".format(oldest,youngest,comman_brith_date))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def view_rows(df):
    """
    this function shows rows of a data fram during excution
    Args:df
    Returns:None
    """
    print('Would You like to see  rows of raw Data?')
    raw_input = input('Enter "Yes" or "No"\n')
    # variable to keep track of veiwing data
    old_number = 0
    new_number = 0
    # check for the input
    while raw_input.upper() not in ['YES', 'NO']:
        raw_input = input('please Type "YES" or "NO"')

    while raw_input.upper() == "YES":
        number_exit = input("Enter Number of lines or NO to exit ")
        if number_exit.lower() == 'no':
            return

        new_number += int(number_exit)

        print(df.iloc[old_number:new_number])
        old_number = new_number

    if raw_input.upper() == "NO":
        return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
