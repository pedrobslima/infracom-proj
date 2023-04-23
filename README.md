[Projeto de infracom para o dia 23/04]

- O servidor é representado por server.py

- A pasta do servidor, no início, só possui um arquivo filler, para impedir que o github não apague a pasta na hora do push. Será onde os arquivos recebidos por server.py serão armazenados

- O cliente é representado por client.py

- Ambos client.py e server.py tem uma variável 'PROBAB_PERDA'. Quem for rodar o código pode mudá-la, em cada um dos arquivos, para alterar a probabilidade de perdas de pacote na hora da transferência de arquivos (mais detalhes no código)
  - No client.py a declaração da variável é na linha 17
  - No server.py a declaração da variável é na linha 8
  - A função para a geração de perdas está em funcoes.py

- A pasta do cliente, no início, possui 3 arquivos que poderão ser usados como teste para a transferência, além de ser a pasta em que as cópias dos arquivos, vindas do servidor, serão armazenadas

- funcoes.py é onde se encontram todas as funções criadas, que usadas tanto em client.py como em server.py
