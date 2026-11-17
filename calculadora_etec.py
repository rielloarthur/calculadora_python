# Importa a biblioteca tkinter (interface gráfica) e a apelida de "tk"
import tkinter as tk


# Define a classe Calculadora, que agrupa toda a lógica e a interface
class Calculadora:
    # Construtor: roda automaticamente ao criar uma Calculadora; recebe a janela principal
    def __init__(self, janela):
        # Guarda a janela dentro do objeto para usá-la em outros métodos
        self.janela = janela
        # Define o título que aparece na barra da janela
        janela.title("Calculadora")
        # Impede redimensionar a janela (largura=False, altura=False)
        janela.resizable(False, False)

        # Texto da conta digitada até agora; começa vazio
        self.expressao = ""

        # Cria o campo de texto que funciona como visor
        self.visor = tk.Entry(
            janela, font=("Arial", 24), justify="right",  # janela pai, fonte Arial 24, texto alinhado à direita
            bd=8, relief="sunken", state="readonly"  # borda de 8px, efeito "afundado", só leitura (não digita direto)
        )
        # Posiciona o visor na linha 0, ocupando as 4 colunas e esticando em todas as direções
        self.visor.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Botões (texto de cada linha)
        botoes = [
            ["C", "(", ")", "/"],  # linha 1: limpar, parênteses e divisão
            ["7", "8", "9", "*"],  # linha 2: números e multiplicação
            ["4", "5", "6", "-"],  # linha 3: números e subtração
            ["1", "2", "3", "+"],  # linha 4: números e soma
            ["0", ",", "⌫", "="],  # linha 5: zero, vírgula, apagar e igual
        ]  # fim da lista de botões

        # Percorre cada linha; i = número da linha na grade (começa em 1, pois a 0 é o visor)
        for i, linha in enumerate(botoes, start=1):
            # Percorre cada botão da linha; j = coluna, texto = o que está escrito no botão
            for j, texto in enumerate(linha):
                # Função que será chamada ao clicar; "t=texto" fixa o valor de texto deste botão
                def executar(t=texto):
                    # Envia o texto do botão para o método clicar
                    self.clicar(t)

                # Cria o botão
                tk.Button(
                    janela, text=texto, font=("Arial", 18), width=4, height=2,  # janela pai, texto, fonte, largura e altura
                    command=executar  # função chamada quando o botão é clicado
                # Posiciona o botão na grade, esticando e com 1px de espaço em volta
                ).grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

        # Permite usar o teclado
        # Qualquer tecla pressionada chama o método tecla
        janela.bind("<Key>", self.tecla)
        # A tecla Enter chama o método tecla_enter
        janela.bind("<Return>", self.tecla_enter)
        # A tecla Backspace chama o método tecla_backspace
        janela.bind("<BackSpace>", self.tecla_backspace)

    # Método que mostra um texto no visor
    def atualizar_visor(self, texto):
        # Libera o visor para edição (ele é readonly)
        self.visor.config(state="normal")
        # Apaga todo o conteúdo atual, do índice 0 até o fim
        self.visor.delete(0, tk.END)
        # Insere o novo texto na posição 0
        self.visor.insert(0, texto)
        # Trava o visor de novo, só para leitura
        self.visor.config(state="readonly")

    # Método que trata qualquer clique (de botão ou teclado); valor = texto do botão
    def clicar(self, valor):
        # Se o botão for "C"...
        if valor == "C":
            # ...zera a expressão
            self.expressao = ""
        # Se for o botão de apagar...
        elif valor == "⌫":
            # ...remove o último caractere da expressão
            self.expressao = self.expressao[:-1]
        # Se for o botão de igual...
        elif valor == "=":
            # Tenta calcular; se algo der errado, cai no except
            try:
                # Troca a vírgula por ponto, pois o Python só entende ponto decimal
                numeros_sem_vircula= self.expressao.replace(",", ".")
                # Esta linha não tem efeito: o resultado do replace não é guardado em nenhuma variável
                self.expressao.replace(",", ".")
                # Calcula a conta que está escrita como texto
                resultado = eval(numeros_sem_vircula)
                # Converte o resultado para texto e o deixa como nova expressão (permite continuar a conta)
                self.expressao = str(resultado)
            # Captura qualquer erro (ex.: divisão por zero, conta incompleta)
            except Exception:
                # Limpa a expressão
                self.expressao = ""
                # Mostra "Erro" no visor
                self.atualizar_visor("Erro")
                # Sai do método para não sobrescrever o "Erro" na linha final
                return
        # Para qualquer outro botão (números, operadores, parênteses, vírgula)...
        else:
            # ...adiciona o caractere ao final da expressão
            self.expressao += valor
        # Mostra a expressão no visor, trocando ponto por vírgula (formato brasileiro)
        self.atualizar_visor(self.expressao.replace(".", ","))

    # Método chamado quando qualquer tecla é pressionada; evento traz informações da tecla
    def tecla(self, evento):
        # Verifica se o caractere digitado é um dos permitidos
        if evento.char in "0123456789+-*/,()":
            # Se for, trata como se tivesse clicado no botão correspondente
            self.clicar(evento.char)

    # Método chamado ao pressionar Enter
    def tecla_enter(self, evento):
        # Age como o botão "="
        self.clicar("=")

    # Método chamado ao pressionar Backspace
    def tecla_backspace(self, evento):
        # Age como o botão "⌫"
        self.clicar("⌫")


# Só executa o bloco abaixo se o arquivo for rodado diretamente (não importado por outro)
if __name__ == "__main__":
    # Cria a janela principal do tkinter
    janela = tk.Tk()
    # Cria a calculadora dentro dessa janela
    Calculadora(janela)
    # Inicia o loop que mantém a janela aberta e respondendo a cliques e teclas
    janela.mainloop()
