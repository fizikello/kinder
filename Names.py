import pandas as pd
import copy


class Names:

    def __init__(self, filename):

        self.filename = filename
        self.data_backup = pd.read_csv(self.filename)
        self.data = self.data_backup
        self.current_index = self.data.index.start

        print(f'init index: {self.data.index}')
        # ---------------------------------------
        self.filter_counts = None
        self.filter_gender = None
        self.filter_parent = None

        # --------------------------------------
        self.reset_indexes()
        #self.last_index = self.data.index.stop
        #self.first_index = self.data.index.start
        #self.step_index = self.data.index.step

        #self.current_index = self.first_index

        print(f'index: {self.data.index}')


    def query(self, condition, value):

        if condition == 'Gender' and (value == 'male' or value == 'female'):
            return self.data.query(condition + " == @value", inplace=True)
        elif (condition == 'Counts' or 'Counts_2022') and ('<' in value or '>' in value):
            threshold = value[1:]
            return self.data.query(condition + " " + value[0] + ' ' + threshold, inplace=True)
        elif (condition == 'Arek' or condition == 'Kinga') and (value == 'like' or value == 'dislike' or value == 'maybe' or value == 'Unknown'):
            return self.data.query(condition + " == @value", inplace=True)
        else:
            print('Exception')
            return None

    def refresh_database(self):
        self.data_backup = pd.read_csv(self.filename)
        self.data = self.data_backup

    def apply_filters(self):
        pass

    def get_database(self):
        print(type(self.filter))

        if isinstance(self.filter, type(None)):
            return self.data
        else:
            return self.data[self.filter]

    def set_filter(self, condition, value):

        if condition == 'Gender' and value == 'male' or value == 'female':
            self.filter_gender = self.data[condition] == value
        elif condition == 'Counts' and '>' in value:
            threshold = int(value[1:])
            self.filter_counts = self.data[condition] > threshold
        elif condition == 'Counts' and '<' in value:
            threshold = int(value[1:])
            self.filter_counts = self.data[condition] < threshold
        else:
            print('Exception')
            self.filter = None

    def update_filter(self):

        if not isinstance(self.filter_counts, type(None)) and not isinstance(self.filter_gender, type(None)):
            self.filter = self.filter_gender & self.filter_counts

    def update_data(self):
        # check whether the row exists
        pass

    def reset_indexes(self):
        self.last_index = self.data.index.stop
        self.first_index = self.data.index.start
        self.step_index = self.data.index.step
        self.current_index = self.first_index

    def reset_indexes_INT(self):
        self.last_index = self.data.index[-1]
        self.first_index = self.data.index[0]
        self.current_index = self.first_index

    def save_choices(self):

        test_save = pd.merge(self.data_backup, self.data, on=['Name', 'Gender'], how='left', indicator=True)
        test_save["Arek"] = test_save["Arek_y"].fillna(test_save["Arek_x"])
        test_save["Kinga"] = test_save["Kinga_y"].fillna(test_save["Kinga_x"])
        test_save.drop(['Counts_y', 'Arek_y', 'Kinga_y', 'Counts_2022_y', '_merge', 'Arek_x', 'Kinga_x'], axis=1, inplace=True)
        test_save.rename(columns={'Counts_x': 'Counts', 'Counts_2022_x': 'Counts_2022'}, inplace=True)

        print(f'saving... {self.filename}')
        test_save.to_csv(self.filename, sep=',', index=False)

        self.refresh_database()



        """
        test_counter = 0
        for index, row in self.data.iterrows():
            print(row)
            print(self.data_backup[self.data_backup["Name"] == row['Name']])
            new_ix = self.data_backup[self.data_backup["Name"] == row["Name"]].index
            print(f'index = {self.data_backup[self.data_backup["Name"] == row["Name"]].index}')
            self.data_backup.loc[new_ix, 'Arek'] = row['Arek']
            print(self.data_backup[self.data_backup["Name"] == row['Name']])
        """


        # porównaj z backupem
        # zapisz do głównego pliku z wynikami

    def common_choice(self):
        self.data = self.data_backup
        filter_1 = self.data['Arek'] == 'like'
        filter_2 = self.data['Kinga'] == 'like'
        self.data = self.data[filter_1 & filter_2]
