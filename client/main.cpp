#include <QtCore>
#include <QWidget>
#include <QApplication>
#include <QListWidget>
#include <QListWidgetItem>
#include <QIcon>
#include <QSplitter>
#include <QTextEdit>
#include <iostream>

#include "friend.h"

int main(int argc, char *argv[]) {
   FriendManager *friendManager = new FriendManager();

   QApplication app(argc, argv);

   QWidget *window = new QWidget();

   window->resize(500, 700);
   window->setWindowTitle("Akai");
   window->show();

   QSplitter *splitter = new QSplitter(window);

   QListWidget *list = new QListWidget();
   list->addItem(new QListWidgetItem(QIcon("example_user.png"), "Example User"));

   splitter->addWidget(list);
   splitter->addWidget(new QTextEdit());

   splitter->show();

   return app.exec();
}
