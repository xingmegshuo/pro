import pymysql
from tool import MySQL


conn = pymysql.connect(host='localhost',user='root',passwd='528012',db='data_value')
cursor = conn.cursor()

my_sql = MySQL()


def get_value(table):
    my_sql.query('''select * from {}'''.format(table))
    my_sql.commit()
    data = my_sql.show() 
    return data


def deal_data(a,b,c):
    new_data = []
    for i in range(0,len(a)):
        new_data.append([a[i],b[i],c[i]])
    return new_data



def insert_value(content): 
    count = 1
    for i in content:
        # cursor.execute('''insert into a(id,content) value({},'{}')'''.format(count,i[0][1]))
        cursor.execute('''insert into b(id,content,A) value({},'{}',{})'''.format(count,i[1][1],count))
        cursor.execute('''insert into c(id,content,B) value({},'{}',{})'''.format(count,i[2][1],count))

        conn.commit()
        count += 1



if __name__ =='__main__':
    a_data = get_value('a')
    b_data = get_value('b')
    c_data = get_value('c')
    # print(a_data,b_data,c_data)
    content = deal_data(a_data,b_data,c_data)
    print(content)
    insert_value(content)