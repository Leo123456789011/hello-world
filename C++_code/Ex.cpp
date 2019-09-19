#include <iostream>
#include <vector>
#include <typeinfo>
#include "math.h"

//using namespace std;

// stack overflow function
// float i = 2;

// float foo(){    
//     i = pow(i,1.5);
//     if (i > 0){
//     cout << i << endl;
//     return foo();}
// }

double NormalizeAngle(const double angle) { 
  double a = fmod(angle + M_PI, 2.0 * M_PI); //fmod(x,y),computes the floating-point remainder of the division operation x/y
  if (a < 0.0) {
    a += (2.0 * M_PI);
  }
  return a - M_PI;
}

int main(){
    
// vector<float> vec;
// //std::cout << 5 + 10 * 20 /2 << std::endl;
// for (int i = 1; i <= 500 ; i ++)
//     vec.push_back(i);

// cout << *( vec.begin() + 1 ) << endl;
// cout << *( vec.end()-1 ) << endl;
// cout << typeid(*vec.begin()).name() << endl;

// Test a int is even or odd:
// int test;
// cout << "Input a int: " << endl;
// cin >>  test;
// if(test%2 == 0){
//  cout << "Is even" << endl;
// }else if(test%2 == 1){
//     cout << "Is odd" << endl;
// }

// What is stack overflow?
//cout << foo();

// && || ==
// double a = 0;
// double b = 1;
// double c = 0;
//  if ( a == c || b == c ){
// std::cout << "a == c || b == c" << std::endl;
// } 
// if (a == 0 && c == 0){
//     std::cout << "a == 0 && c == 0" << std::endl;
// }


//const char *cp = "Hello_World";
// char* const cp = "Hello_World";

// std::cout << *cp << std::endl;

// cp = "A";

// std::cout << *cp << std::endl;

//if(cp && *cp){
//   std::cout << "true" << std::endl;
//}

// int in;

// while(std::cin >> in && in != 42)

//     std::cout << in << std::endl;

// }

// int a[4] = {};

// for(int i = 0; i <= 4; i++){

//     while(std::cin >> a[i]);
//     std::cout << a[i] << std::endl; 
// }

// double b[4];
// for(int i = 0; i <= 3; i++){
//     std::cin >> b[i];
//     //std::cout << "b[i]: " << b[i] << std::endl;
//     //std::cout << "i: " << i << std::endl;
// }


// for(int i = 0; i <= 4; i++){
//     std::cout << "b" << "["<< i << "]: " << b[i] << std::endl;
// }
// int i = 0;
// int j = 2;
// int k = 3;

// std::cout << (i!=j<k) << std::endl;

// int i;
// if( i = 0){
//     std::cout << "Flag" << std::endl;
// }
// #include <vector>

// vector<int> g1; 
  
//     for (int i = 1; i <= 5; i++) 
//         g1.push_back(i); 
    
//     for (int i = 0; i <= 4; i++){
//         g1[i]%2 == 1 ? (g1[i]*=2):(NULL); 
//         std::cout << g1[i] << std::endl;    
//         }


// char ch = 'e';

// switch (ch){

//     case 'a':
//         std::cout << "a" << std::endl;
//         break;
//     case 'b':
//         std::cout << "b" << std::endl;
//         break;
//     case 'c':
//         std::cout << "c" << std::endl;
//         break;
//     default:
//         std::cout << "default" << std::endl;
//         break;
// }

// float grade;
// std::cout << "Please input the grade: " << std::endl;
// std::cin >> grade;
// if (grade < 0){
//     std::cout << "Not valid input !" << std::endl;
//     return 0;
//     }

// if (grade < 60)
//     std::cout << "You are failed, haha!!" << std::endl;
// else if (grade >= 60 && grade <70)
//     std::cout << "pass" << std::endl;
// else if (grade >= 70 && grade < 80)
//     std::cout << "C" << std::endl;
// else if (grade >= 80 && grade < 90)
//     std::cout << "B" << std::endl;
// else if (grade >= 90 && grade <= 100)
//     std::cout << "A" << std::endl;
// else
//     std::cout << "Not valid input !" << std::endl;
// return 0;

double a;
std::cin >> a;

std::cout << NormalizeAngle(a) << std::endl;


}

