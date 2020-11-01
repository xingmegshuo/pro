/*************************************************************************
	> File Name: array_learn.cpp
	> Author: 
	> Mail: 
	> Created Time: 2019年08月05日 星期一 19时31分18秒
 ************************************************************************/

#include<iostream>
 
using namespace std;

int main()
{
    const int N = 5;
    int nums[N];
    for(int i = 0;i < N;i++)
    {
        cout << "请输入数组元素" << i;
        cin >> nums[i];
    }
    cout << nums;
    return 0;
}
