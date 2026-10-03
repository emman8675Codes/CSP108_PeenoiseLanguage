from enum import Enum, auto

class TokenType(Enum): 

    # Identifier & Literals 
    TAGATUKOY = auto()          # identifier
    BILANG = auto()             # numeric literal
    TITIK = auto()              # string literal
    KARAKTER = auto()           # char literal
    TOTOO = auto()              # true
    MALI = auto()               # false

    # Java Data Types 
    URI_BUONG_NUMERO = auto()   # int 
    URI_LUTANG_NUMERO = auto()  # float
    URI_TITIK = auto()          # char
    URI_SALITA = auto()         # String
    URI_KATOTOHANAN = auto()    # boolean

    # Keywords 
    ITAKDA = auto()             # var / declaration helper
    IPAKITA = auto()            # System.out.println
    KUNG = auto()               # if
    KUNDI_KUNG = auto()         # else if
    KUNDI = auto()              # else
    PIHITAN = auto()            # switch
    KASO = auto()               # case
    HINTO = auto()              # break
    LIKAS = auto()              # default

    # Operators
        # Assignment
    PAGTATAKDA = auto()         # =

        # Relational
    PAREHO = auto()             # == 
    DI_PAREHO = auto()          # !=
    HIGIT = auto()              # >
    MABABA = auto()             # <
    HIGIT_O_PAREHO = auto()     # >=
    MABABA_O_PAREHO = auto()    # <=

        # Logical
    LOHIKAL_AT  = auto()        # &&
    LOHIKAL_O = auto()          # ||
    LOHIKAL_HINDI = auto()      # !

        # Arithmetic
    DAGDAG = auto()             # +
    BAWAS = auto()              # -
    PARAMI = auto()             # *
    HATI = auto()               # /
    LABIS = auto()              # %

    # Delimiters 
    KALIWANG_KUKO = auto()      # {
    KANANG_KUKO = auto()        # }
    KALIWANG_PANIPI = auto()    # (
    KANANG_PANIPI = auto()      # )
    TULDOK_KUWIT = auto()       # ;
    TUTULDOK = auto()           # :
    KUWIT = auto()              # ,

    DULO = auto()               # EOF
        