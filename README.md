# coronavirus_data_colector

## corona.py
o script corona.py coleta dados de casos, mortes e recuperações do site https://www.worldometers.info/coronavirus/ e salva em um csv chamado corona.csv.

é possivel coletar dados de um país específico ao usa-lo como argumento na execução pelo terminal

## corona_regex.py
similar ao corona.py mas ao invés de usar requests-html ele usa regex

## create_crontab.py
o script create_crontab.py cria uma tarefa no linux que irá executar o script corona.py a cada 20 minutos
para especificar venv incluir como primeiro parâmetro ao executar script no terminal
para especificar pais incluir como segundo parãmetro ao executar script no terminal(caso não queira especificar a venv deixe primeiro argumento como 'local')
ex: python3 create_crontab.py local brazil
