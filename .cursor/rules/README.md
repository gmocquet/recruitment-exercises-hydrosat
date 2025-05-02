# 🧠 Cursor Rules – Coding Principles & Quality Guidelines

This folder contains **Cursor AI rules** designed to guide code generation according to the principles of clean architecture, maintainability, and clarity.

It includes:
- the 5 SOLID principles (SRP, OCP, LSP, ISP, DIP),
- the KISS principle for simplicity,
- robust error handling (no silent nulls, fail fast),
- and a rule enforcing English as the default language for all generated content.

---

## ✅ Available Rules

| Rule file                        | Description |
|----------------------------------|-------------|
| `solid-srp.mdc`                | Enforces the **Single Responsibility Principle**: one reason to change per class/module. |
| `solid-ocp.mdc`                | Enforces the **Open/Closed Principle**: open for extension, closed to modification. |
| `solid-lsp.mdc`                | Enforces the **Liskov Substitution Principle**: subclasses must be safely interchangeable with their base class. |
| `solid-isp.mdc`                | Enforces the **Interface Segregation Principle**: prefer many small interfaces over one large interface. |
| `solid-dip.mdc`     | Promotes **constructor-based dependency injection** and inversion of dependencies (DIP). |
| `kiss-principle.mdc`           | Enforces the **KISS principle**: prioritize simplicity and clarity over abstraction or cleverness. |
| `language-english.mdc`         | Ensures **all output is in English**, including code, comments, documentation, and explanations. |
| `no-silent-null.mdc`           | Forbids returning `null` silently on failure. Always throw meaningful exceptions instead. |
| `fail-fast.mdc`                | Enforces the **Fail Fast principle**: throw immediately on invalid input or failed state. Prevent error propagation. |

---

## 🧱 SOLID principales

| Principle | Full Name                          | Purpose                                                                 |
|-----------|------------------------------------|-------------------------------------------------------------------------|
| **S**     | Single Responsibility Principle (SRP) | A class should have only one responsibility                            |
| **O**     | Open/Closed Principle (OCP)         | Open for extension, closed for modification                            |
| **L**     | Liskov Substitution Principle (LSP) | Subclasses must be usable in place of their superclasses without side effects |
| **I**     | Interface Segregation Principle (ISP) | Prefer multiple specific interfaces over one general-purpose interface |
| **D**     | Dependency Inversion Principle (DIP) | High-level modules should not depend on low-level modules; both should depend on abstractions |

---

## ⚙️ Application Behavior

- Most rules use `globs` targeting `src/**/*.py` and similar files to apply only to code.
- Rules with `alwaysApply: true` are **automatically loaded by Cursor AI** for every interaction in relevant files.
- You can also manually trigger a rule in a prompt by typing:
@solid-srp
@solid-ocp
@solid-lsp
@solid-isp
@solid-dip
@kiss-principle
@language-english
@no-silent-null
@fail-fast

---

## 🧪 Recommended Usage Flow

When writing or reviewing code:
1. Use **SRP** to keep logic cleanly separated.
2. Apply **OCP** by extending functionality without rewriting core code.
3. Ensure that subclasses follow **LSP** without breaking expectations.
4. Design interfaces according to **ISP** to avoid bloated contracts.
5. Inject all dependencies explicitly via **DI**, favoring interfaces.
6. Keep it simple with **KISS**, optimizing only when necessary.
7. Write all code and related content **in English**, including comments, logs, messages, and docblocks.
8. Never return null silently — **raise meaningful exceptions** instead.
9. **Fail fast** on invalid input or broken assumptions - detect and throw early.
---

## 📁 Good to Know

These rules are compatible with:
- Cursor AI agents & prompts,
- Code templates and scaffolding via `.cursor/templates/`,
- Linting and analysis tools like Ruff,
- CI pipelines for code quality enforcement.

---

## 🔍 Philosophy

> "Code should be easy to read, safe to use, and hard to break. Keep it clear, throw when it fails, and evolve by extension — not mutation."
