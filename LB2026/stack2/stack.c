#include <stdio.h>
#include <stdlib.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win()
{
    system("/bin/sh");
}

int main()
{
    setup();
    char username[256];
    char password[256];
    printf("Hallo man. Register for impact\n");
    printf("What is your name: ");
    scanf("%255s", username);
    printf("You are register with login: ", username);
    printf(username);
    printf("\n");
    printf("Set your password: ");
    scanf("%s", password);

    printf("Haha, no impact\n");
}
