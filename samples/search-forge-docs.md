{
  "query": "getting started overview",
  "results": [
    {
      "pageContent": "Subject: Getting started (part 1/2)\n\n# Prepare to build your first Forge app\n\nWelcome to developing with the Forge platform for Atlassian cloud apps. Work through the steps below to set up your development environment. To get started using Forge, you’ll install the CLI, log in with an Atlassian API scoped token, and create an Atlassian developer site that has Confluence and all of the Jira applications installed.\n\nAfter setting up, you'll go through a three-part tutorial to create a simple hello world app for Bitbucket, Confluence, Jira, or Jira Service Management.\n\nFor more of an introduction to creating and managing an app with the Forge CLI, check out our Atlassian Developer YouTube channel.\n\n## Before you begin\n\nForge apps are written in JavaScript so you'll need to be familiar with JavaScript. It's also helpful to be familiar with React.\n\nNote:  \nThe content on this page is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our Atlassian Government Cloud developer portal.\n\n### Set up Node.js\n\nThe Forge CLI requires a fully supported LTS release of Node.js installed; namely, versions 22.x or 24.x. Follow the Node.js setup instructions specific to your operating system below:\n\n## Install the Forge CLI\n\nInstall the Forge CLI using npm. You’ll install the CLI globally so that the commands can be run across your system. Warning:  \nDo not install `forge` with `root` privileges. In case that has been done, you might need to uninstall forge. This can be done using the command in mac (or similar in other OS)\n\n```\nsudo rm -rf ~/Library/Preferences/@forge\n\n```\n\n1. Install the Forge CLI globally by running:  \n```  \nnpm install -g @forge/cli  \n```\n2. Verify that the CLI is installed correctly by running:  \n```  \nforge --version  \n```\n\nYou should see a version number reported in the terminal. If a version number is not shown, then the installation failed. Repeat step 1 and look for errors reported in the terminal.\n\nWith the CLI installed, view the complete list of Forge commands by running `forge --help`.\n\n## Build your first Forge app\n\nAfter installing the Forge CLI, follow the prompts in the terminal, or use the steps outlined below to build a hello world app.\n\n1. Log in with your Atlassian account and API token. Token generation instructions below.  \n```  \nforge login  \n```\n2. Set up a cloud developer site.  \nA free Atlassian cloud developer site lets you install and test your app on Atlassian apps including Confluence and Jira. If you don't have one yet, set it up now:\n\n  1. Go to <http://go.atlassian.com/cloud-dev> and create a site using the email address associated with your Atlassian account.\n  2. Once your site is ready, log in and complete the setup wizard.\n3. Create a new Forge app from a template, or follow one of the detailed tutorials for a guided walkthrough.  \n```  \nforge create  \n```\n4. Deploy your app code to Forge.  \n```  \ncd <your-app-dir>  \nforge deploy  \n```\n5. Install the app to your Atlassian site. You can now view and test your app.  \n```  \nforge install  \n```\n6. Run a local tunnel for hot reload and log streams while developing.  \n```  \nforge tunnel  \n```",
      "metadata": {
        "product": "forge",
        "docType": "developer_documentation",
        "subject": "Getting started (part 1/2)",
        "source": "https://developer.atlassian.com/platform/forge/getting-started",
        "id": "5af6a75069274706466a1efcd7ccceb33d1852a1-0",
        "$dist": 0.52293384,
        "score": 0.47706616,
        "doc_type": "developer_documentation"
      }
    },
    {
      "pageContent": "Subject: Getting started (part 1/2)\n\n# Getting started with global:ui (EAP)\n\nWarning:  \nBy signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials and currently support only UI Kit (`render: native`), as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information. As conditions on your right to use the Forge global:ui module and Global component during this EAP, you agree not to (and not to authorize any third party to) deploy any Marketplace App using the Forge global:ui module or Global component in a Production environment.\n\nTo join the EAP for `global:ui`, complete the sign up form.\n\nFor more details, see Forge EAP, Preview, and GA.\n\nThis tutorial walks you through creating your first app using the `global:ui` module. By the end, you'll have a working global app that appears in the Atlassian app switcher with its own side navigation and content area.\n\n## Before you begin\n\nComplete Getting started before working through this tutorial.\n\nNote:  \nForge apps can't be viewed by anonymous users. When testing a Forge app, you should be logged in to your Atlassian cloud developer site.\n\n### Set up a cloud developer site\n\nAn Atlassian cloud developer site lets you install and test your app on Atlassian apps including Confluence and Jira. If you don't have one yet, set it up now:\n\n1. Go to <http://go.atlassian.com/cloud-dev> and create a site using the email address associated with your Atlassian account.\n2. Once your site is ready, log in and complete the setup wizard.\n\nYou can install your app to multiple Atlassian sites. However, app data won't be shared between separate Atlassian apps, sites, or Forge environments.\n\nThe limits on the numbers of users you can create are as follows:\n\n* Confluence: 5 users\n* Jira Service Management: 1 agent\n* Jira Software and Jira Work Management: 5 users\n\n## Install the experimental CLI\n\nThe `global:ui` module requires an experimental version of the Forge CLI during the EAP. Install it by running:\n\n```\nnpm install -g @forge/cli@latest\n\n```\n\nNote:  \nThis experimental CLI version includes `global:ui` templates. Once the EAP concludes, these templates will be available in the standard Forge CLI.\n\n## Create your app\n\nNote:  \nWhen you create a new app, Forge will prompt you to set a default environment. In this tutorial we use the `development` environment as our default. Learn more about staging and production environments.\n\n1. Navigate to the directory where you want to create the app. A new subdirectory with the app’s name will be created there.\n2. Create your app by running:  \n```  \nforge create  \n```\n3. Enter a name for your app (up to 50 characters). For example, _my-global-app_.\n4. Select **Global (EAP)** as the category.\n5. Select your template.\n6. Change to the app subdirectory to see the app files:  \n```  \ncd my-global-app  \n```",
      "metadata": {
        "product": "forge",
        "docType": "developer_documentation",
        "subject": "Getting started (part 1/2)",
        "source": "https://developer.atlassian.com/platform/forge/global-ui/getting-started",
        "id": "6a131991552525cfe3ca0eac6068be759e5de052-0",
        "$dist": 0.52774155,
        "score": 0.47225845,
        "doc_type": "developer_documentation"
      }
    },
    {
      "pageContent": "Subject: Overview (part 2/2)\n\n## Next steps\n\nReady to start building? Here are practical next steps to create apps using UI Kit:\n\nExplore example appsSee real-world examples of UI Kit apps across Jira, Confluence, and Bitbucket.\n\nBrowse example apps\n\nTry tutorialsFollow step-by-step tutorials to build your first UI Kit app.\n\nStart with tutorials",
      "metadata": {
        "product": "general",
        "docType": "developer_documentation",
        "subject": "Overview (part 2/2)",
        "source": "https://developer.atlassian.com/platform/forge/ui-kit/get-started-with-ui/",
        "id": "8294855752495e5c4d17d972f592dd397d84f9fb-1",
        "$dist": 0.5336703,
        "score": 0.46632969999999996,
        "doc_type": "developer_documentation"
      }
    }
  ]
}