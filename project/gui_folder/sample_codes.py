"""
Curated sample codes for Peenoise Language IDE.
Users can load these directly from the GUI to test the language syntax and compiler.
"""

SAMPLE_CODES = {
    "Pangunahing Pagsubok (Main Demo)": """// Peenoise Language - Pangunahing Pagsubok
buong_numero edad = 20;
lutang_numero marka = 88.5;
katotohanan pasado = totoo;
salita bati = "Maligayang Pagdating sa Peenoise!";

// Pagsusuri ng Kondisyon (kung / kundi_kung / kundi)
kung (edad >= 18 && pasado == totoo) {
    ipakita(bati);
} kundi_kung (edad == 17) {
    ipakita("Kulang ng isang taon para maging legal.");
} kundi {
    ipakita("Bata pa.");
}

// Pihitan Statement (switch-case)
pihitan (edad) {
    kaso 18:
        ipakita("Bagong adulto (18 taong gulang)");
        hinto;
    kaso 20:
        ipakita("Saktong dalawampu ang edad!");
        hinto;
    likas:
        ipakita("Ibang edad");
        hinto;
}
""",

    "Kondisyonal: Pagsusuri ng Edad": """// Pagsusuri ng Edad at Lisensya
buong_numero edad = 19;
katotohanan may_lisensya = totoo;

kung (edad >= 18 && may_lisensya == totoo) {
    ipakita("18 and above: Maaari nang magmaneho!");
} kundi_kung (edad >= 18 && may_lisensya == mali) {
    ipakita("18 and above: Kumuha muna ng lisensya.");
} kundi {
    ipakita("17 below: Hindi pa pinapayagan.");
}
""",

    "Aritmetika at Kalkulasyon": """// Mga Kalkulasyon sa Matematika
buong_numero a = 25;
buong_numero b = 10;

buong_numero dagdag = a + b;
buong_numero bawas = a - b;
buong_numero parami = a * b;
buong_numero hati = a / b;
buong_numero labis = a % b;

ipakita("Kabuuan ng 25 + 10:");
ipakita(dagdag);

ipakita("Natira sa 25 % 10:");
ipakita(labis);

// Pagsasama ng Salita (String Concatenation)
salita unahan = "Mabuhay, ";
salita dulo = "Pilipinas!";
ipakita(unahan + dulo);
""",

    "Pihitan: Antas ng Grado": """// Sistema ng Grado gamit ang Pihitan
buong_numero grado_kategorya = 1;

pihitan (grado_kategorya) {
    kaso 1:
        ipakita("Baitang A: Napakahusay!");
        hinto;
    kaso 2:
        ipakita("Baitang B: Magaling!");
        hinto;
    kaso 3:
        ipakita("Baitang C: Pasado.");
        hinto;
    likas:
        ipakita("Baitang D: Kailangan pang mag-aral.");
        hinto;
}
""",

    "Pagsubok sa Maling Semantika (Error Demo)": """// Halimbawa ng Semantic Error
// Hindi maaring magpasa ng 'salita' sa 'buong_numero'
buong_numero bilang = "Hindi Ito Numero";
ipakita(bilang);
"""
}
