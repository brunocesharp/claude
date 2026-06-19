---
name: generating-java-unit-tests
description: >
  Generates JUnit 5 unit test files in Java 25 from BDD documentation, following TDD
  (tests written before implementation), Spring Boot conventions, and Given-When-Then structure.
  Use when the user asks to create unit tests, write JUnit tests, apply TDD, generate tests
  from BDD, or provides a BDD specification (Gherkin scenarios, Feature files, or
  Given-When-Then descriptions). Also triggers for: "teste unitário", "TDD Java", "JUnit",
  "Mockito", "gerar testes do BDD", "criar teste", "testar serviço", "testar controller".
  Does NOT apply to integration tests, Cucumber end-to-end tests, or performance tests.
---

# Generating Java Unit Tests

Generates `.java` test files for Java 25 + Spring Boot using JUnit 5 and Mockito.
Each test method is derived **directly from a BDD scenario** — one scenario = one test method.

## Fixed decisions — never ask

| Decision | Value |
|---|---|
| Test names language | Portuguese |
| External dependencies | Always mocked with `@Mock` |
| Implementation class exists? | No — TDD writes the test first |
| File name | `<ClassName>Test.java` (auto-derived) |

## Workflow

Copy this checklist and check off each step:

```
Progress:
- [ ] Step 1: Request or validate BDD documentation
- [ ] Step 2: Collect context
- [ ] Step 3: Map BDD scenarios to test methods
- [ ] Step 4: Write the test file
- [ ] Step 5: Confirm the file was created
```

### Step 1 — Request or validate BDD documentation

**If BDD was not provided**, ask before anything else:

> "Por favor, informe a documentação BDD (cenários em Gherkin ou descrições Given-When-Then)
> para que eu possa gerar os testes unitários."

**Do not proceed to Step 2 until BDD is provided.**

BDD is considered provided when the user shares at least one scenario in any of these formats:
- Gherkin (`Feature` / `Scenario` / `Given` / `When` / `Then`)
- Plain Given-When-Then prose
- Numbered or bulleted behavior descriptions

### Step 2 — Collect context

If `docs/project-config.json` exists in the project root, read it to extract `name` and `docs_root` for context — but do not require it. The skill works without it.

Extract from the BDD and user's message. Ask **only** for the project root path if not provided.

| Information | Source |
|---|---|
| Class name | Feature name, `Scenario` subject, or user's message |
| Package | Project conventions or user's message |
| Layer | Class name suffix: `Service`, `Repository`, `Controller` |
| Dependencies | External interactions in BDD steps → mock each one |
| Project root path | `project-config.json` → `docs_root` parent, or ask once if unknown |

### Step 3 — Map BDD scenarios to test methods

Convert each BDD scenario into one test method. Follow this mapping:

| BDD element | Test element |
|---|---|
| `Feature` / subject | `@DisplayName` on the test class |
| `Scenario` title | `@DisplayName` on the test method |
| `Given` steps | `// Given` block — arrange state and mocks |
| `When` step | `// When` block — invoke the method under test |
| `Then` steps | `// Then` block — assertions with messages |
| `And` / `But` | Append to the previous `Given`, `When`, or `Then` block |

For BDD mapping examples and edge cases, see [references/bdd-mapping.md](references/bdd-mapping.md).

### Step 4 — Write the test file

Follow the coding rules in [references/coding-rules.md](references/coding-rules.md).
For layer-specific patterns, see [references/layer-patterns.md](references/layer-patterns.md).

### Step 5 — Confirm creation

After writing the file, confirm it exists:

```bash
ls -la <output_path>/<ClassName>Test.java
```

## Maven dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```
