import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from .client import InstagramClient
from .collectors.profile import ProfileCollector
from .collectors.media import MediaCollector
from .collectors.network import NetworkCollector
from .collectors.hashtag import HashtagCollector
from .exporters.jsonExporter import JsonExporter
from .exporters.csvExporter import CsvExporter
import json

console = Console()

def getAuthenticatedClient():
    """Helper function to get authenticated Instagram client"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Authenticating..."),
        console=console,
        transient=True
    ) as progress:
        progress.add_task("auth", total=None)
        client = InstagramClient()
        if not client.login():
            console.print("[bold red]Authentication failed[/bold red]")
            return None
    return client

@click.group()
def cli():
    """Instagram OSINT CLI Tool - Gather intelligence from Instagram profiles"""
    pass

@cli.command()
@click.argument('username')
@click.option('--output', '-o', help='Export to file (json/csv)')
def profile(username, output):
    """Get profile information for a user"""
    console.print(f"[bold blue]Gathering profile info for: {username}[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = ProfileCollector(client)
    data = collector.getProfileInfo(username)
    
    if 'error' in data:
        console.print(f"[bold red]Error: {data['error']}[/bold red]")
        return

    # Display results in a table
    table = Table(title=f"Profile: {username}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in data.items():
        table.add_row(key, str(value))

    console.print(table)
    
    # Export if requested
    if output:
        if output.endswith('.json'):
            result = JsonExporter.exportToJson(data, output)
        elif output.endswith('.csv'):
            result = CsvExporter.exportToCsv(data, output)
        else:
            console.print("[yellow]Unknown format. Use .json or .csv extension[/yellow]")
            return
        
        if result['success']:
            console.print(f"\n[green]✓ Exported to {result['filename']}[/green]")
        else:
            console.print(f"\n[red]✗ Export failed: {result['error']}[/red]")

@cli.command()
@click.argument('username')
@click.option('--amount', '-a', default=12, help='Number of posts to retrieve')
@click.option('--output', '-o', help='Export to file (json/csv)')
def media(username, amount, output):
    """Get recent media posts from a user"""
    console.print(f"[bold blue]Gathering recent media for: {username}[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = MediaCollector(client)
    data = collector.getRecentMedia(username, amount)
    
    if isinstance(data, dict) and 'error' in data:
        console.print(f"[bold red]Error: {data['error']}[/bold red]")
        return

    # Display results
    table = Table(title=f"Recent Media: {username}")
    table.add_column("Type", style="cyan")
    table.add_column("Caption", style="white", max_width=40)
    table.add_column("Likes", style="green")
    table.add_column("Comments", style="yellow")
    table.add_column("Date", style="magenta")

    for post in data:
        table.add_row(
            post['type'],
            post['caption'][:40] + '...' if len(post['caption']) > 40 else post['caption'],
            str(post['likes']),
            str(post['comments']),
            post['timestamp']
        )

    console.print(table)
    console.print(f"\n[dim]Total posts retrieved: {len(data)}[/dim]")
    
    # Export if requested
    if output:
        if output.endswith('.json'):
            result = JsonExporter.exportToJson(data, output)
        elif output.endswith('.csv'):
            result = CsvExporter.exportToCsv(data, output)
        else:
            console.print("[yellow]Unknown format. Use .json or .csv extension[/yellow]")
            return
        
        if result['success']:
            console.print(f"[green]✓ Exported to {result['filename']}[/green]")

@cli.command()
@click.argument('username')
@click.option('--amount', '-a', default=50, help='Number of posts to analyze')
def patterns(username, amount):
    """Analyze posting patterns and engagement"""
    console.print(f"[bold blue]Analyzing posting patterns for: {username}[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = MediaCollector(client)
    data = collector.analyzePostingPatterns(username, amount)
    
    if 'error' in data:
        console.print(f"[bold red]Error: {data['error']}[/bold red]")
        return

    # Summary
    console.print("[bold]📊 Posting Pattern Analysis[/bold]\n")
    console.print(f"Posts Analyzed: [cyan]{data['totalAnalyzed']}[/cyan]")
    console.print(f"Most Active Hour: [green]{data['mostActiveHour']}:00[/green]")
    console.print(f"Most Active Day: [green]{data['mostActiveDay']}[/green]")
    console.print(f"Avg Likes per Post: [yellow]{data['avgLikes']:.1f}[/yellow]")
    console.print(f"Avg Comments per Post: [yellow]{data['avgComments']:.1f}[/yellow]")
    
    # Hourly distribution
    console.print("\n[bold]🕐 Hourly Activity:[/bold]")
    hourTable = Table()
    hourTable.add_column("Hour", style="cyan")
    hourTable.add_column("Posts", style="green")
    
    for hour in sorted(data['hourlyDistribution'].keys()):
        hourTable.add_row(f"{hour}:00", str(data['hourlyDistribution'][hour]))
    
    console.print(hourTable)

@cli.command()
@click.argument('username')
@click.option('--amount', '-a', default=50, help='Number of followers to retrieve')
@click.option('--output', '-o', help='Export to file (json/csv)')
def followers(username, amount, output):
    """Get followers list"""
    console.print(f"[bold blue]Gathering followers for: {username}[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = NetworkCollector(client)
    data = collector.getFollowers(username, amount)
    
    if isinstance(data, dict) and 'error' in data:
        console.print(f"[bold red]Error: {data['error']}[/bold red]")
        return

    # Display results
    table = Table(title=f"Followers: {username}")
    table.add_column("Username", style="cyan")
    table.add_column("Full Name", style="white")
    table.add_column("Verified", style="green")
    table.add_column("Private", style="yellow")

    for follower in data:
        table.add_row(
            follower['username'],
            follower['fullName'],
            "✓" if follower['isVerified'] else "✗",
            "✓" if follower['isPrivate'] else "✗"
        )

    console.print(table)
    console.print(f"\n[dim]Total followers retrieved: {len(data)}[/dim]")
    
    # Export if requested
    if output:
        if output.endswith('.json'):
            result = JsonExporter.exportToJson(data, output)
        elif output.endswith('.csv'):
            result = CsvExporter.exportToCsv(data, output)
        
        if result['success']:
            console.print(f"[green]✓ Exported to {result['filename']}[/green]")

@cli.command()
@click.argument('username')
@click.option('--amount', '-a', default=50, help='Number of accounts to retrieve')
@click.option('--output', '-o', help='Export to file (json/csv)')
def following(username, amount, output):
    """Get following list"""
    console.print(f"[bold blue]Gathering following for: {username}[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = NetworkCollector(client)
    data = collector.getFollowing(username, amount)
    
    if isinstance(data, dict) and 'error' in data:
        console.print(f"[bold red]Error: {data['error']}[/bold red]")
        return

    # Display results
    table = Table(title=f"Following: {username}")
    table.add_column("Username", style="cyan")
    table.add_column("Full Name", style="white")
    table.add_column("Verified", style="green")
    table.add_column("Private", style="yellow")

    for user in data:
        table.add_row(
            user['username'],
            user['fullName'],
            "✓" if user['isVerified'] else "✗",
            "✓" if user['isPrivate'] else "✗"
        )

    console.print(table)
    console.print(f"\n[dim]Total following retrieved: {len(data)}[/dim]")
    
    # Export if requested
    if output:
        if output.endswith('.json'):
            result = JsonExporter.exportToJson(data, output)
        elif output.endswith('.csv'):
            result = CsvExporter.exportToCsv(data, output)
        
        if result['success']:
            console.print(f"[green]✓ Exported to {result['filename']}[/green]")

@cli.command()
@click.argument('username1')
@click.argument('username2')
def mutual(username1, username2):
    """Find mutual followers between two accounts"""
    console.print(f"[bold blue]Finding mutual followers between: {username1} and {username2}[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = NetworkCollector(client)
    data = collector.getMutualConnections(username1, username2)
    
    if 'error' in data:
        console.print(f"[bold red]Error: {data['error']}[/bold red]")
        return

    console.print(f"[green]Found {data['count']} mutual followers[/green]\n")

    if data['mutualFollowers']:
        table = Table(title="Mutual Followers")
        table.add_column("Username", style="cyan")
        table.add_column("Full Name", style="white")

        for user in data['mutualFollowers']:
            table.add_row(user['username'], user['fullName'])

        console.print(table)

@cli.command()
@click.argument('hashtag')
@click.option('--amount', '-a', default=27, help='Number of posts to retrieve')
@click.option('--output', '-o', help='Export to file (json/csv)')
def hashtag(hashtag, amount, output):
    """Get top posts for a hashtag"""
    console.print(f"[bold blue]Gathering top posts for: #{hashtag}[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = HashtagCollector(client)
    
    # Get hashtag info
    info = collector.getHashtagInfo(hashtag)
    if 'error' not in info:
        console.print(f"[dim]Total posts with #{hashtag}: {info['mediaCount']:,}[/dim]\n")
    
    # Get top posts
    data = collector.getTopPostsByHashtag(hashtag, amount)
    
    if isinstance(data, dict) and 'error' in data:
        console.print(f"[bold red]Error: {data['error']}[/bold red]")
        return

    # Display results
    table = Table(title=f"Top Posts: #{hashtag}")
    table.add_column("Username", style="cyan")
    table.add_column("Caption", style="white", max_width=30)
    table.add_column("Likes", style="green")
    table.add_column("Comments", style="yellow")

    for post in data:
        table.add_row(
            post['username'],
            post['caption'],
            str(post['likes']),
            str(post['comments'])
        )

    console.print(table)
    console.print(f"\n[dim]Posts retrieved: {len(data)}[/dim]")
    
    # Export if requested
    if output:
        if output.endswith('.json'):
            result = JsonExporter.exportToJson(data, output)
        elif output.endswith('.csv'):
            result = CsvExporter.exportToCsv(data, output)
        
        if result['success']:
            console.print(f"[green]✓ Exported to {result['filename']}[/green]")

@cli.command()
@click.argument('usernames', nargs=-1, required=True)
@click.option('--output', '-o', default='batch_results.json', help='Output filename')
def batch(usernames, output):
    """Analyze multiple profiles at once"""
    console.print(f"[bold blue]Batch analyzing {len(usernames)} profiles...[/bold blue]\n")

    client = getAuthenticatedClient()
    if not client:
        return
    
    collector = ProfileCollector(client)
    results = {}
    
    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Processing...", total=len(usernames))
        
        for username in usernames:
            data = collector.getProfileInfo(username)
            results[username] = data
            progress.update(task, advance=1)
    
    # Display summary
    table = Table(title="Batch Analysis Results")
    table.add_column("Username", style="cyan")
    table.add_column("Followers", style="green")
    table.add_column("Following", style="yellow")
    table.add_column("Posts", style="magenta")
    table.add_column("Verified", style="blue")

    for username, data in results.items():
        if 'error' not in data:
            table.add_row(
                username,
                str(data['followers']),
                str(data['following']),
                str(data['posts']),
                "✓" if data['isVerified'] else "✗"
            )

    console.print(table)
    
    # Export
    result = JsonExporter.exportToJson(results, output)
    if result['success']:
        console.print(f"\n[green]✓ Batch results exported to {result['filename']}[/green]")

if __name__ == '__main__':
    cli()
