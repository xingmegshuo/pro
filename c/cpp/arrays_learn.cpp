/*************************************************************************
	> File Name: arrays_learn.cpp
	> Author: 
	> Mail: 
	> Created Time: 2019年11月19日 星期二 12时06分42秒
 ************************************************************************/

#include<iostream>
 
using namespace std;


int main()
{
    //使用二维数组
    string stu_names[] {"刘备","关羽","张飞"};
    srring course_names[] {"语文","数学","英语"};
    const int ROW = 3;
    const int COL = 3;
    double scores[ROW][COL];
    for(int i = 0; i < ROW; i++){
        for(int j = 0; j < COL; j++){
            cout << stu_names[i] << "的" << course_names[j] << "成绩: ";
            cin >> scores[i][j];
        }
    }


}
