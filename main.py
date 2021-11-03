
class Order():

    """
    Objeto característico das ordens.
    
    Parametros
    ----------
    type : Se a ordem deve ser executada apenas imediatamente(market) ou armazenada(limit)

    side : Se a ordem é de compra(buy) ou venda(sell)

    price: Preço máximo para compras ou mínimo para vendas das ordens de tipo limit.
           Recebe o valor -1 para ordens do tipo market

    qty  : Quantidade requisitada da ordem

    """

    def __init__(self, comando):

        temp = comando.split()

        if temp[0] == "market":
            self.type = "market"
            self.side = temp[1]
            self.price = -1
            self.qty = int(temp[2]) #TODO colocar try aqui

        elif temp[0] == "limit":
            self.type = "limit"
            self.side = temp[1] 
            self.price = int(temp[2]) #TODO colocar try aqui
            self.qty = int(temp[3]) #TODO colocar try aqui

        else:
            raise #TODO arrumar as exceções




class Ledger():
    """
    Objeto armazenador das ordens.
    
    Parametros
    ----------
    buy  : lista de listas das ordens de compra. As listas internas agrupam objetos Order
           que possuam mesmo preço ordenados pela ordem do pedido.

    sell : lista de listas das ordens de venda. As listas internas agrupam objetos Order
           que possuam mesmo preço ordenados pela ordem do pedido.

    
    Funções Públicas
    ----------------
    new  : permite adicionar nova ordem ao objeto através de uma string. Caso seja do
           tipo market executa imediatamente descantando qualquer parte que não pode ser
           executada. Caso seja do tipo limit, executa o que for possível, visto que é
           preferível uma execução, mesmo que parcial, imediata a sua não execução, e 
           armazena o restante no objeto.

    """


    def __init__(self):
        self.buy = []
        self.sell = []


    def _insert(self, order, ledgerSide):
        """
        Usa binary search para inserir um elemento em uma lista ordenada pelos preços.
        Resulta em lista de listas onde a lista externa está ordenada por preços e a
         lista interna por data

        Parametros
        ----------
        self : Ledger Object
            Ledger armazenador
        order : Order Object
            Ordem que esta sendo inserida
        ledgerSide : list
            Lista de compra ou venda do Ledger


        Retorno
        -------
        Int 0
            Retorna 0
        """

        n = len(ledgerSide)
        if n == 0:
            ledgerSide.append([order])
        else:
            l = 0
            r = n
            while l < r:
                m = (l+r)//2
                if ledgerSide[m][0].price == order.price:
                    ledgerSide[m].append(order)
                    return 0
                elif ledgerSide[m][0].price < order.price:
                    l = m + 1
                else:
                    r = m
            ledgerSide.insert(l, [order])
            return 0
        return 0


    def _update(self, ledgerSide):
        """
        Remove objetos Ordem com quantidade zero e listas sem elementos

        Parametros
        ----------
        self : Ledger Object
            Ledger armazenador
        ledgerSide : list
            Lista de compra ou venda do Ledger


        Retorno
        -------
        Int
            Retorna 1 caso tenha sido removido uma lista, simbolizando
             o fim dos elementos com mesmo preço
            Retorna 0 caso contrário
        """
        if ledgerSide[0][0].qty == 0:
            ledgerSide[0].pop(0)
        if len(ledgerSide[0]) == 0:
            ledgerSide.pop(0)
            return 1
        return 0


    def _executeBuy(self, order):
        """
        Realiza os trades de compra possíveis e retorna um objeto Order com o que não
        pode ser realizado.

        Parametros
        ----------
        self : Ledger Object
            Ledger armazenador
        order : Order object
            Ordem a ser executada


        Retorno
        -------
        Int
            Retorna um Objeto Order caso ainda haja resto após a operação
            Retorna None caso contrário
        """

        tempQty = 0
        tempPrice = 0
        while order.qty > 0 and (order.price >= self.sell[0][0].price or order.price == -1):
            if self.sell[0][0].qty >= order.qty:
                self.sell[0][0].qty -= order.qty
                print("Trade, price: ", self.sell[0][0].price," qty: ", order.qty)
                order.qty = 0
                self._update(self.sell)
                return None
            else:
                tempPrice = self.sell[0][0].price
                tempQty += self.sell[0][0].qty
                order.qty -= self.sell[0][0].qty
                self.sell[0][0].qty = 0
                if self._update(self.sell):
                    print("Trade, price: ", tempPrice," qty: ", tempQty)
                    tempPrice = 0
                    tempQty = 0 
            if len(self.sell) == 0:
                return order
        return order

    def _executeSell(self, order):
        """
        Realiza os trades de venda possíveis e retorna um objeto Order com o que não
        pode ser realizado.

        Parametros
        ----------
        self : Ledger Object
            Ledger armazenador
        order : Order object
            Ordem a ser executada


        Retorno
        -------
        Int
            Retorna um Objeto Order caso ainda haja resto após a operação
            Retorna None caso contrário
        """
        tempQty = 0
        tempPrice = 0
        while order.qty > 0 and (order.price <= self.buy[0][0].price or order.price == -1):
            if self.buy[0][0].qty >= order.qty:
                self.buy[0][0].qty -= order.qty
                print("Trade, price: ", self.buy[0][0].price," qty: ", order.qty)
                order.qty = 0
                self._update(self.buy)
                return None
            else:
                tempPrice = self.buy[0][0].price
                tempQty += self.buy[0][0].qty
                order.qty -= self.buy[0][0].qty
                self.buy[0][0].qty = 0
                if self._update(self.buy):
                    print("Trade, price: ", tempPrice," qty: ", tempQty)
                    tempPrice = 0
                    tempQty = 0
            if len(self.buy) == 0:
                return 0
        return order

    def _execute(self, order):
        """
        Direciona da ordem ao comando de execução a depender do
         tipo de ordem: limit ou market
         lado da operação: compra ou venda
        e lida com os casos especiais do _insert

        Parametros
        ----------
        self : Ledger Object
            Ledger armazenador
        order : Order object
            Ordem a ser executada


        Retorno
        -------
        Int
            Retorna 0 ao finalizar a operação
        """

        if order.type == "market": # ordem market
            if order.side == "buy":
                self._executeBuy(order)

            elif order.side == "sell":
                self._executeSell(order)


        else: #ordem limit
            if order.side == "buy":
                if len(self.sell) > 0: #verificar se pode ser executado
                    if self._executeBuy(order) == None:
                        return 0
                if len(self.buy) == 0:
                    self.buy.append([order])
                    return 0
                elif len(self.buy) == 1:
                    if order.price > self.buy[0][0].price:
                        self.buy.append([order])
                    elif order.price < self.buy[0][0].price:
                        self.buy = [[order], self.buy[0]]
                    else:
                        self.buy[0].append(order)
                    return 0
                else: #inserir
                    self._insert(order, self.buy)
            else: # side sell
                if len(self.buy) > 0: #verificar se pode ser executado
                    if self._executeSell(order) == None:
                        return 0
                if len(self.sell) == 0:
                    self.sell.append([order])
                    return 0
                elif len(self.sell) == 1:
                    if order.price > self.sell[0][0].price:
                        self.sell.append([order])
                    elif order.price < self.sell[0][0].price:
                        self.sell = [[order], self.sell[0]]
                    else:
                        self.sell[0].append(order)
                    return 0
                else: #inserir
                    self._insert(order, self.sell)

    def new(self, order):
        """
        Insere um novo elemento no Ledger após verificar se não é possível sua execução

        Parametros
        ----------
        self : Ledger Object
            Ledger armazenador
        order : Order object
            Ordem a ser executada


        Retorno
        -------
        Int
            Retorna um Objeto Order caso ainda haja resto após a operação
            Retorna None caso contrário
        """

        temp = Order(order)


        if not self._execute(temp):
            pass
        else:
            if temp.side == "buy":
                self._insert(temp, self.buy)
            else:
                self._insert(temp, self.sell)


def main():

    ledger = Ledger()

    print("Favor digitar as ordens no formato:"
            + " <limit ou market> <buy or sell> <preço> <quantidade>")

    while True:
        try:
            command = input(">")
            ledger.new(command)
        except:
            print("Comando inválido")


if __name__ == "__main__":
    main()


