/**
 * ============================================
 * TESOURO DIRETO - GOOGLE SHEETS FUNCTION
 * ============================================
 * 
 * Função personalizada para Google Sheets
 * que consome os dados do arquivo JSON
 * hospedado no GitHub.
 * 
 * ============================================
 * EXEMPLOS
 * ============================================
 * 
 * =TESOURO_DIRETO(
 *   "Tesouro Selic 2027";
 *   "Preco Resgate"
 * )
 * 
 * =TESOURO_DIRETO(
 *   "Tesouro Selic 2027";
 *   "Preco Compra";
 *   "Taxa Compra"
 * )
 * 
 * =TESOURO_DIRETO(
 *   "IPCA 2035";
 *   "Tipo";
 *   "Vencimento";
 *   "Atualizacao"
 * )
 * 
 * ============================================
 * PARÂMETROS DISPONÍVEIS
 * ============================================
 * 
 * "Taxa Resgate"
 * "Taxa Compra"
 * "Preco Resgate"
 * "Preco Compra"
 * "Vencimento"
 * "Tipo"
 * "Atualizacao"
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

    "taxa resgate": "taxa_resgate",

    "taxa compra": "taxa_compra",

    "preco resgate": "preco_resgate",

    "preco compra": "preco_compra",

    "vencimento": "vencimento",

    "tipo": "tipo"

  };

  // ============================================
  // MONTA RESULTADO
  // ============================================

  const resultado = parametros.map(p => {

    const parametro =
      p
        .toLowerCase()
        .trim();

    // ============================================
    // ATUALIZAÇÃO
    // ============================================

    if (parametro == "atualizacao") {

      return dados.atualizacao;

    }

    // ============================================
    // DADOS DO TÍTULO
    // ============================================

    const chave = mapa[parametro];

    return chave
      ? tituloEncontrado[chave]
      : "Parâmetro inválido";

  });

  // ============================================
  // RETORNA RESULTADO
  // ============================================

  return [resultado];

}
