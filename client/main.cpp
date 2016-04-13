#include "friend.h"
#include "ui.h"

int main(int argc, char *argv[]) {
   FriendManager *friendManager = new FriendManager();

   UI *ui = new UI(argc, argv, friendManager);
   ui->exec();

   return 0;
}
