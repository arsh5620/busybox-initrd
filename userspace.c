#include <stdio.h>
#include <unistd.h>

int main() {
  printf("Hello from userspace!\n");
  while (1) {
    sleep(1);
  }
}