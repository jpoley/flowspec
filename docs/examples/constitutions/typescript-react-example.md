# TypeScript React Constitution Example

## Overview

This example shows how a **Medium** tier constitution template is customized for a TypeScript React project:

- **Project Type**: Web application (SPA)
- **Language**: TypeScript 5+
- **Framework**: React 18 with Next.js 14
- **Testing**: Jest + React Testing Library
- **Linting**: ESLint + Prettier
- **Package Manager**: pnpm (preferred over npm)
- **CI/CD**: GitHub Actions

## Detection Process

When `specify init` detects this project:

1. **Language Detection**: Finds `tsconfig.json` → TypeScript
2. **Framework Detection**: Finds `next.config.js` or `package.json` dependencies → Next.js
3. **Test Framework**: Finds `jest.config.js` → Jest
4. **Linter Detection**: Finds `.eslintrc.js` → ESLint
5. **Formatter Detection**: Finds `.prettierrc` → Prettier
6. **Package Manager**: Finds `pnpm-lock.yaml` → pnpm

## Before: Template (constitution-medium.md)

```markdown
## Technology Stack
<!-- SECTION:TECH_STACK:BEGIN -->
<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->
[LANGUAGES_AND_FRAMEWORKS]

### Linting & Formatting
<!-- NEEDS_VALIDATION: Detected linting tools -->
[LINTING_TOOLS]
<!-- SECTION:TECH_STACK:END -->
```

## After: Customized Constitution

```markdown
## Technology Stack
<!-- SECTION:TECH_STACK:BEGIN -->
### Languages & Frameworks
- **Language**: TypeScript 5.3+
- **UI Framework**: React 18
- **Meta Framework**: Next.js 14 (App Router)
- **Package Manager**: pnpm (NEVER use npm)
- **Node Version**: 20 LTS (via .nvmrc)

### Testing
- **Unit Testing**: Jest 29+
- **Component Testing**: React Testing Library
- **E2E Testing**: Playwright (for critical flows)
- **Coverage Target**: 75%

### Code Quality
- **Linter**: ESLint 8+ with TypeScript plugin
- **Formatter**: Prettier 3+
- **Type Checking**: `tsc --noEmit` in CI
- **Pre-commit**: Husky + lint-staged (eslint + prettier)

### Build & CI/CD
- **Build Tool**: Next.js built-in (turbopack in dev)
- **CI Platform**: GitHub Actions
- **Node Versions Tested**: 18 LTS, 20 LTS
- **Container Registry**: ghcr.io
- **Deployment**: Vercel (preview + production)
<!-- SECTION:TECH_STACK:END -->
```

## What Was Detected

The LLM detected:

- ✅ TypeScript 5.3+ from `tsconfig.json`: `"target": "ES2022"`
- ✅ React 18 from `package.json` dependencies
- ✅ Next.js 14 from `package.json` and `next.config.js`
- ✅ Jest from `jest.config.js` or `package.json` scripts
- ✅ ESLint from `.eslintrc.js` or `.eslintrc.json`
- ✅ Prettier from `.prettierrc` or `package.json`
- ✅ pnpm from `pnpm-lock.yaml`

## What Needed Validation

User needed to confirm/customize:

- Package manager preference (pnpm vs bun vs yarn)
- Coverage target (75% is suggested)
- E2E testing tool (Playwright vs Cypress)
- Deployment target (Vercel vs self-hosted)
- Node version strategy (LTS only vs latest)

## Related Examples

- [Python FastAPI Example](python-fastapi-example.md) - Backend API comparison
- [Go API Example](go-api-example.md) - Backend comparison
- [Rust CLI Example](rust-cli-example.md) - Systems language approach
