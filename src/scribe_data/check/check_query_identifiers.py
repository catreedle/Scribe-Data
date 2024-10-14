# from pathlib import Path
# from typing import Optional
# import re
# import json

# LANGUAGE_DATA_EXTRACTION_DIR = Path(__file__).parent.parent / "language_data_extraction"

# LANGUAGE_METADATA_FILE = (
#     Path(__file__).parent.parent / "resources" / "language_metadata.json"
# )
# DATA_TYPE_METADATA_FILE = (
#     Path(__file__).parent.parent / "resources" / "data_type_metadata.json"
# )

# ENGLISH_FILE = LANGUAGE_DATA_EXTRACTION_DIR / "English" / "verbs" / "query_verbs.sparql"

# query_language_pattern = r"\?lexeme\s+dct:language\s+wd:Q\d+"


# def extract_qid_from_sparql(file_path: Path, pattern: str) -> Optional[str]:
#     """
#     Extract the QID from the specified SPARQL file.
#     Args:
#         file_path (Path): Path to the SPARQL file.
#     Returns:
#         str | None: The extracted QID or None if not found.
#     """
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             content = file.read()
#             print(file)
#             # Use regex to find the QID (e.g., wd:Q34311)
#             match = re.search(pattern, content)
#             if match:
#                 return match.group(0).replace(
#                     "?lexeme dct:language wd:", ""
#                 )  # Return the found QID
#     except Exception as _:
#         pass
#         # print(f"Error reading {file_path}: {e}")
#     return None  # Return None if not found or an error occurs


# language_QID = extract_qid_from_sparql(ENGLISH_FILE, query_language_pattern)


# def get_qid_for_language(language: str, data: dict) -> str:
#     for lang in data["languages"]:
#         if lang["language"].lower() == language.lower():
#             return lang["qid"]
#     return None  # Return None if the language is not found


# # Get the QID for English


# def check_query_language_identifier(dir_name: str, language_identifier):
#     try:
#         with LANGUAGE_METADATA_FILE.open("r", encoding="utf-8") as file:
#             language_metadata = json.load(file)

#     except (IOError, json.JSONDecodeError) as e:
#         print(f"Error reading language metadata: {e}")

#     language_QID_metadata = get_qid_for_language(dir_name, language_metadata)

#     return language_QID_metadata == language_identifier


# print(check_query_language_identifier("ENGLISH", language_QID))


def check_queries():
    # Dummy data simulating query files with incorrect identifiers
    incorrect_language_qids = [
        "English/nouns/query_nouns.sparql",
        "Spanish/verbs/query_verbs.sparql",
    ]

    incorrect_data_type_qids = [
        "English/nouns/query_nouns.sparql",  # Same file in both lists
        "French/verbs/query_verbs_1.sparql",
    ]

    # Check if there are any incorrect queries
    if incorrect_language_qids or incorrect_data_type_qids:
        print(
            "There are queries that have incorrect language or data type identifiers.\n"
        )

        if incorrect_language_qids:
            print("Queries with incorrect languages QIDs are:")
            for file in incorrect_language_qids:
                print(f"- {file}")

        if incorrect_data_type_qids:
            print("\nQueries with incorrect data type QIDs are:")
            for file in incorrect_data_type_qids:
                print(f"- {file}")
    else:
        print("All queries are correct.")


if __name__ == "__main__":
    check_queries()
