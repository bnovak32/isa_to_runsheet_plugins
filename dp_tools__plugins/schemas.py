""" Schemas for validation 
Uses Schema to allow usage of validation functions
"""
from schema import Schema
from schema import Optional as schema_Optional
from typing import Optional
import pandera as pa

check_single_value = pa.Check(
    lambda x: len(x.unique()) == 1,
    title="Check that all values in the column are identical",
    description="Useful for columns that contain dataset level metadata like organism and paired_end.",
    error="Dataset level columns do NOT contain one unique value"
    )

check_read2_path_populated_if_paired_end = pa.Check(
    lambda df: ("read2_path" in df.columns and df['paired_end'].iloc[0] == True) or
               ("read2_path" not in df.columns and df['paired_end'].iloc[0] == False),
    title="Check 'read2_path' is only populated if paired_end is True",
    description="Failures here are likely either due to manual user error or inappropriate source file (e.g. ISA archive)",
    error="Expected 'read2_path' to be populated only if paired_end is True"
    )

runsheet = {
    "methylseq": pa.DataFrameSchema(
        columns={
            "Original Sample Name": pa.Column(str),
            "organism": pa.Column(str, check_single_value),
            "paired_end": pa.Column(bool, check_single_value),
            "read1_path": pa.Column(str),
            "read2_path": pa.Column(str, required=False), # Expect if paired_end is True
        },
        # define checks at the DataFrameSchema-level
        #checks=check_read2_path_populated_if_paired_end
    ),
    "methylseqRNA": pa.DataFrameSchema(
        columns={
            "Original Sample Name": pa.Column(str),
            "organism": pa.Column(str, check_single_value),
            "paired_end": pa.Column(bool, check_single_value),
            "read1_path": pa.Column(str),
            "read2_path": pa.Column(str, required=False), # Expect if paired_end is True
        },
        # define checks at the DataFrameSchema-level
        checks=check_read2_path_populated_if_paired_end
    ),
    "amplicon": pa.DataFrameSchema(
        columns={
            "Original Sample Name": pa.Column(str),
            "organism": pa.Column(str),
            "host organism": pa.Column(str),
            "paired_end": pa.Column(bool, check_single_value),
            "read1_path": pa.Column(str),
            "read2_path": pa.Column(str, required=False), # Expect if paired_end is True
            "F_Primer": pa.Column(str, check_single_value), # Expect if paired_end is True
            "R_Primer": pa.Column(str, check_single_value, required=False), # Expect if paired_end is True
            "raw_R1_suffix": pa.Column(str), # No single value check for now
            "raw_R2_suffix": pa.Column(str, check_single_value, required=False), # Expect if paired_end is True
            "groups": pa.Column(str)
        },
        # define checks at the DataFrameSchema-level
        checks=check_read2_path_populated_if_paired_end
    ),
    "metagenomics": pa.DataFrameSchema(
        columns={
            "Original Sample Name": pa.Column(str),
            "organism": pa.Column(str),
            "paired_end": pa.Column(bool, check_single_value),
            "read1_path": pa.Column(str),
            "read2_path": pa.Column(str, required=False), # Expect if paired_end is True
        }
    ),
    "estimatehost": pa.DataFrameSchema(
        columns={
            "Original Sample Name": pa.Column(str),
            "organism": pa.Column(str),
            "host organism": pa.Column(str, required=False), # Expect iff host organism exists
            "paired_end": pa.Column(bool, check_single_value),
            "read1_path": pa.Column(str),
            "read2_path": pa.Column(str, required=False), # Expect if paired_end is True
        }
    )
}

import pandas as pd

class runsheet: # Bad casing since we will use the class definition itself for all static methods

    @staticmethod
    def check_single_value(column: pd.Series, error_msg: str, errors: list[str]) -> None:
        if len(column.unique()) != 1:
            errors.append(error_msg)

    @staticmethod
    def check_read2_path_populated_if_paired_end(df: pd.DataFrame, errors: list[str]) -> None:
        if "read2_path" in df.columns and df['paired_end'].iloc[0] == True:
            return
        elif "read2_path" not in df.columns:
            # checks paired flag if no read2 provided, if paired == True but read1 file is 
            # tar.gz format, then allows pass because multiple files are zipped together
            if df['paired_end'].iloc[0] == False:
                return
            elif df['read1_path'].iloc[0].endswith('tar.gz'):
                return
        else:
            errors.append("Expected 'read2_path' to be populated only if paired_end is True")

    @staticmethod
    def validate(df_runsheet: pd.DataFrame) -> bool:
        errors = []
        
        # Check for single value in specified columns
        runsheet.check_single_value(df_runsheet['organism'], "Dataset level columns do NOT contain one unique value for 'organism'", errors)

        runsheet.check_single_value(df_runsheet['paired_end'], "Dataset level columns do NOT contain one unique value for 'paired_end'", errors)
        
        # Check for 'read2_path' population if paired_end is True
        runsheet.check_read2_path_populated_if_paired_end(df_runsheet, errors)

        if errors:
            raise ValueError("\n".join(errors))
        else:
            return True
