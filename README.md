# Codex First Skills Pack

Публичный пакет инженерных skills для Codex и других Markdown-based coding agents.

Этот репозиторий помогает работать с Codex не как с одноразовым генератором
кода, а как с инженерным партнёром: сначала прояснять задачу, собирать
правильный контекст, проектировать решение, разбивать работу на проверяемые
шаги, сверяться с актуальными источниками, отлаживать по фактам, писать
проверки и делать ревью перед тем, как считать работу готовой.

Пакет вдохновлён репозиторием
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), но не
является его зеркалом. Это компактная Codex-oriented адаптация с фокусом на
ежедневный engineering workflow.

## Что Это Такое

Skills в Codex это небольшие папки с инструкциями. В каждой папке лежит
`SKILL.md`:

- frontmatter с `name` и `description` помогает Codex понять, когда skill нужно
  загрузить;
- основное тело `SKILL.md` описывает workflow, проверки, stop-lines и типичные
  ошибки;
- Codex читает полный skill только тогда, когда запрос пользователя подходит
  под его описание.

Идея простая: пользователь не обязан помнить точное имя skill. Он может сказать
обычным языком: "разбей на задачи", "проверь по актуальным docs", "разбери баг",
"докажи тестом", "сделай review". Codex должен сам выбрать подходящий skill и
следовать его процессу.

## Для Кого Этот Пакет

Пакет полезен, если вы хотите, чтобы Codex:

- не начинал писать код до понимания задачи;
- не терялся в большом репозитории;
- не полагался на устаревшую память для API, SDK, CLI и cloud-сервисов;
- не делал большие непроверенные изменения одним куском;
- разбирал ошибки системно, а не угадывал фикс;
- добавлял тесты или focused checks перед заявлением "готово";
- отделял planning, implementation, review и risky decisions;
- не трогал production, auth, data, billing или irreversible cleanup без явного
  approval.

## Что Входит В Пакет

| Skill | Когда Использовать |
|---|---|
| `context-engineering` | Нужно начать или продолжить работу в repo/workspace, понять source of truth, собрать короткий context pack. |
| `spec-driven-development` | Нужно определить, что именно строим: intent, scope, non-goals, acceptance criteria, verification. |
| `planning-and-task-breakdown` | Нужно превратить мутную или большую задачу в шаги, зависимости, stop-lines и критерии готовности. |
| `incremental-implementation` | Нужно делать multi-file change маленькими проверяемыми slices, а не одним большим diff. |
| `source-driven-development` | Нужно свериться с актуальными официальными docs по API, SDK, CLI, framework или cloud behavior. |
| `api-and-interface-design` | Нужно спроектировать API, schema, event, webhook, CLI, config, module boundary или другой contract. |
| `test-driven-development` | Нужно исправить баг или изменить поведение через тест, regression guard или focused check. |
| `debugging-and-error-recovery` | Команда падает, CI красный, build broken, runtime bug, logs/errors, tool/API/network failure. |
| `code-review-and-quality` | Нужно проверить diff, PR, commit или agent-produced code перед merge/ship. |
| `deprecation-and-migration` | Нужно безопасно убрать старый код, cron, API, schema, integration, config или workflow. |
| `doubt-driven-review` | Нужно оспорить уверенное решение перед risky work: production, auth, data, billing, public API, migration, irreversible cleanup. |

## Быстрая Установка В Codex

Склонируйте репозиторий:

```bash
git clone https://github.com/pimenov/codex-first-skills-pack.git
cd codex-first-skills-pack
```

Проверьте пакет:

```bash
python3 scripts/validate_skills.py
```

Установите skills в Codex:

```bash
scripts/install.sh
```

По умолчанию installer копирует skills сюда:

```bash
${CODEX_HOME:-$HOME/.codex}/skills
```

Сначала можно сделать dry-run:

```bash
scripts/install.sh --dry-run
```

Установить только один skill:

```bash
scripts/install.sh --skill source-driven-development
```

После установки перезапустите Codex, чтобы новый список skills подхватился.

## Установка Через Сам Codex

Если в вашем Codex есть встроенный `skill-installer`, можно просто дать ему
репозиторий и попросить поставить skills.

Пример запроса:

```text
Установи skills из репозитория https://github.com/pimenov/codex-first-skills-pack
в мой Codex. Сначала прочитай README, сделай безопасную установку, не
перезаписывай существующие skills без моего подтверждения, затем скажи, что
установлено и нужно ли перезапустить Codex.
```

Можно установить один skill:

```text
Установи skill `source-driven-development` из GitHub repo
pimenov/codex-first-skills-pack, path `skills/source-driven-development`.
```

Или несколько skills:

```text
Установи skills из GitHub repo pimenov/codex-first-skills-pack:
- skills/context-engineering
- skills/source-driven-development
- skills/debugging-and-error-recovery
- skills/test-driven-development
```

## Как Codex Выбирает Skills

Skills лучше всего работают вместе с правилами в `AGENTS.md`. Добавьте в свой
глобальный или project-level `AGENTS.md` routing-блок из:

```text
templates/AGENTS.skills-routing.md
```

После этого пользователь может говорить обычными фразами:

- "проверь по актуальным docs";
- "разбей на задачи";
- "сделай пакет работы";
- "команда падает, разбери баг";
- "сначала докажи тестом";
- "сделай code review";
- "проверь, не самообманываемся";
- "можно ли удалить старую реализацию".

Codex должен сопоставить такую фразу с подходящим skill, прочитать его
`SKILL.md` и работать по описанному workflow.

## Как Skills Активируются

В Codex skills обычно лежат здесь:

```text
~/.codex/skills/<skill-name>/SKILL.md
```

Если переменная `CODEX_HOME` указывает на другой Codex home, путь будет таким:

```text
${CODEX_HOME}/skills/<skill-name>/SKILL.md
```

Codex видит `name` и `description` каждого skill. Когда запрос пользователя
совпадает с описанием, Codex загружает полный `SKILL.md` и следует инструкциям
из него.

## Что Этот Пакет Не Делает

Пакет не:

- даёт Codex право менять production без approval;
- заменяет project-level `AGENTS.md`;
- заменяет тесты, code review, CI/CD или deploy process;
- содержит секреты, токены, credential setup или доступы к сервисам;
- предполагает наличие Notion, Linear, GitHub, Jira или другого внешнего
  трекера;
- является полным зеркалом `addyosmani/agent-skills`.

Project-specific правила всегда важнее, если они конкретнее.

## Структура Репозитория

```text
skills/
  <skill-name>/
    SKILL.md
scripts/
  install.sh
  validate_skills.py
templates/
  AGENTS.skills-routing.md
docs/
  customizing.md
  how-it-works.md
```

## Проверка Пакета

Перед публикацией или локальной установкой можно прогнать:

```bash
python3 scripts/validate_skills.py
scripts/install.sh --dry-run
git diff --check
```

`validate_skills.py` проверяет:

- наличие `SKILL.md`;
- корректный frontmatter;
- совпадение имени папки и `name`;
- базовую длину `description`;
- отсутствие явных приватных следов в skills.

## Как Адаптировать Под Себя

1. Установите нужные skills.
2. Добавьте routing-блок из `templates/AGENTS.skills-routing.md` в свой
   `AGENTS.md`.
3. Допишите свои правила:
   - язык общения;
   - tracker или documentation layer;
   - production approval policy;
   - test/build/lint команды;
   - deploy и rollback правила.
4. Не добавляйте приватные правила прямо в публичный пакет. Для company/private
   workflows лучше сделать отдельный private skills pack.

Подробнее: [docs/customizing.md](docs/customizing.md).

## Attribution

Этот репозиторий является независимой Codex-oriented адаптацией, вдохновлённой
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), который
распространяется под MIT license.

Подробности: [NOTICE.md](NOTICE.md).

## License

MIT. См. [LICENSE](LICENSE).
