/**
 * ============================================
 * TESOURO DIRETO - GOOGLE SHEETS FUNCTION
 * ============================================
 * 
 * Função personalizada para Google Sheets
 * que consome os dados do arquivo JSON
 * hospedado no GitHub.
 * 
 * EXEMPLOS:
 * 
 * =TESOURO_DIRETO("Tesouro Selic 2027";"preco")
 * 
 * =TESOURO_DIRETO("Tesouro Selic 2027";"preco";"vencimento")
 * 
 * =TESOURO_DIRETO("IPCA 2035";"tipo";"preco";"rendimento")
 * 
 * ============================================
 * PARÂMETROS DISPONÍVEIS
 * ============================================
 * 
 * "preco"
 * "rendimento"
 * "vencimento"
 * "tipo"
 * 
 * ============================================
 */

function TESOURO_DIRETO(titulo) {

  // ============================================
  // URL DO JSON
  // ============================================

  const url =
    "COLE_AQUI_O_LINK_RAW_DO_JSON";

  // ============================================
  // CAPTURA PARÂMETROS
  // ============================================

  const parametros =
    Array.from(arguments).slice(1);

  // ============================================
  // BAIXA JSON
  // ============================================

  const response = UrlFetchApp.fetch(url);

  const dados = JSON.parse(
    response.getContentText()
  );

  // ============================================
  // PROCURA TÍTULO
  // ============================================

  const tituloEncontrado =
    dados.titulos.find(t =>

      t.titulo
        .toLowerCase()
        .includes(
          titulo
            .toLowerCase()
            .trim()
        )

    );

  // ============================================
  // TÍTULO NÃO ENCONTRADO
  // ============================================

  if (!tituloEncontrado) {

    return "Título não encontrado";

  }

  // ============================================
  // MAPEAMENTO DOS PARÂMETROS
  // ============================================

  const mapa = {

    rendimento: "rendimento_anual",

    preco: "preco_resgate",

    vencimento: "vencimento",

    tipo: "tipo"

  };

  // ============================================
  // MONTA RESULTADO
  // ============================================

  const resultado = parametros.map(p => {

    const chave =
      mapa[
        p
          .toLowerCase()
          .trim()
      ];

    return chave
      ? tituloEncontrado[chave]
      : "Parâmetro inválido";

  });

  // ============================================
  // RETORNA RESULTADO
  // ============================================

  return [resultado];

}
