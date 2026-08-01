#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import NamedTuple, Sequence

from PIL import Image, UnidentifiedImageError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

BYTES_PER_KB = 1024
BYTES_PER_MB = 1024 * 1024

console = Console()


class CompressionResult(NamedTuple):
    filename: str
    orig_size: int
    new_size: int
    success: bool
    error_msg: str = ""


def main() -> None:
    """CLI entry point for image compression script."""
    args = parse_args()

    console.print(
        f"[bold blue]Starting image optimization in:[/bold blue] {args.dir}\n"
    )

    try:
        compress_images(
            images_dir=args.dir,
            quality=args.quality,
            remove_pngs=args.remove_pngs,
        )
    except FileNotFoundError as err:
        console.print(f"[bold red]Error:[/bold red] {err}")
        sys.exit(1)


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    project_root = Path(__file__).resolve().parent.parent
    default_dir = project_root / "images"

    parser = argparse.ArgumentParser(
        description="Compress PNG images in a directory to optimized JPGs."
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=default_dir,
        help="Target directory containing PNG images",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=88,
        help="JPEG quality level (1-100, default: 88)",
    )
    parser.add_argument(
        "--remove-pngs",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Delete original PNG files after conversion (pass --no-remove-pngs to preserve)",
    )

    return parser.parse_args(args)


def compress_images(
    images_dir: Path,
    quality: int = 88,
    remove_pngs: bool = True,
) -> None:
    """Convert all PNG images in images_dir to optimized JPGs."""
    if not images_dir.exists():
        raise FileNotFoundError(f"Directory '{images_dir}' does not exist.")

    png_files = sorted(list(images_dir.glob("*.png")))
    if not png_files:
        console.print(f"[yellow]No PNG images found in {images_dir}[/yellow]")
        return

    table = Table(
        title="Image compression results",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Filename", style="cyan")
    table.add_column("Original PNG size", justify="right", style="red")
    table.add_column("Optimized JPG size", justify="right", style="green")
    table.add_column("Savings", justify="right", style="bold yellow")

    total_orig_bytes = 0
    total_new_bytes = 0
    success_count = 0
    fail_count = 0

    for png_path in png_files:
        result = compress_single_image(
            png_path=png_path,
            quality=quality,
            remove_png=remove_pngs,
        )

        if result.success:
            success_count += 1
            total_orig_bytes += result.orig_size
            total_new_bytes += result.new_size

            savings_perecentage = (
                ((result.orig_size - result.new_size) / result.orig_size * 100)
                if result.orig_size > 0
                else 0.0
            )

            table.add_row(
                result.filename,
                format_bytes(result.orig_size),
                format_bytes(result.new_size),
                f"{savings_perecentage:.1f}%",
            )
        else:
            fail_count += 1
            console.print(
                f"[bold red]Failed to convert {result.filename}:[/bold red] {result.error_msg}"
            )

    if success_count > 0:
        overall_savings = (
            ((total_orig_bytes - total_new_bytes) / total_orig_bytes * 100)
            if total_orig_bytes > 0
            else 0.0
        )
        table.add_section()
        table.add_row(
            "[bold]Total[/bold]",
            format_bytes(total_orig_bytes),
            format_bytes(total_new_bytes),
            f"[bold]{overall_savings:.1f}%[/bold]",
        )
        console.print()
        console.print(table)

    summary_style = "green" if fail_count == 0 else "yellow"
    summary_text = (
        f"[bold {summary_style}]Processed {success_count}/{len(png_files)} image(s) successfully.[/bold {summary_style}]\n"
        f"Master SVG files remain untouched for future editing."
    )
    console.print()
    console.print(Panel(summary_text, title="Summary", border_style=summary_style))


def compress_single_image(
    png_path: Path,
    quality: int = 88,
    remove_png: bool = True,
) -> CompressionResult:
    """Convert and optimize a single PNG image to JPG."""
    orig_size = png_path.stat().st_size
    jpg_path = png_path.with_suffix(".jpg")

    try:
        with Image.open(png_path) as img:
            rgb_img = img.convert("RGB")
            rgb_img.save(jpg_path, "JPEG", quality=quality, optimize=True)

        new_size = jpg_path.stat().st_size
        if remove_png:
            png_path.unlink()

        return CompressionResult(
            filename=png_path.name,
            orig_size=orig_size,
            new_size=new_size,
            success=True,
        )
    except (UnidentifiedImageError, OSError, ValueError) as e:
        return CompressionResult(
            filename=png_path.name,
            orig_size=orig_size,
            new_size=0,
            success=False,
            error_msg=str(e),
        )


def format_bytes(size_bytes: int) -> str:
    """Format bytes to human-readable string (KB/MB)."""
    if size_bytes >= BYTES_PER_MB:
        return f"{size_bytes / BYTES_PER_MB:.2f} MB"
    return f"{size_bytes / BYTES_PER_KB:.1f} KB"


if __name__ == "__main__":
    main()
