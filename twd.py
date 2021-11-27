import os
import sqlite3

class twd():
    def __init__(self):
        self.__dbpath=[]
        self.version='0.1.3'
    def get_dbpath(self):
        return self.__dbpath
    def change_dbpath(self,paths):
        for i,path in enumerate(paths):
            if os.path.exists(path):
                try:
                    conn = sqlite3.connect(path)
                except Exception as err:
                    raise Exception('路径错误:{}'.format(i))
                else:
                    conn.close()
                    continue
            else:
                raise Exception('路径不存在:{}'.format(i))
        self.__dbpath=paths
    def __connect_db(self,i):
        conn = sqlite3.connect(self.__dbpath[i])
        cur = conn.cursor()
        return (conn,cur)
    def __disconnect_db(self,conn,cur,save=True):
        if save:
            conn.commit()
        cur.close()
        conn.close()
    def __search_db(self,name,text):
        for i,_ in enumerate(self.__dbpath):
            conn,cur = self.__connect_db(i)
            cur.execute('select * from twd where {}=?'.format(name),(text,))
            data=cur.fetchall()
            self.__disconnect_db(conn,cur,False)
            if not data:
                continue
            return data[0]
        raise Exception('数据库在{}里未搜索到内容:{}'.format(name,text))
    def twd_into_text(self,twd,times=1,password=0,pytext=None):
        times=int(times)
        if pytext != None:
            pytext=list(pytext)
        if times < 1:
            raise Exception('转换次数不能小于1!')
        text=twd
        password=int(password)
        for _ in range(times):
            pytext_i=0
            list_code = text.split('/')
            list_code.pop(0)
            text=''
            for code in list_code:
                num_code=int(code[1:])
                num_code-=password
                if pytext != None:
                    py_code=int(self.__search_db('word',pytext[pytext_i])[0][1:])
                    num_code-=py_code
                    pytext_i+=1
                    if pytext_i >= len(pytext):
                        pytext_i=0
                code='t'+str(num_code)
                _,word = self.__search_db('code',code)
                if word == '#换行符':
                    word='\n'
                text+=word
        return text
    def text_into_twd(self,text,times=1,password=0,pytext=None):
        times=int(times)
        if pytext != None:
            pytext=list(pytext)
        if times < 1:
            raise Exception('转换次数不能小于1!')
        twd=''
        password=int(password)
        for _ in range(times):
            pytext_i=0
            for word in text:
                if word == '\n':
                    word = '#换行符'
                code,_ = self.__search_db('word',word)
                code=str(int(code[1:])+password)
                if pytext != None:
                    py_code=int(self.__search_db('word',pytext[pytext_i])[0][1:])
                    code=str(int(code)+py_code)
                    pytext_i+=1
                    if pytext_i >= len(pytext):
                        pytext_i=0
                twd+='/t'+code
            text=twd
            twd=''
        return text
if __name__ == '__main__':
    import os,sys
    while True:
        os.system('cls')
        print('您正在以调试模式运行')
        mode=input('请选择模式:\n1.twd到文本\n2.文本到twd\n0.退出\n')
        t=twd()
        t.change_dbpath([r'plugins\twd.db'])
        if mode == '1':
            text = input('请输入twd:\n')
            print(t.twd_into_text(text,times=2))
            input('按回车继续..')
            continue
        elif mode == '2':
            text = input('请输入文本:\n')
            print(t.text_into_twd(text,times=2))
            input('按回车继续..')
            continue
        elif mode == '0':
            sys.exit(0)

