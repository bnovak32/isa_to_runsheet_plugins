from pathlib import Path
import argparse
import sys

# Import for access at the module level
from . import schemas

SUPPORTED_CONFIG_TYPES = ['metagenomics', 'estimatehost', 'methylseq', 'methylseqRNA']

def _parse_args():
    """Parse command line args."""
    parser = argparse.ArgumentParser()
    parser.add_argument( "--config-type", required=True )
    parser.add_argument( "--config-version", default="Latest" )
    args, unknown = parser.parse_known_args()
    return args


args = _parse_args()
assert (
    args.config_type in SUPPORTED_CONFIG_TYPES
), f"Invalid config type supplied: '{args.config_type}' Supported config types: {SUPPORTED_CONFIG_TYPES} "

query_config_fn = f"{args.config_type}_v{args.config_version}.yaml"
x = [p for p in Path(__file__).parent.glob("*.yaml") if p.name == query_config_fn]
assert (
    len(x) > 0
), f"Invalid version requested: '{args.config_version}' for config type {args.config_type}"

config = Path(__file__).parent / query_config_fn

# Set config path
#config = Path(__file__).parent / "metagenomics_v1.yaml"
