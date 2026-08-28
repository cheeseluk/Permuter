from collections import defaultdict

def format_results(valid_words):
    # Sort alphabetically first, so they are ordered within their length groups
    sorted_words = sorted(valid_words)

    # Group by length (using descending order for lengths)
    grouped_results = defaultdict(list)
    for word in sorted_words:
        grouped_results[len(word)].append(word)

    # Sort the dictionary keys so the longest words are at the top
    return dict(sorted(grouped_results.items(), reverse=True))


import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


def display_rich_ui(grouped_words, original_rack, execution_time):
    console = Console()

    # 1. Create a Header/Summary Box
    summary_text = (
        f"[bold white]Rack Submitted:[/bold white] [yellow]{original_rack.upper()}[/yellow]\n"
        f"[bold white]Search Execution Time:[/bold white] [green]{execution_time:.6f} seconds[/green]\n"
        f"[bold white]Total Valid Words Found:[/bold white] [cyan]{sum(len(v) for v in grouped_words.values())}[/cyan]"
    )

    console.print(Panel(
        summary_text,
        title="[bold magenta]Permuter Scooter Engine[/bold magenta]",
        expand=False,
        border_style="magenta"
    ))

    # 2. Build the Results Table
    table = Table(
        title="Unscrambled Matches",
        title_style="italic",
        box=box.ROUNDED,
        header_style="bold cyan",
        border_style="dim"
    )

    table.add_column("Word Length", justify="center", style="bold yellow")
    table.add_column("Valid Anagrams", style="green")

    # Sort keys descending so the longest words stay at the top
    for length in sorted(grouped_words.keys(), reverse=True):
        words = grouped_words[length]
        # Join the list into a clean, comma-separated string
        word_string = ", ".join(words)

        table.add_row(f"{length} Letters", word_string)

    console.print(table)