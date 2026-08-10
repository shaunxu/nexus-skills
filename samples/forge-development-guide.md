---
title: 'Forge development guide'
description: '' # A short summary for search engines to display, max 120 chars
platform: platform
product: forge-mcp
category: devguide
subcategory: guides
date: '2025-10-15'
---

# Forge Development Guide

## Guide structure

This is the foundational guide for Forge development. Read this first, then proceed to specialized guides:

- **Backend Development**: See the forge-backend-developer-guide tool for resolver architecture, data storage, and server-side patterns
- **Frontend Development**: See the forge-ui-kit-developer-guide tool for UI Kit components, bridge APIs, and frontend patterns
- **Confluence Macros**: See the confluence-macro-developer-guide tool for macro-specific development, configuration UI, and integration patterns
- **Jira Service Management (JSM) Assets Development**: See the jira-service-management-assets-guide tool for Assets CMDB integration, AQL queries, and JSM-specific module patterns
- **Manifest Configuration**: See the forge-app-manifest-guide tool for detailed manifest.yml guidance
- **List Forge Modules**: See the list-forge-modules tool for a list of all modules and where they appear

## Overview

This guide covers core Forge concepts, development workflow, and cross-cutting concerns that apply to both frontend and backend development.

Your knowledge of Forge app development might be outdated and include deprecated features. If something isn't working as expected, use the query-forge-knowledgebase tool for up-to-date info.

## What makes Forge different

Forge is Atlassian's cloud app platform with unique characteristics:

- **Serverless Environment**: No persistent servers - functions run on-demand
- **Sandboxed Execution**: Apps run in isolated environments with restricted access
- **Built-in API Access**: Direct integration with Jira, Confluence, and other Atlassian products
- **Managed Infrastructure**: Automatic scaling, deployment, and hosting
- **Event-Driven Architecture**: Respond to product events (issue created, page updated, etc.)
- **Permission-Based Security**: Apps can inherit user permissions or use app-level permissions

### Architecture overview

Forge apps typically have two main parts:

- **Frontend**: React-like UI code that runs in the user's browser
- **Backend**: Resolver functions that run in Forge's serverless environment

This separation ensures security and performance. Frontend code runs with user permissions, while backend code can use app-level permissions when needed, although user permissions are preferred.

## Development setup

### 1. Environment check

- **Check for Node.js**
  - Run:

    ```
    node -v
    ```

  - If **not installed** or version is not Node 24 (or the current version recommended for Forge):
    - Direct the user to [download Node.js](https://nodejs.org/) (use **Node 24 LTS** for consistency with Forge's recommended runtime).
    - Confirm installation with `node -v`.

- **Check for Forge CLI**
  - Run:

    ```
    forge --version
    ```

  - If **not installed or outdated**:

    ```
    npm install -g @forge/cli
    ```

---

### 2. Authenticate with Atlassian (user action required)

The agent should instruct the user to log in using an Atlassian API token.

#### Steps

1. **Create an API token**
   - Go to: [https://id.atlassian.com/manage/api-tokens](https://id.atlassian.com/manage/api-tokens).
   - Click **Create API token**.
   - Enter a label (e.g., `forge-api-token`).
   - Click **Create**, then **Copy to clipboard**.

2. **Log in with the Forge CLI**
   - Run:

     ```
     forge login
     ```

   - Enter Atlassian account email.
   - Enter API token (from step 1).
   - Optionally respond to the CLI’s prompt about usage analytics.

3. **Confirm success**
   - CLI should display:

     ```
     ✔ Logged in as <user>
     ```

   - Credentials are stored securely in the OS keychain (Linux requires `libsecret`).

#### Important notes

- **Do not run** `forge` **with** `sudo` **or root.** This may cause file permission issues.
- If login fails with a permissions error, reinstall Forge without root.

#### Agent guidance

- **Check:** If `forge login` has not been run, prompt user to follow the above steps.
- **Pause:** Wait for confirmation that login succeeded.
- **Advise:** Warn if the user attempts to run commands with `sudo`.

---

### 3. Create a new Forge app

- Run:

  ```
  forge create
  ```

- User will be prompted to:
  - Select an app template (e.g., “Hello World”).
  - Name the app.
  - Confirm project folder creation.

---

### 4. Development workflow

#### a. Install project dependencies

- After project creation, ensure dependencies in `package.json` are installed:

  ```
  npm install
  ```

#### b. Add dev tools

- Install testing and linting libraries:

  ```
  npm install --save-dev jest eslint
  ```

- Add config files (`jest.config.js`, `.eslintrc.json`) as needed.

#### c. Write code and tests

- Modify app functionality.
- Add tests under a `/tests` directory.

#### d. Run linting and tests

- Run ESLint:

  ```
  npm run lint
  ```

- Run Jest:

  ```
  npm test
  ```

- Run Forge-specific linter:

  ```
  forge lint
  ```

#### e. Verify

- Ensure tests pass and linting shows no errors.

---

### 5. Deploy the app

- Run:

  ```
  forge deploy
  ```

- Packages and uploads the app to Forge.

---

### 6. Install the app

- Run:

  ```
  forge install
  ```

- User must select:
  - Target Atlassian site (e.g., `yourcompany.atlassian.net`).
  - Product (Jira, Confluence, etc.).

---

### 7. Debugging (optional)

- Run:

  ```
  forge tunnel
  ```

- Provides real-time logs for debugging.

---

### Agent’s mental model

- **Pre-checks:** Node.js + Forge CLI.
- **User action:** Atlassian login (API token).
- **Development loop:** `npm install` → add dev tools → write code/tests → lint/test/forge lint.
- **Build cycle:** create → deploy → install.
- **Debug cycle:** use `tunnel`.

### Development best practices

We suggest you configure the following for your environment:

1. **Type Safety**: TypeScript with strict mode for catching errors early
2. **Testing**: Jest with a comprehensive testing setup
3. **Code Quality**: ESLint with TypeScript support for consistent code (do not change this)
4. **Fast Feedback**: Pre-configured npm scripts for quick validation

### Important notes

- TypeScript files are used directly by Forge (no compilation step needed)
- Tests run against TypeScript source files
- Always run Forge CLI commands from the app root directory using the `forge cli`.

## Code standards

### TypeScript guidelines

- **Strict Mode**: Always use TypeScript with strict type checking enabled
- **No Any**: Use proper TypeScript types and interfaces instead of `any` or `unknown`
- **Clear Interfaces**: Define explicit interfaces for resolver requests, responses, and data structures
- **Documentation**: Use verbose commentary for intermediate TypeScript developers with limited Forge experience

### Naming conventions

- **Files/Folders**: kebab-case (`user-service.ts`, `issue-panel/`)
- **Variables/Functions**: camelCase (`getUserData`, `issueKey`)
- **Components/Classes**: PascalCase (`UserProfile`, `IssueService`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`)

### Project structure

```
src/
├── index.ts              # Main entry point
├── resolvers/            # Backend resolver functions
│   ├── index.ts
│   └── __tests__/        # Resolver tests
├── frontend/             # React frontend
│   ├── index.tsx
│   └── __tests__/        # Component tests
└── setupTests.ts         # Jest test setup
```

Tests are co-located with source code in `__tests__/` folders for easy discovery and maintenance.

### Dependencies

- **Use current versions**: Before adding a dependency, use npm to look up the latest version (e.g. `npm view <package> version` or check the npm registry). LLMs often suggest outdated versions from training data—prefer the latest compatible version.
- **Forge libraries**: For `@forge/*` packages (e.g. `@forge/resolver`, `@forge/react`), use the latest versions recommended for the Forge platform; avoid pinning to old versions.
- Import packages from reputable npm libraries when needed
- Always run `npm install` after creating the app and when adding dependencies
- Use the npm package name for imports, not relative paths where possible

## Security principles

### API request context

Understanding when to use different request contexts in backend resolvers is crucial for security:

- `.asUser()`: Preferred for most cases - requests run with the user's permissions and include built-in authorization checks
- `.asApp()`: Use only when you need app-level permissions - **you must implement your own authorization checks** using relevant product permission REST APIs

### Permission management

- **Minimize Scopes**: Only request permissions (scopes) that are strictly required for your app's functionality. You can find the required scopes by using the `query-forge-knowledgebase` tool for relevant product APIs, as well as other system components like storage
- **Principle of Least Privilege**: Grant the minimum permissions necessary for each operation
- **User Context**: Frontend code always runs with user permissions - use this when possible

## Architecture guidelines

### API integration patterns

- **Frontend-First**: Often simpler to make API requests from the frontend using `requestJira`, `requestConfluence`, etc. from `@forge/bridge`
- **Backend When Needed**: Use resolvers for operations requiring app-level permissions or complex business logic
- **Payload Signature**: When receiving data in the resolver, use the shared types to define the payload signatures, never unknown or any. Ensure that the frontend strictly follows matching data types when sending data as part of the submission.
- **Choose Simplicity**: Always prefer the simplest solution that meets your requirements

### Module selection

- **Global Pages**: Default choice when no specific module fits your use case (e.g., `jira-global-page-ui-kit`)
- **Specific Modules**: Use targeted modules (issue panels, content actions) when they match your functionality
- **Module Discovery**: Use the query-forge-knowledgebase tool to learn about available modules and their configuration
- **Module Types**: Different modules (global pages, issue panels, content actions) have different requirements
- **Documentation**: Use the query-forge-knowledgebase tool to understand available modules and their capabilities

### Problem-solving approach

1. **Understand Requirements**: Seek clarification on unclear requirements before implementation
2. **Check Feasibility**: If something isn't possible natively in Forge, explore alternative approaches
3. **Suggest Alternatives**: When direct solutions aren't available, propose similar effects using different methods
4. **Use Resources**: Use the query-forge-knowledgebase tool for up-to-date APIs and capabilities, and other Forge references

## Testing philosophy

### Testing strategy

- **Co-located Tests**: Tests live in `__tests__/` folders next to the code they test for easy discovery and maintenance
- **Framework Integration**: We recommend using a testing framework like Jest with TypeScript support
- **Multiple Levels**: Unit tests for business logic, integration tests for API interactions

### Test organization

```
src/
├── domain/
│   ├── services/
│   │   ├── user-service.ts
│   │   └── __tests__/
│   │       └── user-service.test.ts
├── resolvers/
│   ├── user-resolver.ts
│   └── __tests__/
│       └── user-resolver.test.ts
```

### Testing commands

If you have the tools installed, we recommend using the following checks to test during development:

- `npm run type-check`: TypeScript compilation check
- `npm run lint`: ESLint for code quality
- `npm run lint:fix`: Auto-fix linting issues
- `npm run test`: Run all tests once
- `npm run test:watch`: Continuous testing during development
- `npm run test:coverage`: Generate coverage reports
- Tests are included in `npm run ci` for comprehensive validation

## Frontend vs backend development

### When to use frontend

- User interface components and interactions
- API calls that use user permissions
- Simple data display and form handling
- Real-time user feedback

### When to use backend (Resolvers)

- Operations requiring app-level permissions
- Complex business logic and data processing
- Integration with external systems
- Scheduled tasks and background processing
- Webhook event handling

**Detailed Implementation**: See the forge-backend-developer-guide, forge-ui-kit-developer-guide, and confluence-macro-developer-guide tools for specific patterns and examples.

## Data storage options

Forge provides several storage mechanisms for different use cases:

### Entity properties

- **Purpose**: Store key-value data against Jira entities (Issues, Projects, Users, etc.) and Confluence content
- **Access**: Use REST APIs directly - there is no dedicated client-side API for Forge apps
- **Examples**: Issue Properties REST API for Jira, Content Properties API for Confluence
- **Important**: You MUST use REST APIs to access entity properties - don't assume a dedicated Forge API exists

### Forge storage solutions

- **Forge Key-Value Storage (KVS)**: Simple key-value pairs with API via @forge/kvs
- **Forge Custom Entities**: Structured data storage with queries and relationships, extending KVS
- **Forge SQL**: SQL-based data storage for complex queries

### Storage selection guidelines

- **Entity Properties**: When data is naturally associated with specific Jira/Confluence entities
- **Key-Value Storage**: For simple app configuration and user preferences
- **Custom Entities**: For structured app data with relationships
- **Forge SQL**: For complex data queries and reporting needs

**Implementation Details**: See the forge-backend-developer-guide tool for specific storage patterns and code examples.

### Environment detection

Check if the app is in preview mode by testing `getAppContext` availability:

**Frontend:**

```typescript
import { view } from '@forge/bridge';

const PREVIEW_CLOUD_ID = 'preview-mode';

const isPreviewMode = async (): Promise<boolean> => {
  const context = await view.getContext();
  return !context.cloudId || context.cloudId === PREVIEW_CLOUD_ID;
};
```

**Backend:**

```typescript
import { getAppContext } from '@forge/api';

const isPreviewMode = (): boolean => {
  try {
    getAppContext();
    return false; // getAppContext succeeded, we're in live mode
  } catch (error) {
    return true; // getAppContext failed, we're in preview mode
  }
};
```

### Mock data requirements

**Use the bundled forge-context library for type-safe mock data creation:**

**Recommended Pattern - Type-safe Factory Functions:**

Use direct imports of specific context types and the factory function for all mock creation:

```typescript
import { createMockContext, type IssueActivityContext } from './lib/forge-context';

// Simple mock with defaults
const defaultContext = createMockContext('jira:issueActivity');

// Custom mock with overrides (recommended)
const customContext: IssueActivityContext = createMockContext('jira:issueActivity', {
  issue: { key: 'DEMO-123', type: 'Bug' },
  project: { key: 'SUPPORT', type: 'service_desk' },
});
```

**Inspect Available Fields:**

Use TypeScript's IntelliSense for the most efficient way to discover context shapes:

```typescript
import type { IssueActivityContext, CustomFieldContext, ProjectPageContext } from './lib/forge-context';

const exampleContext: IssueActivityContext = {
  // refer to the type for required fields
};
```

**Runtime Inspection (when needed):**  
For debugging or exploration purposes only:

```typescript
import { createMockContext } from './lib/forge-context';

// Inspect a context shape at runtime
console.log('Context shape:', createMockContext('jira:issueActivity'));
```

### Error handling

The recommended pattern for handling preview vs live mode with type-safe mocks:

```typescript
// Frontend
import { view } from '@forge/bridge';
import { createMockContext, type IssueActivityContext } from './lib/forge-context';

const PREVIEW_CLOUD_ID = 'preview-mode';

const safeDataFetchFrontend = async <T>(fetchFn: () => Promise<T>, mockFn: () => T): Promise<T> => {
  try {
    const context = await view.getContext();
    if (context.cloudId === PREVIEW_CLOUD_ID) return mockFn();
    return await fetchFn();
  } catch (error) {
    return mockFn(); // Fallback to mock
  }
};

// Recommended usage pattern
const getIssueContext = (): Promise<IssueActivityContext> =>
  safeDataFetchFrontend(
    () => view.getContext() as Promise<IssueActivityContext>,
    () =>
      createMockContext('jira:issueActivity', {
        issue: { key: 'DEMO-123', type: 'Story' },
        project: { key: 'DEMO', type: 'software' },
      }),
  );
```

```typescript
// Backend
import { getAppContext } from '@forge/api';
import { createMockContext, type ProjectPageContext } from './lib/forge-context';

const safeDataFetchBackend = async <T>(fetchFn: () => Promise<T>, mockFn: () => T): Promise<T> => {
  try {
    getAppContext(); // Test if we're in live mode
    return await fetchFn();
  } catch (error) {
    return mockFn(); // Either preview mode or API error, use mock
  }
};

// Recommended usage pattern
const getProjectContext = (): Promise<ProjectPageContext> =>
  safeDataFetchBackend(
    () => someApiCall(),
    () =>
      createMockContext('jira:projectPage', {
        project: { key: 'ENGINEERING', type: 'software' },
      }),
  );
```

## Forge CLI usage

### Important CLI guidelines

- **Working Directory**: Run `pwd` first to get the current path, then ensure all Forge commands run from the app root directory
- **Error Handling**: When a Forge CLI command fails, ALWAYS display the full output
- **Auth errors**: If you get a UserNotFoundError or similar errors, please ask the user to check that their API token and email address are correctly set up.

### Command flags

- **Non-Interactive Flag**: ALWAYS use `--non-interactive` for: `deploy`, `environments`, `install`
- **Interactive Commands**: NEVER use `--non-interactive` for other commands
- **Help Flag**: Use `--help` to understand available options for any command
- **Verbose Flag**: Use `--verbose` to troubleshoot failing commands

### Common commands

- **Linting**: `lint` - Use this to quickly test for problems before deploying
- **Help**: `--help` on any command to see available options

## Deployment process

### Deployment command

```shell
forge deploy --non-interactive -e <environment-name>
```

Example:

```shell
forge deploy --non-interactive -e development
```

- **Environment**: Use `development` unless specified otherwise
- **Verification**: NEVER use `--no-verify` flag unless explicitly requested
- **Pre-deployment**: Always run `npm run ci` to catch issues before deployment

### Deployment vs installation

**Deployment** uploads your app code to Atlassian's infrastructure:

- Updates the app's code in Atlassian's systems
- Makes new functionality available for installation
- Required after any code changes

**Installation** makes your deployed app available in specific Atlassian sites:

- Connects the app to a specific Jira/Confluence instance
- Applies the app's permissions and modules to that site
- Only needed when first setting up or when permissions change

## Installation process

### Installation commands

**New Installation:**

```shell
forge install --non-interactive --site <site-url> --product <product-name> --environment <environment-name>
```

Example:

```shell
forge install --non-interactive --site https://mycompany.atlassian.net --product jira --environment development
```

**Upgrade Existing Installation:**

```shell
forge install --non-interactive --upgrade --site <site-url> --product <product-name> --environment <environment-name>
```

Example:

```shell
forge install --non-interactive --upgrade --site https://mycompany.atlassian.net --product jira --environment development
```

**Note**: Only upgrade if you've changed the app's scopes or permissions in the manifest.

## Manifest configuration

### Before making changes

- **Node runtime**: In `manifest.yml`, always set the app runtime to the current Forge-recommended Node version (e.g. `nodejs24.x`). See the forge-app-manifest-guide tool. LLMs may suggest older runtimes—use the recommended version for consistency.
- **Use the Guide**: Always see the forge-app-manifest-guide tool before modifying `manifest.yml`
- **Understand Structure**: The tool provides critical information about syntax and requirements
- **Validate Changes**: Run `forge lint` after every manifest modification

### Validation process

1. Make changes to `manifest.yml`
2. Run `forge cli lint` to validate syntax
3. Fix any errors before proceeding
4. Deploy and install to apply permission changes

### Important notes

- **Permission Updates**: New scopes or egress controls only take effect after deployment and installation
- **Syntax Errors**: Always use `forge cli lint` if you see manifest-related errors
- **Critical Validation**: Manifest syntax errors will prevent deployment

## Debugging

### Application logging

Forge automatically captures logs from the frontend and logs you generate in the backend:

- **Backend Logs**: Use `console.log()`, `console.error()`, etc. in resolvers - all output is captured in Forge Logs
- **Access Logs**: Use `forge cli logs -e development --limit 20` to view recent logs
- **Current Time**: Run `date -u` to get the current UTC time for comparing log timestamps

### Development debugging

- **Lint First**: Use `forge cli lint` to catch configuration issues
- **Pre-deployment**: Always run `npm run ci` before deploying to catch issues early

### Production debugging

- **App Logs**: Use the `forge cli logs` command to troubleshoot errors in deployed applications
- **Error Context**: Logs provide crucial context for runtime issues
- **Systematic Approach**: Check logs systematically when investigating issues

### Common debugging commands

- **Linting**: `forge cli lint` - Quick test for configuration problems before deploying
- **Forge Build**: `forge cli build` Simulate the Forge build process before deploying. Use after `npm run ci` shows no errors.
- **Logs**: `forge cli logs` - Check runtime logs from deployed apps
- **Verbose**: Use `--verbose` flag to troubleshoot failing commands
- **Help**: Use `--help` on any command to see available options

