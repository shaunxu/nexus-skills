---
title: 'Forge backend developer guide'
description: '' # A short summary for search engines to display, max 120 chars
platform: platform
product: forge-mcp
category: devguide
subcategory: guides
date: '2025-10-15'
---

# Forge backend developer guide

## Related tools

- forge-development-guide
- forge-app-manifest-guide
- forge-ui-kit-developer-guide
- jira-service-management-assets-guide

## Prerequisites

Before using this guide:

- Read the **forge-development-guide** tool for core concepts, development workflow, and security principles
- Understand TypeScript and modern JavaScript fundamentals
- Have the development environment set up (Node.js 24 or the current version recommended for Forge, and Forge CLI)

## Introduction

This guide focuses on backend-specific concerns: resolver architecture, business logic organization, data storage patterns, and API integrations. It emphasizes clean architecture principles using a layered approach where resolvers coordinate business logic through domain services.

## Backend-specific concepts

### Resolvers

- **Entry Points**: Resolvers are the primary entry points for backend logic
- **Manifest**: Module section in manifest MUST have a `resolver` attribute to link the resolver implementation.
- **Request Handling**: Handle web requests, webhook events, and scheduled tasks. For **Web Triggers** (`webtrigger`): implement authentication in the handler function without it, endpoints are public and insecure.
- **Coordination**: Orchestrate business logic, but don't contain it
- **Context**: Run with app-level permissions when needed
- **Payload Type**: You MUST NEVER use `unknown` or `any` as a type for payload in a resolver request or response. Always use the type defined as part of the common shared types. Flag lint errors if the formats don't match.

### Event-driven architecture

- **Webhooks**: Respond to Jira/Confluence events (issue created, page updated)
- **Scheduled Functions**: Run background tasks on a schedule
- **Asynchronous Processing**: Handle long-running operations efficiently

### Data integration patterns

- **Product APIs**: Integration with Jira, Confluence, and other Atlassian products
- **Product Scopes**: Use the search-forge-docs tool to identify the scopes required for each of the products
- **JSM Assets Integration**: See the jira-service-management-assets-guide tool for Assets API patterns, AQL queries, and object lifecycle management
- **External APIs**: Connect to third-party services with proper error handling
- **Storage Abstraction**: Clean separation between business logic and data persistence
- **Scopes and Permissions**: You MUST use the search-forge-docs tool to check if any services need extra scopes and update the manifest for example: forge kvs storage or sql
- **Assets-Specific Scopes**: For JSM Assets apps, see the jira-service-management-assets-guide tool for scope requirements, including `read:cmdb-object:jira`, `read:cmdb-schema:jira`, and related permissions

## Backend architecture

### Layered architecture for Forge backend

This guide follows a simplified layered architecture approach:

- **Domain Layer**: Pure business logic with entities, services, and value objects
- **Resolvers**: Presentation layer that handles inbound requests/events and coordinates with domain services
- **Infrastructure Layer**: Implementations for external systems (Jira API, storage)
- **Shared**: Common utilities and error handling

### Backend file structure

```
src/
├── index.ts              # Main entry point and resolver exports
├── domain/
│   ├── entities/         # Domain entities
│   ├── services/         # Business logic services
│   └── value-objects/    # Value objects
├── resolvers/            # Presentation layer
│   ├── web/              # Web-based resolvers
│   ├── events/           # Event-based resolvers
│   └── validation/       # Input validation
├── infrastructure/
│   ├── storage/          # Storage implementations (Forge Storage)
│   ├── jira-api/         # Jira API implementations
│   └── config/           # Configuration & dependency injection
└── shared/
    ├── errors/           # Custom error types
    └── utils/            # Shared utilities
```

**Testing**: Tests are co-located with source code in `__tests__/` folders next to the files they test.

## Getting started: Simple Wishes app

Let's build a minimal "Wishes" app that demonstrates the layered architecture. Users can create wishes as Jira issues and mark them as fulfilled.

### Shared type definitions

Shared types define the contract between the front end and the back end when sending data. If the front end does not match the shared types for the payload sent to the back end, the front end should be changed to match the payload data type.  
Before diving into the implementation, define the common types we'll use across our app. For example:

```typescript
// Domain types
export type WishStatus = 'Open' | 'Done';

// Jira API response types
export interface JiraIssue {
  key: string;
  fields: {
    summary: string;
    description?: {
      content?: Array<{
        content?: Array<{
          text?: string;
        }>;
      }>;
    };
    status: {
      name: string;
    };
  };
}

export interface CreateIssueResponse {
  key: string;
}

export interface JiraTransition {
  id: string;
  to: {
    name: string;
  };
}

export interface JiraTransitionsResponse {
  transitions: JiraTransition[];
}

export interface JiraSearchResponse {
  issues: JiraIssue[];
}

// Service interfaces
export interface IJiraService {
  createWish(title: string, description: string): Promise<CreateIssueResponse>;
  transitionIssue(issueKey: string, status: string): Promise<void>;
  getWishes(): Promise<JiraIssue[]>;
}
```

### Domain layer

Domain entity (`src/domain/entities/wish.ts`):

```typescript
export type WishStatus = 'Open' | 'Done';

export class Wish {
  public readonly title: string;
  public readonly description: string;
  public readonly issueKey: string;
  public status: WishStatus;

  constructor(title: string, description: string, issueKey: string, status: WishStatus = 'Open') {
    this.title = title;
    this.description = description;
    this.issueKey = issueKey;
    this.status = status;
  }

  fulfill(): void {
    this.status = 'Done';
  }

  isPending(): boolean {
    return this.status === 'Open';
  }
}
```

Domain service (`src/domain/services/wish-service.ts`):

```typescript
import { Wish, WishStatus } from '../entities/wish';
import type { IJiraService, JiraIssue } from '../types'; // Shared types

// Helper function to safely validate and convert status
function validateWishStatus(status: string): WishStatus {
  if (status === 'Open' || status === 'Done') {
    return status;
  }
  // Default to 'Open' for any unrecognized status
  console.warn(`Unknown status "${status}", defaulting to "Open"`);
  return 'Open';
}

export class WishService {
  constructor(private readonly jiraService: IJiraService) {}

  async createWish(title: string, description: string): Promise<Wish> {
    const issue = await this.jiraService.createWish(title, description);
    return new Wish(title, description, issue.key, 'Open');
  }

  async fulfillWish(issueKey: string): Promise<Wish> {
    await this.jiraService.transitionIssue(issueKey, 'Done');
    const wish = new Wish('', '', issueKey, 'Done');
    return wish;
  }

  async getAllWishes(): Promise<Wish[]> {
    const issues = await this.jiraService.getWishes();
    return issues.map(
      (issue): Wish =>
        new Wish(
          issue.fields.summary,
          issue.fields.description?.content?.[0]?.content?.[0]?.text || '',
          issue.key,
          validateWishStatus(issue.fields.status.name), // Safe status validation
        ),
    );
  }
}
```

### Infrastructure layer

Jira service (`src/infrastructure/jira-api/jira-service.ts`):

```typescript
import api, { route } from '@forge/api';
import type {
  CreateIssueResponse,
  JiraIssue,
  JiraTransition,
  JiraTransitionsResponse,
  JiraSearchResponse,
} from '../types'; // Shared types

export class JiraService {
  async createWish(title: string, description: string): Promise<CreateIssueResponse> {
    const response = await api.asApp().requestJira(route`/rest/api/3/issue`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        fields: {
          project: { key: 'DEMO' },
          summary: title,
          description: {
            type: 'doc',
            version: 1,
            content: [{ type: 'paragraph', content: [{ type: 'text', text: description }] }],
          },
          issuetype: { name: 'Task' },
          labels: ['wish'],
        },
      }),
    });

    return (await response.json()) as CreateIssueResponse;
  }

  async transitionIssue(issueKey: string, status: string): Promise<void> {
    const transitions = await this._getTransitions(issueKey);
    const transition = transitions.find(t => t.to.name === status);

    if (transition) {
      await api.asApp().requestJira(route`/rest/api/3/issue/${issueKey}/transitions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transition: { id: transition.id } }),
      });
    }
  }

  async getWishes(): Promise<JiraIssue[]> {
    // Use /rest/api/3/search/jql (the /rest/api/3/search endpoint is deprecated)
    const response = await api.asApp().requestJira(route`/rest/api/3/search/jql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jql: 'labels = wish ORDER BY created DESC',
        fields: ['summary', 'description', 'status'],
      }),
    });

    const data = (await response.json()) as JiraSearchResponse;
    return data.issues;
  }

  private async _getTransitions(issueKey: string): Promise<JiraTransition[]> {
    const response = await api.asApp().requestJira(route`/rest/api/3/issue/${issueKey}/transitions`);
    const data = (await response.json()) as JiraTransitionsResponse;
    return data.transitions;
  }

  async getIssue(issueKey: string): Promise<JiraIssue | null> {
    try {
      const response = await api.asApp().requestJira(route`/rest/api/3/issue/${issueKey}`);
      if (!response.ok) {
        if (response.status === 404) {
          return null; // Issue doesn't exist
        }
        throw new Error(`Failed to get issue: ${response.status}`);
      }
      return (await response.json()) as JiraIssue;
    } catch (error) {
      if (error instanceof Error && error.message.includes('404')) {
        return null; // Issue doesn't exist
      }
      throw error;
    }
  }
}
```

**Important: Error Handling for Jira API Calls**

When working with Jira API calls, you MUST handle cases where resources may not exist (404 errors). Always check if an issue exists before performing operations on it, especially when:
- Getting issue details
- Finding or manipulating issue links
- Removing dependencies or relationships
- Accessing issue properties

Example: Safe issue link removal pattern:

```typescript
async findIssueLinkId(issueKey: string, linkedIssueKey: string, linkType: string): Promise<string | null> {
  // First, verify the issue exists
  const issue = await this.getIssue(issueKey);
  if (!issue) {
    throw new Error(`Issue ${issueKey} not found`);
  }

  // Then get issue links
  const response = await api.asApp().requestJira(route`/rest/api/3/issue/${issueKey}?fields=issuelinks`);
  if (!response.ok) {
    if (response.status === 404) {
      return null; // Issue doesn't exist
    }
    throw new Error(`Failed to get issue links: ${response.status}`);
  }

  const data = await response.json();
  const links = data.fields?.issuelinks || [];
  
  // Find the matching link
  const link = links.find((l: any) => 
    (l.outwardIssue?.key === linkedIssueKey || l.inwardIssue?.key === linkedIssueKey) &&
    (l.type?.name === linkType || l.type?.inward === linkType || l.type?.outward === linkType)
  );

  return link?.id || null;
}

async removeDependencyLink(issueKey: string, linkedIssueKey: string, linkType: string): Promise<void> {
  // Verify both issues exist before attempting to remove link
  const issue = await this.getIssue(issueKey);
  if (!issue) {
    throw new Error(`Issue ${issueKey} not found`);
  }

  const linkedIssue = await this.getIssue(linkedIssueKey);
  if (!linkedIssue) {
    throw new Error(`Linked issue ${linkedIssueKey} not found`);
  }

  // Find the link ID
  const linkId = await this.findIssueLinkId(issueKey, linkedIssueKey, linkType);
  if (!linkId) {
    // Link doesn't exist, nothing to remove - this is not an error
    console.log(`No ${linkType} link found between ${issueKey} and ${linkedIssueKey}`);
    return;
  }

  // Remove the link
  const response = await api.asApp().requestJira(route`/rest/api/3/issueLink/${linkId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error(`Failed to remove dependency link: ${response.status}`);
  }
}
```

### Resolver layer

Web resolver (`src/resolvers/web/wishes-resolver.ts`):

Infer the resolver request payload type from shared types and frontend components submit flow, and NEVER use broad types like unknown or any. Always ensure the payload in the resolver request matches the data supplied by the frontend components through form submissions. If the frontend components are not sending data that matches the resolver payload, the frontend component code should be changed.

```typescript
import Resolver from '@forge/resolver';
import { WishService } from '../../domain/services/wish-service';
import { JiraService } from '../../infrastructure/jira-api/jira-service';

// Specific resolver request type for wishes app
// Note: In real applications, customize this interface for your specific use case
// The base template uses a generic `payload?: unknown` approach
interface WishesResolverRequest {
  payload?: {
    title?: string;
    description?: string;
    issueKey?: string;
    [key: string]: unknown;
  };
  context?: {
    accountId?: string;
    cloudId?: string;
    [key: string]: unknown;
  };
}

// Response types for each resolver function
interface CreateWishResponse {
  wish: {
    title: string;
    issueKey: string;
    status: string;
  };
}

interface FulfillWishResponse {
  wish: {
    issueKey: string;
    status: string;
  };
}

interface GetAllWishesResponse {
  wishes: Array<{
    title: string;
    description: string;
    issueKey: string;
    status: string;
  }>;
}

const resolver = new Resolver();

// Simple dependency injection with proper typing
const jiraService = new JiraService();
const wishService = new WishService(jiraService);

resolver.define('createWish', async (req: WishesResolverRequest): Promise<CreateWishResponse> => {
  const { title, description } = req.payload || {};

  if (!title || !description) {
    throw new Error('Title and description are required');
  }

  const wish = await wishService.createWish(title, description);
  return {
    wish: {
      title: wish.title,
      issueKey: wish.issueKey,
      status: wish.status,
    },
  };
});

resolver.define('fulfillWish', async (req: WishesResolverRequest): Promise<FulfillWishResponse> => {
  const { issueKey } = req.payload || {};

  if (!issueKey) {
    throw new Error('Issue key is required');
  }

  const wish = await wishService.fulfillWish(issueKey);
  return {
    wish: {
      issueKey: wish.issueKey,
      status: wish.status,
    },
  };
});

resolver.define('getAllWishes', async (): Promise<GetAllWishesResponse> => {
  const wishes = await wishService.getAllWishes();
  return {
    wishes: wishes.map(wish => ({
      title: wish.title,
      description: wish.description,
      issueKey: wish.issueKey,
      status: wish.status,
    })),
  };
});

export const handler = resolver.getDefinitions();
```

### Event resolvers (Forge triggers)

A Forge `trigger` module invokes a resolver function when an Atlassian product event (`avi:jira:*`, `avi:jira-software:*`, `avi:confluence:*`, `avi:bitbucket:*`, …) is fired.

> **⚠️ Always look up the specific event's payload before writing field accesses.** Field names and nesting vary per event — some events nest under an entity-named sub-object (e.g. issue events under `event.issue`, comment events under `event.comment`), while others expose fields directly at the root of `event`. For example, issue link events have **no** `event.issueLink` object; their fields are at the root (`event.id`, `event.sourceIssueId`, `event.destinationIssueId`, `event.issueLinkType`). Never assume by analogy from the event name. The Forge documentation is the source of truth: use `search-forge-docs` with a query like `<event name> payload` to retrieve the exact schema before writing handlers.

### Manifest configuration

`manifest.yml`:

```yaml
modules:
  function:
    - key: wishes-resolver
      handler: src/resolvers/index.ts

  jira:projectPage:
    - key: wishes-page
      title: Wishes
      url: /wishes
      resolver:
        function: wishes-resolver

permissions:
  scopes:
    - write:jira-work
    - read:jira-work
```

### Simple test example

Test (`src/domain/services/__tests__/wish-service.test.ts`):

```typescript
import { describe, it, expect, jest } from '@jest/globals';
import { WishService } from '../wish-service';
import type { Wish } from '../../entities/wish';
import type { IJiraService } from '../../types'; // Shared types

// Mock the Jira service with proper TypeScript typing
const createMockJiraService = (): jest.Mocked<IJiraService> => ({
  createWish: jest.fn(),
  transitionIssue: jest.fn(),
  getWishes: jest.fn(),
});

describe('WishService', () => {
  it('should create a wish', async () => {
    const mockJiraService = createMockJiraService();
    mockJiraService.createWish.mockResolvedValue({ key: 'DEMO-1' });

    const wishService = new WishService(mockJiraService);
    const wish: Wish = await wishService.createWish('Learn Forge', 'Build awesome apps');

    expect(wish.title).toBe('Learn Forge');
    expect(wish.issueKey).toBe('DEMO-1');
    expect(wish.isPending()).toBe(true);
    expect(mockJiraService.createWish).toHaveBeenCalledWith('Learn Forge', 'Build awesome apps');
  });

  it('should fulfill a wish', async () => {
    const mockJiraService = createMockJiraService();
    mockJiraService.transitionIssue.mockResolvedValue(undefined);

    const wishService = new WishService(mockJiraService);
    const wish: Wish = await wishService.fulfillWish('DEMO-1');

    expect(wish.issueKey).toBe('DEMO-1');
    expect(wish.status).toBe('Done');
    expect(mockJiraService.transitionIssue).toHaveBeenCalledWith('DEMO-1', 'Done');
  });

  it('should handle invalid status gracefully', async () => {
    const mockJiraService = createMockJiraService();
    mockJiraService.getWishes.mockResolvedValue([
      {
        key: 'DEMO-1',
        fields: {
          summary: 'Test Wish',
          status: { name: 'InvalidStatus' }, // Invalid status
        },
      },
    ]);

    const wishService = new WishService(mockJiraService);
    const wishes: Wish[] = await wishService.getAllWishes();

    expect(wishes[0].status).toBe('Open'); // Should default to 'Open'
  });
});
```

### Complete directory structure

```
src/
├── index.ts              # Main entry point
├── types.ts              # Shared type definitions
├── frontend/
│   ├── index.tsx
│   └── __tests__/        # Component tests
├── domain/
│   ├── entities/
│   │   ├── wish.ts
│   │   └── __tests__/    # Entity tests
│   └── services/
│       ├── wish-service.ts
│       └── __tests__/    # Service tests
│           └── wish-service.test.ts
├── resolvers/
│   ├── index.ts          # Main resolver exports
│   ├── __tests__/        # Resolver tests
│   └── web/
│       └── wishes-resolver.ts
├── infrastructure/
│   └── jira-api/
│       ├── jira-service.ts
│       └── __tests__/    # API integration tests
├── shared/
│   └── errors/
│       └── __tests__/    # Error handling tests
└── setupTests.ts         # Jest test setup
```

### Testing approach

Note: The Forge app template does not include a testing framework by default. We recommend setting up Jest for backend testing, as all examples in this guide use Jest. However, you can use other testing frameworks (such as Mocha or AVA) with a similar setup and directory structure.

#### Why Jest?

Jest is a popular JavaScript testing framework that works well with TypeScript and modern JavaScript. It offers fast test execution, built-in mocking, and a straightforward configuration.

#### Setting up Jest

```
npm install --save-dev jest @types/jest ts-jest
```

Add a basic Jest configuration (e.g., `jest.config.js`):

```
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/__tests__/**/*.test.ts'],
  setupFilesAfterEnv: ['./setupTests.ts'],
};
```

For more details, see the Jest documentation.

#### Test organization

- **Co-located tests:** Place tests in `__tests__/` folders next to the files they test.
- **Naming:** Use the `.test.ts` suffix for test files (e.g., `wish-service.test.ts`).
- **Simple imports:** Use relative imports from tests to source files.
- **Test discovery:** Jest will automatically find tests in `__tests__/` folders.

#### Example directory structure

```
src/
├── domain/
│   ├── entities/
│   │   ├── wish.ts
│   │   └── __tests__/
│   │       └── wish.test.ts
│   └── services/
│       ├── wish-service.ts
│       └── __tests__/
│           └── wish-service.test.ts
├── resolvers/
│   ├── web/
│   │   └── wishes-resolver.ts
│   └── __tests__/
│       └── wishes-resolver.test.ts
└── setupTests.ts
```

#### Running tests

```
npm run test          # Run all tests
npm run test:watch    # Run tests in watch mode
npm run test:coverage # Run tests with coverage report
```
