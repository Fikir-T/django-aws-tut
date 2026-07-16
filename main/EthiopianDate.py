def ethiocal(day, month, year):
    weekdays = ['ሰኞ', 'ማክሰኞ', 'ረቡዕ', 'ሐሙስ', 'ዓርብ', 'ቅዳሜ', 'እሑድ']
    julian = 1723856 + 365 * int(year) + (int(year) // 4) + 30 * int(month) + int(day) - 31
    weekday = julian % 7
    weekday_name = weekdays[weekday]
    return weekday_name

def gregorian_to_ethiopian(gday, gmonth, gyear):
    ETHIOPIAN_EPOCH_JDN = 1723856

    # Convert Gregorian date to Julian Day Number (JDN)
    a = (14 - gmonth) // 12
    y = gyear + 4800 - a
    m = gmonth + 12 * a - 3

    jdn = gday + ((153 * m + 2) // 5) + 365 * y + (y // 4) - (y // 100) + (y // 400) - 32045
    days_since_epoch = jdn - ETHIOPIAN_EPOCH_JDN
    four_year_cycles = days_since_epoch // 1461
    days_left = days_since_epoch % 1461

    eth_year = 4 * four_year_cycles + days_left // 365
    day_of_year = days_left % 365

    eth_month = day_of_year // 30 + 1
    eth_day = day_of_year % 30 + 1

    return eth_day, eth_month, eth_year

# print(gregorian_to_ethiopian(6, 6, 2025))
# print(ethiocal(29, 9, 2017))