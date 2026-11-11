import tkinter as tk


class Calculadora:
    def __init__(self, janela):
        self.janela = janela
        janela.title("Calculadora")
        janela.resizable(False, False)

        self.expressao = ""

        # Visor
        self.visor = tk.Entry(
            janela, font=("Arial", 24), justify="right",
            bd=8, relief="sunken", state="readonly"
        )
        self.visor.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Botões (texto de cada linha)
        botoes = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "⌫", "="],
        ]

        for i, linha in enumerate(botoes, start=1):
            for j, texto in enumerate(linha):
                tk.Button(
                    janela, text=texto, font=("Arial", 18), width=4, height=2,
                    command=lambda t=texto: self.clicar(t)
                ).grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

        # Permite usar o teclado
        janela.bind("<Key>", self.tecla)
        janela.bind("<Return>", lambda e: self.clicar("="))
        janela.bind("<BackSpace>", lambda e: self.clicar("⌫"))

    def atualizar_visor(self, texto):
        self.visor.config(state="normal")
        self.visor.delete(0, tk.END)
        self.visor.insert(0, texto)
        self.visor.config(state="readonly")

    def clicar(self, valor):
        if valor == "C":
            self.expressao = ""
        elif valor == "⌫":
            self.expressao = self.expressao[:-1]
        elif valor == "=":
            try:
                # eval é aceitável aqui porque só chegam caracteres permitidos
                resultado = eval(self.expressao)
                self.expressao = str(resultado)
            except Exception:
                self.expressao = ""
                self.atualizar_visor("Erro")
                return
        else:
            self.expressao += valor
        self.atualizar_visor(self.expressao)

    def tecla(self, evento):
        if evento.char in "0123456789+-*/.()":
            self.clicar(evento.char)


if __name__ == "__main__":
    janela = tk.Tk()
    Calculadora(janela)
    janela.mainloop()