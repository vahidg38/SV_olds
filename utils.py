import scipy.io as sio
from math import ceil
from statistics import mean, stdev
import pandas as pd
import numpy as np


def fault_generation(df_real, type='bias', sensor='PM25', magnitude=0, start=0, stop=100):
    if (start < 0) or (stop > len(df_real)) or (start == stop):
        raise Exception("Inappropriate boundries.")
    # faulty = df_real[sensor].values
    faulty = []
    pos = 0  # position of the sensor in the dataframe
    if sensor == 'PM25':
        faulty = df_real.PM25.values
        pos = 0
    elif sensor == 'PM10':
        faulty = df_real.PM10.values
        pos = 1
    elif sensor == 'CO2':
        faulty = df_real.CO2.values
        pos = 2
    elif sensor == 'Temp':
        faulty = df_real.Temp.values
        pos = 3
    elif sensor == 'Humidity':
        faulty = df_real.Humidity.values
        pos = 4
    else:
        raise Exception("Inappropriate sensor name.")

    if (type == 'Bias'):
        for i in range(start, stop):
            faulty[i] += magnitude

    elif (type == 'Complete_failure'):
        for i in range(start, stop):
            faulty[i] = magnitude

    elif (type == 'Drift'):
        m1 = mean(df_real[sensor])
        s1 = stdev(df_real[sensor])

        m2 = m1 + magnitude
        s2 = s1 + magnitude

        for i in range(start, stop):
            faulty[i] = m2 + (faulty[i] - m1) * (s2 / s1)

    elif (type == 'Degradation'):
        mu, sigma = 0, 0.1
        noise = np.random.normal(mu, sigma, [stop - start, ])
        faulty += magnitude * noise

    else:
        raise Exception("Inappropriate failure type.")
    df_real.drop(sensor, axis=1, inplace=True)
    # df_real[sensor] = faulty
    df_real.insert(pos, sensor, faulty, True)
    return df_real


# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix
    return matrix, norm


def de_normalize_2d(matrix, norm):
    matrix = matrix * norm  # denormalized matrix
    return matrix

def data_loading(mat_file='IAQ_2month_Vah.mat', train_test_ratio=4):
    d = sio.loadmat(mat_file)
    d = d["Platfrom_C"]

    #d, norm = normalize_2d(d)

    train_data = []
    test_data = []



    for i in range(d.shape[0]):
        if i% (train_test_ratio+1)==0:
         test_data.append(d[i])
        else:
         train_data.append(d[i])


    return train_data, test_data

def create_dataframe(data):

    sensors = ['PM25', 'PM10', 'CO2', 'Temp', 'Humidity']
    data = pd.DataFrame(data, columns=sensors)
    return data
