import numpy
import pandas as pd
pd.set_option('display.max_rows', None)

TRESHOLD = 10

male_names = pd.read_excel("database/meskie.xlsx", sheet_name="IMIONA_MĘSKIE")
female_names = pd.read_excel("database/zenskie.xlsx", sheet_name="IMIONA_KOBIET")
new_names = pd.read_csv("database/IMIONA_NADANE_DZIECIOM_W_POLSCE_W_I_POŁOWIE_2022_R._-_IMIĘ_PIERWSZE.csv")
new_names.dropna(inplace=True)
new_names['Gender'] = new_names['Płeć'].map({'M': 'male', 'K': 'female'})
del new_names['Płeć']
new_names.rename(columns={'Imię': 'Name', 'Liczba': 'Counts_2022'}, inplace=True)
new_names['Counts_2022'] = new_names['Counts_2022'].astype('int64')

# Kinga chce tylko mało popularne w zeszlym roku
#filter_newnames = new_names['Counts_2022'] < 100.
#new_names = new_names[filter_newnames]

#print(new_names)
print(new_names.info())

male_names['Gender'] = 'male'
female_names['Gender'] = 'female'
treshold = TRESHOLD

names = pd.concat([male_names, female_names])
filter_names = names['Liczba'] > treshold
#filter_gender = names['Gender'] == 'female' or 'male'
names = names[filter_names]

names.rename(columns={'IMIĘ 1': 'Name', 'Liczba': 'Counts'}, inplace=True)

names['Arek'] = 'Unknown'
names['Kinga'] = 'Unknown'
print(names.info())
#print(names)
"""
# print(new_names.head(3))
for ix in new_names.index:
    tmp = new_names.loc[ix]
    tmp_filter_name = names['Name'] == tmp['Imię']
    tmp_filter_gender = names['Gender'] == tmp['Płeć']
    # print(names[tmp_filter_name & tmp_filter_gender])
    print(names[tmp_filter_name & tmp_filter_gender])
    names[tmp_filter_name & tmp_filter_gender]['Counts_2022'] = 1
    #if numpy.isnan(tmp['Liczba']) == False:
    #    names[tmp_filter_name & tmp_filter_gender]['Counts_2022'] = int(tmp['Liczba'])
"""
#print(names)

out = pd.merge(names, new_names, on=['Name', 'Gender'], how='left', indicator=True)
out.fillna(0, inplace=True)
print(out.info())
del out['_merge']
# print(out.sort_values(by='Counts_2022', ascending=True))

#out.to_csv('names_01.csv', sep=',', index=False)
out.to_csv('names_95.csv', sep=',', index=False)
