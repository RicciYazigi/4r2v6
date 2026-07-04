#!/usr/bin/env python3
"""
Evidence Index Generator - SHA-256 Cryptographic Sealing
Part of 4R2 Coherence Engine Audit-Grade Infrastructure

Audit Index: RICCI-AUDIT-20260125
Version: 1.0

Usage:
    python generate_evidence_index.py [--evidence-dir ./evidence] [--output evidence_index.json]

This script scans the evidence directory and generates a cryptographically
verifiable index of all evidence artifacts with their SHA-256 hashes.

RULE: If an artifact is not listed in evidence_index.json, it DOES NOT EXIST
for audit purposes.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
UTC = timezone.utc
from pathlib import Path
from typing import Dict, List, Any
import argparse

def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def get_file_metadata(filepath: Path) -> Dict[str, Any]:
    """Get file metadata"""
    stat = filepath.stat()
    return {
        "size_bytes": stat.st_size,
        "modified_utc": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat().replace("+00:00", "Z"),
        "created_utc": datetime.fromtimestamp(stat.st_ctime, UTC).isoformat().replace("+00:00", "Z")
    }

def generate_evidence_index(
    evidence_dir: Path,
    extensions: List[str] = None,
    recursive: bool = True
) -> Dict[str, Any]:
    """
    Generate evidence index with SHA-256 hashes.
    
    Args:
        evidence_dir: Directory containing evidence files
        extensions: List of file extensions to include (default: all)
        recursive: Whether to scan subdirectories
    
    Returns:
        Dictionary with evidence index data
    """
    if extensions is None:
        extensions = [".json", ".jsonl", ".csv", ".txt", ".log", ".md", ".py"]
    
    evidence_files = {}
    total_size = 0
    
    # Scan directory
    if recursive:
        files = list(evidence_dir.rglob("*"))
    else:
        files = list(evidence_dir.glob("*"))
    
    for filepath in sorted(files):
        if not filepath.is_file():
            continue
        
        # Check extension
        if extensions and filepath.suffix.lower() not in extensions:
            continue
        
        # Skip hidden files
        if filepath.name.startswith("."):
            continue
        
        # Compute hash
        sha256 = compute_sha256(filepath)
        metadata = get_file_metadata(filepath)
        
        # Use relative path as key
        rel_path = str(filepath.relative_to(evidence_dir))
        
        evidence_files[rel_path] = {
            "sha256": sha256,
            "size_bytes": metadata["size_bytes"],
            "modified_utc": metadata["modified_utc"]
        }
        
        total_size += metadata["size_bytes"]
    
    return {
        "schema_version": "1.0",
        "audit_index": "RICCI-AUDIT-20260125",
        "generated_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "generator": "generate_evidence_index.py v1.0",
        "evidence_directory": str(evidence_dir.absolute()),
        "statistics": {
            "total_files": len(evidence_files),
            "total_size_bytes": total_size,
            "extensions_included": extensions
        },
        "files": evidence_files
    }

def verify_evidence_index(index_path: Path, evidence_dir: Path) -> Dict[str, Any]:
    """
    Verify existing evidence index against actual files.
    
    Returns verification report.
    """
    with open(index_path, "r") as f:
        index = json.load(f)
    
    results = {
        "verified_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "status": "PASS",
        "total_files": len(index.get("files", {})),
        "verified": 0,
        "failed": 0,
        "missing": 0,
        "details": []
    }
    
    for rel_path, expected in index.get("files", {}).items():
        filepath = evidence_dir / rel_path
        
        if not filepath.exists():
            results["missing"] += 1
            results["details"].append({
                "file": rel_path,
                "status": "MISSING",
                "expected_sha256": expected["sha256"]
            })
            continue
        
        actual_sha256 = compute_sha256(filepath)
        
        if actual_sha256 == expected["sha256"]:
            results["verified"] += 1
            results["details"].append({
                "file": rel_path,
                "status": "VERIFIED",
                "sha256": actual_sha256
            })
        else:
            results["failed"] += 1
            results["details"].append({
                "file": rel_path,
                "status": "HASH_MISMATCH",
                "expected_sha256": expected["sha256"],
                "actual_sha256": actual_sha256
            })
    
    if results["failed"] > 0 or results["missing"] > 0:
        results["status"] = "FAIL"
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Generate or verify evidence index with SHA-256 hashes"
    )
    parser.add_argument(
        "--evidence-dir", "-e",
        type=Path,
        default=Path("./evidence"),
        help="Directory containing evidence files"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("evidence_index.json"),
        help="Output file for evidence index"
    )
    parser.add_argument(
        "--verify", "-v",
        action="store_true",
        help="Verify existing index instead of generating"
    )
    parser.add_argument(
        "--include-all", "-a",
        action="store_true",
        help="Include all file types, not just common evidence formats"
    )
    
    args = parser.parse_args()
    
    if args.verify:
        # Verification mode
        if not args.output.exists():
            print(f"ERROR: Index file not found: {args.output}")
            sys.exit(1)
        
        print(f"Verifying evidence index: {args.output}")
        print(f"Evidence directory: {args.evidence_dir}")
        print("-" * 60)
        
        results = verify_evidence_index(args.output, args.evidence_dir)
        
        print(f"Status: {results['status']}")
        print(f"Total files: {results['total_files']}")
        print(f"Verified: {results['verified']}")
        print(f"Failed: {results['failed']}")
        print(f"Missing: {results['missing']}")
        
        if results["status"] == "FAIL":
            print("\nFailed/Missing files:")
            for detail in results["details"]:
                if detail["status"] != "VERIFIED":
                    print(f"  [{detail['status']}] {detail['file']}")
            sys.exit(1)
        else:
            print("\nAll evidence files verified successfully!")
            sys.exit(0)
    
    else:
        # Generation mode
        if not args.evidence_dir.exists():
            print(f"Creating evidence directory: {args.evidence_dir}")
            args.evidence_dir.mkdir(parents=True, exist_ok=True)
        
        extensions = None if args.include_all else [".json", ".jsonl", ".csv", ".txt", ".log", ".md", ".py"]
        
        print(f"Generating evidence index...")
        print(f"Evidence directory: {args.evidence_dir}")
        print(f"Output file: {args.output}")
        print("-" * 60)
        
        index = generate_evidence_index(args.evidence_dir, extensions=extensions)
        
        # Write index
        with open(args.output, "w") as f:
            json.dump(index, f, indent=2)
        
        print(f"Generated: {args.output}")
        print(f"Total files indexed: {index['statistics']['total_files']}")
        print(f"Total size: {index['statistics']['total_size_bytes']:,} bytes")
        print("\nFiles:")
        for filepath, data in index["files"].items():
            print(f"  {filepath}")
            print(f"    SHA-256: {data['sha256'][:16]}...")
        
        print("\nEvidence index generated successfully!")
        print("RULE: If not in this index, it DOES NOT EXIST for audit.")

if __name__ == "__main__":
    main()
