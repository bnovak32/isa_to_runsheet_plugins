This repository includes a valid `dp_tools` plugin folder with configuration schemas for:

| Configuration type | matching GeneLab pipeline | 
|--------------------|-------------------|
| metagenomics       | Metagenomics Illumina |
| estimatehost       | Metagenomics Estimate Host Reads |
| methylseq          | whole genome or RRBS methylseq |
| methylseqRNA       | whole transcriptome methylseq |

This plugin requires dp_tools v1.3.5-rc3 or later.

Examples:
```
# methyl transcriptomics
dpt-isa-to-runsheet --plugin-dir dp_tools__plugins --isa-archive OSD-48_metadata_OSD-48-ISA.zip --accession OSD-48 --config-type methylseqRNA

# DNA methylSeq
dpt-isa-to-runsheet --plugin-dir dp_tools__plugins --isa-archive OSD-48_metadata_OSD-48-ISA.zip --accession OSD-48 --config-type methylseq

# Metagenomics - standard pipeline ("Host organism" ignore)
dpt-isa-to-runsheet --plugin-dir dp_tools__plugins --isa-archive OSD-249_metadata_OSD-249-ISA.zip --accession OSD-249 --config-type metagenomics

# Metagenomics - Estimate Host Reads (requires "Host Organism" in sample metadata)
dpt-isa-to-runsheet --plugin-dir dp_tools__plugins --isa-archive OSD-572_metadata_OSD-572-ISA-v3.zip --accession OSD-572 --config-type estimatehost
```
