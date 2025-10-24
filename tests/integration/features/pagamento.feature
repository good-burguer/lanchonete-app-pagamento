Feature: Gerenciamento de pagamentos
  Como usuário da API de pagamentos
  Quero poder criar, consultar, atualizar, listar e deletar pagamentos
  Para que os pedidos sejam gerenciados corretamente

  # -----------------------------
  # Cenário: Criar pagamento
  # -----------------------------
  Scenario: Criar um pagamento com sucesso
    Given que eu tenho um payload de pagamento válido
    When eu envio um POST para "/pagamento"
    Then o status HTTP deve ser 201
    And a resposta deve conter "codigo_pagamento" e "status"

  Scenario: Criar pagamento com dados inválidos
    Given que eu tenho um payload de pagamento inválido
    When eu envio um POST para "/pagamento"
    Then o status HTTP deve ser 400
    And a mensagem de erro deve indicar campos obrigatórios

  # -----------------------------
  # Cenário: Buscar pagamento
  # -----------------------------
  Scenario: Buscar um pagamento existente
    Given que existe um pagamento criado
    When eu envio um GET para "/pagamento/{codigo_pagamento}"
    Then o status HTTP deve ser 200
    And a resposta deve conter "pedido_id" e "status"

  Scenario: Buscar um pagamento inexistente
    Given que não existe pagamento com o código "999"
    When eu envio um GET para "/pagamento/999"
    Then o status HTTP deve ser 404
    And a mensagem de erro deve indicar "Pagamento não encontrado"

  # -----------------------------
  # Cenário: Listar pagamentos
  # -----------------------------
  Scenario: Listar todos os pagamentos
    Given que existem pagamentos criados
    When eu envio um GET para "/pagamento"
    Then o status HTTP deve ser 200
    And a lista de pagamentos não deve estar vazia

  # -----------------------------
  # Cenário: Atualizar pagamento
  # -----------------------------
  Scenario: Atualizar um pagamento existente
    Given que existe um pagamento criado
    And eu tenho um payload de atualização válido
    When eu envio um PUT para "/pagamento/{codigo_pagamento}"
    Then o status HTTP deve ser 200
    And a resposta deve refletir a atualização

  Scenario: Atualizar um pagamento inexistente
    Given que não existe pagamento com o código "999"
    And eu tenho um payload de atualização válido
    When eu envio um PUT para "/pagamento/999"
    Then o status HTTP deve ser 404
    And a mensagem de erro deve indicar "Pagamento não encontrado"

  # -----------------------------
  # Cenário: Deletar pagamento
  # -----------------------------
  Scenario: Deletar um pagamento existente
    Given que existe um pagamento criado
    When eu envio um DELETE para "/pagamento/{codigo_pagamento}"
    Then o status HTTP deve ser 204

  Scenario: Deletar um pagamento inexistente
    Given que não existe pagamento com o código "999"
    When eu envio um DELETE para "/pagamento/999"
    Then o status HTTP deve ser 404
    And a mensagem de erro deve indicar "Pagamento não encontrado"
