#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
  char buf[49];
  while (1) {
    printf("Slowly but...? ");
    fgets(buf+28, 21, stdin);
    if (!strncmp(buf+28, "surely", 6)) {
      puts("That's right, slowly but surely is key!");
      exit(0);
    } else {
      printf("No! What is slowly but ");
      printf(buf+28);
      printf("?? Try again!\n\n");
    }
  }
}

void affah_ini() {
  __asm__(
    ".intel_syntax noprefix;"
    ".att_syntax;"
  );
}

__attribute__((constructor))
void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}
