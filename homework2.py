#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 08:15:12 2024

@author: shaiyaan
HOMEWORK NUMBER 2 NUID: 002144619
"""
import sys
sys.path.append("/Users/shaiyaan/Desktop/hw_data/neu")
import utils
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

FIlENAMES=[
           '/Users/shaiyaan/Desktop/hw_data/marathon_data/baa_results_2010.csv', 
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2011.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2012.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/baa_results_2013.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2014.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2015.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2016.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2017.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2018.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/2019_boston_marathon.csv', 
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2021.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2022.csv',
            '/Users/shaiyaan/Desktop/hw_data/marathon_data/boston_marathon_2023.csv',
            ]

def read_all_files(FILENAMES):
    all_data = []
    for file in FILENAMES:
        if "2019" in file:
            year = "2019"
        else:
            year = file.split('_')[-1].replace('.csv', '')
        data = utils.read_csv(file)
        headers = data[0]
        for rows in data[1:]:
            dct = {headers[i]: rows[i] for i in range(len(headers))}
            dct["Year"] = year 
            all_data.append(dct)
    return all_data

def convert_time_seconds(time_str):
    h, m, s = map(int, time_str.split(":"))
    seconds = h * 3600 + m * 60 + s
    return seconds

def convert_back_format(seconds):
    hours = int(seconds) // 3600 # divide the whole number
    remaining_seconds = int(seconds) % 3600 # whatever if left from those hours
    minutes = int(remaining_seconds) // 60 # lots of sdeconds left, fivide by 60 to getymiute form
    seconds = int(remaining_seconds) % 60 # remainder still so find the other seconds
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def mean2013(all_data):
    data2013 = [data for data in all_data if data["Year"] == "2013"]
    filter_time = [data["OfficialTime"] for data in data2013]
    convert_seconds = [convert_time_seconds(time) for time in filter_time]
    mean = sum(convert_seconds) // len(convert_seconds)
    regular_format = convert_back_format(mean)
    return regular_format

def median2010(all_data):
    year2010 = [data for data in all_data if data["Year"] == "2010"]
    all_age = [age["AgeOnRaceDay"] for age in year2010]
    clean_age = utils.str_to_num(all_age, int)
    median = utils.median(clean_age)
    return median

def notUSArunners2023(all_data):
    # so I gotta filter for only 2023, than pick our countryofresabbrev not us, and then count
    data2023 = [data for data in all_data if data["Year"] == "2023"]
    runners = [country["CountryOfResAbbrev"] for country in data2023 if country["CountryOfResAbbrev"] != "USA"]
    dct= {}
    max_count = 0
    max_country = ""
    for country in runners:
        if country in dct:
            dct[country] += 1
            if dct[country] > max_count:
                max_count = dct[country]
                max_country = country
        else:
            dct[country] = 1
    return max_country

def women2021(all_data):
    data2021 = [data for data in all_data if data["Year"] == "2021"]
    women = [data["Gender"] for data in data2021 if data["Gender"] == "F"]
    return len(women)

def correlation_women(all_data):
    dct = {}
    for data in all_data:
        if data["Gender"] == "F":
            yearly = data["Year"]
            time = data["OfficialTime"]
            if yearly not in dct:
                dct[yearly] = []
            dct[yearly].append(convert_time_seconds(time))
    mean_per_year = {year: sum(values) / len(values) for year, values in dct.items()}
    year = [int(key) for key in mean_per_year.keys()]
    mean = [values for values in mean_per_year.values()]
    r_value = stats.linregress(year, mean)
    return r_value

def meanAmericans(all_data):
    americans = [data for data in all_data if data["CountryOfResAbbrev"] == "USA"]
    finish_times_per_year = {}
    for data in americans:
        year = data["Year"]
        times = data["OfficialTime"]
        if year not in finish_times_per_year:
            finish_times_per_year[year] = []
        finish_times_per_year[year].append(convert_time_seconds(times))
    means_per_year = {year: sum(times)/ len(times) for year, times in finish_times_per_year.items()}
    years = [int(year) for year in means_per_year.keys()]
    means = [time for time in means_per_year.values()]
    sns.regplot(x=years, y=means) # plotting for first plot question
    plt.title("A linear regression plot between year and mean finish times of American runners in the top 1000.")
    plt.show()
    r_value = stats.linregress(years, means)
    return r_value

def predict2020(all_data):
    r_value = meanAmericans(all_data)
    slope = r_value.slope
    intercept = r_value.intercept
    predicted_mean = slope * 2020 + intercept
    return (convert_back_format(predicted_mean))

def normalized_median_age(all_data):
    yearly_avg = {}
    yearly_age = {}
    for data in all_data:
        year = data["Year"]
        time = data["OfficialTime"]
        age = data["AgeOnRaceDay"]
        if year not in yearly_avg:
            yearly_avg[year] = []
        if year not in yearly_age:
            yearly_age[year] = []
        yearly_avg[year].append(convert_time_seconds(time))                         
        yearly_age[year].append(int(age))
    means_per_year = {year: sum(time) / len(time) for year, time in yearly_avg.items()}
    median_age_per_year = {year: utils.median(age) for year, age in yearly_age.items()}
    years = [int(year) for year in means_per_year.keys()]
    mean = [time for time in means_per_year.values()]
    median = [median for median in median_age_per_year.values()]
    normal_mean = utils.normalize(mean)c
    normal_median = utils.normalize(median) 
    sns.lineplot(x=years, y=normal_mean, color='red', label='Normalized Mean Finish Time')
    sns.lineplot(x=years, y=normal_median, color='blue', label='Normalized Median Age')
    plt.show()
    
def main():
    all_data = read_all_files(FIlENAMES)
    problem1 = mean2013(all_data)
    print(f"The mean finish time for top 10000 runners in 2013 is {problem1}")
    problem2 = median2010(all_data)
    print(f"The median age for top 10000 runners in 2010 is {problem2}")
    problem3 = notUSArunners2023(all_data)
    print(f"The country with the most amount of runners in 2023 was {problem3}")
    problem4 = women2021(all_data)
    print(f"The amount of women that finished in the top 1000 in 2021 was {problem4}")
    problem5 = correlation_women(all_data)
    print(f"The values for women who ran overtime was {problem5}")
    problem6 = meanAmericans(all_data) # contains plot and other stats
    print(f"The values we found for runners that were american were {problem6}")
    problem7 = predict2020(all_data)
    print(f"The predicted tie for average finish time for men in 2020 is {problem7}")
    normalized_median_age(all_data)
if __name__ == "__main__":
    main()
  
    

