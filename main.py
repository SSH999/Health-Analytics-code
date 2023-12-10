import pandas as pd
import matplotlib.pyplot as plt

file_path = 'HealthApp_2k.log_structured.csv'
df = pd.read_csv(file_path, delimiter=',')

# Extract relevant information for analysis
step_entries = df[df['Content'].str.contains('getTodayTotalDetailSteps')]
lsc_entries = df[df['Component'].str.contains('Step_LSC')]
extsdm_entries = df[df['Component'].str.contains('Step_ExtSDM')]
heart_rate_entries = df[df['Component'].str.contains('HeartRateSensor')]
sleep_entries = df[df['Component'].str.contains('Sleep')]
sync_entries = df[df['Content'].str.contains('startSync')]
alarm_entries = df[df['Content'].str.contains('Alarm uploadStaticsToDB totalSteps')]

# Extract and convert step count to integers
step_entries['Step Count'] = step_entries['Content'].str.extract(r'##(\d+)').astype(int)

# Convert 'Time' to datetime using a custom format
step_entries['Time'] = pd.to_datetime(step_entries['Time'], format='%Y%m%d-%H:%M:%S:%f')
lsc_entries['Time'] = pd.to_datetime(lsc_entries['Time'], format='%Y%m%d-%H:%M:%S:%f')
extsdm_entries['Time'] = pd.to_datetime(extsdm_entries['Time'], format='%Y%m%d-%H:%M:%S:%f')
heart_rate_entries['Time'] = pd.to_datetime(heart_rate_entries['Time'], format='%Y%m%d-%H:%M:%S:%f')
sleep_entries['Time'] = pd.to_datetime(sleep_entries['Time'], format='%Y%m%d-%H:%M:%S:%f')
sync_entries['Time'] = pd.to_datetime(sync_entries['Time'], format='%Y%m%d-%H:%M:%S:%f')
alarm_entries['Time'] = pd.to_datetime(alarm_entries['Time'], format='%Y%m%d-%H:%M:%S:%f')

# Group by time and sum the step counts
daily_steps = step_entries.groupby(pd.Grouper(key='Time', freq='D')).sum().reset_index()

plt.figure(figsize=(10, 6))
plt.plot(daily_steps['Time'], daily_steps['Step Count'], marker='o')
plt.title('Daily Step Count')
plt.xlabel('Time')
plt.ylabel('Step Count')
plt.grid(True)
plt.show()


if not lsc_entries.empty:
    plt.figure(figsize=(10, 6))
    plt.plot(lsc_entries['Time'], lsc_entries['EventId'], marker='o')
    plt.title('Active Times (Step_LSC)')
    plt.xlabel('Time')
    plt.ylabel('EventId')
    plt.grid(True)
    plt.show()

if not extsdm_entries.empty:
    plt.figure(figsize=(10, 6))
    plt.plot(extsdm_entries['Time'], extsdm_entries['Content'].str.extract(r'totalCalories=(\d+)').astype(float), marker='o', label='Calories')
    plt.plot(extsdm_entries['Time'], extsdm_entries['Content'].str.extract(r'totalAltitude=(\d+)').astype(float), marker='o', label='Altitude')
    plt.title('Calories and Altitude (Step_ExtSDM)')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

if not heart_rate_entries.empty:
    plt.figure(figsize=(10, 6))
    plt.plot(heart_rate_entries['Time'], heart_rate_entries['Content'].str.extract(r'heartRate=(\d+)').astype(float), marker='o')
    plt.title('Heart Rate')
    plt.xlabel('Time')
    plt.ylabel('Heart Rate')
    plt.grid(True)
    plt.show()


if not sleep_entries.empty:
    sleep_entries['Duration'] = sleep_entries['Content'].str.extract(r'duration=(\d+)').astype(int)
    plt.figure(figsize=(10, 6))
    plt.plot(sleep_entries['Time'], sleep_entries['Duration'], marker='o')
    plt.title('Sleep Duration')
    plt.xlabel('Time')
    plt.ylabel('Duration (minutes)')
    plt.grid(True)
    plt.show()


if not sync_entries.empty:
    plt.figure(figsize=(10, 6))
    plt.scatter(sync_entries['Time'], sync_entries.index, marker='o', label='Sync Events')
    plt.title('Sync Events')
    plt.xlabel('Time')
    plt.ylabel('Event Index')
    plt.legend()
    plt.grid(True)
    plt.show()

plt.show()
