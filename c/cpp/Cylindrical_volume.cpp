/*************************************************************************
	> File Name: Cylindrical_volume.cpp
	> Author: 
	> Mail: 
	> Created Time: 2019年08月05日 星期一 14时27分03秒
 ************************************************************************/

#include<iostream>
#include<cmath>

using namespace std;
int main()
{
    const float PI = 3.14f; //定义一个float类型的常量
    float radius = 2.5f;
    float height = 90.0f;
    double volume = PI * pow(radius,2) * height;
    cout << "体积是:" << volume << endl;

    return 0;

}
