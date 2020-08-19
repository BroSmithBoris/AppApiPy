from Func import Insert
from Func import Del
from Func import Help
from Func import Save


def insert():
    dlg = Insert.InsertDialog()
    dlg.exec_()

def delete():
    dlg = Del.DeleteDialog()
    dlg.exec_()


def about(self):
    dlg = Help.AboutDialog()
    dlg.exec_()




