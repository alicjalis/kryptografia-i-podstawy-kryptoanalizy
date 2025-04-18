#include <iostream>
#include <vector>

int gcd(int a, int b) {
    while( b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int gcd_multiple(const std::vector<int>& numbers) {
    int result = numbers[0];
    for (size_t i = 1; i < numbers.size(); i++) {
        result = gcd(result, numbers[i]);
    }
    return result;
}
int main() {

    while(true){
    int choice;
    std::cout << "Enter 1 for Euclidean Alogrithm \nEnter 2 for extension of Euclidean Algorithm\nEnter 3 to quit\n";
    std::cin >> choice;
        if(choice==1){
                int num1, num2;
                std::cout << "Enter integers: \n";
                std::cin >> num1 >> num2;
                std::cout<<"GCD of " << num1 << " and " << num2 << " is " << gcd(num1, num2) << "\n\n";
            continue;
        }
        if(choice==2){
            int n;
            std::cout << "Enter number of integers: \n";
            std::cin >> n;
            if (n < 2) {
                std::cout << "Please enter at least 2 numbers \n";
                return 1;
            }
            std::vector<int> numbers(n);
            std::cout << "Enter " << n << " positive integers \n";
            for(int i= 0; i < n; i++){
                std::cin >> numbers[i];
            }
            std::cout << "GCD of the given numbers is " << gcd_multiple(numbers) << "\n\n";
            continue;
        }
        if(choice==3){
            break;
        }
        else{
            std::cout<<"Wrong input\n";
            break;
        }
    }
    return 0;
}
