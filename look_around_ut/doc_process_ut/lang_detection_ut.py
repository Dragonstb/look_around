import numpy as np
from nltk.corpus import stopwords
from look_around.dev_tools import utils
from typing import List
import unittest
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../look_around')
# autopep8: off
from look_around.doc_process import lang_detection as ld
# autopep8: on


class TestStopsRemoval(unittest.TestCase):

    langs: List[str]

    def setUp(self) -> None:
        self.langs = ['dutch', 'english', 'french', 'german',
                      'italian', 'nepali', 'turkish', 'spanish']

    def test_dutch(self):
        # text from https://en.wikipedia.org/wiki/Wikipedia:About
        text = "Het is zo'n verbazend simpel concept: iedere bezoeker kan de knop 'bewerken' aanklikken en direct aan de slag gaan. Je bijdrage, groot of klein, wordt niet door een commissie van redacteuren beoordeeld, wat de snelheid en het plezier om deel te nemen ten goede komt. Andere deelnemers kunnen jouw bijdrage op hun beurt zo nodig aanvullen en/of corrigeren. In de praktijk blijkt dat bij de Wikipedia heel effectief te werken, vergeleken met andere web-projecten met eenzelfde soort doelstelling."
        expect = 'dutch'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_english(self):
        # text from https://en.wikipedia.org/wiki/Wikipedia:About
        text = "Wikipedia is a free online encyclopedia that anyone can edit, and millions already have. Wikipedia's purpose is to benefit readers by presenting information on all branches of knowledge. Hosted by the Wikimedia Foundation, it consists of freely editable content, whose articles also have numerous links to guide readers to more information."
        expect = 'english'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_french(self):
        # text from https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:%C3%80_propos_de_Wikip%C3%A9dia
        text = "Wikipédia est une encyclopédie alimentée sur Internet par des volontaires. Universelle, multilingue et fonctionnant sur le principe du wiki, chacun peut y collaborer immédiatement. Wikipédia a pour objectif d'offrir un contenu libre, objectif et vérifiable que chacun peut modifier et améliorer, sans nécessiter de s'enregistrer. Tous les articles de Wikipédia sont un travail en progression qui peut être modifié et amélioré par tout le monde."
        expect = 'french'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_german(self):
        # text from https://de.wikipedia.org/wiki/Wikipedia:%C3%9Cber_Wikipedia
        text = "Das Ziel der Wikipedia ist der Aufbau einer Enzyklopädie durch freiwillige und ehrenamtliche Autorinnen und Autoren. Der Name Wikipedia setzt sich zusammen aus Wiki (entstanden aus wiki, dem hawaiischen Wort für ‚schnell‘) und encyclopedia, dem englischen Wort für ‚Enzyklopädie‘. Ein Wiki ist ein Webangebot, dessen Seiten jeder leicht und ohne technische Vorkenntnisse direkt im Webbrowser bearbeiten kann."
        expect = 'german'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_italian(self):
        # text from https://it.wikipedia.org/wiki/Wikipedia:Sala_stampa/Wikipedia
        text = "Wikipedia è un'enciclopedia multilingue liberamente consultabile sul Web, fondata sulla certezza che ciascuno possieda delle conoscenze che può condividere con gli altri. L'ambizioso progetto, che prende il via il 15 gennaio 2001 in lingua inglese, nell'arco di soli quattro mesi ha visto nascere altre 13 edizioni, tra le quali quella in italiano."
        expect = 'italian'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_nepali(self):
        # text from https://ne.wikipedia.org/wiki/%E0%A4%B5%E0%A4%BF%E0%A4%95%E0%A4%BF%E0%A4%AA%E0%A4%BF%E0%A4%A1%E0%A4%BF%E0%A4%AF%E0%A4%BE:%E0%A4%B5%E0%A4%BF%E0%A4%95%E0%A4%BF%E0%A4%AA%E0%A4%BF%E0%A4%A1%E0%A4%BF%E0%A4%AF%E0%A4%BE%E0%A4%95%E0%A5%8B_%E0%A4%AC%E0%A4%BE%E0%A4%B0%E0%A5%87%E0%A4%AE%E0%A4%BE
        text = "विकिपिडिया एक खुल्ला विश्वकोष हो। यसको लेखन विश्वभरका थुप्रै स्वयंसेवक लेखकहरूले गरिरहेका छन्। यो वेबसाइट एक विकि हो। यसको अर्थ कसैले पनि (तपाईले समेत) यसलाई परिवर्तन गर्न सक्नु हुनेछ। विकिपिडियाको सुरुवात जनवरी २००२ मा अङ्ग्रेजी भाषाको विकिपीडियाबाट भएको हो। हाल यसको नेपाली संस्करण भने प्रारम्भिक अवस्थामा छ। नेपाली भाषाको ३२,९१५ लेखहरू समेत गरि सबै विकिपीडियाहरूमा हाल १ करोड भन्दा बढी लेखहरू छन। प्रत्येक दिन संसारभरका सयौँ मानिसहरूले हजारौँ परिवर्तनहरू गर्दछन र कयौँ नयाँ लेखहरू निर्माण गर्दछन्। "
        expect = 'nepali'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_turkish(self):
        # text from https://nl.wikipedia.org/wiki/Help:Unieke_van_Wikipedia
        text = "Vikipedi projesinin, 2002'de hayata geçen Türkçe koludur. Kurulduğu günden itibaren, internetin en geniş kaynak sitesi olma yönünde ilerlemektedir. Vikipedi, içeriği dünyanın her köşesinden gönüllü insanlar tarafından ortaklaşa hazırlanan açık kodlu, özgür, kâr amacı gütmeyen ücretsiz bir ansiklopedidir."
        expect = 'turkish'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_spanish(self):
        # text from https://es.wikipedia.org/wiki/Wikipedia:Acerca_de
        text = "Wikipedia en español es la versión en español de Wikipedia, un proyecto de enciclopedia web multilingüe de contenido libre basado en un modelo de edición abierta. Wikipedia crece cada día gracias a la participación de gente de todo el mundo, siendo el mayor proyecto de recopilación de conocimiento jamás realizado en la historia de la humanidad."
        expect = 'spanish'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_no_text(self):
        text = ""
        expect = 'unknown'
        lang = ld.detect_lang(text, self.langs)
        self.assertEqual(expect, lang)

    def test_no_languages(self):
        text = "abra cadabra"
        expect = 'unknown'
        lang = ld.detect_lang(text, [])
        self.assertEqual(expect, lang)

    def test_threshold_ok(self):
        stops = np.array(stopwords.words('english'))
        words_1 = utils.pick_several_from_array(stops, size=10, replace=False)
        words_2 = [
            'Hippopotomonstrosesquipedaliophobia' for _ in range(len(words_1))]
        words = words_1.tolist() + words_2  # 50% stop words
        text = ' '.join(words)
        expect = 'english'
        lang = ld.detect_lang(text, ['english'], threshold=0.499)
        self.assertEqual(expect, lang)

    def test_threshold_missed(self):
        stops = np.array(stopwords.words('english'))
        words_1 = utils.pick_several_from_array(stops, size=10, replace=False)
        words_2 = [
            'Hippopotomonstrosesquipedaliophobia' for _ in range(len(words_1))]
        words = words_1.tolist() + words_2  # 50% stop words
        text = ' '.join(words)
        expect = 'english'
        lang = ld.detect_lang(text, ['english'], threshold=0.501)
        self.assertEqual(expect, lang)


if __name__ == '__main__':
    unittest.main()
