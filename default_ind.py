import pandas as pd
import time

merged_df = pd.read_pickle("data_unprocessed.pkl")

i = 0
ind = 0

start_time = time.time()
first_time = start_time

nr_rows = merged_df.shape[0]
prev_id = merged_df.loc[0]['LoanSequenceNumber']

status = []
DefaultInds = []
MaxDef = []

while i < nr_rows:
    current_id = merged_df.loc[i]['LoanSequenceNumber']
    current_status = merged_df.loc[i]['CurrentLonDeliquencyStatus']

    if i % 100000 == 0:
        print (f"i = {i}, curr_id = {current_id}, zajelo = {time.time() - start_time}")
        start_time = time.time()

    if current_id != prev_id:
        m = max(status)
        MaxDef.extend([m] * len(status))

        if m == 1: #prepaid
            ind = 1
        elif m >= 3: #default
            ind = 0
        else: #non-default - paid
            ind = 2

        DefaultInds.extend([ind] * len(status))
        status = []

    
    status.append(current_status)

    i += 1
    prev_id = current_id

m = max(status)
MaxDef.extend([m] * len(status))
DefaultInds.extend([ind] * len(status))
    
print("Przypisuje MaxDefault:")
start_time = time.time()
merged_df['MaxDefault'] = MaxDef
print (f"zajelo = {time.time() - start_time}")

print("Przypisuje DefaultInd:")
start_time = time.time()
merged_df['DefaultInd'] = DefaultInds
print (f"zajelo = {time.time() - start_time}")

print("Zapisuje...")
start_time = time.time()
merged_df.to_csv(r'data_default_ind.csv')
print("Zapisano")
print (f"zajelo = {time.time() - start_time}")
print (f"wszystko zajelo = {time.time() - first_time}")