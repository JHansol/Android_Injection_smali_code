import os
from xml.etree.ElementTree import parse
import shutil # file copy

path = "C:\\" # project path
filename = "hhh"
apkpath = ""
index = 1

folderename = "hhh"

keypath = "C:\\k.jks" # your key path
keyname = 'mykey'
main_path = ''
main_path_file = ''

class android_analysis():

    def depack(self):
        print(os.getcwd())
        apkpath = 'java -jar apktool.jar d ' + path + '\\' + filename + '.apk'
        os.system(apkpath + ' -o ' + path + '\\' + filename + str(index))

    def repack(self):
        print(os.getcwd())
        apkpath = 'java -jar apktool.jar b ' + path + '\\' + folderename + str(index)
        os.system(apkpath + ' -o ' + path + '\\' + filename + str(index) + '.apk')

    def sign(self):
        jar = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "
        print jar + keypath + ' ' + path + '\\' + filename + str(index) + '.apk' + ' '+ keyname
        os.system(jar + keypath + ' ' + path + '\\' + filename + str(index) + '.apk' + ' '+ keyname )

    def mani_parse(self, path):
            tree = parse(path + '\\AndroidManifest.xml')
            note = tree.getroot()

            for child in note.iter():
                if child.tag == 'activity':
                    for childs in child.iter():
                        for ss in childs.items():
                            if 'android.intent.action.MAIN' in ss:
                                # print child.items()
                                # print child.keys()
                                for ccc in child.attrib:
                                    if ccc == '{http://schemas.android.com/apk/res/android}name':
                                        print '[1] success main class parse : '+ child.attrib[ccc]
                                        return child.attrib[ccc]
            return 0

    def str_conver(self, pathz):
        smali_merge = '\\smali\\'
        listfile = os.listdir(path + '\\' + filename + str(index) +'\\')
        if 'smali_classes2' in listfile:
            smali_merge = '\\smali_classes2\\'

        main_path = path + '\\' + filename + str(index) +smali_merge + pathz.replace('.','\\')
        max = len(main_path.split('\\')[len(main_path.split('\\'))-1])
        main_path = main_path[0:len(main_path) - max-1]

        ##print main_path
        print '[2] file copy success'
        shutil.copy('set.smali', main_path)

        main_path_file = path + '\\' + filename + str(index) +smali_merge + pathz.replace('.','\\') + '.smali'

        list = []
        cnt = 0;
        f = open(main_path_file, 'a+')
        while True:
            line = f.readline()
            if not line: break
            list.append(line)
        for aa in range(len(list)):
            if 'protected onCreate(Landroid/os/Bundle;)' in list[aa]:
                cnt = 1
            if cnt == 1 :
                if 'return-void' in list[aa]:
                    tmp = aa
                    for b in range(aa):
                        tmp = tmp - 1
                        if '.line' in list[tmp]:
                            #print list[tmp]
                            aa = tmp
                            cnt = 2
                            break
                if cnt == 2:
                    add_smali ="    .line 999\n"      # line count ignore
                    add_smali +="    new-instance v0, Lone/studio/sol/linears/xyz/loging_load/set;\n"
                    add_smali +="    invoke-direct {v0}, Lone/studio/sol/linears/xyz/loging_load/set;-><init>()V\n\n"
                    add_smali +="    .line 1000\n"
                    add_smali +="    .local v0, \"ab\":Lone/studio/sol/linears/xyz/loging_load/set;\n"
                    add_smali +="    invoke-static {p0}, Lone/studio/sol/linears/xyz/loging_load/set;->LoadFiles(Landroid/app/Activity;)V\n\n"
                    list.insert(aa,add_smali)
                    #for aaa in list:
                    #    print aaa
                    shutil.copy(main_path_file, main_path_file + 'back')

                    fz = open(main_path_file, 'w')
                    fz.writelines(list)
                    print '[3] success file write!'
                    fz.close()
        f.close()
        return main_path_file

    def file_copy(self):
        shutil.copy('set.smali', main_path)

if __name__ == '__main__':
    c1 = android_analysis()
    while True:
        print '****************** select menu ******************'
        print '****************** 1. depackage *****************'
        print '****************** 2. Injection smali ***********'
        print '****************** 3. repackage *****************'
        print '****************** 3. signing *******************'
        val = input("input : ")
        if val == 1:
            c1.depack()
        elif val == 2:
            ac = c1.mani_parse(path + "\\" + filename + str(index))
            c1.str_conver(ac)
        elif val == 3:
            c1.repack()
        elif val == 4:
            c1.sign()

