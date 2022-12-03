"""
Process Unicode
------------

Module for processing Unicode based corpuses for autosuggestion generation.

Contents:
    gen_emoji_autosuggestions
"""

import csv
import json
from importlib.resources import files

import emoji
from icu import Char, UProperty
from tqdm.auto import tqdm

from scribe_data.load.update_utils import (
    get_language_iso,
    get_path_from_process_unicode,
    get_path_from_update_data,
)

from . import _resources


def gen_emoji_autosuggestions(
    language="English",
    num_emojis=None,
    ignore_keywords=None,
    update_scribe_apps=False,
    verbose=True,
):
    """
    Generates a dictionary of keywords (keys) and emoji unicode(s) associated with them (values).

    Parameters
    ----------
        language : string (default=en)
            The language autosuggestions are being generated for.

        num_emojis: int (default=None)
            The limit for number of emojis that autosuggestions should be generated from.

        ignore_keywords : str or list (default=None)
            Keywords that should be ignored.

        update_scribe_apps : bool (default=False)
            Saves the created dictionaries as JSONs in Scribe app directories.

        verbose : bool (default=True)
            Whether to show a tqdm progress bar for the process.

    Returns
    -------
        Autosuggestions dictionaries for emoji keywords-to-unicode are saved locally or uploaded to Scribe apps.
    """

    autosuggest_dict = {}

    iso = get_language_iso(language)

    if isinstance(ignore_keywords, str):
        keywords_to_ignore = [ignore_keywords]
    elif isinstance(ignore_keywords, list):
        keywords_to_ignore = ignore_keywords
    else:
        keywords_to_ignore = []

    # Pre-set up the emoji popularity data.
    popularity_dict = {}

    with files(_resources).joinpath("2021_ranked.tsv").open() as popularity_file:
        tsv_reader = csv.DictReader(popularity_file, delimiter="\t")
        for tsv_row in tsv_reader:
            popularity_dict[tsv_row["Emoji"]] = int(tsv_row["Rank"])

    path_to_scribe_org = get_path_from_process_unicode()
    annotations_file_path = f"{path_to_scribe_org}/Scribe-Data/node_modules/cldr-annotations-full/annotations/{iso}/annotations.json"
    annotations_derived_file_path = f"{path_to_scribe_org}/Scribe-Data/node_modules/cldr-annotations-derived-full/annotationsDerived/{iso}/annotations.json"

    cldr_file_paths = {
        "annotations": annotations_file_path,
        "annotationsDerived": annotations_derived_file_path,
    }

    for cldr_file_key, cldr_file_path in cldr_file_paths.items():
        with open(cldr_file_path, "r") as file:
            cldr_data = json.load(file)

        cldr_dict = cldr_data[cldr_file_key]["annotations"]

        for cldr_char in tqdm(
            iterable=cldr_dict, 
            desc=f"Characters processed from '{cldr_file_key}' CLDR file for {language}", 
            unit="cldr characters", 
            disable=not verbose,
        ):
            # Filter CLDR data for emoji characters.
            if cldr_char in emoji.EMOJI_DATA:
                emoji_rank = popularity_dict.get(cldr_char)

                # If number limit specified, filter for the highest-ranked emojis.
                if num_emojis and (
                    emoji_rank is None
                    or emoji_rank > num_emojis
                ):
                    continue

                # Process for emoji variants.
                has_modifier_base = Char.hasBinaryProperty(
                    cldr_char, UProperty.EMOJI_MODIFIER_BASE
                )
                if has_modifier_base and len(cldr_char) > 1:
                    continue

                # Only fully-qualified emoji should be generated by keyboards.
                # See www.unicode.org/reports/tr51/#Emoji_Implementation_Notes.
                if (
                    emoji.EMOJI_DATA[cldr_char]["status"]
                    == emoji.STATUS["fully_qualified"]
                ):
                    emoji_annotations = cldr_dict[cldr_char]

                    for emoji_keyword in emoji_annotations["default"]:
                        if (
                            # Use single-word annotations as keywords.
                            len(emoji_keyword.split()) == 1
                            and emoji_keyword not in keywords_to_ignore
                        ):
                            autosuggest_dict.setdefault(emoji_keyword, []).append(
                                {
                                    "emoji": cldr_char,
                                    "is_base": has_modifier_base,
                                    "rank": emoji_rank,
                                }
                            )

    if verbose:
        print(
            f"Number of emoji trigger keywords found for {language}: {len(autosuggest_dict)}"
        )

    if update_scribe_apps:
        output_path = f"{get_path_from_update_data()}/Scribe-iOS/Keyboards/LanguageKeyboards/{language.capitalize()}/Data/emoji_suggestions.json"
    else:
        output_path = f"{language.lower()}_emoji_suggestions.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(autosuggest_dict, file, ensure_ascii=False, indent=0)

    print(
        f"Emoji autosuggestions for {language} generated and saved to '{output_path}'."
    )

    return autosuggest_dict
