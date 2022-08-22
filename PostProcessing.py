import io
import os
import pandas
import pandas as pd
import Constants

old_motor = False
semtech = False


def post_process_tap(filename2):
    df = process_tap_event(filename2)
    if df.empty == False:
        tmp = os.path.splitext(filename2)[-2].split('_')
        tmp[-1] = 'processed.csv'
        tmp = '_'.join(tmp)
        df.to_csv(tmp, index=False)


def post_process_swipe(filename2):
    df = process_swipe_event(filename2)
    if df.empty == False:
        tmp = os.path.splitext(filename2)[-2].split('_')
        tmp[-1] = 'processed.csv'
        tmp = '_'.join(tmp)
        df.to_csv(tmp, index=False)


def post_process_linearity_jitter(filename2):
    df = preprocess_format(filename2, True)

    df['date_time'] = pd.to_datetime(df['date_time'])
    df.set_index('date_time', inplace=True)
    cols = ['x', 'y', 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    df = df[cols]
    df = df.rename(columns={17: 'Slider reported position',
                            19: 'Slider base1', 20: 'Slider instant1',
                            21: 'Slider base2', 22: 'Slider instant2',
                            23: 'Slider base3', 24: 'Slider instant3',
                            25: 'Slider base4', 26: 'Slider instant4',
                            27: 'CaptureBtn base', 28: 'CaptureBtn instant',
                            29: 'FaceProx base', 30: 'FaceProx instant'})
    tmp = os.path.splitext(filename2)[-2].split('_')
    tmp[-1] = 'processed.csv'
    tmp = '_'.join(tmp)
    df.to_csv(tmp)
    return df


def post_process_noise_full_scan_x_hover(filename2):
    df = preprocess_format(filename2, False)

    df['date_time'] = pd.to_datetime(df['date_time'])
    df.set_index('date_time', inplace=True)
    cols = ['x', 'y', 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    df = df[cols]
    df = df.rename(columns={17: 'Slider reported position',
                            19: 'Slider base1', 20: 'Slider instant1',
                            21: 'Slider base2', 22: 'Slider instant2',
                            23: 'Slider base3', 24: 'Slider instant3',
                            25: 'Slider base4', 26: 'Slider instant4',
                            27: 'CaptureBtn base', 28: 'CaptureBtn instant',
                            29: 'FaceProx base', 30: 'FaceProx instant'})
    tmp = os.path.splitext(filename2)[-2].split('_')
    tmp[-1] = 'processed.csv'
    tmp = '_'.join(tmp)
    df.to_csv(tmp)

    return df


def preprocess_format(filename, is_jitter_linearity):
    with open(filename, 'r') as f:
        lines = f.readlines()
    str_data = ''
    tmp = io.StringIO(str_data)
    count = 0;
    for line in lines:
        if "motor position" in line:
            x = line.split(',')[1]
            y = line.split(',')[2].strip()
        elif '[trace  ] {CAPT}: module_captouch.c' in line:
            # if this is noise/full scan/arbitary x-hover measurements, only read first NUM_OF_SAMPLES_PER_MEASUREMENT lines
            if (is_jitter_linearity == False):
                if (count < Constants.NUM_OF_SAMPLES_PER_MEASUREMENT_NOISE_FULL_SCAN + 1):
                    tmp.write(line.strip() + ', Pos ' + x + ' ' + y + '\n')
                    count = count + 1
                else:
                    # reset the counter and read next batch
                    count = 0
            # else this is jitter linearity measurements, read all lines.
            else:
                tmp.write(line.strip() + ', Pos ' + x + ' ' + y + '\n')
    # str_data = io.StringIO(str_data)
    tmp.seek(0)
    df = pd.read_csv(tmp, sep=',', header=None)
    # df = pd.read_csv(filename,skiprows=[0,1],sep=',',header=None)

    df0 = df[0].str.split(expand=True)
    df0_time_slider = df0[[1, 17, 19, 20, 21, 22, 23, 24, 25, 26]]
    df0_time_slider[1] = '2022-' + df0.iloc[:, 0] + ' ' + df0.iloc[:, 1]

    df1 = df[1].str.split(expand=True)
    df1_btn = df1[[2, 3]]
    df1_btn = df1_btn.rename({2: 27, 3: 28}, axis=1)

    df2 = df[2].str.split(expand=True)
    df2_face = df2[[2, 3]]
    df2_face = df2_face.rename({2: 29, 3: 30}, axis=1)

    df3 = df[3].str.split(expand=True)
    df3_coordinates = df3[[1, 2]]
    df3_coordinates = df3_coordinates.rename({1: 'x', 2: 'y'}, axis=1)

    df = pd.concat([df3_coordinates, df0_time_slider, df1_btn, df2_face], axis=1)
    df = df.replace(',', '', regex=True)
    df = df.rename(columns={1: 'date_time'}, errors="raise")
    df = df.dropna()
    return df


def process_tap_event(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    str_data = ''
    tmp = io.StringIO(str_data)
    for line in lines:
        if "motor position" in line:
            x = line.split(',')[1]
            y = line.split(',')[2].strip()
        elif "motor tap" in line:
            count = line.split(',')[1].strip()
        elif 'reporting tap event:' in line:
            tmp.write(line.strip() + ', Pos ' + x + ' ' + y + ', Motor Tapped ' + count + '\n')

    if tmp.tell() == 0:
        print("No tap is detected by system!")
        return pandas.DataFrame()

    tmp.seek(0)
    df = pd.read_csv(tmp, sep=',', header=None)

    df0 = df[0].str.split(expand=True)
    df0_time = '2022-' + df0.iloc[:, 0] + ' ' + df0.iloc[:, 1]
    df0_status = df0[[18]]
    df0_status = df0_status.rename({18: 'event'}, axis=1)

    df1 = df[1].str.split(expand=True)
    df1_coordinates = df1[[1, 2]]
    df1_coordinates = df1_coordinates.rename({1: 'x', 2: 'y'}, axis=1)

    df2 = df[2].str.split(expand=True)
    df2_tap = df2[[2]]
    df2_tap = df2_tap.rename({2: 'tap_count'}, axis=1)

    df = pd.concat([df0_time, df1_coordinates, df0_status, df2_tap], axis=1)
    df = df.rename(columns={0: 'date_time'}, errors="raise")
    df = df.dropna()
    return df


def process_swipe_event(filename):
    if 'Swipe_Forward' in filename:
        direction = 0
    else:
        direction = 1
    with open(filename, 'r') as f:
        lines = f.readlines()
    str_data = ''
    tmp = io.StringIO(str_data)
    for line in lines:
        if "motor position" in line:
            x = line.split(',')[1]
            y = line.split(',')[2].strip()
        elif "motor swipe" in line:
            swipe_count = line.split(',')[1].strip()
        elif ('Captouch: New gesture detected: gesture=SWIPE_FORWARD' in line and direction == 0) or (
                'Captouch: New gesture detected: gesture=SLIDE_FORWARD' in line and direction == 0):
            tmp.write(line.strip() + ', Pos ' + x + ' ' + y + ', Motor Swiped ' + swipe_count + '\n')
        elif ('Captouch: New gesture detected: gesture=SWIPE_BACKWARD' in line and direction == 1) or (
                'Captouch: New gesture detected: gesture=SLIDE_BACKWARD' in line and direction == 1):
            tmp.write(line.strip() + ', Pos ' + x + ' ' + y + ', Motor Swiped ' + swipe_count + '\n')

    if tmp.tell() == 0:
        print("No swipe is detected by system!")
        return pandas.DataFrame()

    tmp.seek(0)
    df = pd.read_csv(tmp, sep=',', header=None)

    df0 = df[0].str.split(expand=True)
    df0_time = '2022-' + df0.iloc[:, 0] + ' ' + df0.iloc[:, 1]
    df0_status = df0[[19]]
    df0_status = df0_status.rename({19: 'gesture'}, axis=1)

    df1 = df[1].str.split(expand=True)
    df1_coordinates = df1[[1, 2]]
    df1_coordinates = df1_coordinates.rename({1: 'x', 2: 'y'}, axis=1)

    df2 = df[2].str.split(expand=True)
    df2_tap = df2[[2]]
    df2_tap = df2_tap.rename({2: 'swipe_count'}, axis=1)

    df = pd.concat([df0_time, df1_coordinates, df0_status, df2_tap], axis=1)
    df = df.rename(columns={0: 'date_time'}, errors="raise")
    df = df.dropna()
    return df


if __name__ == '__main__':
    sensor_data_filename = 'C:/Users/wenhaochen/Documents/GitHub/Stella_Captouch_Test_System/data/Swipe_Forward_Measurement_2022-05-31_18-48-37_raw.txt'
    result = post_process_swipe(sensor_data_filename)
    print(result)
