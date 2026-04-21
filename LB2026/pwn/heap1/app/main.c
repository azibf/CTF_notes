#include "stdlib.h"
#include "unistd.h"
#include "stdio.h"

typedef struct _accessor {
    char command[0x10];
    int can_access;
} accessor;

accessor* manager;

void create_accessor() {
    manager = (accessor*)malloc(sizeof(accessor));
    if (!manager) exit(1);

    manager->can_access = 0;

    printf("Command: ");
    read(0, manager->command, sizeof(manager->command));

    printf("Success\n");
}

void free_manager() {
    if (manager) free(manager);
}

void add_user() {
    unsigned int size;

    printf("Size: ");
    if (scanf("%u", &size) != 1) exit(2);

    void* name = malloc(size);
    if (!name) exit(3);

    printf("Name: ");
    read(0, name, size - 1);
}

void execute() {
    if (manager->can_access) system(manager->command); 
}

void menu() {
    printf("1. Add accessor\n");
    printf("2. Delete accessor\n");
    printf("3. Add user\n");
    printf("4. Execute\n");
}

int main() {
    menu();
    unsigned int choice;
    while (1) {
        printf("> ");
        if (scanf("%u", &choice) != 1) exit(2);
        switch (choice)
        {
        case 1:
            create_accessor();
            break;
        case 2:
            free_manager();
            break;
        case 3:
            add_user();
            break;
        case 4:
            execute();
            break;
        
        default:
            break;
        }
    }
}

__attribute__((constructor))
void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

