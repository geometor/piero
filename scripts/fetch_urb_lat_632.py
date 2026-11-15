"""Primary witness acquisition and local Venice 1509 Part III audit for Piero della Francesca."""

from __future__ import annotations

import argparse
import json
import urllib.request
from collections.abc import Sequence
from pathlib import Path

__all__ = [
    "IIIF_MANIFEST_URL",
    "audit_local_pacioli_part3",
    "build_parser",
    "fetch_iiif_manifest",
    "main",
    "run",
]

IIIF_MANIFEST_URL = "https://digi.vatlib.it/iiif/MSS_Urb.lat.632/manifest.json"
_REPO_ROOT = Path(__file__).resolve().parents[1]
_URB_DIR = _REPO_ROOT / "resources" / "quinque_corporibus" / "urb_lat_632"
_PACIOLI_1509_DIR = (
    _REPO_ROOT.parent / "pacioli" / "resources" / "de_divina_proportione" / "paganini_1509"
)


def audit_local_pacioli_part3(pacioli_dir: Path = _PACIOLI_1509_DIR) -> dict[str, object]:
    """Inspect Venice 1509 Part III scans (0085..0136) already staged in sister repo ``pacioli``.

    Args:
        pacioli_dir: Path to ``pacioli/resources/de_divina_proportione/paganini_1509``.

    Returns:
        Dictionary summarizing discovered Part III folio scans and cropped woodcuts.
    """
    part3_scans: list[str] = []
    woodcut_count = 0
    if pacioli_dir.is_dir():
        for num in range(85, 137):
            stem = f"{num:04d}"
            candidate = pacioli_dir / f"{stem}.png"
            if candidate.is_file():
                part3_scans.append(candidate.name)
            woodcut_count += sum(
                1
                for item in pacioli_dir.glob(f"{stem}.*.png")
                if item.is_file()
            )

    return {
        "pacioli_1509_dir": str(pacioli_dir),
        "exists": pacioli_dir.is_dir(),
        "part3_scan_count": len(part3_scans),
        "part3_woodcut_crops": woodcut_count,
        "first_scan": part3_scans[0] if part3_scans else None,
        "last_scan": part3_scans[-1] if part3_scans else None,
    }


def fetch_iiif_manifest(
    manifest_url: str = IIIF_MANIFEST_URL,
    output_dir: Path = _URB_DIR,
    limit_images: int = 0,
) -> Path:
    """Download DigiVatLib IIIF v2.0 manifest (and optional folio images) for ``Urb. lat. 632``.

    Args:
        manifest_url: IIIF manifest endpoint on ``digi.vatlib.it``.
        output_dir: Local destination directory under ``resources/quinque_corporibus/``.
        limit_images: Maximum number of canvas images to download (``0`` = manifest only).

    Returns:
        Filesystem path to the saved ``manifest.json``.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"

    req = urllib.request.Request(
        manifest_url,
        headers={"User-Agent": "GEOMETOR-Scriptorium/0.1 (+https://geometor.com)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw_bytes = resp.read()
    manifest_path.write_bytes(raw_bytes)

    if limit_images > 0:
        manifest = json.loads(raw_bytes.decode("utf-8"))
        sequences = manifest.get("sequences", [])
        canvases = sequences[0].get("canvases", []) if sequences else []
        scans_dir = output_dir / "scans"
        scans_dir.mkdir(parents=True, exist_ok=True)

        for idx, canvas in enumerate(canvases[:limit_images], start=1):
            images = canvas.get("images", [])
            if not images:
                continue
            service = images[0].get("resource", {}).get("service", {})
            service_id = service.get("@id")
            if not service_id:
                continue
            img_url = f"{service_id.rstrip('/')}/full/full/0/default.jpg"
            dest = scans_dir / f"{idx:04d}.jpg"
            if dest.is_file():
                continue
            img_req = urllib.request.Request(
                img_url,
                headers={"User-Agent": "GEOMETOR-Scriptorium/0.1 (+https://geometor.com)"},
            )
            with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                dest.write_bytes(img_resp.read())

    return manifest_path


def build_parser() -> argparse.ArgumentParser:
    """Construct the acquisition and witness-audit CLI parser.

    Returns:
        Configured :class:`argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog="fetch_urb_lat_632",
        description="Audit Venice 1509 Part III scans and fetch Vatican Cod. Urb. lat. 632 IIIF.",
    )
    parser.add_argument(
        "--check-local-pacioli",
        action="store_true",
        help="Inspect local Venice 1509 Part III scans in ../pacioli without network access.",
    )
    parser.add_argument(
        "--fetch-manifest",
        action="store_true",
        help="Download IIIF manifest.json from digi.vatlib.it (requires network access).",
    )
    parser.add_argument(
        "--limit-images",
        type=int,
        default=0,
        help="Optional number of full-resolution IIIF folio JPEGs to download.",
    )
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the witness audit or IIIF download workflow.

    Args:
        argv: Command-line arguments.

    Returns:
        Exit code ``0`` on success.
    """
    args = build_parser().parse_args(list(argv) if argv is not None else [])
    if args.check_local_pacioli or not args.fetch_manifest:
        report = audit_local_pacioli_part3()
        print(json.dumps(report, indent=2))
    if args.fetch_manifest:
        saved = fetch_iiif_manifest(limit_images=args.limit_images)
        print(f"Saved IIIF manifest to {saved}")
    return 0


def main() -> None:
    """Console entry point."""
    raise SystemExit(run())


if __name__ == "__main__":
    main()
