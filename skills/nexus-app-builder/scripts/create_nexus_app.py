#!/usr/bin/env python3
"""
Automated Nexus App Creation Script
Wraps 'nexus create' with non-interactive friendly behavior and better error handling.

Run from the skill directory:
    python3 -m scripts.create_nexus_app --template react-custom-ui --name my-app

Reference: wiki/reference/cli/create.md
"""

import argparse
import json
import os
import subprocess
import sys


# Templates listed by wiki/reference/cli/create.md. The Nexus CLI does not
# provide a command to enumerate templates dynamically, so this list is
# maintained from the documentation.
NEXUS_TEMPLATES = [
    "angular-custom-ui",
    "vue-custom-ui",
    "react-custom-ui",
    "javascript-custom-ui",
    "event-typescript",
    "webhook-typescript",
]


def validate_prerequisites():
    """Check if Nexus CLI and Node.js are available."""
    try:
        subprocess.run(["nexus", "--version"], capture_output=True, check=True)
        subprocess.run(["node", "-v"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def validate_template(template_name):
    """
    Validate that a template name is one of the templates supported by Nexus CLI.
    Returns (is_valid, suggestions) tuple.
    """
    if template_name in NEXUS_TEMPLATES:
        return True, None

    words = template_name.lower().replace("-", " ").split()
    suggestions = []
    for valid_template in NEXUS_TEMPLATES:
        valid_words = valid_template.lower().replace("-", " ").split()
        if any(word in valid_words for word in words):
            suggestions.append(valid_template)

    return False, suggestions[:5] if suggestions else NEXUS_TEMPLATES[:5]


def check_login():
    """
    Check whether the current developer is logged in.

    Uses `nexus whoami --json`. On success it prints a JSON array of accounts,
    for example:

        [
          {
            "account_id": "...",
            "account_name": "Shaun",
            "account_mobile": "..."
          }
        ]

    When unauthenticated it exits non-zero and prints:

        Unauthorized. Run nexus login to log in again.

    Returns (logged_in, identity) where identity is the account display name
    when logged in, or the error message when not.
    """
    result = subprocess.run(
        ["nexus", "whoami", "--json"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        return False, message

    try:
        accounts = json.loads(result.stdout)
    except json.JSONDecodeError:
        return False, result.stdout.strip()

    if not isinstance(accounts, list) or not accounts:
        return False, result.stdout.strip()

    account = accounts[0]
    identity = account.get("account_name") or account.get("account_id") or ""
    return True, identity


def create_app(template, app_name, output_dir=None):
    """
    Create a Nexus app using 'nexus create'.

    Args:
        template: Template name (e.g., 'react-custom-ui').
        app_name: Name for the new app.
        output_dir: Parent directory where the app folder will be created.

    Returns:
        True if successful, False otherwise.
    """
    if not validate_prerequisites():
        print("❌ Prerequisites missing. Ensure Node.js v24+ and Nexus CLI are installed.")
        print("   Install: npm install -g @pc-nexus/cli")
        return False

    is_valid, suggestions = validate_template(template)
    if not is_valid:
        print(f"❌ Template '{template}' is not recognized.")
        print("\n📋 Did you mean one of these?")
        for suggestion in suggestions:
            print(f"   - {suggestion}")
        print("\n💡 Supported templates are documented in wiki/reference/cli/create.md")
        return False

    logged_in, identity = check_login()
    if not logged_in:
        print("❌ You are not logged in to Nexus CLI.")
        print("   Run `nexus login` in your terminal and provide your personal access token.")
        if identity:
            print(f"   Details: {identity}")
        return False
    print(f"👤 Logged in as: {identity}")

    cwd = os.path.abspath(output_dir) if output_dir else os.getcwd()

    if not os.path.isdir(cwd):
        print(f"❌ Parent directory does not exist: {cwd}")
        return False

    app_path = os.path.join(cwd, app_name)
    if os.path.exists(app_path):
        print(f"❌ Directory already exists: {app_path}")
        print("   Choose a different app name or remove the existing folder.")
        return False

    # `nexus create --help` exposes no non-interactive / accept-terms
    # flag, so we rely on --template to skip the template prompt. The command
    # is run from the parent directory and Nexus creates the app subfolder.
    cmd = ["nexus", "create", app_name, "--template", template]

    try:
        print(f"\n📦 Creating Nexus app: {app_name}")
        print(f"📋 Template: {template}")
        print(f"📂 Location: {cwd}")
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

        if result.returncode != 0:
            stderr = result.stderr.strip()
            stdout = result.stdout.strip()
            print(f"❌ Failed to create app (exit code {result.returncode})")
            if stdout:
                print(f"\n--- stdout ---\n{stdout}")
            if stderr:
                print(f"\n--- stderr ---\n{stderr}")
            print("\n💡 If the CLI requires an interactive terminal, run manually:")
            print(f"   nexus create {app_name} --template {template}")
            return False

        print(f"✅ App created successfully at: {app_path}")
        print("📝 Next steps:")
        print(f"   1. cd {app_path}")
        print("   2. Customize manifest.yaml, src/resolvers/index.ts, and web/main")
        print("   3. npm run build-web")
        print("   4. nexus deploy -e development")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create app: {e}")
        if e.stdout:
            print(f"\n--- stdout ---\n{e.stdout}")
        if e.stderr:
            print(f"\n--- stderr ---\n{e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Automated Nexus app creation"
    )
    parser.add_argument(
        "--template",
        required=True,
        help="Nexus template (e.g., react-custom-ui, angular-custom-ui)",
    )
    parser.add_argument("--name", required=True, help="App name")
    parser.add_argument(
        "--directory",
        help="Parent output directory (defaults to current directory)",
    )

    args = parser.parse_args()

    success = create_app(args.template, args.name, args.directory)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
