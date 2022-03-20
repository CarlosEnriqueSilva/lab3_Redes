# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:33:41 2022

@author: Seccion 2 Grupo 1
"""
import socket
import threading
import os
import logging
import datetime
import time
import hashlib

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.accept_connections()
    
    def accept_connections(self):
        #ip = socket.gethostbyname(socket.gethostname())
        ip = '0.0.0.0'
        port = int(input('Ingresar puerto para el servidor --> '))

        self.s.bind((ip,port))
        self.s.listen(100)

        print('Servidor corriendo en: ' + ip)
        print('En el puerto: ' + str(port))

        arch = input('Ingresar archivo a trasmitir: (i.e. 100MB.txt) ')
        numClientes = int(input('Ingrese cantidad de clientes que tiene que estar conectados para empezar a trasmitir '))
        
        p = 1 
        now = datetime.datetime.now()
        logName = 'Logs/'+ str(now.year) + '-' + str(now.month) + '-' + str(now.day)+ '-' + str(now.hour)+ '-' +  str(now.minute)+ '-' + str(now.second) + 'prueba' + str(p) + '-log.log'
        b = os.path.getsize(arch)
        logging.basicConfig(filename=logName, level=logging.INFO)
        logging.info('Inicio de envio de archivos')
        logging.info('Nombre archivo: ' + arch)
        logging.info('Tamaño del archivo: ' + str(b) + " Bytes")
        logging.info('Cantidad de clientes: ' + str(numClientes))
        
        threads = list()
        conectClient = 0

        while 1:
            c, addr = self.s.accept()
            print('Conexion recibida numero:', (conectClient + 1))
            
            #print('C:',c,'addr:', addr)
            #print(addr[1])
            
            threads.append(threading.Thread(target=self.handle_client,args=(c,addr,arch,conectClient +1,numClientes,)))
            conectClient += 1
            
            if conectClient == numClientes:
                for t in threads:
                    t.start()
                    
                for t in threads:
                    t.join()
                threads = list()
                conectClient = 0
                arch = input('Ingresar archivo a trasmitir: (i.e. 100MB.txt) ')
                numClientes = int(input('Ingrese cantidad de clientes que tiene que estar conectados para empezar a trasmitir '))
                p += 1
                logName = str(now.year) + '-' + str(now.month) + '-' + str(now.day)+ '-' + str(now.hour)+ '-' +  str(now.minute)+ '-' + str(now.second) + 'prueba' + str(p) + '-log.log'
                logging.basicConfig(filename=logName, level=logging.INFO)
                b = os.path.getsize(arch)
                logging.info('Inicio de envio de archivos')
                logging.info('Nombre archivo: ' + arch)
                logging.info('Tamaño del archivo: ' + str(b) + " Bytes")
                logging.info('Cantidad de clientes: ' + str(numClientes))
                
                
    def handle_client(self,c,addr,data,num,numClientes):
        #data = c.recv(1024).decode()
        logging.info('Cliente addr: ' + str(addr) + ' c: ' + str(c))
        iniciar = c.recv(50000).decode()
        if iniciar == 'Listo':
            if not os.path.exists(data):
                c.send("El Archivo no existe".encode())
    
            else:
                c.send("iniciando-envio".encode())
                nombree = 'Cliente-' + str(num) + '-Prueba-' + str(numClientes) + '.txt'
                c.send(nombree.encode())
                
                if c.recv(50000).decode() == 'Nombre recibido correctamente':
                    print('Enviando: ',data)
                    
                    file = open(data,'rb')
                    contenido = file.read().decode().strip()
                    #print('Contenido:', contenido)
                    hashVal = str(hashlib.sha256(contenido.encode()).hexdigest())
                    #print('Hash: ', hashVal)
                    file = open(data,'rb')
        
                    start = time.time()
                   # print('Data: ', data)
                    if data != '':
                        
                        data = file.read(50000)
                        while data:
                    #        print('Dat:',data)
                            c.send(data)
                            data = file.read(50000)   
                        c.send("EOF".encode())
                        
                    confirm = c.recv(50000).decode()
                    if confirm == 'OK':
                        logging.info('Archivo entregado exitosamente a cliente: ' + str(addr[1]))
                        end=time.time()
                        logging.info('Tiempo de entrega: ' + str(end-start))
                        c.send(hashVal.encode())
                        
        
                        c.shutdown(socket.SHUT_RDWR)
                        c.close()
                    
            

server = Server()