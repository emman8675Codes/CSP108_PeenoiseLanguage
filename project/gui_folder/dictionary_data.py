"""
Comprehensive syntax dictionary and references for the Peenoise Language.
Categorized list of language constructs, keywords, operators, and data types
with explanations, signatures, and copyable/insertable code examples.
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DictionaryEntry:
    name: str
    category: str
    english_equiv: str
    syntax: str
    description: str
    example: str
    tags: List[str]

DICTIONARY_ENTRIES: List[DictionaryEntry] = [
    # --- MGA URI NG DATOS (DATA TYPES) ---
    DictionaryEntry(
        name="buong_numero",
        category="Uri ng Datos",
        english_equiv="int (Integer)",
        syntax="buong_numero <pangalan> = <halaga>;",
        description="Ginagamit para sa mga buong bilang (positibo, negatibo, o sero) na walang butal o decimal point.",
        example='buong_numero edad = 20;\nbuong_numero bilang_ng_mag_aaral = 45;',
        tags=["int", "integer", "number", "numero", "bilang", "data type"]
    ),
    DictionaryEntry(
        name="lutang_numero",
        category="Uri ng Datos",
        english_equiv="float (Floating-Point)",
        syntax="lutang_numero <pangalan> = <halaga>;",
        description="Ginagamit para sa mga bilang na may floating point o decimal values.",
        example='lutang_numero grado = 89.75;\nlutang_numero presyo = 149.99;',
        tags=["float", "decimal", "double", "numero", "lutang", "data type"]
    ),
    DictionaryEntry(
        name="salita",
        category="Uri ng Datos",
        english_equiv="String (Text)",
        syntax='salita <pangalan> = "<halaga>";',
        description="Ginagamit para sa mga teksto o pangungusap. Kinakailangang nakapaloob sa dobleng panipi (\").",
        example='salita bati = "Maligayang Pagdating!";\nsalita pangalan = "Juan Dela Cruz";',
        tags=["string", "text", "salita", "teksto", "data type"]
    ),
    DictionaryEntry(
        name="titik_uri",
        category="Uri ng Datos",
        english_equiv="char (Character)",
        syntax="titik_uri <pangalan> = '<karakter>';",
        description="Ginagamit para sa nag-iisang karakter lamang. Kinakailangang nakapaloob sa isahang panipi (').",
        example="titik_uri baitang = 'A';\ntitik_uri seksyon = 'B';",
        tags=["char", "character", "titik", "letra", "data type"]
    ),
    DictionaryEntry(
        name="katotohanan",
        category="Uri ng Datos",
        english_equiv="boolean (Boolean)",
        syntax="katotohanan <pangalan> = totoo; // o mali",
        description="May dalawang posibleng halaga lamang: 'totoo' (true) o 'mali' (false). Ginagamit sa lohika at pagsusuri ng kondisyon.",
        example='katotohanan nakapasa = totoo;\nkatotohanan tapos_na = mali;',
        tags=["boolean", "bool", "totoo", "mali", "katotohanan", "data type"]
    ),

    # --- MGA UTOS AT PAHAYAG (STATEMENTS & COMMANDS) ---
    DictionaryEntry(
        name="ipakita",
        category="Mga Utos",
        english_equiv="print / System.out.println",
        syntax="ipakita(<ekspresyon>);",
        description="Inilalabas o ipinapakita ang halaga ng ekspresyon o salita sa console/terminal ng kinalabasan.",
        example='ipakita("Kumusta, Mundo!");\nipakita(edad);',
        tags=["print", "println", "output", "display", "ipakita", "sulat"]
    ),
    DictionaryEntry(
        name="itakda",
        category="Mga Utos",
        english_equiv="assign / variable assignment",
        syntax="itakda <pangalan> = <bagong_halaga>;",
        description="Ginagamit upang magbago o magtalaga muli ng bagong halaga sa isang dati nang naideklarang baryabol.",
        example='buong_numero iskor = 50;\nitakda iskor = 100;\n// o maaari ring direktang: iskor = 100;',
        tags=["assign", "set", "itakda", "update", "baryabol"]
    ),
    DictionaryEntry(
        name="hinto",
        category="Mga Utos",
        english_equiv="break",
        syntax="hinto;",
        description="Agad na tinatapos ang pagpapatupad ng kasalukuyang pihitan (switch statement).",
        example='kaso 1:\n    ipakita("Isa");\n    hinto;',
        tags=["break", "stop", "hinto", "exit", "pihitan"]
    ),

    # --- KONDISYON AT PAGPAPASIYA (CONDITIONALS) ---
    DictionaryEntry(
        name="kung",
        category="Kondisyonal",
        english_equiv="if",
        syntax="kung (<kondisyon>) {\n    // mga gagawin\n}",
        description="Pangunahing sangay ng kondisyon. Isasagawa ang nasa loob ng panaklong na kulot kapag ang kondisyon ay 'totoo'.",
        example='kung (edad >= 18) {\n    ipakita("Kwalipikadong bumoto.");\n}',
        tags=["if", "kung", "condition", "kondisyon", "branch"]
    ),
    DictionaryEntry(
        name="kundi_kung",
        category="Kondisyonal",
        english_equiv="else if",
        syntax="kundi_kung (<kondisyon>) {\n    // mga gagawin\n}",
        description="Pangalawang pagsusuri kapag ang naunang 'kung' o 'kundi_kung' ay 'mali'.",
        example='kung (marka >= 90) {\n    ipakita("Napakahusay");\n} kundi_kung (marka >= 75) {\n    ipakita("Pumasa");\n}',
        tags=["else if", "kundi_kung", "condition", "kondisyon"]
    ),
    DictionaryEntry(
        name="kundi",
        category="Kondisyonal",
        english_equiv="else",
        syntax="kundi {\n    // mga gagawin kapag mali lahat\n}",
        description="Ang huling sangay kapag walang tumamang kondisyon sa mga naunang 'kung' o 'kundi_kung'.",
        example='kung (edad >= 18) {\n    ipakita("Matanda na.");\n} kundi {\n    ipakita("Bata pa.");\n}',
        tags=["else", "kundi", "default", "kondisyon"]
    ),

    # --- PIHITAN AT KASO (SWITCH-CASE) ---
    DictionaryEntry(
        name="pihitan",
        category="Pihitan at Kaso",
        english_equiv="switch",
        syntax="pihitan (<baryabol>) {\n    kaso <halaga>:\n        ...\n        hinto;\n    likas:\n        ...\n        hinto;\n}",
        description="Pagsusuri ng maraming posibleng halaga ng isang baryabol gamit ang switch-case na estruktura.",
        example='pihitan (kulay) {\n    kaso 1:\n        ipakita("Pula");\n        hinto;\n    likas:\n        ipakita("Iba pang kulay");\n        hinto;\n}',
        tags=["switch", "pihitan", "case", "kaso", "branch"]
    ),
    DictionaryEntry(
        name="kaso",
        category="Pihitan at Kaso",
        english_equiv="case",
        syntax="kaso <halaga>:\n    // mga pahayag\n    hinto;",
        description="Tukoy na opsiyon sa loob ng pihitan na itutugma sa sinusuring halaga.",
        example='kaso 18:\n    ipakita("Debut age!");\n    hinto;',
        tags=["case", "kaso", "pihitan"]
    ),
    DictionaryEntry(
        name="likas",
        category="Pihitan at Kaso",
        english_equiv="default",
        syntax="likas:\n    // mga pahayag kung walang tumugma\n    hinto;",
        description="Ang default na sangay sa loob ng pihitan kapag walang tumugmang 'kaso'.",
        example='likas:\n    ipakita("Hindi kinikilalang opsiyon.");\n    hinto;',
        tags=["default", "likas", "pihitan", "fallback"]
    ),

    # --- MGA LITERAL NA BOOLEAN ---
    DictionaryEntry(
        name="totoo / mali",
        category="Lohika",
        english_equiv="true / false",
        syntax="totoo  |  mali",
        description="Mga batayang halaga ng katotohanan (boolean literals).",
        example='katotohanan bukas = totoo;\nkatotohanan sarado = mali;',
        tags=["true", "false", "totoo", "mali", "boolean"]
    ),

    # --- MGA OPERATOR (OPERATORS) ---
    DictionaryEntry(
        name="Aritmetika (+, -, *, /, %)",
        category="Mga Operator",
        english_equiv="Arithmetic (+, -, *, /, %)",
        syntax="+ (dagdag), - (bawas), * (parami), / (hati), % (labis)",
        description="Mga matematikang kalkulasyon para sa mga buong_numero at lutang_numero. Ang '+' ay sumusuporta rin sa pagsasama ng mga salita (string concat).",
        example='buong_numero kabuuan = 10 + 5;\nbuong_numero sukli = 20 - 7;\nbuong_numero doble = 4 * 2;\nbuong_numero kalahati = 10 / 2;\nbuong_numero tira = 10 % 3;\nsalita buo = "Hi " + "Juan";',
        tags=["arithmetic", "plus", "minus", "multiply", "divide", "modulo", "dagdag", "bawas"]
    ),
    DictionaryEntry(
        name="Paghahambing (==, !=, >, <, >=, <=)",
        category="Mga Operator",
        english_equiv="Relational / Comparison",
        syntax="== (pareho), != (di-pareho), > (higit), < (mababa), >=, <=",
        description="Naghahambing ng dalawang halaga at nagbabalik ng 'totoo' o 'mali'.",
        example='katotohanan a = (10 > 5);   // totoo\nkatotohanan b = (5 == 5);   // totoo\nkatotohanan c = (10 != 10); // mali',
        tags=["comparison", "relational", "equal", "greater", "less", "pareho", "higit"]
    ),
    DictionaryEntry(
        name="Lohikal (&&, ||, !)",
        category="Mga Operator",
        english_equiv="Logical (AND, OR, NOT)",
        syntax="&& (lohikal at), || (lohikal o), ! (lohikal hindi)",
        description="Pinagsasama o binabaligtad ang mga boolean na kondisyon.",
        example='kung (edad >= 18 && may_lisensya == totoo) {\n    ipakita("Maaaring magmaneho.");\n}\nkung (!nakapasa) {\n    ipakita("Subukan muli.");\n}',
        tags=["logical", "and", "or", "not", "lohikal"]
    ),

    # --- KOMENTO ---
    DictionaryEntry(
        name="Mga Komento (//, /* */, #)",
        category="Mga Simbolo",
        english_equiv="Comments",
        syntax="// Isang linya\n# Alternatibong linya\n/* Maramihang linya */",
        description="Mga linyang hindi pinapansin ng compiler. Ginagamit para sa paliwanag o tala ng programmer.",
        example='// Ito ay isang komento\nbuong_numero x = 10; # komento rin\n/* \n   Maramihang\n   linya ng komento\n*/',
        tags=["comment", "komento", "paliwanag"]
    ),
]

CATEGORIES = [
    "Lahat",
    "Uri ng Datos",
    "Mga Utos",
    "Kondisyonal",
    "Pihitan at Kaso",
    "Mga Operator",
    "Mga Simbolo"
]
