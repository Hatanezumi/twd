import os
import sys
import configparser
try:
    from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QTextEdit
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QColor,QIcon, QTextCursor
    import sqlite3
    import twd
except Exception as err:
    import tkinter.messagebox
    tkinter.messagebox.showerror('严重错误','无法导入模块,请检查文件完整性!\n{}'.format(err))
    sys.exit(0)
class MainWindow():#主窗口
    def __init__(self):
        self.ui=QUiLoader().load('ui/main.ui')
        #事件连接
        self.process=Process(self.ui)
        self.ui.main_textedit.textChanged.connect(self.process.text_changed)
        self.ui.action_new.triggered.connect(self.process.new_file)
        self.ui.action_open.triggered.connect(self.process.open_file)
        self.ui.action_save.triggered.connect(self.process.save_file)
        self.ui.action_saveas.triggered.connect(self.process.saveas_file)
        self.ui.action_set.triggered.connect(self.process.set)
        self.ui.action_close.triggered.connect(self.process.close)
        self.ui.action_exit.triggered.connect(self.process.exit)
        self.ui.action_twd_text.triggered.connect(self.process.twd_text)
        self.ui.action_text_twd.triggered.connect(self.process.text_twd)
        self.ui.action_search.triggered.connect(self.process.search)
class PasswordWindow():#密码窗口
    def __init__(self):
        self.ui=QUiLoader().load('ui/password.ui')
    def connect(self,func):
        #连接特定处理函数
        self.ui.pushButton.clicked.connect(func)
    def set_title(self,title):
        #自定义标题
        self.ui.setWindowTitle(title)
class SetWindow():#设置窗口
    def __init__(self):
        self.ui=QUiLoader().load('ui/set.ui')
    def connect(self,up,down,add,del_db,save_db,reset_config):
        self.ui.up_Button.clicked.connect(up)
        self.ui.down_Button.clicked.connect(down)
        self.ui.add_Button.clicked.connect(add)
        self.ui.del_Button.clicked.connect(del_db)
        self.ui.save_Button.clicked.connect(save_db)
        self.ui.reset_config.clicked.connect(reset_config)
class SearchWindow():#查找窗口 
    def __init__(self):
        self.ui=QUiLoader().load('ui/search.ui')
    def connect(self,up,down):
        self.ui.up_Button.clicked.connect(up)
        self.ui.down_Button.clicked.connect(down)
class Process():#主处理类
    def __init__(self,mainwindow):
        self.version='0.1.3'
        self.__icon=QIcon('icon.ico')
        #---------------------------------------
        self.__mainwindow=mainwindow#确定主窗口
        self.__mainwindow.setWindowIcon(self.__icon)
        #---------------------------------------
        self.__text_changed=False
        self.__twd=twd.twd()
        self.__config=configparser.ConfigParser()
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('data\config.ini'):
            self.__config.add_section('user')
            self.__config.add_section('database')
            if os.path.exists('twd.db'):
                self.__config.set('database','num','1')
                self.__config.set('database','path0',os.path.join(os.getcwd(),'twd.db'))
            else:
                self.__config.set('database','num','0')
            with open('data\config.ini','w',encoding='UTF-8') as file:
                self.__config.write(file)
        self.file_path=None
        self.config_path='data\config.ini'
        self.__database_paths=self.__load_database()
        if self.__database_paths == 'ERROR':
            self.__database_paths=[]
        if len(self.__database_paths) > 0:
            self.__twd.change_dbpath(self.__database_paths)
            self.__exists_database=True
        else:
            self.__exists_database=False
        #---------------------------------------
        self.__passwordwindow=PasswordWindow()#注册密码窗口
        self.__passwordwindow_isconnect=False
        #---------------------------------------
        self.__setwindow=SetWindow()#注册设置窗口
        self.__setwindow_isconnect=False
        self.__set_database_paths=self.__database_paths#set方法的临时数据库地址变量，为了解决传递嵌套函数后变量地址不统一的情况
        #---------------------------------------
        self.__searchwindow=SearchWindow()#注册查找窗口
        self.__searchwindow_isconnect=False
        #---------------------------------------
    @staticmethod
    def selfcheck():#自检
        import tkinter.messagebox
        if not os.path.exists('ui/main.ui'):
            tkinter.messagebox.showerror('严重错误','无法找到ui文件:ui/main.ui')
            sys.exit(0)
        if not os.path.exists('ui/password.ui'):
            tkinter.messagebox.showerror('严重错误','无法找到ui文件:ui/password.ui')
            sys.exit(0)
        if not os.path.exists('ui/search.ui'):
            tkinter.messagebox.showerror('严重错误','无法找到ui文件:ui/search.ui')
            sys.exit(0)
        if not os.path.exists('ui/set.ui'):
            tkinter.messagebox.showerror('严重错误','无法找到ui文件:ui/set.ui')
            sys.exit(0)
    def __setEnable(self,action_new=None,action_open=None,action_save=None,action_saveas=None,
    action_set=None,action_close=None,action_exit=None,action_search=None,
    action_twd_text=None,action_text_twd=None,main_textedit=None):#控件的enable项处理
        if action_new != None:
            self.__mainwindow.action_new.setEnabled(action_new)
        if action_open != None:
            self.__mainwindow.action_open.setEnabled(action_open)
        if action_save != None:
            self.__mainwindow.action_save.setEnabled(action_save)
        if action_saveas != None:
            self.__mainwindow.action_saveas.setEnabled(action_saveas)
        if action_set != None:
            self.__mainwindow.action_set.setEnabled(action_set)
        if action_close != None:
            self.__mainwindow.action_close.setEnabled(action_close)
        if action_exit != None:
            self.__mainwindow.action_exit.setEnabled(action_exit)
        if action_search != None:
            self.__mainwindow.action_search.setEnabled(action_search)
        if action_twd_text != None:
            self.__mainwindow.action_twd_text.setEnabled(action_twd_text)
        if action_text_twd != None:
            self.__mainwindow.action_text_twd.setEnabled(action_text_twd)
        if main_textedit != None:
            self.__mainwindow.main_textedit.setEnabled(main_textedit)
    def __ask_save(self):#询问保存
        if self.__text_changed:
            choice=QMessageBox.question(self.__mainwindow,'警告','警告:文本未被保存，是否保存?',QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel,QMessageBox.Yes)
            if choice == QMessageBox.Yes:
                if self.save_file() == 'cancel':
                    return 'cancel'
            elif choice == QMessageBox.Cancel:
                return 'cancel'
    def __show_passwordwindow(self,mode):#显示密码窗口
        def getdata():#对接的函数
            data = [self.__passwordwindow.ui.normal_password_checkbox.isChecked(),self.__passwordwindow.ui.normal_password_edit.text(),self.__passwordwindow.ui.times_edit.text(),self.__passwordwindow.ui.pytext_checkbox.isChecked(),self.__passwordwindow.ui.pytext_edit.text()]
            #格式(普通密码checkbox,普通密码edit,转换次数edit,偏移文本checkbox,偏移文本edit)
            self.__passwordwindow.ui.close()
            self.__get_password(data,self.__passwordwindow_mode)
        if not self.__passwordwindow_isconnect:
            self.__passwordwindow.connect(getdata)#设置对接函数
            self.__passwordwindow_isconnect=True
        if mode == 0 or mode == 2:#标题设置
            self.__passwordwindow.set_title('解密方式')
        elif mode == 1 or mode == 3:
            self.__passwordwindow.set_title('加密方式')
        self.__passwordwindow_mode=mode
        self.__passwordwindow.ui.setWindowModality(Qt.ApplicationModal)#设置模态窗口
        self.__passwordwindow.ui.setWindowIcon(self.__icon)
        self.__passwordwindow.ui.show()
    def __get_password(self,password,mode):#获得密码后的处理
        if not password:
            self.__setEnable(main_textedit=False)
            return
        try:
            if password[0] == False:
                password[1]=0
            if password[3] == False:
                password[4]=None
            database_paths=self.__load_database()#同步最新的数据库地址
            self.__twd.change_dbpath(database_paths)
            if mode == 0:#常规解密
                text=self.__twd.twd_into_text(self.__data,times=password[2],password=password[1],pytext=password[4])
                self.new_file()
                self.__mainwindow.main_textedit.setPlainText(text)
                self.__text_changed=False
            elif mode == 1:#加密及保存文件
                r_twd=self.__twd.text_into_twd(self.__data,times=password[2],password=password[1],pytext=password[4])
                with open(self.file_path,'w',encoding='UTF-8') as file:
                    file.write(r_twd)
                QMessageBox.information(self.__mainwindow,'信息','保存成功')
                self.__text_changed=False
            elif mode == 2:#解密并输出到文本框
                text=self.__twd.twd_into_text(self.__data,times=password[2],password=password[1],pytext=password[4])
                self.new_file()
                self.__mainwindow.main_textedit.setPlainText(text)
                self.__text_changed=False
            elif mode == 3:#加密并输出到文本框
                r_twd=self.__twd.text_into_twd(self.__data,times=password[2],password=password[1],pytext=password[4])
                self.new_file()
                self.__mainwindow.main_textedit.setPlainText(r_twd)
                self.__text_changed=False
        except Exception as err:
            QMessageBox.critical(self.__mainwindow,'错误','出现意外错误:{}'.format(err))
            self.close()
    def __write_config(self,config,section,key=None,value=None):#写配置文件
        self.__config.read(config,encoding='UTF-8')
        if not self.__config.has_section(section):
            self.__config.add_section(section)
        if key:
            self.__config.set(section,key,value)
        with open(config,'w',encoding='UTF-8') as file:
            self.__config.write(file)
    def __test_database(self,database_path):#测试数据库可用性
        if os.path.exists(database_path):
            try:
                conn = sqlite3.connect(database_path)
            except Exception as err:
                return (0,'路径错误',err)
            else:
                conn.close()
                return (1,'合法')
        else:
            return (0,'路径不存在')
    def __load_database(self) -> list:#加载配置文件中的数据库地址
        database_paths=[]
        try:
            self.__config.read(self.config_path,encoding='UTF-8')
            if self.__config.has_option('database','num'):
                database_num=int(self.__config.get('database','num'))
            else:
                raise Exception('未找到重要配置项(database,num)')
            for i in range(database_num):
                if self.__config.has_option('database','path{}'.format(i)):
                    database_paths.append(self.__config.get('database','path{}'.format(i)))
                else:
                    QMessageBox.warning(self.__mainwindow,'警告','未找到配置项(database,path{})'.format(i))
        except Exception as err:
            QMessageBox.critical(self.__mainwindow,'错误','读取配置文件出错:{}\n如有需要请重置配置项'.format(err))
            return 'ERROR'
        for i,database in enumerate(database_paths):
            result = self.__test_database(database)
            if result[0] == 0:
                QMessageBox.warning(self.__mainwindow,'数据库错误','警告:\n数据库无效:{}\n原因:{}'.format(database,result[1]))
                database_paths.pop(i)
        return database_paths
    def text_changed(self):#文本改变
        self.__text_changed=True
    def new_file(self):#新建文件
        if self.__ask_save() == 'cancel':
            return
        self.__mainwindow.main_textedit.clear()
        self.__text_changed = False
        self.__setEnable(main_textedit=True,action_new=True,action_save=True,action_saveas=True,action_close=True,action_text_twd=True,action_twd_text=True,action_search=True,action_exit=True,action_open=True,action_set=True)
    def open_file(self):#打开文件
        if not self.__exists_database:
            QMessageBox.warning(self.__mainwindow,'缺少数据库','警告:无有效的数据库，请到设置中手动添加')
            return
        if self.__ask_save() == 'cancel':
            return
        self.__mainwindow.main_textedit.clear()
        self.__text_changed = False
        self.__setEnable(main_textedit=True)
        try:
            self.__config.read(self.config_path,encoding='UTF-8')
            if self.__config.has_option('user','path'):
                dir=self.__config.get('user','path')
            else:
                dir=None
        except Exception as err:
            QMessageBox.warning(self.__mainwindow,'警告','警告,读取配置文件出错:{}'.format(err))
        path,_=QFileDialog.getOpenFileName(self.__mainwindow,'选择文件位置',filter='twd文件(*.twd)',dir=dir)
        if not path:
            self.close()
            return
        if not os.path.exists(path):
            QMessageBox.critical(self.__mainwindow,'错误','文件不存在!')
            self.close()
            return
        self.__write_config(self.config_path,'user','path',os.path.dirname(path))
        try:
            with open(path,'r',encoding='UTF-8') as file:
                data=file.read()
        except Exception as err:
            QMessageBox.critical(self.__mainwindow,'错误','打开文件出现了错误:{}'.format(err))
            self.close()
        else:
            self.file_path=path
            self.__data=data#将数据保存到类的变量
            self.__show_passwordwindow(0)
    def save_file(self):#保存文件
        if not self.__exists_database:
            QMessageBox.warning(self.__mainwindow,'缺少数据库','警告:无有效的数据库，请到设置中手动添加')
            return
        if not self.file_path:
            try:
                self.__config.read(self.config_path,encoding='UTF-8')
                if self.__config.has_option('user','path'):
                    dir=self.__config.get('user','path')
                else:
                    dir=None
            except Exception as err:
                QMessageBox.warning(self.__mainwindow,'警告','警告,读取配置文件出错:{}'.format(err))
            self.file_path,_=QFileDialog.getSaveFileName(self.__mainwindow,'选择保存位置',filter='twd文件(*.twd)',dir=dir)
            if not self.file_path:
                return 'cancel'
            self.__write_config(self.config_path,'user','path',os.path.dirname(self.file_path))
        text=self.__mainwindow.main_textedit.toPlainText()
        self.__data=text
        self.__show_passwordwindow(1)
    def saveas_file(self):#另存文件
        if not self.__exists_database:
            QMessageBox.warning(self.__mainwindow,'缺少数据库','警告:无有效的数据库，请到设置中手动添加')
            return
        try:
            self.__config.read(self.config_path,encoding='UTF-8')
            if self.__config.has_option('user','path'):
                dir=self.__config.get('user','path')
            else:
                dir=None
        except Exception as err:
            QMessageBox.warning(self.__mainwindow,'警告','警告,读取配置文件出错:{}'.format(err))
        path,_=QFileDialog.getSaveFileName(self.__mainwindow,'选择保存位置',filter='twd文件(*.twd)',dir=dir)
        if not path:
            return 'cancel'
        self.file_path=path
        self.__write_config(self.config_path,'user','path',os.path.dirname(self.file_path))
        text=self.__mainwindow.main_textedit.toPlainText()
        r_twd=self.__twd.text_into_twd(text)
        with open(path,'w',encoding='UTF-8') as file:
            file.write(r_twd)
        QMessageBox.information(self.__mainwindow,'信息','保存成功')
        self.__text_changed=False
    def set(self):#设置
        def up():
            text=self.__setwindow.ui.database_list.currentItem().text()
            for i,path in enumerate(self.__set_database_paths):
                if text == path:
                    if i != 0:
                        self.__set_database_paths[i]=self.__set_database_paths[i-1]
                        self.__set_database_paths[i-1]=text
                    break
            self.__setwindow.ui.database_list.clear()
            self.__setwindow.ui.database_list.addItems(self.__set_database_paths)
        def down():
            text=self.__setwindow.ui.database_list.currentItem().text()
            for i,path in enumerate(self.__set_database_paths):
                if text == path:
                    if i+1 < len(self.__set_database_paths):
                        self.__set_database_paths[i]=self.__set_database_paths[i+1]
                        self.__set_database_paths[i+1]=text
                    break
            self.__setwindow.ui.database_list.clear()
            self.__setwindow.ui.database_list.addItems(self.__set_database_paths)
        def add():
            try:
                self.__config.read(self.config_path,encoding='UTF-8')
                if self.__config.has_option('user','path'):
                    dir=self.__config.get('user','path')
                else:
                    dir=None
            except Exception as err:
                QMessageBox.warning(self.__mainwindow,'警告','警告,读取配置文件出错:{}'.format(err))
            path,_=QFileDialog.getOpenFileName(self.__mainwindow,'选择文件位置',filter='数据库文件(*.db)',dir=dir)
            if not path:
                return
            path=os.path.normpath(path)
            for paths in self.__set_database_paths:
                if paths == path:
                    QMessageBox.warning(self.__mainwindow,'警告','该数据库已存在')
                    return
            self.__set_database_paths.append(path)
            self.__setwindow.ui.database_list.clear()
            self.__setwindow.ui.database_list.addItems(self.__set_database_paths)
        def del_db():
            text=self.__setwindow.ui.database_list.currentItem().text()
            for i,path in enumerate(self.__set_database_paths):
                if text == path:
                    self.__set_database_paths.pop(i)
                    break
            self.__setwindow.ui.database_list.clear()
            self.__setwindow.ui.database_list.addItems(self.__set_database_paths)
        def save_db():
            self.__config.read(self.config_path,encoding='UTF-8')
            self.__config.remove_section('database')
            with open(self.config_path,'w',encoding='UTF-8') as file:
                self.__config.write(file)
            self.__write_config(self.config_path,'database','num',str(len(self.__set_database_paths)))
            for i,path in enumerate(self.__set_database_paths):
                self.__write_config(self.config_path,'database','path{}'.format(i),path)
            self.__database_paths=self.__set_database_paths#将数据库地址同步到全局
            self.__twd.change_dbpath(self.__database_paths)
            QMessageBox.about(self.__mainwindow,'成功','保存成功')
        def reset_config():
            choice = QMessageBox.question(self.__mainwindow,'重置配置项','确定重置配置项?\n注意此操作会将所有的配置内容清空')
            if choice == QMessageBox.Yes:
                os.remove(self.config_path)
                self.__config=configparser.ConfigParser()
                if not os.path.exists('data'):
                    os.mkdir('data')
                if not os.path.exists('data\config.ini'):
                    self.__config.add_section('user')
                    self.__config.add_section('database')
                    if os.path.exists('twd.db'):
                        self.__config.set('database','num','1')
                        self.__config.set('database','path0',os.path.join(os.getcwd(),'twd.db'))
                    else:
                        self.__config.set('database','num','0')
                    with open('data\config.ini','w',encoding='UTF-8') as file:
                        self.__config.write(file)
                self.__setwindow.ui.database_list.clear()
                self.__set_database_paths=self.__load_database()
                self.__database_paths=self.__set_database_paths#将数据库地址同步到全局
                self.__twd.change_dbpath(self.__database_paths)
                if self.__set_database_paths == 'ERROR':
                    self.__set_database_paths=[]
                self.__setwindow.ui.database_list.addItems(self.__set_database_paths)
                QMessageBox.about(self.__mainwindow,'重置成功','配置项已重置成功')
        self.__set_database_paths=self.__load_database()
        if not self.__setwindow_isconnect:
            self.__setwindow.connect(up,down,add,del_db,save_db,reset_config)
            self.__setwindow_isconnect=True
        self.__setwindow.ui.database_list.clear()
        self.__setwindow.ui.setWindowModality(Qt.ApplicationModal)#设置模态窗口
        self.__setwindow.ui.setWindowIcon(self.__icon)
        self.__setwindow.ui.show()
        self.__setwindow.ui.database_list.addItems(self.__set_database_paths)
        self.__setwindow.ui.version_text.setText('当前版本:'+self.version)
    def close(self,force=False):#关闭
        if not force:
            if self.__ask_save() == 'cancel':
                return
        self.__mainwindow.main_textedit.clear()
        self.__text_changed=False
        self.file_path=None
        self.__setEnable(main_textedit=False,action_new=True,action_close=False,action_exit=True,action_open=True,action_save=False,action_saveas=False,action_search=False,action_set=True,action_text_twd=False,action_twd_text=False)
    def exit(self,force=False):#退出
        if not force:
            if self.__ask_save() == 'cancel':
                return
        self.__mainwindow.close()
    def twd_text(self):#twd到文本
        if not self.__exists_database:
            QMessageBox.warning(self.__mainwindow,'缺少数据库','警告:无有效的数据库，请到设置中手动添加')
            return
        self.__data=self.__mainwindow.main_textedit.toPlainText()
        self.__text_changed=False
        self.__show_passwordwindow(2)
    def text_twd(self):#文本到twd
        if not self.__exists_database:
            QMessageBox.warning(self.__mainwindow,'缺少数据库','警告:无有效的数据库，请到设置中手动添加')
            return
        self.__data=self.__mainwindow.main_textedit.toPlainText()
        self.__text_changed=False
        self.__show_passwordwindow(3)
    def search(self):#查找
        def find(stext):
            text = self.__mainwindow.main_textedit.toPlainText()
            idx = text.find(stext)
            idx_list=[]
            while idx != -1:
                idx_list.append(idx)
                idx = text.find(stext,idx+1)
            return idx_list
        def up():
            idx_list = find(self.__searchwindow.ui.search_edit.text())#获得所有的符合条件是索引列表
            pos=self.__mainwindow.main_textedit.textCursor().position()#获得当前光标位置
            st=self.__mainwindow.main_textedit.textCursor().selectedText()#获得当前选中文本
            if st:#如果文本存在则光标位置减去选中文本长度
                pos-=len(st)
            selection=QTextEdit.ExtraSelection()#新建选中类
            linecolor=QColor(255,242,0,160)#设置颜色(好像没用)
            selection.format.setBackground(linecolor)
            cursor = self.__mainwindow.main_textedit.textCursor()#获得当前的光标
            for i,idx in enumerate(idx_list):
                if idx < pos:
                    if len(idx_list)-1 >= i+1:
                        if idx_list[i+1] < pos:
                            continue
                    cursor.setPosition(idx)#将光标位置设置成索引
                    cursor.movePosition(QTextCursor.Right,QTextCursor.KeepAnchor,len(self.__searchwindow.ui.search_edit.text()))#设置光标长度
                    self.__mainwindow.main_textedit.setTextCursor(cursor)#将光标导入
                    selection.cursor=self.__mainwindow.main_textedit.textCursor()#获取selection的光标
                    selection.cursor.clearSelection()#清除当前选中
                    self.__mainwindow.main_textedit.setExtraSelections([selection])#导入选中
                    self.__searchwindow.ui.text.setText('{}/{}'.format(i+1,len(idx_list)))
                    return
            QMessageBox.about(self.__searchwindow.ui,'失败','未查找到文本')
            self.__searchwindow.ui.text.setText('')
        def down():
            idx_list = find(self.__searchwindow.ui.search_edit.text())#获得所有的符合条件是索引列表
            pos=self.__mainwindow.main_textedit.textCursor().position()#获得当前光标位置
            selection=QTextEdit.ExtraSelection()#新建选中类
            linecolor=QColor(255,242,0,160)#设置颜色(好像没用)
            selection.format.setBackground(linecolor)
            cursor = self.__mainwindow.main_textedit.textCursor()#获得当前的光标
            for i,idx in enumerate(idx_list):
                if idx >= pos:
                    cursor.setPosition(idx)#将光标位置设置成索引
                    cursor.movePosition(QTextCursor.Right,QTextCursor.KeepAnchor,len(self.__searchwindow.ui.search_edit.text()))#设置光标长度
                    self.__mainwindow.main_textedit.setTextCursor(cursor)#将光标导入
                    selection.cursor=self.__mainwindow.main_textedit.textCursor()#获取selection的光标
                    selection.cursor.clearSelection()#清除当前选中
                    self.__mainwindow.main_textedit.setExtraSelections([selection])#导入选中
                    self.__searchwindow.ui.text.setText('{}/{}'.format(i+1,len(idx_list)))
                    return
            QMessageBox.about(self.__searchwindow.ui,'失败','未查找到文本')
            self.__searchwindow.ui.text.setText('')
        if not self.__searchwindow_isconnect:
            self.__searchwindow.connect(up,down)
            self.__searchwindow_isconnect=True
        self.__searchwindow.ui.setWindowIcon(self.__icon)
        self.__searchwindow.ui.show()
if __name__ == '__main__':
    Process.selfcheck()
    app=QApplication()
    win=MainWindow()
    win.ui.show()
    sys.exit(app.exec_())