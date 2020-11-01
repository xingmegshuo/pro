/*************************************************************************
	> File Name: diamond.cpp
	> Author: 
	> Mail: 
	> Created Time: 2019年08月05日 星期一 18时30分10秒
 ************************************************************************/

#include<iostream>
 
using namespace std;

int main()
{
    int n;
    cout << "输入菱形大小:" << endl;
    cin >>n;

    for(int i = 1;i <= n;++i)
    {
        for(int j = 1;j <= n - i;++j)
        {
            cout << " ";
        }
        for(int j = 1;j <= 2*i;++j)
        {
            cout << "*";
        }
        cout << endl;
    }
    for(int i = n;i >= 1;--i)
    {
        for(int j = 1;j <= n - i;++j)
        {
            cout << " ";
        }
        for(int j = 1;j <= 2*i;++j)
        {
            cout << "*";
        }
        cout << endl;
    }



    return 0;
}
