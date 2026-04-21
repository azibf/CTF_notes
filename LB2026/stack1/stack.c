#include <stdio.h>
#include <stdlib.h>

void win()
{
    system("/bin/sh");
}

int main()
{
    char username[256];
    char password[256];
    printf("Hallo man. Register for impact\n");
    printf("What is your name: ");
    scanf("%s", username);
    printf("Set your password: ");
    scanf("%s", password);
    printf("You are register with login: %s\n", username);
    printf("Haha, no impact\n");
}