import random as rm
import pickle


# Court object used to store information of a registration
class Court:
    def __init__(self, index, time, date):
        self.booked = False
        self.name = None
        self.password = rm.randint(0, 99999)  # For canceling registration
        self.skill = None  # Player's skill level
        self.look = None  # Whether one is looking for others to play with
        self.index = index
        self.time = time
        self.date = date

    # Format for print(Court a) command
    def __str__(self):
        return f"Date: {self.date+1} Hour: {self.time+1} Court: {self.index+1}\nBooked: {self.booked} Name: {self.name} Skill: {self.skill}\n"


def save_object(obj, filename):
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def get_hour_booked_rate(week, date, hour):
    num = len(week[int(date)][int(hour)])
    booked = 0
    for i in range(num):
        if week[int(date)][int(hour)][i].booked:
            booked += 1
    return booked/num


def get_available_hours(week, date):
    print(f"These are the available hours on Day {date+1}: ", end="")
    for hour in range(0, 10):
        if get_hour_booked_rate(week, date, hour) != 1:
            print(f"Hour {hour+1} ({hour+6}:00) {get_hour_booked_rate(week, date, hour)*100}% | ", end="")
    print("")


def get_the_date(text):
    date = -1
    while date < 0 or date > 6:
        date = int(input(text)) - 1
        if date < 0 or date > 6:
            print("Invalid date, try again")
    return date


def get_the_skill(text):
    skill = ''
    while skill != 'A' and skill != 'B' and skill != 'C' and skill != 'D':
        skill = input(text)
        skill = skill.upper()
        if skill != 'A' and skill != 'B' and skill != 'C' and skill != 'D':
            print("Invalid skill, try again")
    return skill


def get_the_look(text):
    look = ''
    while look != 'y' and look != 'n':
        look = input(text)
        look = look.lower()
        if look != 'y' and look != 'n':
            print("Invalid input, try again")

    if look.lower() == 'y':
        result = True

    else:
        result = False

    return result


def get_the_hour(text,week,date,reg):
    hour = -1
    while hour < 0 or hour > 9 or (get_hour_booked_rate(week, date, hour) == 1 and reg):
        hour = int(input(text)) - 1
        if hour < 0 or hour > 9:
            print("Invalid hour, try again")

        if get_hour_booked_rate(week, date, hour) == 1:
            print('Sorry but we are all booked for this time, Please try another time.')

    return hour


def get_the_index(text):
    index = -1
    while index < 0 or index > 9:
        index = int(input(text)) - 1
        if index < 0 or index > 9:
            print("Invalid index, try again")
    return index


def menu():
    print("Welcome to the Smart Badmington Registration System!")
    print("What would you like to do?")
    print('1. Register Court')
    print('2. Cancel Registration')
    print('3. Check Availability')
    print('4. Look for people to play')
    print('5. Print all bookings')
    print('6. Exit')
    print("Please enter your choice: ")


def main():
    try:
        with open('week.pkl', 'rb') as inp:
            week = pickle.load(inp)

    except FileNotFoundError:
        week = []

        for i in range(0, 7):
            date = []
            for j in range(0, 10):
                hour = []
                for k in range(0, 10):
                    hour.append(Court(k, j, i))
                date.append(hour)
            week.append(date)
        print('Blank schedule created')
        save_object(week, 'week.pkl')

    menu()
    option = input()

    if option == '1':
        textDate = "What date would you like to register? Day (1-7) "
        date = get_the_date(textDate)

        get_available_hours(week, date)

        textHour = "What hour would you like to register? Hour (1-10) "
        hour = get_the_hour(textHour, week, date, True)

        name = input("What is your name? ")

        textSkill = "What is your skill level? (A/B/C/D) "
        skill = get_the_skill(textSkill)

        textLook = "Are you looking for others to play with you (y/n) "
        look = get_the_look(textLook)

        index = 0
        for i in range(10):
            if not week[date][hour][i].booked:
                index = i
                break

        week[date][hour][index].booked = True
        week[date][hour][index].name = name
        week[date][hour][index].skill = skill
        week[date][hour][index].look = look

        print(f'Registered {name} with skill level {skill}\non Day {date+1} and Hour {hour+5}:00 on Court {index+1}\nYour '
              f'password for this reservation is {week[date][hour][index].password:05}')

    elif option == '2':
        textDate = "What is the date of your reservation? Day (1-7) "
        date = get_the_date(textDate)

        textHour = "What is the hour of your reservation? Hour (1-10) "
        hour = get_the_hour(textHour, week, date, False)

        textIndex = "What is the court number of your reservation? Court (1-10) "
        index = get_the_index(textIndex)

        if week[date][hour][index].booked:
            password = int(input("What is your password? "))
            if week[date][hour][index].password == password:
                week[date][hour][index] = Court(index, hour, date)
                print("Cancellation successful")
            else:
                print("Wrong password")
                print("Please enter your information to cancel the reservation")
                name = input("What is your name? ")

                textSkill = "What is your skill level? (A/B/C/D) "
                skill = get_the_skill(textSkill)

                textLook = "Are you looking for others to play with you (y/n) "
                look = get_the_look(textLook)

                if name == week[date][hour][index].name and week[date][hour][index].skill == skill and week[date][hour][index].look == look:
                    week[date][hour][index] = Court(index, hour, date)
                    print("Cancellation successful")

                else:
                    print("Credentials wrong please try again")
        else:
            print("The court is not booked yet, please try again")

    elif option == '3':
        dayNum = 0
        for day in week:
            num = len(week[0]) * len(week[0][0])
            booked = 0
            for hour in day:
                for court in hour:
                    if court.booked:
                        booked += 1
            print(f'Day {dayNum+1}, the courts are {booked/num*100}% booked')
            dayNum += 1

        textDate = "Which date do you want to check? Day (1-7) "
        date = get_the_date(textDate)

        get_available_hours(week, date)

        textHour = "Which hour do you want to check? Hour (1-10) "
        hour = get_the_hour(textHour, week, date, False)

        for i in range(len(week[0][0])):
            if week[date][hour][i].booked:
                print(week[date][hour][i])

    elif option == '4':
        textSkill = "What is your skill level? (A/B/C/D) "
        skill = get_the_skill(textSkill)

        have = False
        print('Here are the people that are looking for people to play with:')
        for day in week:
            for hour in day:
                for court in hour:
                    if court.look and skill == court.skill:
                        print(court)
                        if not have:
                            have = True

        if have:
            textDate = "What is the date of your desired reservation? "
            date = get_the_date(textDate)

            textHour = "What is the hour of your desired reservation? "
            hour = get_the_hour(textHour, week, date, False)

            textIndex = "What is the court number of your desired reservation? "
            index = get_the_index(textIndex)

            name = input("What is your name? ")
            week[date][hour][index].name = week[date][hour][index].name + " and "+name
            week[date][hour][index].look = not week[date][hour][index].look
            print(week[date][hour][index])
        else:
            print('Sorry we do not have people at your skill level that is looking for people to play with.')

    elif option == '5':
        pwd = input("Enter administrative password: ")
        if pwd == 'qwerty':
            for date in week:
                for hour in date:
                    for index in hour:
                        if index.booked:
                            print(index)
                            print(f'Password: {index.password:02}')
                            print('---')
        else:
            print('Access denied')

    elif option == '6':
        print("Thank you for using Smart Badmington Registration System!")
        return

    else:
        print('Wrong input. Please try again.')

    save_object(week, 'week.pkl')
    print("---")


if __name__ == '__main__':
    main()
