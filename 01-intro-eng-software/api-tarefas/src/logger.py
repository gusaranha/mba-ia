from datetime import datetime
import logging
import json
import sys


# Configuração global de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("app")

def log_structured(level: str, event: str, **kwargs):
    """
    Função auxiliar para criar logs estruturados em JSON.

    ✅ Logs em JSON são:
    - Indexáveis (CloudWatch, Datadog, Elastic)
    - Consultáveis (queries complexas)
    - Alertáveis (triggers automáticos)
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "event": event,
        **kwargs
    }

    if level == "ERROR":
        logger.error(json.dumps(log_entry))
    elif level == "WARNING":
        logger.warning(json.dumps(log_entry))
    elif level == "INFO":
        logger.info(json.dumps(log_entry))
    else:
        logger.debug(json.dumps(log_entry))