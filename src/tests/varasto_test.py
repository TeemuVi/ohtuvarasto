import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_luodun_varaston_tilavuus_tilanteessa_kun_luku_on_negatiivinen(self):
        luotu_varasto = Varasto(-1)
        self.assertAlmostEqual(luotu_varasto.tilavuus, 0.0)

    def test_varasto_jossa_negatiivinen_saldon_aloitus(self):
        luotu_varasto = Varasto(8,-3)
        self.assertAlmostEqual(luotu_varasto.saldo, 0.0)

    def test_varasto_jonka_alkusaldo_suurempikuin_tilavuus(self):
        luotu_varasto = Varasto(3,6)
        self.assertAlmostEqual(luotu_varasto.saldo, 3)

    def test_negatiivisen_lisayksen_tilanne(self):
        self.varasto.lisaa_varastoon(1)
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 1)

    def test_varaston_ylitaytto(self):
        self.varasto.lisaa_varastoon(14)
        self.assertAlmostEqual(self.varasto.saldo, 10.0)

    def test_viety_negatiivinen(self):
        self.varasto.lisaa_varastoon(4)
        otettu = self.varasto.ota_varastosta(-3)
        self.assertAlmostEqual(otettu, 0.0)
        self.assertAlmostEqual(self.varasto.saldo, 4)

    def test_varastosta_otetaan_enemman_kun_varastossa_on(self):
        self.varasto.lisaa_varastoon(6)
        otettu = self.varasto.ota_varastosta(8)
        self.assertAlmostEqual(self.varasto.saldo, 0.0)
        self.assertAlmostEqual(otettu, 6)

    def test_teksti_tulostuu_oikein(self):
        self.varasto.lisaa_varastoon(6)
        haluttu_vastaus = "saldo = 6, vielä tilaa 4"
        self.assertEqual(str(self.varasto), haluttu_vastaus)
