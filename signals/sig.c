#include<stdio.h>
#include<signal.h>
#include<unistd.h>

void sig_handler(int signo)
{
    printf("received signal %d\n", signo);
    if (signo == SIGQUIT) {
        signal(signo, SIG_DFL); // restore the default handler
        kill(getpid(),signo); // re-raise the signal
    }
}

int main(void)
{
  if (signal(SIGINT, sig_handler) == SIG_ERR)  printf("Can't catch SIGINT\n");   // Ctrl + C
  if (signal(SIGTERM, sig_handler) == SIG_ERR)  printf("Can't catch SIGTERM\n"); // Same as SIGINT but cannot be sent with Ctrl + C
  if (signal(SIGQUIT, sig_handler) == SIG_ERR)  printf("Can't catch SIGQUIT\n"); // Ctrl + \-
  if (signal(SIGABRT, sig_handler) == SIG_ERR)  printf("Can't catch SIGABRT\n"); // Same as SIGQUIT, but cannot be blocked but can be caught and not sent via keyboard
  if (signal(SIGHUP, sig_handler) == SIG_ERR)  printf("Can't catch SIGHUP\n");   
  if (signal(SIGKILL, sig_handler) == SIG_ERR)  printf("Can't catch SIGKILL\n"); // expected to fail
  if (signal(SIGSTOP, sig_handler) == SIG_ERR)  printf("Can't catch SIGSTOP\n"); // Ctrl + Z. expected to fail
  while(1) 
    sleep(1);
  return 0;
}
