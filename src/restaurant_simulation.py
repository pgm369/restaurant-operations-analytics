import pandas as pd
import random
from datetime import datetime, timedelta

NUMBER_OF_PARTIES = 200

TABLE_CAPACITY = 47

START_DATE = datetime(2026, 1, 1)

OUTPUT_FILE = "../data/restaurant_operations.csv"

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

def generate_date():

    random_days = random.randint(0, 364)

    date = START_DATE + timedelta(days=random_days)

    return date

def generate_hour():

    hours = [
        11,11,
        12,12,12,
        13,13,
        14,
        15,
        16,
        17,17,
        18,18,18,
        19,19,19,
        20,20,
        21
    ]

    return random.choice(hours)

def generate_party_size():

    sizes = (
        [1]*10 +
        [2]*35 +
        [3]*20 +
        [4]*20 +
        [5]*7 +
        [6]*5 +
        [7]*2 +
        [8]*1
    )

    return random.choice(sizes)

def calculate_large_party(party_size):
    if party_size < 6:
        return False
    else:
        return True
    

def generate_reservation():

    return random.random() < 0.35

#FRONT OF HOUSE STAFF ONLY

def calculate_foh_staff(hour, is_weekend):

    if hour in [18,19]:
        return random.randint(32,36)

    elif hour in [12,13]:
        return random.randint(28,32)

    elif is_weekend:
        return random.randint(28,34)

    else:
        return random.randint(22,28)

def calculate_tables_used(hour, is_weekend):

    if hour in [18,19]:

        tables_used = random.randint(42,47)

    elif hour in [12,13]:

        tables_used = random.randint(35,45)

    elif is_weekend:

        tables_used = random.randint(30,44)

    else:

        tables_used = random.randint(20,35)

    return tables_used

def calculate_actual_wait(
    party_size,
    tables_available,
    staff,
    is_weekend,
    hour
):

    wait = 10


    # Capacity pressure

    if tables_available <= 2:

        wait += 45


    elif tables_available <= 5:

        wait += 30


    elif tables_available <= 10:

        wait += 15



    # Larger parties take longer

    wait += party_size * 3

    #Dinner rush adds operational pressure
    if hour in [18,19,20]:
        wait += random.randint(5,15)

    # Weekends tend to have higher demand
    if is_weekend:
        wait += random.randint(3, 10)

    # More staff can reduce wait
    wait -= (staff - 20) * 0.7

    # Natural variation
    wait += random.randint(-8, 12)

    return max(5, round(wait))

def calculate_estimated_wait(
    party_size,
    tables_available,
    staff,
    is_weekend,
    hour
):

    estimated_wait = 10

    # Host sees available capacity
    if tables_available <= 2:
        estimated_wait += 40

    elif tables_available <= 5:
        estimated_wait += 25

    elif tables_available <= 10:
        estimated_wait += 15

    # Larger parties
    estimated_wait += party_size * 2

    # Dinner rush
    if hour in [18, 19, 20]:
        estimated_wait += 10

    # Weekend demand
    if is_weekend:
        estimated_wait += 5

    # Staffing
    estimated_wait -= (staff - 20) * 0.5

    # Host estimation is not perfect
    # This represents judgment/uncertainty
    estimated_wait += random.randint(-5, 10)

    return max(5, round(estimated_wait))


def calculate_wait_range(estimated_wait):


    if estimated_wait <= 15:

        return 5,15,"5-15 min"


    elif estimated_wait <= 30:

        return 15,30,"15-30 min"


    elif estimated_wait <= 45:

        return 30,45,"30-45 min"


    elif estimated_wait <= 60:

        return 45,60,"45-60 min"


    elif estimated_wait <= 75:

        return 60,75,"60-75 min"


    elif estimated_wait <= 90:

        return 75,90,"75-90 min"
    

    elif estimated_wait <= 105:
    
        return 90,105,"90-105 min"
    
    elif estimated_wait <= 120:
            
        return 105,120,"105-120 min"

    elif estimated_wait <= 135:

        return 120,135, "120-135 min"

    else:
        return 135,150, "135+ min"

def calculate_quote_accuracy(
    actual_wait,
    lower,
    upper
):

    if lower <= actual_wait <= upper:

        return True

    else:

        return False

def categorize_wait(actual_wait):

    if actual_wait <=15:
        return "5-15 min"

    elif actual_wait <=30:
        return "15-30 min"

    elif actual_wait <=45:
        return "30-45 min"

    elif actual_wait <=60:
        return "45-60 min"

    elif actual_wait <=75:
        return "60-75 min"

    elif actual_wait <=90:
        return "75-90 min"

    elif actual_wait <=105:
            return "90-105 min"

    elif actual_wait <=120:
            return "105-120 min"
    else:
        return "135+ min"

records = []

for party_id in range(1, NUMBER_OF_PARTIES + 1):


    date = generate_date()

    day = date.strftime("%A")


    is_weekend = day in [
        "Saturday",
        "Sunday"
    ]


    hour = generate_hour()


    party_size = generate_party_size()

    large_party = calculate_large_party(party_size)

    reservation = generate_reservation()


    staff = calculate_foh_staff(
        hour,
        is_weekend
    )


    tables_used = calculate_tables_used(
        hour,
        is_weekend
    )


    tables_available = (
        TABLE_CAPACITY -
        tables_used
    )


    occupancy_rate = round(
        tables_used / TABLE_CAPACITY,
        2
    )


    actual_wait = calculate_actual_wait(
        party_size,
        tables_available,
        staff,
        is_weekend,
        hour
    )

    estimated_wait = calculate_estimated_wait(party_size,
                                              tables_available,
                                              staff,
                                              is_weekend,
                                              hour)


    quote_lower, quote_upper, quote_range = calculate_wait_range(
        estimated_wait
    )


    quote_accuracy = calculate_quote_accuracy(
        actual_wait,
        quote_lower,
        quote_upper
    )


    wait_category = categorize_wait(
        actual_wait
    )


    records.append([

        party_id,
        date.date(),
        day,
        hour,
        is_weekend,

        party_size,
        large_party,
        reservation,

        staff,

        tables_used,
        tables_available,
        occupancy_rate,

        quote_lower,
        quote_upper,
        quote_range,

        actual_wait,

        wait_category,

        quote_accuracy

    ])


# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame(

    records,

    columns=[

        "party_id",
        "date",
        "day_of_week",
        "hour",
        "is_weekend",

        "party_size",
        "large_party",
        "reservation",

        "staff_on_shift",

        "tables_used",
        "tables_available",
        "occupancy_rate",

        "quoted_wait_lower",
        "quoted_wait_upper",
        "quoted_wait_range",

        "actual_wait",

        "wait_category",

        "quote_accuracy"

    ]

)

# -----------------------------
# Export CSV
# -----------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print(df.head())

print("\nAverage Wait Time:")
print(df["actual_wait"].mean())


print("\nQuote Accuracy:")
print(
    df["quote_accuracy"].mean()
)