import sys

# O console do Windows (cp1252) não imprime emoji e quebra com UnicodeEncodeError.
# Esta linha força a saída em UTF-8. (Inofensiva no Linux/Mac.)
sys.stdout.reconfigure(encoding="utf-8")

from agents import (
    Agent, Runner, RunContextWrapper,
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered,
    input_guardrail, TResponseInputItem,
)

from provedor import configurar

configurar()

@input_guardrail
def bloquear_off_topics(
        ctx: RunContextWrapper,
        agent: Agent,
        input: list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    texto = input if isinstance(input, str) else str(input)
    proibidos = ["religião", "política", "sexo", "pornografia", "violência", "futebol", "fofoca"]

    print(texto)

    violou = False
    motivo = "ok"
    for palavra in proibidos:
        if palavra in texto.lower():
            violou = True
            motivo = f"Pergunta sobre '{palavra}' não é permitida."
            break

    return GuardrailFunctionOutput(
        tripwire_triggered=violou,
        output_info={"motivo": motivo}
    )


agente = Agent(
    name="tutor_programacao",
    instructions="Você é um tutor de programação.",
    input_guardrails=[bloquear_off_topics],
)


def main():
    try:
        runner = Runner.run_sync(agente, "Quem foi o campeão brasileiro de 1987?")
        print(runner.final_output)
    except InputGuardrailTripwireTriggered as e:
        print(f"Pergunta bloqueada: {e.guardrail_result.output.output_info['motivo']}")


main()
