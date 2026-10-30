"""Testes do research.py check.
Rodar: uv run --no-project --with pytest --with pyyaml pytest plugins/sdd/skills/sdd-setup/scripts/tests"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent

GOOD = """---
tipo: concorrentes
---
# Concorrentes

O segmento cresceu 18% em 2025 [1] e movimentou R$ 2,3 bilhões [2].
A base estimada é de 40 mil clientes (estimativa: 2 fontes divergentes).
Em 2026 o produto lançou a versão 3 sem número quantitativo.

| Concorrente | Preço | Clientes |
|---|---|---|
| Alfa | R$ 99/mês [3] | 12 mil [3] |

```
exemplo 50% dentro de código não conta
```

## Limites da pesquisa

- Sem dados de 30% do mercado informal.

## Fontes

- [1] Relatório Setorial ABC — https://exemplo.org/rel — acessado em 2026-10-30
- [2] Notícia — https://exemplo.com/n — acessado em 30/10/2026
- [3] Site da Alfa, página de preços — https://alfa.com/precos — acessado em 2026-10-30
"""


def run(path: Path):
    result = subprocess.run([sys.executable, str(SCRIPTS / "research.py"), "check", str(path)],
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout.strip()
    return result.returncode, (text if text.startswith("error:") else json.loads(text))


def test_documento_valido(tmp_path):
    path = tmp_path / "c.md"
    path.write_text(GOOD, encoding="utf-8")
    code, result = run(path)
    assert code == 0 and result["valid"], result["problems"]
    assert result["sources"] == 3 and result["warnings"] == []


def test_aponta_numero_sem_fonte_e_fonte_incompleta(tmp_path):
    bad = GOOD.replace("cresceu 18% em 2025 [1] e movimentou", "cresceu 18% em 2025. Ele movimentou") \
              .replace("— https://exemplo.com/n — acessado em 30/10/2026", "— sem link") \
              .replace("| 12 mil [3] |", "| 12 mil [4] |")
    bad += "\nUS$ 5 por usuário segundo o mercado.\n"
    path = tmp_path / "c.md"
    path.write_text(bad, encoding="utf-8")
    code, result = run(path)
    joined = "\n".join(result["problems"])
    assert code == 0 and not result["valid"]
    assert "número sem fonte" in joined and "cresceu 18%" in joined
    assert "fonte [2] sem link" in joined and "fonte [2] sem data" in joined
    assert "[4] citado, mas não está" in joined
    assert "US$ 5" not in joined, "linha depois de ## Fontes é tratada como seção Fontes"
    assert result["warnings"] == ["fonte [1] declarada e não citada"]


def test_arquivo_inexistente(tmp_path):
    code, message = run(tmp_path / "x.md")
    assert code == 1 and "não existe" in message
