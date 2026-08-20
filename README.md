# Visualizador de Poços

Repositório dedicado à visualização interativa de poços, perfis compostos e dados geoespaciais associados à área de estudo.

O projeto tem como objetivo disponibilizar uma interface web para a localização dos poços em mapa e para o acesso aos respectivos perfis compostos, permitindo a exploração integrada dos dados utilizados na pesquisa.

---

## Visualização

O visualizador interativo será disponibilizado por meio do GitHub Pages.

**Acessar o visualizador:**
https://daniellesimeao.github.io/Visualizador-Pocos/

> O visualizador encontra-se em desenvolvimento e será atualizado progressivamente à medida que novos dados e funcionalidades forem incorporados ao projeto.

---

## Dados

O repositório reúne dados utilizados para a localização e visualização dos poços, bem como os respectivos perfis compostos.

Os principais conjuntos de dados incluem:

* localização dos poços;
* dados geoespaciais utilizados como base cartográfica;
* perfis compostos dos poços em formato PDF;
* informações associadas aos poços;
* marcadores estratigráficos e outros dados de interesse, quando disponíveis.

Os dados serão organizados de forma a permitir sua utilização tanto no visualizador web quanto em outros ambientes de análise geocientífica.

---

## Organização do repositório

A estrutura do repositório está organizada da seguinte forma:

```text
Visualizador-Pocos/
│
├── dados/
│   ├── pocos.geojson
│   └── raster/
│
├── perfis/
│   ├── P01.pdf
│   ├── P02.pdf
│   ├── P03.pdf
│   └── ...
│
├── imagens/
│
├── modelo/
│
├── index.html
├── README.md
├── CITAÇÃO.cff
├── LICENÇA
└── DADOS DE LICENÇA
```

A estrutura poderá ser modificada conforme novas funcionalidades e conjuntos de dados sejam incorporados ao projeto.

---

## Poços

A localização dos poços será representada espacialmente no visualizador por meio de dados geográficos.

Os dados originalmente disponíveis em formato Shapefile poderão ser convertidos para formatos adequados à visualização web, como GeoJSON.

Cada poço poderá apresentar informações básicas, como:

* identificação do poço;
* localização;
* coordenadas;
* profundidade, quando disponível;
* informações complementares;
* acesso ao respectivo perfil composto.

---

## Perfis compostos

Os perfis compostos dos poços são disponibilizados em formato PDF.

A partir do mapa interativo, o usuário poderá selecionar um poço e acessar o respectivo perfil composto.

A estrutura de correspondência entre poços e perfis será organizada de forma padronizada, permitindo a associação entre cada ponto espacial e seu arquivo correspondente.

Exemplo:

```text
P01 → perfis/P01.pdf
P02 → perfis/P02.pdf
P03 → perfis/P03.pdf
```

---

## Base cartográfica

O visualizador utilizará dados raster e outros dados geoespaciais como base para a representação espacial da área de estudo.

Esses dados serão utilizados como plano de fundo para a localização e visualização dos poços.

A estrutura e o formato definitivo dos dados raster serão definidos de acordo com suas características espaciais, resolução e tamanho dos arquivos.

---

## Funcionalidades

O projeto está sendo desenvolvido de forma incremental.

As funcionalidades previstas incluem:

* visualização interativa da área de estudo;
* localização dos poços em mapa;
* navegação e zoom no mapa;
* identificação dos poços;
* visualização das informações associadas aos poços;
* acesso aos perfis compostos em PDF;
* visualização de dados geoespaciais de referência;
* identificação de marcadores estratigráficos;
* organização dos poços por diferentes atributos.

Em etapas posteriores, poderão ser incorporadas funcionalidades para visualização interativa das curvas dos perfis geofísicos e dos respectivos picks estratigráficos.

---

## Desenvolvimento

O visualizador é desenvolvido como uma aplicação web utilizando tecnologias compatíveis com o GitHub Pages.

A aplicação será estruturada de forma a separar:

* dados;
* arquivos dos perfis;
* elementos gráficos;
* código da aplicação;
* documentação.

Essa organização permite atualizar os dados sem a necessidade de reconstruir integralmente a aplicação.

---

## Licenças

Este repositório poderá utilizar licenças distintas para o código da aplicação e para os dados disponibilizados.

O código utilizado no desenvolvimento do visualizador será disponibilizado sob a licença indicada no arquivo correspondente.

As condições de uso dos dados geoespaciais, perfis compostos e demais materiais científicos serão definidas de acordo com sua origem e respectivas condições de distribuição.

Consulte os arquivos de licença deste repositório antes de reutilizar ou redistribuir qualquer material.

---

## Citação

Caso os dados, o visualizador, os perfis compostos ou outros materiais disponibilizados neste repositório sejam utilizados em trabalhos científicos, recomenda-se citar o repositório e as respectivas fontes dos dados.

A forma oficial de citação será disponibilizada no arquivo [`CITAÇÃO.cff`](CITAÇÃO.cff).

Informações adicionais sobre autoria, publicação e DOI serão incorporadas ao repositório quando estiverem disponíveis.

---

## DOI e arquivamento

Informações sobre DOI e arquivamento permanente do repositório serão disponibilizadas nesta seção quando o projeto for registrado em um serviço de preservação de dados.

---

## Autoria

**Danielle Simeão Silvério Rocha**

Projeto de pesquisa em Geociências

Universidade Federal do Pará — UFPA

---

## Status do projeto

**Em desenvolvimento.**

O visualizador está sendo desenvolvido progressivamente, com a incorporação e organização dos dados de poços, perfis compostos e informações geoespaciais.

Novas funcionalidades serão adicionadas conforme o desenvolvimento do projeto.

---

## Acesso ao código

O código-fonte e os dados disponibilizados neste projeto podem ser consultados neste repositório.

O visualizador será disponibilizado publicamente por meio do GitHub Pages após sua configuração.
