#include <QtCore>
#include <QWidget>
#include <QApplication>
#include <QListWidget>
#include <QListWidgetItem>
#include <QIcon>
#include <iostream>

int main(int argc, char *argv[]) {
   QApplication app(argc, argv);

   QWidget window;

   window.resize(250, 150);
   window.setWindowTitle("Akai");
   window.show();

   QListWidget *list = new QListWidget();
   list->addItem(new QListWidgetItem(QIcon("example_user.png"), "Example User"));
   list->show();

   return app.exec();
}
