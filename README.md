# Royal Life — vitrine de perfumes com busca por IA

Site institucional e catálogo de vendas para a **Royal Life**, uma marca de perfumes árabes e
importados. Feito em Django, com um catálogo navegável, painel administrativo customizado e uma
busca de produtos usando o **Gemini** para reconhecer perfumes a partir de uma foto ou do nome.

Não existe carrinho/checkout tradicional: toda intenção de compra é direcionada para o
**WhatsApp da loja**, com a mensagem já pré-preenchida com o nome e preço do produto — um modelo
comum em pequenos negócios que vendem por atendimento direto.

## Funcionalidades

- **Página inicial**: carrossel de lançamentos, campanha promocional em destaque (quando ativa),
  seção institucional (missão/valores/propósito) e botão flutuante de WhatsApp.
- **Coleção**: grade de perfumes com busca por nome/marca e filtro por gênero (masculino,
  feminino, unissex), tudo em tempo real no navegador (sem recarregar a página).
- **Busca por IA**: o cliente envia uma foto do frasco/caixa do perfume (ou só digita um nome) e o
  Gemini identifica o perfume e sugere até 3 produtos parecidos do catálogo da loja — útil para
  quem quer "achar um perfume parecido com esse" sem saber o nome exato.
- **Selos automáticos**: "Pronta Entrega" / "Sob Encomenda" conforme o estoque, e "Novo" para os
  lançamentos mais recentes.
- **Painel administrativo** (Django Admin) customizado:
  - Reordenação por arrastar e soltar dos perfumes dentro de cada campanha
    (`django-admin-sortable2`).
  - Cálculo automático de lucro (R$) e margem (%) por perfume, direto na listagem.
  - Slug de marca gerado automaticamente a partir do nome.

## Como funciona a busca por IA

O formulário de busca (por foto ou nome) é processado em
[`core/views.py`](core/views.py) (`_buscar_perfume_ia`). O fluxo:

1. Monta um prompt com o catálogo atual (nome, marca, gênero, notas olfativas) e pede ao Gemini
   para identificar o perfume da foto/nome e escolher até 3 parecidos do catálogo.
2. O modelo responde em JSON estrito, que é interpretado (`_extrair_json`) e casado com os
   perfumes reais do banco pelo ID.
3. A tela mostra o que foi identificado e os produtos parecidos encontrados na loja.

Modelo usado: `gemini-3.1-flash-lite` (constante `GEMINI_MODEL` em `core/views.py`).

## Stack técnica

- **Backend**: Django, `google-generativeai` (Gemini), Pillow (processamento de imagem).
- **Banco de dados**: SQLite em desenvolvimento; PostgreSQL em produção via `dj-database-url`.
- **Armazenamento de mídia**: Cloudinary em produção (se configurado), disco local em
  desenvolvimento.
- **Deploy**: Render, com `gunicorn` servindo a aplicação e `whitenoise` servindo os arquivos
  estáticos.
- **Frontend**: HTML + CSS + JavaScript puro nos templates Django (sem framework de frontend),
  com efeitos de scroll-reveal, modais e carrosséis feitos à mão.

## Rodando localmente

```bash
pip install -r requirements.txt
python manage.py migrate
python create_admin.py        # cria um usuário admin/admin no Django Admin
python manage.py runserver
```

Variáveis de ambiente relevantes (todas opcionais em desenvolvimento, têm valores padrão
seguros para rodar local):

| Variável | Para que serve |
|---|---|
| `GEMINI_API_KEY` | Habilita a busca por IA na Coleção. Sem ela, a busca mostra uma mensagem pedindo para falar pelo WhatsApp. |
| `SECRET_KEY` | Chave secreta do Django (defina uma própria em produção). |
| `DEBUG` | `True`/`False`. |
| `CLOUDINARY_URL` ou `CLOUDINARY_CLOUD_NAME`/`CLOUDINARY_API_KEY`/`CLOUDINARY_API_SECRET` | Ativa o armazenamento de imagens no Cloudinary. |
| `DATABASE_URL` | String de conexão do Postgres em produção (Render). |

## Estrutura

```
core/
  models.py     # Marca, Perfume, Campanha, CampanhaPerfume
  views.py      # home, colecao e a busca por IA (Gemini)
  admin.py      # customizações do Django Admin
  templates/    # home.html, colecao.html
setup/
  settings.py   # configuração do projeto (banco, mídia, Cloudinary)
  urls.py
create_admin.py # script para criar/atualizar o superusuário
```

## Possíveis melhorias

- Checkout de verdade (carrinho + pagamento), hoje tudo termina num link de WhatsApp.
- Testes automatizados (não há nenhum ainda).
- Internacionalizar `SECRET_KEY`/`DEBUG` com valores padrão mais restritivos por segurança.
