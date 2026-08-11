#!/usr/bin/env python3
"""
Nexus App Deployment Automation Script

This script automates the Nexus app deployment and distribution process.
Use --deploy to build and deploy, --distribute to distribute an existing
deployment, or both together.

With --deploy:
  1. Validates prerequisites (Node.js, Nexus CLI)
  2. Installs dependencies
  3. Builds the web frontend (npm run build-web)
  4. Validates and lints the app (nexus lint)
  5. Registers app (if needed)
  6. Ensures target environment exists
  7. Deploys to a Nexus environment (nexus deploy)

With --distribute:
  - Verifies a deployment exists for the target environment (nexus deploy list)
  - Distributes to a PingCode site (nexus distribute)

References:
  - wiki/guide/started/deploy-and-install.md
  - wiki/guide/build/app-deploy.md
  - wiki/guide/build/app-distribute.md
  - wiki/reference/cli/deploy.md
  - wiki/reference/cli/distribute.md
  - wiki/reference/cli/build.md
  - wiki/reference/cli/lint.md
  - wiki/reference/cli/logs.md

Usage:
    python3 -m scripts.deploy_nexus_app --app-dir /path/to/app --deploy
    python3 -m scripts.deploy_nexus_app --app-dir /path/to/app --distribute --site your-domain.pingcode.com
    python3 -m scripts.deploy_nexus_app --app-dir /path/to/app --deploy --distribute --site your-domain.pingcode.com
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


# Well-known environment names per wiki/guide/build/app-environments.md.
# New apps ship with one development / staging / production environment;
# additional development environments can be created.
DEFAULT_ENVIRONMENT = "development"


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")


def print_step(step_num, message):
    print(f"{Colors.OKCYAN}{Colors.BOLD}Step {step_num}: {message}{Colors.ENDC}")


def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def run_command(cmd, cwd=None, capture_output=True, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=check,
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd}")
        if e.stdout and e.stdout.strip():
            print(f"\n--- stdout ---\n{e.stdout.strip()}")
        if e.stderr and e.stderr.strip():
            print(f"\n--- stderr ---\n{e.stderr.strip()}")
        raise


def check_node():
    """Check if Node.js is installed and get version."""
    try:
        result = run_command("node -v")
        version = result.stdout.strip()
        print_success(f"Node.js {version} found")
        return True
    except Exception:
        print_error("Node.js not found. Please install Node.js 24 LTS or later")
        return False


def check_nexus_cli():
    """Check if Nexus CLI is installed and get version."""
    try:
        result = run_command("nexus --version")
        version = result.stdout.strip().split('\n')[0]
        print_success(f"Nexus CLI {version} found")
        return True
    except Exception:
        print_error("Nexus CLI not found. Install with: npm install -g @pc-nexus/cli@latest")
        return False


def check_nexus_login():
    """
    Check if user is logged into the PingCode developer account via
    `nexus whoami --json`. Returns True when an account is present.
    """
    try:
        result = subprocess.run(
            ["nexus", "whoami", "--json"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip()
            print_error("Not logged into Nexus. Run: nexus login")
            if message:
                print(f"  Details: {message}")
            return False

        try:
            accounts = json.loads(result.stdout)
        except json.JSONDecodeError:
            accounts = None

        if isinstance(accounts, list) and accounts:
            account = accounts[0]
            identity = account.get("account_name") or account.get("account_id") or "unknown"
            print_success(f"Logged in to Nexus: {identity}")
            return True

        print_error("Not logged into Nexus. Run: nexus login")
        return False
    except Exception as e:
        print_error(f"Could not verify Nexus login: {e}")
        return False


def install_dependencies(app_dir):
    """Install npm dependencies."""
    print("Installing dependencies (this may take a few minutes)...")
    run_command("npm install", cwd=app_dir)
    print_success("Dependencies installed")
    return True


def has_build_web_script(app_dir):
    """Return True if the app's package.json declares a build-web script."""
    package_json = Path(app_dir) / "package.json"
    if not package_json.exists():
        return False
    try:
        with open(package_json, 'r') as f:
            data = json.load(f)
        scripts = data.get("scripts", {}) or {}
        return "build-web" in scripts
    except Exception:
        return False


def build_web(app_dir):
    """Build the frontend assets (npm run build-web)."""
    if not has_build_web_script(app_dir):
        print_warning("No build-web script found in package.json — skipping frontend build")
        return True
    print("Building frontend assets (npm run build-web)...")
    run_command("npm run build-web", cwd=app_dir)
    print_success("Frontend built")
    return True


def lint_app(app_dir, fix=False):
    """Run nexus lint to validate source files and manifest."""
    print("Validating app with nexus lint...")
    cmd = "nexus lint --fix" if fix else "nexus lint"
    run_command(cmd, cwd=app_dir)
    print_success("Lint passed")
    return True


def _find_manifest(app_dir):
    """Locate manifest.yaml or manifest.yml in the app directory."""
    for name in ("manifest.yaml", "manifest.yml"):
        candidate = Path(app_dir) / name
        if candidate.exists():
            return candidate
    return None


_APP_ID_RE = re.compile(r"^\s*id\s*:\s*['\"]?([A-Za-z0-9\-]+)['\"]?\s*$", re.MULTILINE)


def check_app_registered(app_dir):
    """
    Check if the app is registered by looking for a real app id under the
    `app:` key in the manifest. Nexus auto-generates a UUID-like id when the
    app is created/registered; freshly scaffolded apps may ship without one
    or with a placeholder.
    """
    manifest_path = _find_manifest(app_dir)
    if manifest_path is None:
        return False

    try:
        content = manifest_path.read_text()
    except OSError:
        return False

    # Locate the `app:` block, then read its `id:` field.
    app_block_match = re.search(r"(?m)^app\s*:\s*$", content)
    if not app_block_match:
        return False

    remaining = content[app_block_match.end():]
    # Only inspect lines indented under the app: block (top-level properties).
    collected = []
    for line in remaining.splitlines():
        if line.strip() == "":
            collected.append(line)
            continue
        if not line.startswith((" ", "\t")):
            break
        collected.append(line)
    app_block = "\n".join(collected)

    id_match = _APP_ID_RE.search(app_block)
    if not id_match:
        return False

    app_id = id_match.group(1).strip().lower()
    placeholders = {
        "",
        "will-be-generated",
        "your-app-id",
        "app-id",
        "todo",
        "changeme",
        "change-me",
    }
    if app_id in placeholders or "your-app-id" in app_id or "will-be-generated" in app_id:
        return False

    return True


def register_app(app_dir, app_name=None):
    """
    Register the app with Nexus via `nexus register`. This command is
    interactive (it may prompt for the app name), so we surface a clear
    message when it cannot run non-interactively.
    """
    print_warning("App needs to be registered with Nexus")

    cmd = "nexus register"
    if app_name:
        cmd += f" {app_name}"

    try:
        result = subprocess.run(
            cmd,
            cwd=app_dir,
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print_success("App registered successfully")
            return True
    except Exception:
        pass

    print_warning("`nexus register` may require interactive input")
    print_warning("Please run this command manually in your terminal:")
    print(f"  cd {app_dir}")
    print("  nexus register")
    print_warning("Then run this script again.")
    return False


def list_environments(app_dir):
    """
    Return the list of environments for the app using
    `nexus environments list --json`. Returns an empty list on failure.
    """
    try:
        result = subprocess.run(
            ["nexus", "environments", "list", "--json"],
            cwd=app_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("environments") or data.get("data") or []
    except Exception:
        return []
    return []


def ensure_environment(app_dir, environment):
    """
    Ensure the target environment exists. Development environments can be
    created via `nexus environments create -e <name>`. The default
    development / staging / production environments are provisioned
    automatically when an app is created.
    """
    environments = list_environments(app_dir)
    env_names = set()
    for env in environments:
        if not isinstance(env, dict):
            continue
        name = env.get("name") or env.get("environment") or env.get("id")
        if name:
            env_names.add(str(name).lower())

    if environment.lower() in env_names:
        print_success(f"Environment '{environment}' exists")
        return True

    # staging/production cannot be created manually — only one of each exists.
    if environment.lower() in {"staging", "production"}:
        print_error(
            f"Environment '{environment}' was not found. Only the built-in "
            f"development/staging/production environments can be targeted, "
            f"and staging/production cannot be created via CLI."
        )
        return False

    print(f"Creating development environment '{environment}'...")
    result = subprocess.run(
        ["nexus", "environments", "create", "-e", environment, "--non-interactive"],
        cwd=app_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print_success(f"Environment '{environment}' created")
        return True

    print_error(f"Failed to create environment '{environment}'")
    if result.stdout and result.stdout.strip():
        print(f"\n--- stdout ---\n{result.stdout.strip()}")
    if result.stderr and result.stderr.strip():
        print(f"\n--- stderr ---\n{result.stderr.strip()}")
    return False


def deploy_app(app_dir, environment=DEFAULT_ENVIRONMENT, tag=None, no_verify=False):
    """
    Deploy the app to a Nexus environment. `nexus deploy` packages, uploads
    a new build (when --tag is omitted), and deploys it in one step.
    """
    print(f"Deploying to {environment} environment...")
    cmd = f"nexus deploy --non-interactive -e {environment}"
    if tag:
        cmd += f" --tag {tag}"
    if no_verify:
        cmd += " --no-verify"
    run_command(cmd, cwd=app_dir)
    print_success(f"Deployed to {environment}")
    return True


def list_deployments(app_dir, limit=50):
    """
    Return the list of deployments using `nexus deploy list --json`.
    Returns an empty list on failure.
    """
    try:
        result = subprocess.run(
            ["nexus", "deploy", "list", "--json", "-l", str(limit)],
            cwd=app_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("deployments") or data.get("data") or []
    except Exception:
        return []
    return []


def check_deployment_exists(app_dir, environment):
    """
    Verify that a deployment exists for the given environment by checking
    `nexus deploy list --json`. Returns True if at least one deployment
    targets the specified environment.
    """
    deployments = list_deployments(app_dir)
    env_lower = environment.lower()
    for dep in deployments:
        if not isinstance(dep, dict):
            continue
        dep_env = (
            dep.get("environment")
            or dep.get("env")
            or dep.get("environmentName")
            or dep.get("environment_name")
        )
        if dep_env and str(dep_env).lower() == env_lower:
            return True
    return False


def distribute_app(app_dir, site_url, environment=DEFAULT_ENVIRONMENT):
    """Distribute the deployed app to a PingCode site."""
    print(f"Distributing to {site_url} ({environment})...")
    cmd = f"nexus distribute -s {site_url} -e {environment}"
    run_command(cmd, cwd=app_dir)
    print_success(f"Distributed to {site_url}")
    return True


def get_app_logs(app_dir, environment=DEFAULT_ENVIRONMENT, limit=25):
    """Fetch recent runtime logs via `nexus logs`."""
    print("Fetching recent logs...")
    cmd = f"nexus logs -e {environment} --limit {limit}"
    result = run_command(cmd, cwd=app_dir, capture_output=True)
    output = result.stdout.strip()
    if output:
        print(output)


def main():
    parser = argparse.ArgumentParser(
        description="Automate Nexus app deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build and deploy to development
  python3 -m scripts.deploy_nexus_app --app-dir ./my-nexus-app --deploy

  # Deploy to production using a specific build tag
  python3 -m scripts.deploy_nexus_app --app-dir ./my-nexus-app \\
      --deploy --env production --tag 7d392hf

  # Distribute an existing deployment to a PingCode site
  python3 -m scripts.deploy_nexus_app --app-dir ./my-nexus-app \\
      --distribute --site your-domain.pingcode.com

  # Build, deploy, and distribute in one step
  python3 -m scripts.deploy_nexus_app --app-dir ./my-nexus-app \\
      --deploy --distribute --site your-domain.pingcode.com

  # Skip npm install and frontend build (fast redeploy after code changes)
  python3 -m scripts.deploy_nexus_app --app-dir ./my-nexus-app \\
      --deploy --distribute --site your-domain.pingcode.com --skip-deps --skip-build-web
        """
    )

    parser.add_argument("--app-dir", required=True, help="Path to the Nexus app directory")
    parser.add_argument(
        "--site",
        help="PingCode site URL (e.g., your-domain.pingcode.com)",
    )
    parser.add_argument(
        "--env",
        default=DEFAULT_ENVIRONMENT,
        help=f"Nexus environment to deploy to (default: {DEFAULT_ENVIRONMENT})",
    )
    parser.add_argument(
        "--tag",
        help="Build tag to deploy (from a previous `nexus build`). "
             "When omitted, `nexus deploy` builds a new package.",
    )
    parser.add_argument(
        "--app-name",
        help="App name passed to `nexus register` when the app is not yet registered",
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Build and deploy the app to the target environment",
    )
    parser.add_argument(
        "--distribute",
        action="store_true",
        help="Distribute the deployed app to a PingCode site (requires an existing deployment)",
    )
    parser.add_argument("--skip-deps", action="store_true", help="Skip npm install")
    parser.add_argument(
        "--skip-build-web",
        action="store_true",
        help="Skip `npm run build-web` even when the script is present",
    )
    parser.add_argument(
        "--skip-env-check",
        action="store_true",
        help="Skip verifying/creating the target environment",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip Nexus pre-build validation during deploy (passes --no-verify)",
    )
    parser.add_argument(
        "--lint-fix",
        action="store_true",
        help="Pass --fix to nexus lint to auto-fix issues",
    )
    parser.add_argument("--show-logs", action="store_true", help="Show logs after deployment")
    parser.add_argument(
        "--log-limit",
        type=int,
        default=25,
        help="Number of log lines to show when --show-logs is set (default: 25)",
    )

    args = parser.parse_args()

    if not args.deploy and not args.distribute:
        parser.error("At least one of --deploy or --distribute must be specified")

    if args.distribute and not args.deploy and not args.site:
        parser.error("--site is required when --distribute is used without --deploy")

    app_dir = Path(args.app_dir).resolve()

    if not app_dir.exists():
        print_error(f"App directory not found: {app_dir}")
        sys.exit(1)

    if not _find_manifest(app_dir):
        print_error(f"No manifest.yaml/manifest.yml found in: {app_dir}")
        sys.exit(1)

    print_header("Nexus App Deployment Automation")
    print(f"App Directory: {app_dir}")
    print(f"Environment:   {args.env}")
    actions = []
    if args.deploy:
        actions.append("deploy")
    if args.distribute:
        actions.append("distribute")
    print(f"Actions:       {', '.join(actions)}")
    if args.distribute:
        print(f"Target Site:   {args.site or '(will prompt)'}")
    if args.tag:
        print(f"Build Tag:     {args.tag}")

    # Step 1: Prerequisites
    print_step(1, "Checking Prerequisites")
    if not check_node():
        sys.exit(1)
    if not check_nexus_cli():
        sys.exit(1)
    if not check_nexus_login():
        sys.exit(1)

    step = 2

    # Build / install / lint / register / env-check only when deploying
    if args.deploy:
        # Step 2: Install dependencies
        if not args.skip_deps:
            print_step(step, "Installing Dependencies")
            try:
                install_dependencies(app_dir)
            except Exception as e:
                print_error(f"Failed to install dependencies: {e}")
                sys.exit(1)
        else:
            print_step(step, "Skipping dependency installation")
        step += 1

        # Step 3: Build frontend assets
        if not args.skip_build_web:
            print_step(step, "Building Frontend Assets")
            try:
                build_web(app_dir)
            except Exception as e:
                print_error(f"Frontend build failed: {e}")
                sys.exit(1)
        else:
            print_step(step, "Skipping frontend build")
        step += 1

        # Step 4: Lint / validate
        print_step(step, "Linting and Validating App")
        try:
            lint_app(app_dir, fix=args.lint_fix)
        except Exception as e:
            print_error(f"Lint failed: {e}")
            sys.exit(1)
        step += 1

        # Step 5: Registration
        print_step(step, "Checking App Registration")
        if check_app_registered(app_dir):
            print_success("App is already registered")
        else:
            if not register_app(app_dir, args.app_name):
                print_error("App registration required. Please register manually.")
                sys.exit(1)
        step += 1

        # Step 6: Ensure target environment exists
        if not args.skip_env_check:
            print_step(step, f"Ensuring Environment '{args.env}' Exists")
            if not ensure_environment(app_dir, args.env):
                sys.exit(1)
        else:
            print_step(step, "Skipping environment check")
        step += 1

        # Step 7: Deploy
        print_step(step, f"Deploying to Nexus ({args.env})")
        try:
            deploy_app(
                app_dir,
                environment=args.env,
                tag=args.tag,
                no_verify=args.no_verify,
            )
        except Exception as e:
            print_error(f"Deployment failed: {e}")
            sys.exit(1)
        step += 1
    elif args.distribute:
        # When distributing only, verify a deployment already exists
        print_step(step, f"Verifying deployment for '{args.env}'")
        if not check_deployment_exists(app_dir, args.env):
            print_error(
                f"No deployment found for environment '{args.env}'. "
                f"Run with --deploy first, or check with: nexus deploy list"
            )
            sys.exit(1)
        print_success(f"Deployment found for '{args.env}'")
        step += 1

    # Distribution
    distributed = False
    if args.distribute:
        site = args.site
        if not site:
            print("\n⚠️  PingCode site URL is required for distribution")
            site = input(
                "Enter site URL (e.g., your-domain.pingcode.com): "
            ).strip()
        if not site:
            print_error("Site URL is required for distribution")
            sys.exit(1)

        # Normalize: strip protocol/path so `-s` receives just the host.
        site = re.sub(r"^https?://", "", site).strip().strip("/")

        print_step(step, f"Distributing to {site}")
        try:
            distribute_app(app_dir, site, environment=args.env)
            distributed = True
        except Exception as e:
            print_error(f"Distribution failed: {e}")
            print_warning(
                "The app is deployed; distribute it manually with:\n"
                f"  nexus distribute -s {site} -e {args.env}"
            )
            sys.exit(1)
        step += 1

    # Logs
    if args.show_logs:
        print_step(step, "Recent Logs")
        try:
            get_app_logs(app_dir, environment=args.env, limit=args.log_limit)
        except Exception as e:
            print_warning(f"Could not fetch logs: {e}")

    # Done
    print_header("Operation Complete!")

    if args.deploy and not distributed:
        print_success(f"Your Nexus app is deployed to the '{args.env}' environment!")
        print(f"\n{Colors.BOLD}Next step:{Colors.ENDC}")
        print(
            f"  Distribute it by re-running with --distribute --site <your-domain>.pingcode.com"
        )
    elif distributed:
        print_success(
            f"Your Nexus app is deployed to '{args.env}' and distributed to {site}!"
        )
        print(f"\n{Colors.BOLD}Next steps:{Colors.ENDC}")
        print(f"  1. Sign in to https://{site} as an administrator")
        print("  2. Open the enterprise admin console and go to 「应用审核」")
        print("  3. Approve and install the app, then open it in PingCode")

    print(f"\n{Colors.BOLD}Useful commands:{Colors.ENDC}")
    print(f"  View logs:    nexus logs -e {args.env} --limit 50")
    print(f"  List builds:  nexus build list")
    print(f"  List deploys: nexus deploy list")
    deploy_flag = " --deploy" if args.deploy else ""
    site_flag = f" --site {args.site}" if args.site else ""
    print(
        f"  Redeploy:     python3 -m scripts.deploy_nexus_app "
        f"--app-dir {app_dir}{deploy_flag} --distribute{site_flag} --env {args.env} --skip-deps --skip-build-web"
    )
    print()


if __name__ == "__main__":
    main()
