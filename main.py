import textwrap

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    @staticmethod
    def criar_usuario(usuarios):
        cpf = input("Informe o CPF (somente número): ")
        if any(usuario.cpf == cpf for usuario in usuarios):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return None

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        print("=== Usuário criado com sucesso! ===")
        return usuario

class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.limite_saques = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > self.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

    @staticmethod
    def criar_conta(agencia, numero_conta, usuarios):
        cpf = input("Informe o CPF do usuário: ")
        usuario = next((u for u in usuarios if u.cpf == cpf), None)

        if usuario:
            print("\n=== Conta criada com sucesso! ===")
            return Conta(agencia, numero_conta, usuario)

        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return None

    @staticmethod
    def listar_contas(contas):
        for conta in contas:
            linha = f"""
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero_conta}
                Titular:\t{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

class Banco:
    def __init__(self):
        self.LIMITE_SAQUES = 3
        self.AGENCIA = "0001"
        self.usuarios = []
        self.contas = []

    def menu(self):
        opcoes = """
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(opcoes))

    def executar(self):
        while True:
            opcao = self.menu()

            if opcao == "d":
                numero_conta = int(input("Informe o número da conta: "))
                conta = next((c for c in self.contas if c.numero_conta == numero_conta), None)
                if conta:
                    valor = float(input("Informe o valor do depósito: "))
                    conta.depositar(valor)
                else:
                    print("Conta não encontrada!")

            elif opcao == "s":
                numero_conta = int(input("Informe o número da conta: "))
                conta = next((c for c in self.contas if c.numero_conta == numero_conta), None)
                if conta:
                    valor = float(input("Informe o valor do saque: "))
                    conta.sacar(valor)
                else:
                    print("Conta não encontrada!")

            elif opcao == "e":
                numero_conta = int(input("Informe o número da conta: "))
                conta = next((c for c in self.contas if c.numero_conta == numero_conta), None)
                if conta:
                    conta.exibir_extrato()
                else:
                    print("Conta não encontrada!")

            elif opcao == "nu":
                usuario = Usuario.criar_usuario(self.usuarios)
                if usuario:
                    self.usuarios.append(usuario)

            elif opcao == "nc":
                numero_conta = len(self.contas) + 1
                conta = Conta.criar_conta(self.AGENCIA, numero_conta, self.usuarios)
                if conta:
                    self.contas.append(conta)

            elif opcao == "lc":
                Conta.listar_contas(self.contas)

            elif opcao == "q":
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    banco = Banco()
    banco.executar()
