import random as rm
import pickle


class Court:
    def __init__(self, index, time, date):
        self.booked = False
        self.name = None
        self.password = rm.randint(0, 99999)
        self.skill = None
        self.look = None
        self.index = index
        self.time = time
        self.date = date

    def __str__(self):
        return f"Date: {self.date} Time: {self.time} Court: {self.index}\nBooked: {self.booked} Name: {self.name} Skill: {self.skill}\n"


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def get_hour_booked_rate(week, date, hour):
    num = len(week[int(date)][int(hour)])
    booked = 0
    for i in range(num):
        if week[int(date)][int(hour)][i].booked:
            booked += 1
    return booked/num


def get_available_hours(week, date):
    print(f"These are the available hours on Day {date}: ", end="")
    for hour in range(0, 10):
        if get_hour_booked_rate(week, date, hour) != 1:
            print(f"{hour+6}:00 {get_hour_booked_rate(week, date, hour)*100}% | ", end="")
    print("")


def main():
    try:
        with open('week.pkl', 'rb') as inp:
            week = pickle.load(inp)
            # print(week[0][0][0])

    except FileNotFoundError:
        week = []

        for i in range(1, 8):
            date = []
            for j in range(1, 11):
                hour = []
                for k in range(1, 11):
                    hour.append(Court(k, j, i))
                date.append(hour)
            week.append(date)
        print('Blank schedule created')
        save_object(week, 'week.pkl')

    option = input("What do you want to do?\n1. Register court\n2. Cancel registration\n3. Check avaliablity ")
    if option == '1':
        date = int(input("What date would you like to register? "))
        get_available_hours(week, date)
        hour = int(input("What hour would you like to register? "))
        name = input("What is your name? ")
        skill = input("What is your skill level? (A/B/C/D) ")
        look = input("Are you looking for others to play with you (y/n) ")
        if look.lower() == 'y':
            look = True

        elif look.lower() == 'n':
            look = False

        index = 0
        for i in range(10):
            if not week[date][hour][i].booked:
                index = i
                break

        week[date][hour][index].booked = True
        week[date][hour][index].name = name
        week[date][hour][index].skill = skill
        week[date][hour][index].look = look

        print(f'Register {name} with skill level {skill}\non Day {date} and Hour {hour+5}:00 on Court {index+1}\nYour '
              f'password for this reservation is {week[date][hour][index].password}')

    if option == '2':
        date = int(input("What is the date of your reservation? "))
        hour = int(input("What is the hour of your reservation? "))
        index = int(input("What is the court number of your reservation? "))
        if week[date][hour][index].booked:
            password = int(input("What is your password? "))
            if week[date][hour][index].password == password:
                week[date][hour][index] = Court(index, hour, date)
                print("Cancellation successful")
            else:
                print("Wrong password")
                print("Please enter your information to cancel the reservation")
                name = input("What is your name? ")
                skill = input("What is your skill level? (A/B/C/D) ")
                look = input("Are you looking for others to play with you (y/n) ")
                if look.lower() == 'y':
                    look = True

                elif look.lower() == 'n':
                    look = False

                if name == week[date][hour][index].name and week[date][hour][index].skill == skill and week[date][hour][index].look == look:
                    week[date][hour][index] = Court(index, hour, date)
                    print("Cancellation successful")

                else:
                    print("Credentials wrong please try again")
        else:
            print("The court is not booked yet, please try again")

    save_object(week, 'week.pkl')






if __name__ == '__main__':
    main()
