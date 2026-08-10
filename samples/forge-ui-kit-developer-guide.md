---
title: 'Forge UI Kit developer guide'
description: '' # A short summary for search engines to display, max 120 chars
platform: platform
product: forge-mcp
category: devguide
subcategory: guides
date: '2025-10-15'
---

# Forge UI Kit developer guide

## Related tools

- forge-development-guide
- forge-app-manifest-guide
- atlassian-design-tokens
- confluence-macro-developer-guide
- jira-service-management-assets-guide

## Introduction

This guide focuses on frontend-specific concerns: UI Kit components, React patterns, bridge APIs, and frontend architecture. While UI Kit uses React-like syntax, there are important architectural differences and constraints you need to understand. You MUST not use React components directly. Only use UI Kit components from `@forge/react`.

## UI Kit-specific concepts

### What makes UI Kit different from React

- Sandboxed Environment: UI runs in isolation with no direct DOM access or browser APIs
- Component Restrictions: Must use UI Kit components exclusively - regular HTML elements won't work
- Limited React Features: No portals, ref forwarding, or arbitrary HTML
- Bridge Communication: Frontend communicates with backend via the `invoke()` function
- Permission Context: Frontend code always runs with user permissions
- Hooks: Hooks in Forge are different from normal React hooks. Example `useConfig` does not have a set function.

### Frontend vs backend separation

- Frontend (UI Kit): Lives in `src/frontend`, uses `@forge/bridge` and UI Kit components
- Backend (Resolvers): Handles business logic, can use `@forge/api` and app-level permissions
- Communication: Frontend calls backend resolvers via `invoke()` for data and operations
- JSM Assets Integration: For Assets CMDB frontend components (device selectors, object displays), see the jira-service-management-assets-guide tool for Assets-specific UI patterns and data handling

### Resolvers for backend communication

Resolvers are the mechanism by which front-end-backend separation is possible. They are the interface through which front-end and back-end communication is possible.

- Configuration: The manifest MUST be updated to have a resolver attribute for modules if backend logic is required for them. See the forge-app-manifest-guide tool for details on the `resolver` and other specific module configurations.
- Communication Contract: Shared TypeScript types MUST be used as the communication contract between frontend and backend. These data types MUST be used in the resolver functions to define their request payload format.
- Data Format: While submitting forms, you MUST ensure that the data submitted by each component matches the shared data types used for communication with the backend. If any component does not provide a default schema that matches the defined shared types, then the data MUST be converted into the required structure in the submit method. For complex components like UserPicker, always extract the required attributes and share them while communicating with the backend.
- Architecture Details: If your role is to focus on the frontend, then you are not authorised to implement the resolver function in detail or other backend code. However, frontend developers are responsible for establishing the contract between the frontend and backend, which means you must:
  1. Creating necessary files for the backend resolver functions
  2. Add empty resolver function stubs that return placeholder data of the correct shape. Don't write the handler implementation or other backend code.
  3. You must define the TypeScript types for the data sent to the resolver in `src/types/`.
  4. Add the references to resolver functions to the manifest.json.

### Frontend development setup

#### Frontend file organization

UI Kit-specific frontend structure:

```
src/
├── index.ts           # Exports backend resolvers
├── types/             # Shared type definitions
├── frontend/
    ├── index.tsx       # Main UI Kit entry point
    ├── components/     # Reusable UI Kit components (.tsx)
    ├── hooks/          # Custom React hooks for UI Kit (.ts)
    ├── utils/          # Frontend utilities (.ts)
    └── __tests__/      # UI Kit component tests (.test.tsx)
```

#### Manifest configuration

```yaml
modules:
  jira:issuePanel:
    - key: hello-world-panel
      resource: example-resource
      resolver:
        function: issue-panel-resolver
      render: native # Required for UI Kit modules
      title: Hello world!
      ...
```

Important: `render: native` is required for all UI Kit modules.

## Components

UI Kit provides pre-built components in the @forge/react package that align with Atlassian's design system. Note: these are NOT normal React components. They are configured differently. You are a Forge UI component expert. Before creating any React component using @forge/react, follow this checklist:

- Check if the component is a valid Forge component (not standard React) from the list below
- Confirm the component's intended usage pattern (individual vs group wrapper)
- Look up the exact prop interface for the component using the search-forge-docs tool
- Verify prop names, types, and required vs optional props
- Check for Forge-specific prop patterns (e.g., xcss, testId)
- Validate prop value formats and constraints
- Do not wrap components unnecessarily (avoid redundant Box/Stack/Inline)
- Choose the correct pattern: group vs individual vs layout wrapper.
- Follow Atlassian design system conventions
- Use proper spacing tokens (space.100, space.200, etc.)

### Component usage rules

#### Hierarchy & structure (Enforced by ESLint)

- Tabs: Tabs(id) -> TabList -> Tab(s) and sibling TabPanel(s). No defaultSelected/selected, no props on Tab except text content.
- CheckboxGroup: Requires name + options; never nest <Checkbox> children; no label prop; no mapped children pattern; no defaultChecked on inner checkboxes.
- Heading: Use size; never use level because it is deprecated.
- Form-like inputs (Textfield, TextArea, Select, DatePicker, TimePicker, Range, etc.): No built‑in label prop — use `<Label labelFor=...>` separately. Use search-forge-docs tool to check which inputs have required props like 'name'.
- Must not leave these empty: Text, Heading, Button, Box, Stack, and Inline.
- Remove unused empty containers instead of keeping them for “future layout.”
- Layout components must have meaningful children—not placeholders.

CRITICAL: Forge components are NOT standard React components. Always verify the component exists and check its props with the search-forge-docs tool before using. e.g.:

// Get ProgressBar value range and props
query: 'ProgressBar props'

// Get Form component props and usage examples
query: 'UI Kit Form component props onSubmit handleSubmit useForm'

// Get Tabs component props and onChange behavior
query: 'Tabs TabsProps onChange selected defaultSelected'

### Critical component patterns (Quick reference)

Agents often violate the following rules, so you must validate against these when generating or reviewing code.

#### Tabs (CRITICAL)

```tsx
// ✅ Correct
<Tabs id="main-tabs">
  <TabList>
    <Tab>Details</Tab>
    <Tab>History</Tab>
  </TabList>
  <TabPanel>{/* Details content */}</TabPanel>
  <TabPanel>{/* History content */}</TabPanel>
</Tabs>

// ❌ Wrong Patterns
// - <TabPanel> nested inside <Tab>
// - Missing <TabList>
// - Props on <Tab> (id/label/defaultSelected)
```

Rules: `Tabs` requires `id`; `TabList` groups all `Tab`s; `Tab`s contain only text; `TabPanel`s are direct children of `Tabs` in matching order; no selection props.

#### CheckboxGroup (CRITICAL)

```tsx
// ✅ Correct
<CheckboxGroup
  name="bodyParts"
  options={[
    { label: 'Head', value: 'head' },
    { label: 'Arms', value: 'arms' },
  ]}
  value={selectedValues || []}
  onChange={setSelectedValues}
/>
```

Common Mistakes (❌): using `label` instead of `name`; nesting `<Checkbox>` children; mapping children; using `defaultChecked` on inner checkboxes.

#### Labels

Most form inputs do NOT have a `label` prop. Always pair `<Label labelFor="field-id">Label</Label>` with the input’s `id`.

#### Empty components

Never leave `Text`, `Heading`, `Button`, `Box`, `Stack`, or `Inline` empty. Remove them instead of using them as spacers. Use spacing tokens via layout or `xcss`.

#### Defensive arrays

Wrap potentially undefined arrays: `(arr || [])` before `.map()/.filter()/.includes()` and when passing array props (`value`, `options`). To avoid errors in the UI preview. Minimal patterns:

```tsx
// map
{
  (data.items || []).map(it => <Text key={it.id}>{it.name}</Text>);
}
// includes
{
  (state.selected || []).includes(id) && <Tag>{id}</Tag>;
}
// CheckboxGroup value fallback
<CheckboxGroup name="bodyParts" options={opts} value={selectedValues || []} onChange={setSelectedValues} />;
```

#### Group vs individual

- Group Components (must wrap specific children): `Tabs`, `TabList`, `UserGroup`, `TagGroup`, `ButtonGroup`
- Individual Components (standalone; no redundant wrapping): `Textfield`, `Text`, `Heading`, `Button`, `Select`, `CheckboxGroup`, `DynamicTable`
- Wrapper/Layout Components: `Stack`, `Inline`, `Box` (keep only if adding layout/alignment/spacing)
- Group has required structural children (e.g. `UserGroup` → `<User>` children)
- Individual not redundantly wrapped
- Layout wrapper only when applying spacing/alignment or grouping multiple children

#### UserGroup example

```tsx
// ❌ Wrong - Treating UserGroup as standalone
<UserGroup users={[]} />

// ✅ Correct - UserGroup wraps <User> children
<UserGroup>
  <User accountId="123" />
  <User accountId="456" />
</UserGroup>
```

#### Heading

Use `size` prop only. Do NOT use `level`.

#### Button component

```ts
import { Button } from '@forge/react';

// ✅ Correct Button usage (children required)
<Button appearance="primary" onClick={handleClick} type="button">Save</Button>

// ❌ Common mistakes:
// - Using a 'text' prop (Button uses children)
// - Using native <button> instead of UI Kit Button
// - Styling with raw CSS instead of tokens / xcss
```

#### Quick error prevention checklist

```
[ ] Component exists in @forge/react
[ ] Tabs & CheckboxGroup follow exact structure
[ ] No empty structural/layout components
[ ] All arrays guarded with || []
[ ] Form fields use <Label>
[ ] Avoid unused or speculative props — keep surface minimal and intentional.
[ ] Only functional, working code (no commented placeholders)
[ ] No props on <Tab>; CheckboxGroup uses options not children
[ ] xcss used (not className)
```

### Layout components - common patterns & TypeScript usage

CRITICAL: Never include the title of the app within the UI. The title from the manifest is automatically rendered by the product above the app in the product chrome. If you also include it in the code, there is a duplication. Do NOT include the app title/name in the UI.

#### Stack component (Vertical Layout)

```ts
import { Stack } from '@forge/react';

// ✅ Correct Stack usage
<Stack space="space.100" alignInline="center" alignBlock="start" grow testId="stack-example">
  <Text>Item 1</Text>
  <Text>Item 2</Text>
</Stack>

// Some StackProps include:
// - space: spacing tokens ('space.025' ... 'space.1000')
// - alignInline: 'start' | 'center' | 'end' | 'stretch'
// - alignBlock: 'start' | 'center' | 'end' | 'stretch'
// - spread: 'space-between'
// - grow: 'hug' | 'fill'
```

#### Inline component (Horizontal Layout)

```ts
import { Inline } from '@forge/react';

// ✅ Correct Inline usage
<Inline space="space.050" alignBlock="baseline" alignInline="start" shouldWrap spread="space-between" separator="|" rowSpace="space.050" testId="inline-example">
  <Button appearance="primary">Action 1</Button>
  <Button appearance="default">Action 2</Button>
</Inline>

// Some InlineProps include:
// - space / rowSpace: spacing tokens
// - alignBlock: 'baseline' | 'start' | 'center' | 'end' | 'stretch' // 'baseline' should be used in most cases
// - alignInline: 'start' | 'center' | 'end' | 'stretch'
// - spread: 'space-between'
// - shouldWrap: boolean
// - separator: string
// - grow: 	'hug' | 'fill'
```

#### Box component

Box is a general-purpose container that allows for the controlled use of design tokens.

```ts
function ContainerExample(): JSX.Element {
  const containerStyles = xcss({
    padding: 'space.100',
    backgroundColor: 'color.background.neutral.subtle',
    borderRadius: 'border.radius',
  });

  return (
    <Box xcss={containerStyles}>
      <Text>Content inside a styled container</Text>
    </Box>
  );
}
```

#### Tables (DynamicTable)

The DynamicTable component provides an easy way to lay out elements in a table. It is highly configurable and can support very simple use cases, where you might normally use an HTML table, or more complex use cases with built-in pagination, sorting, re-ordering, and much more. Use the search-forge-docs tool to learn more about the DynamicTable component.

When laying out elements where there are nearly the same number of items per row, or alignment of values in rows would be nice, use the DynamicTable component instead of trying to format it with inline elements. A DynamicTable ensures a clean, aligned layout, even for small lists.

Metrics that focus on a key statistic may look better when displayed as cards made out of inline boxes.

Tables that display Jira issues often include the following columns:

- Issue Key (with link): Always first column, titled 'Work', sortable
- Summary (truncated): Main content, should truncate
- Status (with lozenge): Color-coded status indicators
- Assignee (with User component): Person responsible
- Priority (with icon): Visual priority indicators
- Updated (relative time): Last modified timestamp

### Formatting & design tokens

Forge apps should look like part of an Atlassian product. Use emojis sparingly since they can make a UI look unprofessional.

The Box component supports the XCSS property. To style the box component, use the xcss utility function to wrap the XCSS style definition before passing it to the component. Use the `design-tokens-list` tools to see a full list of the available tokens.

For space in layout, you must use design tokens like "space.200", "space.500" instead of old space values like "medium", "large".

Find available property values using the search-forge-docs tool. Most components DO NOT support design tokens, and their properties are NOT regular React properties, so you MUST look up the props using the knowledge fragments tool.

```ts
import React from 'react';
import { Heading, Box, Stack, Link, xcss, Inline, Text } from '@forge/react';

const textStyle = xcss({
  color: 'color.text',
  marginBottom: 'space.100',
});

const cardStyle = xcss({
  backgroundColor: 'elevation.surface',
  padding: 'space.200',
  borderColor: 'color.border',
  borderWidth: 'border.width',
  borderStyle: 'solid',
  borderRadius: 'border.radius',
  ':hover': {
    backgroundColor: 'elevation.surface.hovered',
  },
});

const GetStartedCard = ({ header, description }) => {
  return (
    <Box xcss={cardStyle}>
      <Stack space="space.100" alignInline="start">
        <Heading as="h3" level="h600">{header}</Heading>
        <Text xcss={textStyle}>{description}</Text>
        <Link href="/">Get started</Link>
      </Stack>
    </Box>
  );
}

export const InteractivityExample = () => (
  <Inline space="space.200" alignBlock="baseline">
    <GetStartedCard header="Set up" description="Create a project and add tasks" />
    <GetStartedCard header="Plan project" description="Assign tasks and set timelines" />
  </Inline>
);
```

## Available UI Kit (@forge/react) components

Remember: Forge components are NOT standard React components. Always verify the component's existence and check its props with the search-forge-docs tool before using it.

### Action components

Use action components to initiate or execute specific tasks within your app.

| Component   | Description                                        |
| ----------- | -------------------------------------------------- |
| Button      | A button that triggers an event or action.         |
| ButtonGroup | A button group displays multiple buttons together. |
| Link        | A component for displaying inline links.           |

### Content & image components

Use content and image components to display text, visuals, and other data in your app.

| Component         | Description                                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AdfRenderer       | A renderer for ADF documents.                                                                                                                          |
| Code              | A code highlight for short strings in the body text.                                                                                                   |
| CodeBlock         | A code block highlights an entire block of code and keeps the formatting.                                                                              |
| Comment (Preview) | A comment displays discussions and user feedback.                                                                                                      |
| DynamicTable      | A table that displays rows of items with optional pagination, sorting, and re-ordering functionality. Use this for table layouts, even for short lists |
| Image             | An image, which functions similarly to a native img element.                                                                                           |
| Icon              | A visual representation for actions or other items.                                                                                                    |
| User              | A representation of a user, displaying details such as name and profile picture.                                                                       |
| UserGroup         | A stack-like entity that encompasses multiple users, including their names and profile pictures.                                                       |

### Feedback components

Use feedback components to provide users with responses or notifications based on their actions in your app.

| Component       | Description                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------ |
| Badge           | A visual indicator for numeric values, such as tallies and scores.                               |
| EmptyState      | An empty state appears when there is no data to display and describes what the user can do next. |
| Lozenge         | A visual indicator to display different status types or states.                                  |
| ProgressBar     | A progress bar communicates the status of a system process.                                      |
| ProgressTracker | A progress tracker displays the steps and progress through a journey.                            |
| SectionMessage  | A text callout to alert users to important information.                                          |
| Spinner         | A spinner is an animated spinning icon that lets users know content is being loaded.             |
| Tag             | A visual indicator for UI objects for quick recognition.                                         |
| TagGroup        | A group of tag components.                                                                       |
| Tooltip         | A floating, non-actionable label used to explain a user interface element or feature.            |

### Primitive & layout components

Use layout components to structure and organize elements within your app.

| Component           | Description                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| Tabs                | Tabs are used to organize content by grouping similar information on the same page. |
| Box                 | A box is a generic container that provides managed access to design tokens.         |
| Inline              | An inline manages the horizontal layout of direct children using flexbox.           |
| Pressable (Preview) | A pressable is a primitive for building custom buttons.                             |
| Stack               | A stack manages the vertical layout of direct children using flexbox.               |
| xcss (utility)      | A styling helper that returns token-aware styles (not a component).                 |

### Overlays components

Use overlay components to highlight certain areas or display additional information in your app.

| Component       | Description                                                                        |
| --------------- | ---------------------------------------------------------------------------------- |
| Modal           | A dialog that appears in a layer above the app's UI and requires user interaction. |
| Popup (Preview) | A pop-up displays brief content in an overlay.                                     |

### Selection & input components

Use selection and input components to allow users to enter information or choose options in your app.

CRITICAL: Most form components do NOT have a built-in `label` prop. You must use separate `Label` components with proper `labelFor` attributes.

| Component            | Description                                                                                                                            |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Calendar (Preview)   | An interactive calendar for date selection experiences.                                                                                |
| Checkbox             | An input control that allows a user to select one or more options from a number of choices.                                            |
| CheckboxGroup        | A list of options where one or more choices can be selected.                                                                           |
| DatePicker           | A date picker allows the user to select a particular date.                                                                             |
| Form                 | A form component that allows for the inclusion of a list of components, a submit button, and a function that handles the submit event. |
| InlineEdit (Preview) | An inline edit displays a custom input component that switches between reading and editing on the same page.                           |
| Radio                | A radio input allows users to select only one option from a number of choices.                                                         |
| RadioGroup           | A radio group presents a list of options where only one choice can be selected.                                                        |
| Range                | A range lets users choose an approximate value on a slider.                                                                            |
| Select               | A dropdown field that allows users to select an option from a list.                                                                    |
| Text area            | An input field that lets users enter long form text, which spans over multiple lines.                                                  |
| Textfield            | An input field that allows a user to write or edit text.                                                                               |
| TimePicker (Preview) | A time picker allows the user to select a specific time.                                                                               |
| Toggle               | A component that allows users to switch between two states, such as on/off or true/false.                                              |
| UserPicker           | A dropdown field that allows users to search and select users from a list.                                                             |

### Typography components

Use typography components to manage the style and appearance of text within your app.

| Component      | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| Heading        | A typography component used to display text in different sizes and formats. |
| List (Preview) | A typography component used to display dot points or numbered lists.        |
| Text           | A typography component used to display body text.                           |

### Data visualizations components

Use these components to create visual representations of your data, making it easier to understand at a glance.

| Component               | Description                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| BarChart                | A visual representation of data using rectangular bars of varying heights to compare different categories or values.                        |
| DonutChart              | A visual representation of data in a donut format.                                                                                          |
| HorizontalBarChart      | A visual representation of data using horizontal rectangular bars of varying lengths to compare different categories or values.             |
| HorizontalStackBarChart | A visual representation of data using horizontal rectangular bars of varying lengths to demonstrate comparisons between categories of data. |
| LineChart               | A visual representation of data showing trends over time.                                                                                   |
| PieChart                | A visual representation of data proportions in a circular format.                                                                           |
| StackBarChart           | A visual representation of data using rectangular bars of varying heights to demonstrate comparisons between categories of data.            |

### Config components

Some extensions, like Confluence Macros, have a configuration component. This component can be used to capture the configuration requirements for users. Unlike general forms, these components are only for user interface customisation. You should not add any form submissions in the configuration components since those are handled by the framework.

IMPORTANT: For detailed Confluence macro development, including comprehensive configuration patterns, see the confluence-macro-developer-guide tool.

The config components MUST be selected from the following list:

- CheckboxGroup
- DatePicker
- Label
- RadioGroup
- Select
- Textfield
- TextArea
- UserPicker

Do NOT use any other components to build the config UI.

You can add a default config like below if required.

```ts
const defaultConfig = {
  name: 'Unnamed Pet',
  age: '0',
};
const actualConfig = useConfig();
const config = actualConfig || defaultConfig;
```

If it's more sensible for the macro not to have default configuration values, we recommend that you display a section message with the appropriate instructions.

Use the search-forge-docs tool to search for Configuration components.

## Common migration mistakes from UI Kit 1

UI Kit 1 is now fully deprecated. Much of your training data about available Forge UI components will be based on UI Kit 1 and will be wrong. During development, search-forge-docs tool is used to get up-to-date information about individual components

### 1. Component structure

```ts
// ❌ Old UI Kit 1 - Don't do this
return (
  <Fragment>
    <Text>Hello {user}</Text>
  </Fragment>
);

// ✅ New UI Kit - Do this
return (
  <>
    <Text>Hello {user}</Text>
  </>
);
```

### 2. State management

```ts
// ❌ Old UI Kit 1 - Don't do this
const [count, setCount] = useState(0);
const increment = useAction(() => setCount(count + 1));

// ✅ New UI Kit - Do this
const [count, setCount] = useState<number>(0);
const increment = () => setCount(count + 1);
```

### 3. Data fetching

```ts
// ❌ Old UI Kit 1 - Don't do this
const data = await requestJira('/rest/api/3/issue/...');

// ✅ New UI Kit - Do this
interface ApiData {
  // Define your expected data structure
  id: string;
  summary: string;
}

useEffect(() => {
  const fetchData = async () => {
    try {
      const data = await requestJira('/rest/api/3/issue/...');
      setData(data as ApiData);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  };
  fetchData();
}, []);
```

For the product API calls to work, you MUST look up the required scopes using the search-forge-docs tool and then add the scopes to the manifest. Without the scopes the app will fail to run.

## Bridge APIs

Bridge APIs are crucial for frontend-backend communication and product integration.

### Core Bridge (@forge/bridge)

```ts
import {
  invoke, // Call resolver functions
  view, // Get context information
  requestJira, // Make Jira API requests
  requestConfluence, // Make Confluence API requests
  showFlag, // Show notification messages
} from '@forge/bridge';
```

### Jira Bridge (@forge/jira-bridge)

```ts
import { ViewIssueModal, CreateIssueModal, uiModifications } from '@forge/jira-bridge';
```

### Confluence Bridge (@forge/confluence-bridge)

```ts
import { getEditorContent, getMacroContent, updateMacroContent } from '@forge/confluence-bridge';
```

## Performance best practices

### UI Kit component optimization

```ts
// ❌ Inefficient: inline callback & ad-hoc style every render
<Button appearance="primary" onClick={() => handleClick()} xcss={xcss({ padding: 'space.100' })}>Save</Button>

// ✅ Optimized: stable callback & extracted styles
const handleClick = useCallback(() => {
  // logic
}, []);

const buttonStyles = xcss({ padding: 'space.100' });

<Button appearance="primary" onClick={handleClick} xcss={buttonStyles}>Save</Button>
```

### UI Kit-specific performance tips

- Use local state for UI-only concerns to avoid unnecessary resolver calls
- Implement proper loading states with `<Spinner />` for better UX
- Batch-related bridge API requests when possible
- Use `useCallback` and `useMemo` for stable props to UI Kit components

## State management patterns

### Event handling in Forms

Forge UI Kit form components use `SerialisableEvent` instead of standard React events. Always extract values from `event.target.value`:

```ts
// ✅ Correct event handling pattern
<Textfield
  onChange={(e) => setFormData((s) => ({
    ...s,
    fieldName: String((e as any).target?.value ?? '')
  }))}
/>

// For Select components, use option object:
<Select
  value={{ label: 'Display', value: 'key' }}
  onChange={(option) => setFormData((s) => ({
    ...s,
    fieldName: String((option as any)?.value ?? '')
  }))}
/>
```

### Local state

```ts
interface ComponentData {
  id: string;
  name: string;
  // Define your data structure
}

const MyComponent = (): JSX.Element => {
  const [data, setData] = useState<ComponentData[] | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const result = await invoke('getDataResolver');
        setData(result as ComponentData[]);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <Spinner />;
  return <DynamicTable rows={data || []} />;
};
```

## Form state

On the submit method of the form, you MUST ensure that data received from all form components is converted to the data format matching the common shared types instead of passing the form data received from each form component directly to invoke backend invocations. Not all attributes required by backend will be in same format as the form components supply so it MUST be converted into common shared type data format which is used by resolver functions as well.

```ts
interface FormData {
  name: string;
  // Define your form fields
}

const FormComponent = (): JSX.Element => {
  const [formData, setFormData] = useState<FormData>({ name: '' });
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true);
    try {
      await invoke('submitDataResolver', { data });
    } catch (error) {
      console.error('Form submission failed:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Form onSubmit={onSubmit}>
      <Textfield
        value={formData.name}
        onChange={(value) => setFormData({ ...formData, name: value })}
      />
      <Button type="submit" isDisabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </Button>
    </Form>
  );
};
```

### Common issues

1. "Cannot use X in frontend code"
   - Likely trying to use `@forge/api` in frontend
   - Move logic to the resolver
2. "Component is not updating"
   - Check React dependency array in useEffect
   - Verify state updates are working
3. "Resolver not receiving data"
   - Check data serialization
   - Ensure proper async/await usage

## Error handling

### API calls

```ts
interface IssueData {
  id: string;
  key: string;
  fields: {
    summary: string;
    // Define expected issue structure
  };
}

try {
  const data = await requestJira('/rest/api/3/issue/...');
  return data as IssueData;
} catch (error) {
  console.error('API request failed:', error);
  showFlag({
    title: 'Error',
    type: 'error',
    description: 'Failed to load issue data',
  });
  throw error;
}
```

## Testing

### Component testing

```ts
import { render, act } from '@testing-library/react';
import { invoke } from '@forge/bridge';

// Mock Forge modules that aren't available in test environment
jest.mock('@forge/bridge', () => ({
  invoke: jest.fn(),
}));

jest.mock('@forge/react', () => ({
  __esModule: true,
  default: {
    render: jest.fn(),
  },
  Text: ({ children }: { children: React.ReactNode }) => children,
  Spinner: () => 'Loading...',
}));

test('component renders data correctly', async () => {
  const mockInvoke = invoke as jest.MockedFunction<typeof invoke>;
  mockInvoke.mockResolvedValueOnce({ data: 'test' });

  await act(async () => {
    render(<MyComponent />);
  });

  // Assert rendered content
});
```

### Testing Bridge interactions

```ts
interface TestFormData {
  name: string;
}

test('component calls resolver correctly', async () => {
  const mockInvoke = invoke as jest.MockedFunction<typeof invoke>;
  mockInvoke.mockResolvedValueOnce({ success: true });

  render(<CreateForm />);
  // Trigger form submission

  expect(mockInvoke).toHaveBeenCalledWith('createItem', {
    name: 'Test Item'
  } as TestFormData);
});
```

## Available hooks

### Supported React hooks

```ts
import {
  useState,
  useEffect,
  useContext,
  useReducer,
  useCallback,
  useMemo,
  useRef,
  useDebugValue,
  useDeferredValue,
  useId,
} from 'react';
```

## Code generation best practices

Before generating any code, validate against the Quick Error Prevention Checklist (in Critical Component Patterns). Only emit fully working code: real imports, valid hooks, complete components (no placeholders), and no commented-out or speculative blocks. If an implementation detail is unknown, restructure or clarify instead of emitting non-functional stubs.

### Code quality anti-patterns (CRITICAL)

#### Non-functional code prevention

Enforce: existing imports only; functional hooks; no experimental/placeholder/commented-out code; validate logic before emitting. See consolidated checklist above.

```ts
// ❌ WRONG - Non-functional useEffect that needs commenting
React.useEffect(() => {
  const getContext = async () => {
    try {
      const context = await view.getContext();
      const key = (context as any)?.moduleKey || '';
      setModuleKey(key);
    } catch (e) {
      setModuleKey('');
    }
  };
  getContext();
}, []);

// ❌ WRONG - Code that requires commenting to work
// React.useEffect(() => {
//   // This doesn't work, commenting it out
// }, []);

// ✅ CORRECT - Only generate working, functional code
useEffect(() => {
  const getContext = async () => {
    try {
      const context = await view.getContext();
      const key = context?.moduleKey || '';
      setModuleKey(key);
    } catch (e) {
      setModuleKey('');
    }
  };
  getContext();
}, []);
```

## Documentation resources

ALWAYS use the search-forge-docs tool before using a UI Kit component for component props, examples, and usage patterns. UI Kit components are NOT regular React components; they have different props. Also use the tool to search for bridge APIs, React hooks, module configuration.

See the confluence-macro-developer-guide tool for:

- Macro Development: Confluence-specific patterns and configuration
- Macro Configuration: Advanced configuration UI patterns and data handling
- Page Context: Accessing the Confluence page and space context
