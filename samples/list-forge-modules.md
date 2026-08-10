---
title: 'List Forge Modules'
description: '' # A short summary for search engines to display, max 120 chars
platform: platform
product: forge-mcp
category: devguide
subcategory: guides
date: '2025-10-15'
---

# Forge modules by app

## Related tools

- forge-development-guide
- forge-app-manifest-guide
- forge-ui-kit-developer-guide
- forge-backend-developer-guide
- jira-service-management-assets-guide
- confluence-macro-developer-guide

Once you find the module you want, use the search-forge-docs tool to find the module key and other important details. However, be careful that the tool has returned details for the module you want and not something similar.

## Common modules (Platform)

Available as part of the Forge platform (product agnostic):

- Consumer `consumer`: Define how the queue processes async events
- Function `function`: Define the app's behavior
- Scheduled Trigger `scheduledTrigger`: Invoke functions repeatedly at set intervals
- Trigger `trigger`: Invoke functions when product events occur
- Web Trigger `webtrigger`: Invoke functions via HTTP requests. **Security**: Web triggers have no built-in auth; the app must implement authentication in the handler function or endpoints are public and insecure.

## Jira modules

- Jira Admin Page `jira:adminPage`: Adds an item in the Apps section of the left navigation of Jira admin settings. When the item is clicked, content is rendered on a new Jira page.
- Jira Backlog Action `jira:backlogAction`: Adds a menu item to the more actions menu on the backlog view. When the menu item is clicked, the associated Forge app for the module is rendered
- Jira Board Action `jira:boardAction`: Adds a menu item to the more actions menu on the board view. When the menu item is clicked, the associated Forge app for the module is rendered.
- Jira Custom Field `jira:customField`: Creates a new custom field in Jira, which makes it easier for users to add information to issues, specific to their teams' needs.
- Jira Custom Field Type `jira:customFieldType`: Create a new custom field type in Jira, which lets Jira administrators create new custom fields based on that type.
- Jira Dashboard Background Script `jira:dashboardBackgroundScript`: Add invisible containers to Dashboards
- Jira Dashboard Gadget `jira:dashboardGadget`: Creates a dashboard gadget that is displayed on the Dashboards page.
- Jira Entity Property `jira:entityProperty`: Requests that fields of an entity property are indexed by Jira to make the fields available to query in JQL.
- Jira Global Page `jira:globalPage`: Adds an item in the Apps section of the main navigation.
- Jira Global Permission `jira:globalPermission`: Create custom global permissions
- Jira Issue Action `jira:issueAction`: Adds a menu item to the more actions menu on the issue view. When the menu item is clicked, the module's function renders a modal dialog.
- Jira Issue Activity `jira:issueActivity`: Add items to Activity panel of Jira issues.
- Jira Issue Context `jira:issueContext`: Adds a collapsible panel under the other fields on the right side of the issue view. These panels give users a quick way to get information related to the issue.
- Jira Issue Glance `jira:issueGlance`: Adds an issue glance to Jira, which is content that is shown/hidden (toggleable) in an issue by clicking a button.
- Jira Issue Navigator Action `jira:issueNavigatorAction`: Adds a menu item to the apps menu on the issue navigator view. When the menu item is clicked, the associated Forge app for the module is rendered.
- Jira Issue Panel `jira:issuePanel`: Adds an issue panel to a Jira issue when a configured button is clicked. The content of the module is shown above the Activity panel on a Jira issue
- Jira Issue View Background Script `jira:issueViewBackgroundScript`: Add invisible containers for updates to the issue view page.
- Jira JQL Function `jira:jqlFunction`: Define custom JQL functions which appear built-in from the user's perspective. This means that they're visible in the query editor and show up in the autocomplete dropdown.
- Jira Personal Settings Page `jira:personalSettingsPage`: Create personal settings pages. Adds an item to the user's profile menu in the main navigation. When the item is clicked, content is rendered on a new Jira page.
- Jira Project Page `jira:projectPage`: Add custom project pages. This adds the app in the horizontal tab navigation in Jira.
- Jira Project Permission `jira:projectPermission`: Create project-specific permissions. Helps in managing permissions for operations performed on objects related to projects.
- Jira Project Settings Page `jira:projectSettingsPage`: Add items to project settings sidebar.
- Jira Sprint Action `jira:sprintAction`: Add menu items to sprint cards in the backlog view. When the menu item is clicked, the associated Forge app for the module is rendered.
- Jira Time Tracking Provider `jira:timeTrackingProvider`: Customize work log experience. Allows an app to replace Jira's native time tracking components with ones defined by the app.
- Jira UI Modifications `jira:uiModifications`: Modify Jira UI. It allows to change the look and behavior of Jira and Jira Service Management.
- Jira Workflow Validator `jira:workflowValidator`: Create workflow validators that can be added to workflow transitions in company-managed projects.
- Jira Workflow Condition `jira:workflowCondition`: Create workflow conditions that can be configured on workflow transitions in company-managed projects.
- Jira Workflow Post Function `jira:workflowPostFunction`: Create workflow post functions that can be configured on workflow transitions in company-managed projects.
- Jira Command Palette `jira:command`: Add items to command palette. They can be used to navigate to app-defined pages (such as jira:globalPage modules) or open custom modals.

## Bitbucket modules

- Custom Merge Check `bitbucket:mergeCheck`: Define custom merge checks. The module allows a Forge app to define checks that can prevent pull requests from merging in Bitbucket until the specified conditions have been met.
- Dynamic Pipelines Provider `bitbucket:dynamicPipelinesProvider`: Generate pipeline definitions. Dynamic Pipelines provider generates pipeline definition at runtime using dynamic logic.
- Repository Code Overview Card `bitbucket:repoCodeOverviewCard`: Adds a card on the right hand sidebar of the repository source page.
- Repository Code Overview Action `bitbucket:repoCodeOverviewAction`: Adds a menu item in the more actions menu on the repository source page. When the menu item is clicked, the module's function renders a modal dialog.
- Repository Code Overview Panel `bitbucket:repoCodeOverviewPanel`: Adds an expandable panel on the repository source page
- Repository Pull Request Card `bitbucket:repoPullRequestCard`: Adds a card on the right hand sidebar of the pull request page
- Repository Pull Request Action `bitbucket:repoPullRequestAction`: Adds a menu item in the more actions menu on the pull request page. When the menu item is clicked, the module's function renders a modal dialog.
- Repository Pull Request Overview Panel `bitbucket:repoPullRequestOverviewPanel`: Adds an expandable panel on the overview tab of the pull request page.
- Repository Main Menu Page `bitbucket:repoMainMenuPage`: Adds a menu item at the bottom of the left navigation of Bitbucket repository pages.
- Repository Settings Menu Page `bitbucket:repoSettingsMenuPage`: Adds an item in the FORGE APPS section of the left navigation of Bitbucket repository settings menu.
- Workspace Settings Menu Page `bitbucket:workspaceSettingsMenuPage`: Adds an item in the FORGE APPS section of the left navigation of Bitbucket workspace settings menu.

## Compass modules

- Compass Admin Page `compass:adminPage`: Add admin configuration pages that is accessible by navigating to Apps, then clicking Configure for the app.
- Compass Component Page `compass:componentPage`: Adds an item to the left navigation on the Compass component details page.
- Compass Data Provider `compass:dataProvider`: Send events and metrics
- Compass Global Page `compass:globalPage`: Create new Compass pages that is accessible by clicking on the Apps dropdown, then clicking on the page name.
- Compass Team Page `compass:teamPage`: Adds an item to the left navigation to team details page.

## Confluence modules

### UI modules

- Confluence Content Action `confluence:contentAction`: Add menu items to the more actions for pages/blogs
- Confluence Content Byline Item `confluence:contentBylineItem`: Add content byline entries, which is the part of the content under the title that includes metadata about contributors and more.
- Confluence Context Menu `confluence:contextMenu`: Add context menu entries. It displays an entry in the context menu when a user selects some text on a page or blog.
- Confluence Custom Content `confluence:customContent`: Create a new custom content type in Confluence that behaves like built-in content types, such as page, blog post or comment
- Confluence Global Page `confluence:globalPage`: Create top-level pages. Displays content in place of a Confluence page. Each module appears as a link in the main navigation menu in Apps section
- Confluence Global Settings `confluence:globalSettings`: Add top-level settings. This module adds a link to the left navigation menu in Confluence global settings.
- Confluence Homepage Feed `confluence:homepageFeed`: Add dynamic content. This module displays content in the right panel of the Confluence Home page.
- Macro `macro`: Insert app UI within a page
- Confluence Page Banner `confluence:pageBanner`: Add page banners to Confluence pages. The banner can be used to display information, notifications, or other content relevant to the page.
- Confluence Space Page `confluence:spacePage`: Create space pages. Displays content in place of a Confluence page. Each module appears as a link in the space navigation menu.
- Confluence Space Settings `confluence:spaceSettings`: Add integration settings. This module adds a tab inside the integration settings of a Confluence space.

### Non-UI modules

- Confluence Background Script `confluence:backgroundScript`: Run background scripts. Adds an invisible container across various Confluence views. This container runs app functions in the background of a page.

## Jira Service Management modules

- Assets Import Type `jiraServiceManagement:assetsImportType`: Displays a modal that allows users to configure their Forge-based imports with information such as login details or configuration information for their app.
- Organization Panel `jiraServiceManagement:organizationPanel`: Adds a panel to the Organization page in the Project settings section. The content of the module is rendered above the search box present on the page.
- Portal Footer `jiraServiceManagement:portalFooter`: Adds a panel at the bottom of customer portal pages
- Portal Header `jiraServiceManagement:portalHeader`: Adds a panel at the top of customer portal pages. This module can be used in Jira Service Management.
- Portal Profile Panel `jiraServiceManagement:portalProfilePanel`: Adds a panel to the Profile page in Jira Service Management portal.
- Portal Request Create Property Panel `jiraServiceManagement:portalRequestCreatePropertyPanel`: This module is displayed on the request creation screen in the customer portal and enables apps to save arbitrary data during request creation as Jira issue properties.
- Portal Request Detail `jiraServiceManagement:portalRequestDetail`: Adds a panel to a portal request. The content of the module is shown below the Activity panel on a portal request.
- Portal Request Detail Panel `jiraServiceManagement:portalRequestDetailPanel`: Adds a panel to a portal request in side panel. The content of the module is shown at the bottom of request side panel.
- Portal Request View Action `jiraServiceManagement:portalRequestViewAction`: Adds an option item to the request view action section that shows up request details page on Jira Service Management customer portal.
- Portal Subheader `jiraServiceManagement:portalSubheader`: Adds a panel rendered underneath the title of customer portal pages.
- Portal User Menu Action `jiraServiceManagement:portalUserMenuAction`: Adds a menu item to the user menu that shows up on Jira Service Management customer portal.
- Queue Page `jiraServiceManagement:queuePage`: Adds an item in the Apps section. You can find the Apps section in the left navigation of Queues in a service project. When the item is clicked, content is rendered on a new Jira page.

Note: For JSM apps integrating with Assets CMDB (Configuration Management Database), see the jira-service-management-assets-guide tool for comprehensive guidance on:

- Assets-specific module configuration and permissions
- AQL (Assets Query Language) integration patterns
- Object lifecycle management and data modeling
- Required scopes: `read:cmdb-object:jira`, `read:cmdb-schema:jira`, `read:cmdb-type:jira`, etc.

## Rovo modules

- Rovo Agent `rovo:agent`: Configure AI teammates. Agents are configurable AI teammates that integrate into Jira and Confluence workflows.
- Action `action`: This module lets a Rovo Agent perform a specific task, like calling an API or running predefined code.
