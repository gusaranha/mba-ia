# ex00_chatbot_triagem_bo.py
# Ex.00 Chatbot - Chat de decisão para triagem de boletins de ocorrência
#
# Dependências: nenhuma (usa apenas Python puro / biblioteca padrão)

def limpar_tela():
    print("\n" + "=" * 55)

def exibir_cabecalho():
    print("=" * 55)
    print("     SISTEMA DE TRIAGEM DE BOLETIM DE OCORRÊNCIA")
    print("          Polícia Civil — Atendimento Digital")
    print("=" * 55)

def perguntar(texto, opcoes=None):
    """Exibe uma pergunta e retorna a resposta do usuário."""
    print(f"\n{texto}")
    if opcoes:
        for i, op in enumerate(opcoes, 1):
            print(f"  [{i}] {op}")
        while True:
            resposta = input("\n>>> Digite o número da opção: ").strip()
            if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
                return int(resposta)
            print("    Opção inválida. Tente novamente.")
    else:
        return input("\n>>> ").strip()

def resultado(tipo, urgencia, artigo, orientacao, cor=""):
    """Exibe o resultado final da triagem."""
    limpar_tela()
    print("\n  RESULTADO DA TRIAGEM")
    print("-" * 55)
    print(f"  Tipo de ocorrência : {tipo}")
    print(f"  Urgência           : {urgencia}")
    print(f"  Artigo do CP       : {artigo}")
    print("-" * 55)
    print(f"\n  ORIENTAÇÃO AO POLICIAL:")
    print(f"  {orientacao}")
    print("\n" + "=" * 55)
    print("  Atendimento encerrado. Registre o protocolo.")
    print("=" * 55 + "\n")

def fluxo_patrimonio():
    """Sub-fluxo para crimes contra o patrimônio."""
    houve_violencia = perguntar(
        "Houve uso de violência ou grave ameaça durante o crime?",
        ["Sim", "Não"]
    )

    if houve_violencia == 1:
        # Com violência → Roubo
        vitima_ferida = perguntar(
            "A vítima sofreu lesões físicas?",
            ["Sim, lesões graves (hospitalização)", "Sim, lesões leves", "Não"]
        )

        if vitima_ferida == 1:
            resultado(
                tipo="LATROCÍNIO (tentativa) ou ROUBO MAJORADO",
                urgencia="🔴 URGÊNCIA ALTA — Ação imediata",
                artigo="Art. 157 §3º CP",
                orientacao="Acionar SAMU imediatamente. Preservar cena. "
                           "Isolar área e acionar delegacia especializada."
            )
        elif vitima_ferida == 2:
            resultado(
                tipo="ROUBO COM LESÃO CORPORAL",
                urgencia="🟠 URGÊNCIA MÉDIA-ALTA",
                artigo="Art. 157 §§1º e 2º CP",
                orientacao="Verificar se vítima precisa de atendimento médico. "
                           "Coletar descrição do suspeito e registro das lesões."
            )
        else:
            resultado(
                tipo="ROUBO SIMPLES",
                urgencia="🟠 URGÊNCIA MÉDIA",
                artigo="Art. 157 caput CP",
                orientacao="Colher descrição detalhada do suspeito e do bem subtraído. "
                           "Verificar câmeras na região. Registrar BO."
            )

    else:
        # Sem violência → Furto
        bem_subtraido = perguntar(
            "O que foi subtraído?",
            ["Veículo", "Residência/estabelecimento arrombado", "Celular/carteira/objetos pessoais", "Outros"]
        )

        if bem_subtraido == 1:
            resultado(
                tipo="FURTO DE VEÍCULO",
                urgencia="🟠 URGÊNCIA MÉDIA",
                artigo="Art. 155 §5º CP",
                orientacao="Registrar placa, modelo e cor do veículo. "
                           "Acionar sistema de alerta para veículos furtados (INFOSEG). "
                           "Verificar câmeras de trânsito na área."
            )
        elif bem_subtraido == 2:
            resultado(
                tipo="FURTO QUALIFICADO (arrombamento)",
                urgencia="🟠 URGÊNCIA MÉDIA",
                artigo="Art. 155 §4º I e II CP",
                orientacao="Preservar cena para perícia. Não tocar na área de entrada. "
                           "Acionar perito para coleta de impressões digitais."
            )
        elif bem_subtraido == 3:
            resultado(
                tipo="FURTO SIMPLES",
                urgencia="🟡 URGÊNCIA BAIXA",
                artigo="Art. 155 caput CP",
                orientacao="Colher descrição de possíveis suspeitos e testemunhas. "
                           "Verificar câmeras de segurança do local. Registrar BO."
            )
        else:
            resultado(
                tipo="FURTO SIMPLES",
                urgencia="🟡 URGÊNCIA BAIXA",
                artigo="Art. 155 caput CP",
                orientacao="Registrar os bens subtraídos com valor estimado. "
                           "Colher dados de testemunhas se houver. Registrar BO."
            )

def fluxo_violencia_pessoa():
    """Sub-fluxo para crimes contra a pessoa."""
    tipo_violencia = perguntar(
        "Qual o tipo de situação?",
        ["Violência doméstica (Lei Maria da Penha)", "Briga/agressão entre desconhecidos",
         "Ameaça (sem agressão física)", "Homicídio ou tentativa de homicídio"]
    )

    if tipo_violencia == 1:
        vitima_segura = perguntar(
            "A vítima está em local seguro agora?",
            ["Sim, está em segurança", "Não, o agressor ainda está presente"]
        )

        if vitima_segura == 2:
            resultado(
                tipo="VIOLÊNCIA DOMÉSTICA — SITUAÇÃO ATIVA",
                urgencia="🔴 URGÊNCIA MÁXIMA — Intervenção imediata",
                artigo="Art. 129 §9º CP + Lei 11.340/2006",
                orientacao="DESLOCAR VIATURA IMEDIATAMENTE. Separar agressor da vítima. "
                           "Verificar medida protetiva vigente. "
                           "Acionar serviço social e delegacia de VD."
            )
        else:
            lesoes = perguntar(
                "A vítima apresenta lesões visíveis?",
                ["Sim, lesões graves", "Sim, lesões leves", "Não, mas houve ameaça"]
            )

            if lesoes == 1:
                resultado(
                    tipo="LESÃO CORPORAL DOLOSA GRAVE — VIOLÊNCIA DOMÉSTICA",
                    urgencia="🔴 URGÊNCIA ALTA",
                    artigo="Art. 129 §§1º e 9º CP + Lei 11.340/2006",
                    orientacao="Encaminhar vítima para IML com urgência. "
                               "Registrar lesões fotograficamente. "
                               "Verificar necessidade de medida protetiva de urgência."
                )
            elif lesoes == 2:
                resultado(
                    tipo="LESÃO CORPORAL DOLOSA LEVE — VIOLÊNCIA DOMÉSTICA",
                    urgencia="🟠 URGÊNCIA MÉDIA-ALTA",
                    artigo="Art. 129 §9º CP + Lei 11.340/2006",
                    orientacao="Encaminhar ao IML para exame de corpo de delito. "
                               "Aplicar formulário de avaliação de risco. "
                               "Orientar sobre medidas protetivas disponíveis."
                )
            else:
                resultado(
                    tipo="AMEAÇA — VIOLÊNCIA DOMÉSTICA",
                    urgencia="🟠 URGÊNCIA MÉDIA",
                    artigo="Art. 147 CP + Lei 11.340/2006",
                    orientacao="Colher depoimento detalhado. "
                               "Verificar histórico de ocorrências anteriores. "
                               "Orientar vítima sobre medida protetiva preventiva."
                )

    elif tipo_violencia == 2:
        resultado(
            tipo="LESÃO CORPORAL / VIAS DE FATO",
            urgencia="🟠 URGÊNCIA MÉDIA",
            artigo="Art. 129 caput CP",
            orientacao="Verificar se há necessidade de atendimento médico. "
                       "Identificar envolvidos e possíveis testemunhas. "
                       "Colher versões separadamente."
        )

    elif tipo_violencia == 3:
        resultado(
            tipo="AMEAÇA",
            urgencia="🟡 URGÊNCIA BAIXA-MÉDIA",
            artigo="Art. 147 CP",
            orientacao="Verificar se há registro de ocorrências anteriores do ameaçador. "
                       "Orientar sobre medida protetiva se houver relação doméstica. "
                       "Colher registros (mensagens, áudios) como prova."
        )

    else:
        resultado(
            tipo="HOMICÍDIO OU TENTATIVA — CENA ATIVA",
            urgencia="🔴 URGÊNCIA MÁXIMA — Protocolo de homicídio",
            artigo="Art. 121 CP (ou Art. 121 tentativa)",
            orientacao="ISOLAR A CENA IMEDIATAMENTE. Acionar DHPP/DEIC. "
                       "Não movimentar nenhum objeto. Registrar testemunhas presentes. "
                       "Acionar IML. Preservar câmeras de segurança da área."
        )

def fluxo_fraude():
    """Sub-fluxo para crimes de fraude e estelionato."""
    canal = perguntar(
        "Como o crime foi cometido?",
        ["Golpe por WhatsApp / ligação falsa (ex: falso banco)",
         "Compra/venda pela internet (produto não entregue ou falso)",
         "Fraude documental (documento falso, cheque sem fundo)",
         "Outro tipo de estelionato"]
    )

    if canal == 1:
        valor = perguntar(
            "Qual o valor aproximado do prejuízo?",
            ["Acima de R$ 5.000", "Entre R$ 500 e R$ 5.000", "Abaixo de R$ 500"]
        )

        if valor == 1:
            resultado(
                tipo="ESTELIONATO DIGITAL — ALTO VALOR",
                urgencia="🟠 URGÊNCIA MÉDIA-ALTA",
                artigo="Art. 171 §2º-A CP",
                orientacao="Orientar vítima a bloquear transferências com o banco IMEDIATAMENTE. "
                           "Colher print das conversas e comprovantes. "
                           "Registrar CNPJ/número usado pelo golpista para investigação."
            )
        else:
            resultado(
                tipo="ESTELIONATO DIGITAL",
                urgencia="🟡 URGÊNCIA BAIXA-MÉDIA",
                artigo="Art. 171 §2º-A CP",
                orientacao="Colher prints de todas as conversas e comprovantes de transferência. "
                           "Registrar número/conta usada pelo golpista. "
                           "Orientar registro no banco e cancelamento de transações."
            )

    elif canal == 2:
        resultado(
            tipo="ESTELIONATO — FRAUDE EM COMÉRCIO ELETRÔNICO",
            urgencia="🟡 URGÊNCIA BAIXA",
            artigo="Art. 171 caput CP",
            orientacao="Colher prints dos anúncios, conversas e comprovantes de pagamento. "
                       "Registrar dados do vendedor (perfil, CPF/CNPJ se disponível). "
                       "Orientar registro no PROCON e plataforma utilizada."
        )

    elif canal == 3:
        resultado(
            tipo="FALSIFICAÇÃO DE DOCUMENTO / ESTELIONATO",
            urgencia="🟠 URGÊNCIA MÉDIA",
            artigo="Art. 297 e/ou Art. 171 CP",
            orientacao="Preservar o documento falso como prova (não devolver). "
                       "Solicitar perícia documental. "
                       "Identificar o apresentador do documento."
        )

    else:
        resultado(
            tipo="ESTELIONATO",
            urgencia="🟡 URGÊNCIA BAIXA",
            artigo="Art. 171 caput CP",
            orientacao="Colher toda documentação disponível como prova. "
                       "Identificar o autor se possível. Registrar BO detalhado."
        )

def iniciar_atendimento():
    """Fluxo principal do chat de decisão."""
    exibir_cabecalho()

    print("\n  Bem-vindo ao sistema de triagem de ocorrências.")
    print("  Vou fazer algumas perguntas para orientar o atendimento.")

    continuar = True

    while continuar:
        limpar_tela()

        # Coleta do nome da vítima
        nome = perguntar("Qual o nome da vítima ou solicitante?")
        if not nome:
            nome = "não informado"

        print(f"\n  Olá, {nome.split()[0].capitalize()}! Vamos iniciar a triagem.\n")

        # Pergunta principal: tipo de crime
        categoria = perguntar(
            "Qual o tipo de ocorrência que deseja registrar?",
            [
                "Crime contra o patrimônio (furto, roubo, arrombamento)",
                "Violência contra a pessoa (agressão, ameaça, homicídio)",
                "Fraude / estelionato (golpe, fraude digital, engano)",
                "Não sei classificar / outros"
            ]
        )

        limpar_tela()

        if categoria == 1:
            fluxo_patrimonio()
        elif categoria == 2:
            fluxo_violencia_pessoa()
        elif categoria == 3:
            fluxo_fraude()
        else:
            print("\n  ENCAMINHAMENTO PARA ATENDIMENTO HUMANO")
            print("-" * 55)
            print("  Ocorrências não classificadas precisam de análise")
            print("  de um policial. Dirija-se ao balcão de atendimento")
            print("  ou ligue 190 para situações de emergência.")
            print("=" * 55)

        # Pergunta se quer novo atendimento
        novo = input("\n  Deseja registrar outra ocorrência? (s/n): ").strip().lower()
        if novo not in ("s", "sim"):
            continuar = False

    print("\n  Obrigado por usar o sistema de triagem digital.")
    print("  Em caso de emergência, ligue 190.\n")

# ── Ponto de entrada ─────────────────────────────────────────
if __name__ == "__main__":
    iniciar_atendimento()
