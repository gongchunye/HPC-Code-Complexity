import sys, os, re

#code by Chunye Gong, 2024.7.28 in Kunming


class CHPCCC():
    #C语言版本的OHPCCC
    
    nLOC = 0
    ndcc = 0

    def init(self):
        #初始化
        dir1 = sys.argv[1]
        print(dir1)
        self.allSrc = []
        self.oprCSet = []
        self.getLocalDir(dir1)
        self.setoprCset()
        # print(self.allSrc)
        
    def setoprCset(self):
        #创建C语言的操作符集合，逐步完善
        #需要手动指定顺序
        op2 = ["\+\+", "\-\-", "\=\=",  "\<\=", "\>\=", "\*\*"]
        op1 = ["\>", "\<", "\+", "\-", "\*", "\/", "\=", "\%", "\!", "\&"]
        self.oprCSet = self.oprCSet + op2 + op1
        
        # print(self.oprCSet)
        # self.oprCSet = sorted(self.oprCSet, reverse =True)
        # print(self.oprCSet)

    def getLocalDir(self,indir):
        #得到当前路径下的源文件，如果有文件夹，则递归找到所有文件
        f2 = os.listdir(indir)
        for xx in f2:
            d2 = indir+"/"+xx
            if os.path.isfile(d2):
                file_extension = d2.split(".")[-1]
                fe = file_extension.lower()
                if (fe == "c" or fe == "h" or fe == "cpp" or fe == "cxx" or fe == "cc"):
                    self.allSrc.append(d2)
            else:
                self.getLocalDir(d2)
    
    def dealSrcCode(self):
        #处理源文件，包括获得源代码，处理和输出
        for fin in self.allSrc:
            if "-noEmptyLine" in fin:
                continue
            self.getSrc(fin)
            self.rmEmptyLine()
            self.rmComments()
            self.dealandOutput(fin)
            # print(fin+": " + "nLOC = " + str(self.nLOC) + "; ndcc = " + str(self.ndcc)  )
        print("nLOC = " + str(self.nLOC) + "; ndcc = " + str(self.ndcc))

    def rmEmptyLine(self):
        tmp = []
        for i in range(len(self.oriSrc)):
            xx = self.oriSrc[i]
            if len(xx.strip()) > 0:
                tmp.append(xx)                
        self.oriSrc2 = tmp
        
    def rmComments(self):
        tmp = []
        bComment = False
        for xx in self.oriSrc2:
            ss = xx.strip()
            if "\\" == ss[0:2]:
                continue
            if "/*" == ss[0:2]:
                bComment = True
            if "*/" == ss[len(ss)-2:len(ss)]:
                bComment = False
                continue
            if bComment:
                continue
            tmp.append(xx)
        self.oriSrc2 = tmp

    def getSrc(self,inp):
        #读取源文件中的代码
        # print(inp)
        ff = open(inp, 'r', encoding='utf-8')
        self.oriSrc = ff.readlines()
        ff.close()

    def getndcc(self, ss):
        #计算ndcc(num degree of code complexity)
        if "include" in ss and "#" in ss: 
            #include有<>号，不要计入
            return
        if "printf" in ss :
            #printf 格式化打印语句
            return
        for op in self.oprCSet:            
            nn = re.findall(op, ss)
            if len(nn) > 0:
                self.ndcc = self.ndcc + len(nn)
                # print(ss, ";  ", op, ";  ", nn, ";  ", len(nn), self.ndcc)
                ss = re.sub(op, "", ss)
        
    def dealandOutput(self,fin):
        #输出没有空格的源文件，并命名为*-noEmptyLine.*
        #计算nLOC和ndcc
        file_extension = fin.split(".")[-1]
        nlen = len(file_extension) + 1
        fileName = fin[0:len(fin)-nlen]+"-noEmptyLine." + file_extension
        # print(file_extension, fileName)
        fout = open(fileName,"w", encoding='utf-8')
        for xx in self.oriSrc2:
            x2 = xx.strip()
            # if len(x2) == 0:
            #     continue
            fout.write(xx)    
            self.getndcc(x2)
            #统计包含注释的行数
            self.nLOC = self.nLOC + 1
        fout.close()    
        
obj = CHPCCC()
obj.init()
obj.dealSrcCode()
