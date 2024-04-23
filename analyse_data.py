import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

arquivos_csv = [arquivo for arquivo in os.listdir() if arquivo.endswith('.csv')]

dados_concatenados = pd.DataFrame()

for arquivo in arquivos_csv:

    dados = pd.read_csv(arquivo)
    
    dados_concatenados = pd.concat([dados_concatenados, dados], ignore_index=True)

    print("Ok")

dados_concatenados.drop(columns=['Unnamed: 0'], inplace=True)

dados_concatenados = dados_concatenados.dropna()

dados_concatenados.reset_index(drop=True, inplace=True)

############ 1. Estatísticas Descritivas:

descritivas = dados_concatenados.describe()
print(descritivas)

############ 2. Correlações:

correlacao = dados_concatenados.corr()
print(correlacao)

plt.figure(figsize=(12, 8))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Matriz de Correlação')
plt.show()


############ 3. Relações com a Variável Alvo ("Crn"):

estatisticas_crn_por_time = dados_concatenados.groupby('Team')['Crn'].describe()
print(estatisticas_crn_por_time)

estatisticas_crn_por_clube = dados_concatenados.groupby('Club')['Crn'].describe()
print(estatisticas_crn_por_clube)

############ 4. Análise de Distribuição:

plt.figure(figsize=(12, 6))
sns.boxplot(data=dados_concatenados, x='Team', y='Crn')
plt.title('Distribuição de "Crn" por Time')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(data=dados_concatenados, x='Club', y='Crn')
plt.title('Distribuição de "Crn" por Clube')
plt.xticks(rotation=90)
plt.show()


############ 6. Análise Comparativa:

media_crn_por_time = dados_concatenados.groupby('Team')['Crn'].mean()
media_crn_por_clube = dados_concatenados.groupby('Club')['Crn'].mean()

print("Média de 'Crn' por Time:")
print(media_crn_por_time)
print("\nMédia de 'Crn' por Clube:")
print(media_crn_por_clube)

