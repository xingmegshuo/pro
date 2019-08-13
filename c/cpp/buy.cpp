/*************************************************************************
	> File Name: buy.cpp
	> Author: 
	> Mail: 
	> Created Time: 2019年08月05日 星期一 16时12分43秒
 ************************************************************************/

#include<iostream>
 
using namespace std;

int main()
{
    double prices_louis = 35123.0, prices_hemes = 11044.5 ,prices_chanel = 1535.0,total = 0;
    total = prices_louis+prices_hemes+prices_chanel;

    if(total >= 50000)
    {
        total *= 0.7;
    }
    else
    {
        total *= 0.9;    
    }
    cout << "最终付款: " << total << endl;
    return 0;
}
