pass_text = "SrZZ5224ZqHVhIE769NgJraUDaOQbfQY"
db_text = "jicaxlkj"
user_text = "jicaxlkj"
host_text =  "queenie.db.elephantsql.com"
port_text = "5432"


import sys
import psycopg2
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import re
from datetime import datetime

#Funcion para convertir un string a numero
def polynomialRollingHash(str):
    
    p = 31
    m = 1e9 + 9
    power_of_p = 1
    hash_val = 0

    for i in range(len(str)):
        hash_val = ((hash_val + (ord(str[i]) -
                                 ord('a') + 1) *
                              power_of_p) % m)
 
        power_of_p = (power_of_p * p) % m
 
    return int(hash_val)

#Clase la cual hace presenta la pantalla de login
#Sus funciones cambian a las distintas pantallas (Cliente, Empleado, Administrador)
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("loginPage.ui", self)
        self.Enter.clicked.connect(self.gotoclient)
        self.adminButton.clicked.connect(self.gotoadmin)
        self.employeeButton.clicked.connect(self.gotoemployee)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def loginfunction(self):
        username = self.Username.text()
        password = self.Password.text()
        print(username, password)

    def gotoclient(self):
        clientpage=clientPage(self.Username.text(), self.Password.text())
        widget.addWidget(clientpage)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoadmin(self):
        adminpage = adminPage(self.Username.text(), self.Password.text())
        widget.addWidget(adminpage)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoemployee(self):
        employeepage = employeePage(self.Username.text())
        widget.addWidget(employeepage)
        widget.setCurrentIndex(widget.currentIndex()+1)


#Clase que presenta la pantalla de Cliente
class clientPage(QDialog):
    def __init__(self, key, key2):
        super(clientPage,self).__init__()
        loadUi("ClientPage.ui", self)
        self.loadClientInfo(key, key2)
        
        self.rButton.clicked.connect(self.clientRefer)
        self.modifyButton.clicked.connect(self.modifyClientInfo)
        self.returnMain.clicked.connect(self.gotomain)
        self.deleteButton.clicked.connect(self.deleteAccount)

    def clientRefer(self):
        email = self.rEmail.text()
        print("Email sent to " + email)

    def loadClientInfo(self, key, key2):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM miembro WHERE memberid = %s AND id = %s'''
        cursor.execute(query, [str(polynomialRollingHash(key)), str(polynomialRollingHash(key2))])

        row = cursor.fetchall()
        
        conn.commit()
        conn.close()

        
        if row:
            self.clientNameLine.setText(row[0][1])
            self.clientLastNameLine.setText(row[0][2])
            self.clientEmailLine.setText((row[0][4])) 
            self.clientAddressLine.setText(row[0][5])
            self.memTierLine.setText(str(row[0][6]))
           
            self.clientNameLine_3.setText(row[0][1])
            self.clientLastNameLine_3.setText(row[0][2])
            self.clientAddressLine_3.setText(row[0][5])
            self.clientAccountStateLine_3.setText(str(row[0][6]))
            
            if datetime.today().strftime('%Y-%m-%d') > str(row[0][7]):
                accState  = " Vencida "
            else:
                accState = " Activa hasta: " + str(row[0][7])

            self.clientAccStateLine.setText(accState)
    
    def modifyClientInfo(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''UPDATE miembro SET nombre = %s, apellido = %s, address = %s, tier = %s WHERE email = %s;'''
        cursor.execute(query, [self.clientNameLine_3.text(), self.clientLastNameLine_3.text(), self.clientAddressLine_3.text(),self.clientAccountStateLine_3.text(), self.clientEmailLine.text()]) 

        conn.commit()
        conn.close()

    def deleteAccount(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''DELETE FROM miembro WHERE memberid = %s'''
        cursor.execute(query, [str(polynomialRollingHash(self.clientEmailLine.text()))])

        conn.commit()
        conn.close()

        self.gotomain()
        return
    
    def gotomain(self):
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex()-1)

#Clase presenta la pantalla de Administrador
class adminPage(QDialog):
    def __init__(self, key, key2): 
        super(adminPage,self).__init__()
        loadUi("AdminPage.ui", self)
        
        self.load()
        self.adminLogin(key,key2)

        self.refreshButton.setIcon(QtGui.QIcon('refresh.png'))
        self.refreshButton.setIconSize(QtCore.QSize(25,25))
        self.refreshButton_2.setIcon(QtGui.QIcon('refresh.png'))
        self.refreshButton_2.setIconSize(QtCore.QSize(25,25))
        self.refreshButton_3.setIcon(QtGui.QIcon('refresh.png'))
        self.refreshButton_3.setIconSize(QtCore.QSize(25,25))
        self.refreshButton.clicked.connect(self.ref)
        self.refreshButton_2.clicked.connect(self.ref)
        self.refreshButton_3.clicked.connect(self.ref)


        self.addItemButton.clicked.connect(self.addItem)
        self.modifyEmp_button.clicked.connect(self.modifyEmpdb)


        self.addBuildingButton.clicked.connect(self.addBuildings)
        self.BuildingListDel.itemActivated.connect(self.deleteBuilding)
        self.ProductListDel.itemActivated.connect(self.deleteItem)
        self.buildingList.itemActivated.connect(self.modifyBuild)
        self.EmpList.itemActivated.connect(self.modifyEmp)
        self.itemList.itemActivated.connect(self.modifyProd)
        self.EmployeeListDel.itemActivated.connect(self.deleteEmployee)

        self.addEmployeeButton.clicked.connect(self.addEmployee)
        
        self.returnMain.clicked.connect(self.gotomain)

        self.modifyBuilding.clicked.connect(self.modifyBuildingdb)
        self.ModItemButton.clicked.connect(self.modifyProductdb)
    
    def adminLogin(self, key, key2):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM administrador WHERE id = %s and password = %s;'''
        cursor.execute(query, [str(key), key2]) 

        conn.commit()
        conn.close()

    def modifyEmpdb(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''UPDATE empleado SET nombre = %s,  apellido = %s, postal = %s, posicion = %s WHERE id = %s;''' 
        cursor.execute(query, [self.EmpNameLine_2.text(), self.clientLastNameLine_2.text(), self.direccionEmp.text(), self.positionEmp_2.text(), self.EmpLabel_2.text()]) 

        conn.commit()
        conn.close()
        self.loadBuildings(self.buildingList)

    def modifyEmp(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        id_number = filter.group(2)
        self.EmpLabel_2.setText(str(id_number))
        

    def modifyBuildingdb(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''UPDATE edificio SET NIVEL = %s, NAME = %s WHERE name = %s;'''
        cursor.execute(query, [str(self.buildingToAddMem_2.text()), str(self.buildingModify.text()), self.buildSelecLabel.text()]) 

        conn.commit()
        conn.close()
        self.loadBuildings(self.buildingList)
    
    def modifyProductdb(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''UPDATE articulos SET id = %s, nombre = %s, precio = %s WHERE id = %s; '''
        cursor.execute(query, [self.itemModify.text(), self.itemModify_1.text(), self.itemModify_2.text(), self.prodSelecLabel.text()]) 

        conn.commit()
        conn.close()
        self.loadArticles(self.itemList)
        
    def load(self):
        self.loadArticles(self.itemList)
        self.loadBuildings(self.buildingList)
        self.loadEmployees(self.EmployeeListDel)
        self.loadEmployees(self.EmpList)
        self.loadArticles(self.ProductListDel)
        self.loadBuildings(self.BuildingListDel)

    def loadEmployees(self, listToShow):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM public.empleado'''
        cursor.execute(query) 

        row = cursor.fetchall() 
        
        conn.commit()
        conn.close()

        for x in range(0, len(row)):
            id = row[x][2]
            name = row[x][0]
            address = row[x][4]
            lastname = row[x][1]
            position_emp = row[x][3]

            temp =  "\nId: "+ str(id) + "\nNombre Empleado: " + str(name) + "\nApellido Empleado: " + str(lastname) + "\nPosicion Empleado: " + position_emp + "\nDireccion Empleado: " + str(address) + "\n"
            listToShow.addItem(temp)

    def ref(self):
        self.itemList.clear()
        self.buildingList.clear()
        self.EmpList.clear()
    
        self.loadArticles(self.itemList)
        self.loadBuildings(self.buildingList)
        self.loadEmployees(self.EmpList)

    def addItem(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''INSERT INTO articulos (ID, nombre, precio) VALUES (%s, %s, %s);'''
        cursor.execute(query, [self.itemToAddId.text(), self.itemToAddName.text(), self.itemToAddPrice.text()]) 

        conn.commit()
        conn.close()
        self.itemList.clear()
        self.loadArticles(self.itemList)
    
    def addBuildings(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''INSERT INTO edificio (name, nivel)
                   VALUES(%s, %s);'''
        cursor.execute(query, [self.buildingToAdd.text(), self.buildingToAddMem.text()]) 

        conn.commit()
        conn.close()
        self.buildingList.clear()
        self.loadBuildings(self.buildingList)
    
    def addEmployee(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''INSERT INTO empleado (nombre, apellido, ID, posicion, postal) VALUES (%s, %s, %s, %s, %s);'''
                   
        cursor.execute(query, [self.EmpNameLine.text(), self.EmpLastNameLine.text(), self.EmpId.text(), self.positionEmp.text() , self.EmpAddressLine.text()]) 

        conn.commit()
        conn.close()
        self.buildingList.clear()
        self.loadEmployees(self.EmployeeListDel)

    def loadBuildings(self, listToShow):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM public.edificio'''
        cursor.execute(query) 

        row = cursor.fetchall() 
        
        conn.commit()
        conn.close()

        for x in range(0, len(row)):
            name = row[x][0]
            Level = row[x][1]

            temp = "\nNivel de Membresía: " + str(name) + "\nNombre Edificio: "+ str(Level) + "\n"
            listToShow.addItem(temp)

    def loadArticles(self, listToShow): 
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM public.articulos'''
        cursor.execute(query) 

        row = cursor.fetchall() 
        
        conn.commit()
        conn.close()

        for x in range(0, len(row)):
            num = row[x][0]
            name = row[x][1]
            price = row[x][2]

            temp = "Numero id: " + str(num) + "\nNombre Producto: " + str(name) + "\nPrecio: "+ str(price) + "\n"
            listToShow.addItem(temp)

    def deleteBuilding(self, item):

        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        name = filter.group(2)
        
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''DELETE FROM edificio WHERE nivel = %s'''
        cursor.execute(query, [name])

        conn.commit()
        conn.close()

        self.BuildingListDel.clear()
        self.loadBuildings(self.BuildingListDel)

    
    def deleteItem(self, item):
        
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        id_number = filter.group(2)

        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''DELETE FROM articulos WHERE id = %s'''
        cursor.execute(query, [id_number])

        conn.commit()
        conn.close()
        
        self.ProductListDel.clear()
        self.loadArticles(self.ProductListDel)
    
    def deleteEmployee(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        number_id = filter.group(2)

        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''DELETE FROM empleado WHERE id = %s'''
        cursor.execute(query, [number_id])

        conn.commit()
        conn.close()

    def modifyProd(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        id_number = filter.group(2)
        self.prodSelecLabel.setText(str(id_number))
        
    def modifyBuild(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        name = filter.group(2)
        self.buildSelecLabel.setText(str(name))
        
    
    def gotomain(self):
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex()-1)
        
#Clase que presenta la pantalla de Empleado
class employeePage(QDialog):
    def __init__(self, key):
        super(employeePage, self).__init__()
        loadUi("EmployeePage.ui", self)
        self.EmployeeLogin(key)
        self.loadClients()
        self.loadClientsMod()
        self.ClientList.itemActivated.connect(self.avisoPago)
        self.addClientButton.clicked.connect(self.addNewClient)
        self.search.clicked.connect(self.searchClient)
        self.returnMain.clicked.connect(self.gotomain)
        self.addPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.modifyClient_button.clicked.connect(self.modifyClientdb)
        self.modClientList.itemActivated.connect(self.modClient)

    def EmployeeLogin(self, key):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM public.empleado WHERE id = %s;'''
        cursor.execute(query, [str(key)]) 

        conn.commit()
        conn.close()

    def avisoPago(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        email = filter.group(2)
        print(email)

    def modClient(self, item):
        filter = re.search(r'([\w\s]+:\s)(\w+)', item.text())
        id = filter.group(2)
        self.cliModLabel.setText(str(id))

    def modifyClientdb(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''UPDATE miembro SET nombre = %s, apellido = %s, address = %s, tier = %s WHERE id = %s;'''
        cursor.execute(query, [self.cliNameMod.text(), self.cliLastNameMod.text(), self.cliAddressLabel.text(),self.clieEstadoCuenta.text(), self.cliModLabel.text()]) 

        conn.commit()
        conn.close()

        self.modClientList.clear()
        self.loadClientsMod()

    def loadClientsMod(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM miembro'''
        cursor.execute(query)

        row = cursor.fetchall()
        
        conn.commit()
        conn.close()

        for x in range(0, len(row)):
            if row:
                num = row[x][0]
                name = row[x][1]
                lastName = row[x][2]
                email = row[x][4] 
                address = row[x][5]
                tier = str(row[x][6])
                
                if datetime.today().strftime('%Y-%m-%d') > str(row[x][7]):
                    accState  = " Vencida "
                else:
                    accState = " Activa hasta: " + str(row[x][7])
           
                temp = "id: " + str(num) + "\nEmail: "+ str(email) + "\nName: " + str(name) + "\nApellido: " + str(lastName) + "\nAddress: " + str(address) + "\nNivel: " + str(tier) + "\nEstado de Cuenta: " + accState + "\n"
                self.modClientList.addItem(temp)
    
    def loadClients(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM miembro'''
        cursor.execute(query)

        row = cursor.fetchall()
        
        conn.commit()
        conn.close()

        for x in range(0, len(row)):
            if row:
                name = row[x][1]
                lastName = row[x][2]
                email = row[x][4] 
                address = row[x][5]
                tier = str(row[x][6])
                
                if datetime.today().strftime('%Y-%m-%d') > str(row[x][7]):
                    accState  = " Vencida "
                else:
                    accState = " Activa hasta: " + str(row[x][7])
           
                temp = "Email: "+ str(email) + "\nName: " + str(name) + "\nApellido: " + str(lastName) + "\nAddress: " + str(address) + "\nNivel: " + str(tier) + "\nEstado de Cuenta: " + accState + "\n"
                self.ClientList.addItem(temp)


    def searchClient(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''SELECT * FROM miembro WHERE memberid = %s'''
        item = str(polynomialRollingHash(self.clientEmailLine.text()))
        cursor.execute(query, [item]) 

        row = cursor.fetchall() 
        
        conn.commit()
        conn.close()
               
        self.clientNameLine.setText(row[0][1])
        self.clientLastNameLine.setText(row[0][2])
        self.clientEmailLine.setText((row[0][4])) 
        self.clientAddressLine.setText(row[0][5])

        if datetime.today().strftime('%Y-%m-%d') > str(row[0][7]):
            accState  = " Vencida "
        else:
            accState = " Activa hasta: " + str(row[0][7])

        self.accStateLine.setText(accState)
        self.memTierLine.setText(str(row[0][6]))

    def addNewClient(self):
        conn = psycopg2.connect(dbname=db_text, user=user_text, password=pass_text, host=host_text, port=port_text)
        cursor = conn.cursor()
        query = '''INSERT INTO miembro (id, nombre, apellido, memberid, email, address, tier, mem_ven)
                   VALUES(%s, %s, %s, %s, %s, %s, %s, %s);'''
        cursor.execute(query, [str(polynomialRollingHash(self.addPassword.text())), self.addClientName.text(), self.addClientLastName.text(), str(polynomialRollingHash(self.addClientEmail.text())) ,
        self.addClientEmail.text(), self.addClientAddress.text(), self.addMemTier.text(), self.clientAccState.text()])
        
        conn.commit()
        conn.close()

    def paymentNotice(self):
        print(self.rEmail.text())
    
    def gotomain(self):
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex()-1)

class accountCreation(QDialog):
    def __init__(self):
        super(accountCreation, self).__init__()



app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(500)
widget.setFixedHeight(620)
widget.setWindowIcon(QtGui.QIcon('icon.png'))
widget.setWindowTitle("Club Membership System")
widget.show()
app.exec_()