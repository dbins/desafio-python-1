from datetime import datetime
import sqlite3
import os
import sys

ROOT_PATH =os.path.abspath(os.curdir)

conexao = sqlite3.connect(ROOT_PATH + "\\" + "banco.sqlite")
#print(conexao)
cursor = conexao.cursor()
cursor.execute('CREATE TABLE if not exists transacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo VARCHAR(100), valor NUMERIC)')
conexao.commit()

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

limite = 500
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            try:
                data = ('DEPOSITO', valor)
                cursor.execute("INSERT INTO transacoes (tipo, valor) VALUES (?,?)", data)
                conexao.commit()
            except Exception as e:
                print (f"Ocorreu um erro:{e}")    
                conexao.rollback()
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        saques = 0
        depositos = 0
        valor = float(input("Informe o valor do saque: "))

        cursor.execute("SELECT SUM(valor) as total FROM transacoes where tipo = 'DEPOSITO'")
        resultado = cursor.fetchone()[0]
        if (resultado):
            depositos = resultado

        cursor.execute("SELECT SUM(valor) as total FROM transacoes where tipo = 'SAQUE'")
        resultado = cursor.fetchone()[0]
        if (resultado):
            saques = resultado

        
        
        saldo = depositos - saques
        
        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            try:
                data = ('SAQUE', valor)
                cursor.execute("INSERT INTO transacoes (tipo, valor) VALUES (?,?)", data)
                conexao.commit()
                numero_saques += 1
            except Exception as e:
                print (f"Ocorreu um erro:{e}")    
                conexao.rollback()
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        saques = 0
        depositos = 0
        cursor.execute("SELECT SUM(valor) as total FROM transacoes where tipo = 'DEPOSITO'")
        resultado = cursor.fetchone()[0]
        if resultado:
            depositos = resultado

        cursor.execute("SELECT SUM(valor) as total FROM transacoes where tipo = 'SAQUE'")
        resultado = cursor.fetchone()[0]
        if resultado:
            saques = resultado

        saldo = depositos - saques

        extrato = ""
        res = cursor.execute("SELECT * FROM transacoes")
        resultados = res.fetchall()
        for item in resultados:
            if item[1]=="DEPOSITO":
               extrato += f"Depósito: R$ {item[2]:.2f}\n"
            else:        
               extrato += f"Saque: R$ {item[2]:.2f}\n"

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("\n================ EXTRATO ================")
        print("\nExtrato emitido em ", dt_string)
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")