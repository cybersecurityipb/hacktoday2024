#include <iostream>
#include <cstring>

using namespace std;

void vuln(char *song){
    char tmp[10];
    cin >> tmp;
    throw runtime_error("who said you can do that?");
    strcpy(song, tmp);
    cout << "new song huh?" << endl;
    return;
}

int main() {
    try
    {
        while (true) {
            int choice = 0;
            char *songs[10];
            int option = 0;
            cout << "[1] new song\n[2] list song\n";
            cin >> choice;
            cout << "Enter song number: ";
            cin >> option;
            if(choice == 1){
                vuln(songs[option]);
            }
            else if(choice == 2){
                cout << (int *)songs[option] << endl;
            }
            else{
                cout << "Invalid choice" << endl;
            }
        }
    }
    catch(const std::exception& e)
    {
        cout << e.what() << std::endl;
    }
    return 0;   
}