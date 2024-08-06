#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

// gcc examination.c -o examination

static const uint64_t TIME_OPTION[] = {1, 5, 10, 15, 30, 60};

void alarm_handler(){ printf("\nOver oVer ovEr oveR\n"); }
void setup() __attribute__((constructor));
void setup() {
    struct sigaction sa;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    sa.sa_flags = 0;
    sa.sa_sigaction = &alarm_handler;
    if (sigaction(SIGALRM, &sa, NULL) < 0)
    {
        perror("sigaction");
        exit(EXIT_FAILURE);
    }
}

int do_teacher(){ 
    int32_t choice;
    int32_t seconds;
    struct sigevent sev;
    struct itimerspec its;
    static timer_t tmid;

    printf("please set the timer\n[1]. 1\t[2]. 5\t[3]. 10\t[4]. 15\t[5]. 30\t[6]. 60\n>> ");
    scanf("%d", &choice);
    printf("timer is set to %lu seconds\n", TIME_OPTION[choice - 1]);

    seconds = TIME_OPTION[choice - 1];

    sev.sigev_notify = SIGEV_SIGNAL;
    sev.sigev_signo = SIGALRM;

    if (timer_create(CLOCK_REALTIME, &sev, &tmid) < 0)
    {
        perror("timer_create");
        return 1;
    }

    its.it_value.tv_sec = seconds;
    its.it_value.tv_nsec = 0;
    its.it_interval.tv_sec = 0;
    its.it_interval.tv_nsec = 0;

    if (timer_settime(tmid, 0, &its, NULL) < 0)
    {
        perror("timer_settime");
        return 1;
    }

    return 0;
}

int do_student(){ 
    char buf[4096] = {0};
    int32_t read_bytes;
    uint32_t amnt;

    printf("length ? ");
    scanf("%d", &amnt);
    if (amnt >= sizeof(buf)) amnt = 4096;
    read_bytes = 0;

    printf("start reading your %d chars answer XD\n\n", amnt);

    do
    {
        read_bytes += read(0, buf + read_bytes, amnt - read_bytes);
    } while (read_bytes != amnt);

    printf("Well goodluck\n");  
    return 0;
}

int main() {
    int32_t choice;

    while (1){
        printf("Exam eXam exAm exaM\n[1]. as teacher\n[2]. as student\n>> ");
        scanf("%d", &choice);

        if (choice == 1) do_teacher();
        else if (choice == 2) do_student();
        else exit(EXIT_FAILURE);
    }
    return 0;
}
