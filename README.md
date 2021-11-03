# Matching Engine
 
 O programa realiza o match entre ordens de compra e venda de um único ativo. O programa tem preferencia primariamente por preços mais baixos
 e em segundo lugar por qual ordem chegou primeiro.
 
 Para executar o programa basta executar o arquivo main.py. O programa foi desenvolvido e testado na versão 3.9.0 do Python.

```python


# Exemplo
>>> limit buy 10 100
>>> limit buy 10 150
>>> limit buy 12 150
>>> market sell 300
Trade, price:  10  qty:  250
Trade, price:  12  qty:  50 
```

