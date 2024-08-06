#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char* MENU =    "[1]. read file\n"\
                "[2]. do the biopsi\n"\
                "[3]. do the test\n"\
                "[4]. exit";

char* DIAGNOSTIC[15] = {0};

void setup() __attribute__((constructor));
void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


int idx(int a){
    int idx;
    printf("(%d)> ", a);
    scanf("%d", &idx);
    if (idx < 0 || idx >14) return 0;
    return idx;
}

int getsz(){
    int val;
    puts("How big is it? ");
    scanf("%d", &val);
    getchar();
    return val;
}

void read_file(){
    int index = idx(1);
    if (DIAGNOSTIC[index] == NULL) return;
    printf("%s\n", DIAGNOSTIC[index]);
}

void biopsi(){
    int index = idx(2);
    int size = getsz();
    DIAGNOSTIC[index] = malloc(size);
    read(0,DIAGNOSTIC[index], size+1);
}

void test(){
    int index = idx(3);
    free(DIAGNOSTIC[index]);
    DIAGNOSTIC[index] = 0;
}

void die(){
    puts("oh no, patient is dead and it's your FAULT!!");
    exit(EXIT_FAILURE);
}

int main(){
    int choice;

    puts("House : Hi, we got a patient here");
    while (1){
        puts(MENU);
        printf("(_)> ");
        scanf("%d", &choice);
        
        switch(choice) { 
            case 1 : 
                read_file();
                break;
            case 2: 
                biopsi();
                break;
            case 3:
                test();
                break;
            case 4:
                die();
                break;
            default: 
                puts("please do your work! or you're fired.");
                break;
        }
    }
    return 0;
}