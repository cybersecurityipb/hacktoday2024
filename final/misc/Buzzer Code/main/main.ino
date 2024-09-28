
const int p1 = 12; //led
const int p2 = 8; // buzzer

const int d1 = 250;  
const int d2 = d1 * 3;
const int g1 = d1;
const int ls = d1 * 3;  
const int ws = d1 * 7;

void f1() {
    digitalWrite(p1, HIGH); delay(d1); digitalWrite(p1, LOW); delay(g1);
    tone(p2, 1000); delay(d2); noTone(p2); delay(g1);
}

void f2() {
    digitalWrite(p1, HIGH); delay(d2); digitalWrite(p1, LOW); delay(g1);
    tone(p2, 1000); delay(d1); noTone(p2); delay(g1);
}

void setup() {
    pinMode(p1, OUTPUT); pinMode(p2, OUTPUT);
}

void loop() {
    f2(); f1(); f1(); f1(); delay(ls); f1(); f1(); f2(); delay(ls); f2(); f2(); f1(); f1(); delay(ls); f1(); f1(); f1(); f2(); f2(); delay(ls); f1(); f2(); f1(); delay(ls); f2(); f1(); f2(); delay(ls);
    f2(); f2(); f2(); f2(); f2(); delay(ls); f2(); f1(); f2(); delay(ls); f2(); f1(); f1(); delay(ls); f1(); f1(); delay(ls); f2(); f1(); f2(); f2(); delay(ls); f1(); delay(ls); f1(); f2(); f1(); delay(ls); f2(); f1(); f2(); f1(); delay(ls); f1(); f1(); f1(); f1(); f2(); delay(ls);
    f2(); f1(); f2(); delay(ls); f1(); f1(); f1(); f1(); f2(); delay(ls);
    f2(); f1(); f1(); f2(); delay(ls);
    f1(); f2(); f2(); f2(); f2(); delay(ls); 
    f2(); f1(); f1(); f2(); delay(ls); 
    f1(); f2(); f2(); f2(); f2(); delay(ls); 
    f2(); f1(); f1(); f2(); delay(ls); 
    f1(); f2(); f2(); f2(); f2(); delay(ls);
    while (true) {
        // Do nothing, program berhenti
    }
}
