#include <iostream>
#include <string>
#include <cmath>
using namespace std;

int main() {
    string data;

    cout << "Enter 4 bit binary data: ";
    cin >> data;

    if (data.size() != 4) {
        cout << "Invalid input. Enter exactly 4 bits." << endl;
        return 0;
    }

    for (int i = 0; i < 4; i++) {
        if (data[i] != '0' && data[i] != '1') {
            cout << "Invalid input. Only 0 and 1 are allowed." << endl;
            return 0;
        }
    }

    int m = data.size();
    int r = 0;

    while (pow(2, r) < (m + r + 1)) {
        r++;
    }

    cout << "Data Bits:" << data << endl;
    cout << "Number of Parity bits:" << r << endl;

    char hamming[8];

    hamming[1] = 'P';
    hamming[2] = 'P';
    hamming[3] = data[3];
    hamming[4] = 'P';
    hamming[5] = data[2];
    hamming[6] = data[1];
    hamming[7] = data[0];

    cout << "\nHamming code positions:" << endl;

    for (int i = 1; i <= 7; i++) {
        cout << "Position " << i << ": " << hamming[i] << endl;
    }

    for (int p = 1; p <= 4; p = p * 2) {
        int parity = 0;

        cout << "P" << p << " checks positions: ";

        for (int i = 1; i <= 7; i++) {
            int temp = i;
            int bit = p;

            while (bit > 1) {
                temp = temp / 2;
                bit = bit / 2;
            }

            if (temp % 2 == 1) {
                cout << i << " ";

                if (i != p) {
                    parity = parity ^ (hamming[i] - '0');
                }
            }
        }

        hamming[p] = parity + '0';
        cout << "-> P" << p << " = " << hamming[p] << endl;
    }

    cout << "\nParity Bits:" << endl;
    cout << "P1 = " << hamming[1] << endl;
    cout << "P2 = " << hamming[2] << endl;
    cout << "P3 = " << hamming[4] << endl;

    cout << "\nFinal Hamming Code: ";

    for (int i = 1; i <= 7; i++) {
        cout << hamming[i];
    }

    cout << endl;

    return 0;
}
