from typing import Dict, TypedDict, Iterable
from deephaven.table import Table
import logging

logger = logging.getLogger(__name__)

class CommandDecoderResults(TypedDict):
  text: str
  """
  The original text passed in
  """

  filters: Dict[str, str]
  """
  Filters that were parsed from the command
  """

  sorts: Dict[str, str]
  """
  Sorts that were parsed from the command
  """

  errors: list[str]
  """
  Errors that occurred while parsing the command
  """

filter_pattern = '^(filter|filters)\\s(.*)\\s(by|on)\\s(.*)$'
sort_pattern = '^(sort|sorts)\\s(.*)\\s?(.*)$'
"""
The pattern to use to parse the command
"""


def decode_text_command(text: str) -> CommandDecoderResults:
  """
  Decode a text command into a fuzzy filter and sort commands.

  Note: This is pretty basic, and supports a fairly rigid command set.

  Args:
    text: The text command to decode

  Returns:
    A CommandDecoderResults object
  """
  import re
  filters: Dict[str, str] = {}
  sorts: Dict[str, str] = {}
  errors: list[str] = []

  clean_text = text.lower().strip()

  expressions = clean_text.split(" and ")

  for expression in expressions:
    filter_match = re.match(filter_pattern, expression)
    if filter_match:
      column = filter_match.group(2).strip()
      value = filter_match.group(4).strip()
      filters[column] = value

    sort_match = re.match(sort_pattern, expression)
    if sort_match:
      column = sort_match.group(2).strip()
      direction = sort_match.group(3).strip()
      sorts[column] = direction

  return CommandDecoderResults(text=text, filters=filters, sorts=sorts, errors=errors)

def get_fuzzy_match(fuzzy_value: str, options: list[str], threshold: float = 50) -> str | None:
  """
  Get the fuzzy match function

  Returns:
    The fuzzy match function
  """
  from rapidfuzz import fuzz, utils
  selected_option: str | None = None
  selected_option_ratio = 0

  for option in options:
    ratio = fuzz.ratio(fuzzy_value, option, processor=utils.default_process)
    if ratio > selected_option_ratio and ratio >= threshold:
      selected_option = option
      selected_option_ratio = ratio

  return selected_option

def get_values_for_column(table: Table, column: str) -> list[str]:
  """
  Get the unique values for a column in a table

  Args:
    table: The table to get the values from
    column: The column to get the values for

  Returns:
    A list of unique values for the column
  """
  from deephaven.numpy import to_numpy
  import numpy as np

  np_values = to_numpy(table.select_distinct(column), [column])
  values: list[str] = []
  for idx, value in np.ndenumerate(np_values):
    values.append(value)

  return values

def get_fuzzy_table_operations(table: Table, text: str, threshold: float = 50) -> CommandDecoderResults:
  """
  Get the filters for a table based on the text, using fuzzy matching.
  Cleans up the raw decoder results and matches them up to the table.

  Args:
    table: The table to filter
    text: The text to use for filtering
    threshold: The lower threshold for fuzzy matching. Will not match if no columns or values are higher than this threshold.

  Returns:
    A dictionary of filters
  """
  filters: Dict[str, str] = {}
  sorts: Dict[str, str] = {}
  errors: list[str] = []

  command = decode_text_command(text)

  column_names = list(map(lambda c: c.name, table.columns))

  for fuzzy_column, fuzzy_value in command['filters'].items():
    column = get_fuzzy_match(fuzzy_column, column_names, threshold)
    if column:
      values = get_values_for_column(table, column)
      value = get_fuzzy_match(fuzzy_value, values, threshold)
      if value:
        filters[column] = value
      else:
        errors.append(f"Could not find a value match for {fuzzy_value}")
    else:
      errors.append(f"Could not find a column match for {fuzzy_column}")
    
  return CommandDecoderResults(text=command['text'], filters=filters, sorts=sorts, errors=errors)

# def use_fuzzy_filtered_tables(tables: dict[str, Table], command: CommandDecoderResults):
#   """
#   Use fuzzy filtered tables based on the command

#   Args:
#     tables: The tables to filter
#     command: The command to use for filtering

#   Returns:
#     A list of tables that have been filtered
#   """
#   filtered_tables = []
#   for table_name, table in tables.items():
#     if command.filters:
#       for column, value in command.filters.items():
#         table = table.where(f"{column}.fuzzyMatch('{value}')")
#     if command.sort:
#       for column, direction in command.sort.items():
#         table = table.sort(f"{column} {direction}")
#     filtered_tables.append(table)
#   return filtered_tables