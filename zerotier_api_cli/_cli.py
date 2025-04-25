import json
import sys
import datetime
import logging
import click
import click_log
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler
from humanize import naturaltime

import zerotier_api_cli._config as cfg
from zerotier_api_cli._api import fetch_members, authorize_member, remove_member

console = Console()
logger = logging.getLogger()

cfg.init_config()

# Helpers --------------------------------------------------
class HelpWithConfig(click.Group):
    def format_help(self, ctx, formatter):
        # first, render the normal help
        super().format_help(ctx, formatter)
        # then tack on your config‐dir epilog
        formatter.write_paragraph()
        formatter.write_text(f"Config file:\n  {cfg.CFG_FILE!s}")

def check_config(token, network_id):
    if not token or not network_id:
        console.print("[bold red]Error:[/] Please provide ZeroTier token and network ID via options or environment variables.")
        sys.exit(1)

# CLI Commands ---------------------------------------------

@click.group(cls=HelpWithConfig)
@click.option("--token", "-t", help="ZeroTier API token", envvar="ZEROTIER_TOKEN")
@click.option("--network-id", "-n", help="ZeroTier network ID", envvar="ZEROTIER_NETWORK_ID")
@click_log.simple_verbosity_option(logger)
@click.pass_context
def cli(ctx, token, network_id):
    "ZeroTier network management CLI"

    handler = RichHandler(rich_tracebacks=True)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    logger.addHandler(handler)

    check_config(token, network_id)
    ctx.obj = {"token": token, "network_id": network_id}

@cli.command()
@click.option("-p", "--pending", is_flag=True, help="Only show pending (unauthorized) clients.")
@click.option("-j", "--json", "as_json", is_flag=True, help="Output as JSON.")
@click.pass_context
def list(ctx, pending, as_json):
    "List all (or pending) clients in the network."
    members = fetch_members(ctx.obj["token"], ctx.obj["network_id"])

    if as_json:
        console.print(json.dumps(members, indent=4))
        return

    table = Table(title="ZeroTier Network Clients for Network " + ctx.obj["network_id"])
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("IPs", style="magenta")
    table.add_column("Authorized", style="yellow")
    table.add_column("Last Online", style="yellow")

    for m in members:
        authorized = m.get("config", {}).get("authorized", False)
        if pending and authorized:
            continue
        last_ts = m.get("lastOnline", 0)
        if last_ts:
            last_dt = datetime.datetime.fromtimestamp(last_ts/1000)
            last_str = naturaltime(last_dt)
        else:
            last_str = "Never"
        ips = ", ".join(m.get("config", {}).get("ipAssignments", []))
        authorized_str = "Yes" if authorized else "No"
        authorized_style = "green" if authorized else "red"
        table.add_row(
            m.get("nodeId"),
            m.get("name", ""),
            ips,
            f"[{authorized_style}]{authorized_str}[/]",
            last_str
        )

    console.print(table)

@cli.command()
@click.argument("member_id")
@click.pass_context
def approve(ctx, member_id):
    "Authorize a pending client by MEMBER_ID."
    try:
        result = authorize_member(ctx.obj["token"], ctx.obj["network_id"], member_id)
        console.print(f"[bold green]Success:[/] Client {member_id} authorized.")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not authorize {member_id}: {e}")
        sys.exit(1)

@cli.command()
@click.argument("member_id")
@click.pass_context
def remove(ctx, member_id):
    "Remove a client by MEMBER_ID."
    try:
        remove_member(ctx.obj["token"], ctx.obj["network_id"], member_id)
        console.print(f"[bold green]Removed:[/] Client {member_id} deleted.")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not remove {member_id}: {e}")
        sys.exit(1)

@cli.command()
@click.option("--token", "-t", help="ZeroTier API token", envvar="ZEROTIER_TOKEN")
@click.option("--network-id", "-n", help="ZeroTier network ID", envvar="ZEROTIER_NETWORK_ID")
def save_settings(token, network_id):
    """Save ZeroTier API token and network ID to configuration file."""
    check_config(token, network_id)
    config_file = cfg.save_config(token, network_id)
    console.print(f"[bold green]Success:[/] Settings saved to {config_file}")
