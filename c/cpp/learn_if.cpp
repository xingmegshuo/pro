/*************************************************************************
	> File Name: learn_if.cpp
	> Author: 
	> Mail: 
	> Created Time: 2019年08月05日 星期一 16时06分23秒
 ************************************************************************/

#include<iostream>
 
using namespace std;

int main()
{
    char pan = '\0';//设置空字符
    cout << "请输入一个字符，我来判断:";
    cin >> pan;
    // A~Z
    if(pan >= 'A' && pan <= 'Z' )
    {
        cout << "是合法的" << endl;
    }
    else
    {
        cout << "非法" << endl;    
    }

}
