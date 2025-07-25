import argparse
import requests
import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def send_prompt(prompt: str, url: str = "http://localhost:8000") -> None:
    """Send a prompt to the API and display the response"""
    try:
        
        response = requests.post(
            f"{url}/generate",
            json={"prompt": prompt}
        )
        response.raise_for_status()
        
       
        data = response.json()
        
        
        console.print("\n[bold green]Response:[/bold green]")
        console.print(Panel(
            data["response"],
            title="AI Response",
            border_style="blue"
        ))
        
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error:[/bold red] Could not connect to API. Is it running?")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="CLI for Local LLM API")
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The prompt to send to the API"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="API URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Start interactive mode"
    )

    args = parser.parse_args()

    if args.interactive:
        console.print("[bold]Interactive Mode[/bold] (Ctrl+C to exit)\n")
        try:
            while True:
                prompt = console.input("[bold yellow]Prompt>[/bold yellow] ")
                if prompt.strip():
                    send_prompt(prompt, args.url)
        except KeyboardInterrupt:
            console.print("\n[bold]Goodbye![/bold]")
    elif args.prompt:
        send_prompt(args.prompt, args.url)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()