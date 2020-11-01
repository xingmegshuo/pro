/*************************************************************************
	> File Name: day_moth.cpp
	> Author: 
	> Mail: 
	> Created Time: 2019年08月05日 星期一 17时51分30秒
 ************************************************************************/

#include<iostream>
 
using namespace std;

int main()
{
    //1997年7月份日历
    
    int day = 31;
    int dayOfweek = 2;

    cout << "一\t二\t三\t四\t五\t六\t日" << endl;
    for(int i = 0;i < dayOfweek -1;i++)
    {
        cout << "\t";
    }
    for(int i = 1;i <= day;i++)
    {
        cout << i;
        if((i+dayOfweek-1) % 7 == 0)
        {
            cout << "\n";
        }
        else
        {
            cout << "\t";    
        }
    }



    return 0;
}
