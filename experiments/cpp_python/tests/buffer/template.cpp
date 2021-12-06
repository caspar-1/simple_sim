// C++ class template example

#include<iostream>

using namespace std;

 

// class template declaration part

template <class any_data_type>

class Test

{

public:

// constructor

Test();

// destructor

~Test();

// method

any_data_type Data(any_data_type);

};

 

template <class any_data_type>

any_data_type Test<any_data_type>::Data(any_data_type Var0)

{return Var0;}

 

// a class template definition part

// should be in the same header file with the class template declaration

// constructor

template <class any_data_type>

Test<any_data_type>::Test()

{cout<<"Constructor, allocate..."<<endl;}

 

// destructor

template <class any_data_type>

Test<any_data_type>::~Test()

{cout<<"Destructor, deallocate..."<<endl;}

 

// the main program

int main(void)

{

Test<int> Var1;

Test<double> Var2;

Test<char> Var3;

Test<char*> Var4;

 

cout<<"\nOne template fits all data type..."<<endl;

cout<<"Var1, int = "<<Var1.Data(100)<<endl;

cout<<"Var2, double = "<<Var2.Data(1.234)<<endl;

cout<<"Var3, char = "<<Var3.Data('K')<<endl;

cout<<"Var4, char* = "<<Var4.Data((char*)"The class template")<<endl<<endl;

return 0;

}