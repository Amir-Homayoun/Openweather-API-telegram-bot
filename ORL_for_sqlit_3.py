import sqlite3

class ORL():
    def __init__(self, name, showing_successful_result__if_not_dont_give_any_thing=None):
        self.showing_successful_result = showing_successful_result__if_not_dont_give_any_thing
        self.database_name=name


    def create_table(self,table_name,parameters):
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        params=parameters.split(' ')
        try:
            create=f"""CREATE TABLE IF NOT EXISTS {table_name}({','.join(params)});"""
            print(create)
            cur.execute(create)
            con.commit()
            con.close()
            if type(self.showing_successful_result)!=type(None):
                print("\n------------Table created successfully------------")
            else:
                None
        except:
            print("\n------------Table didn't create------------")

    def insert(self,table_name,data_for_insert):
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        # making suitable data for inserting
        insert_data=[]
        for i in data_for_insert.split():
            insert_data.append(f"""'{i}'""")

        insert=f"""INSERT INTO {table_name} VALUES({','.join(insert_data)});"""
        print(insert)
        # try:
        cur.execute(insert)
        con.commit()
        con.close()
        if type(self.showing_successful_result) != type(None):
            print("\n------------Table inserted successfully------------")
        else:
            None
        # except:
        #     print("\n------------Data didn't insert------------")

    def select(self, table_name, select, print_output=None):
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()
        # making suitable data for selecting
        selected_data=[]
        for i in select.split():
            if i=='all':
                selected_data.append('*')
            else:
                selected_data.append(i)

        select=f"""SELECT {','.join(selected_data)} FROM {table_name}"""
        # try:
        y=[]
        cur.execute(select)
        if type(print_output) != type(None):
            records=cur.fetchall()
            for i in records:
                # print(i)
                y.append(i)
        return y

    def update(self,selected_setting ,change,chat_id):
        con = sqlite3.connect(self.database_name)
        cur = con.cursor()

        # main=f"DELETE FROM Users WHERE chat_id='{chat_id}';"
        # cur.execute(f"DELETE FROM Users WHERE chat_id='{chat_id}';")
        main = f"UPDATE Users SET {selected_setting} = '{change}' WHERE chat_id = '{chat_id}';"
        print(main)
        cur.execute(main)

        con.commit()
        con.close()
        #     if type(self.showing_successful_result) != type(None):
        #         print("\n------------Table selected successfully------------")
        #     else:
        #         None
        # except:
        #     print("\n------------Data didn't select------------")


# my_data=ORL('shop','yes')
# my_data.create_table('infoh','name age code')
# my_data.insert('infoh',"amir 14 20202020")
# x=my_data.select('infoh','name','yes')
# for i in x:
#     print(i)