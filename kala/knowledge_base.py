# -*- coding: utf-8 -*-
"""Sourced knowledge base for Jyotish (Vedic astrology).

This module holds structured, factual attributes for the 27 nakshatras,
12 rashis, 9 grahas, 12 bhavas, and the 9 Vimsottari mahadasha lords.

Primary classical sources: Brihat Parashara Hora Shastra (BPHS),
Phaladeepika (Mantreswara), and Saravali (Kalyana Varma). Attributes such as
nakshatra deity (devata), symbol, ruling planet (Vimsottari lord), and gana are
long-standing, widely-attested classical assignments. Human-readable trait /
career / signification summaries are concise, non-fear-based paraphrases
grounded in those texts and corroborated by reputable modern references
(see docs/SOURCES.md and the SOURCES list below).

Keys are ASCII English canonical names matching the spellings used elsewhere in
this project (see kala/constants.py). Human-readable strings are provided in
English (en), Hindi/Devanagari (hi), and Telugu (te).

Confidence notes:
- deity, symbol, ruling_planet, gana: HIGH (classical, near-universal agreement).
- rashi lord/element/quality: HIGH (classical).
- graha karaka/significations, bhava themes, dasha effects: HIGH for the core
  significations; the exact wording is an editorial paraphrase.
- hi/te translations: MEDIUM-HIGH; they are faithful summaries, not verbatim
  quotations from the classical Sanskrit.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 27 Nakshatras
# ---------------------------------------------------------------------------
# deity: presiding devata (BPHS / Taittiriya Brahmana tradition)
# symbol: classical emblem
# ruling_planet: Vimsottari dasha lord (matches NAKSHATRA_LORDS in constants.py)
# gana: temperament class -> Deva (divine), Manushya (human), Rakshasa (demonic)

NAKSHATRA_KB = {
    "Ashwini": {
        "deity": "Ashwini Kumaras",
        "symbol": "horse's head",
        "ruling_planet": "Ketu",
        "gana": "Deva",
        "traits": {
            "en": "Quick, energetic and pioneering; natural healers who like to start things and act fast.",
            "hi": "तेज़, ऊर्जावान और अग्रणी; स्वाभाविक चिकित्सक जो कार्य आरम्भ करना और शीघ्र क्रिया करना पसंद करते हैं।",
            "te": "వేగంగా, శక్తివంతంగా, ముందడుగు వేసేవారు; సహజ వైద్యులు, పనులను ప్రారంభించడం, త్వరగా చర్య తీసుకోవడం ఇష్టపడతారు.",
        },
        "career": {
            "en": "Medicine, healing, sports, travel, emergency services and new ventures.",
            "hi": "चिकित्सा, उपचार, खेल, यात्रा, आपातकालीन सेवाएँ और नए उद्यम।",
            "te": "వైద్యం, చికిత్స, క్రీడలు, ప్రయాణం, అత్యవసర సేవలు, కొత్త వ్యాపారాలు.",
        },
    },
    "Bharani": {
        "deity": "Yama",
        "symbol": "yoni (female organ)",
        "ruling_planet": "Venus",
        "gana": "Manushya",
        "traits": {
            "en": "Determined, creative and enduring; carry things through cycles of transformation with strong will.",
            "hi": "दृढ़संकल्पी, रचनात्मक और सहनशील; प्रबल इच्छाशक्ति से परिवर्तन के चक्रों को पूरा करते हैं।",
            "te": "దృఢ సంకల్పం, సృజనాత్మకత, ఓర్పు కలవారు; బలమైన సంకల్పంతో మార్పు దశలను పూర్తి చేస్తారు.",
        },
        "career": {
            "en": "Arts, entertainment, obstetrics, law and work involving discipline or moral judgement.",
            "hi": "कला, मनोरंजन, प्रसूति-चिकित्सा, विधि और अनुशासन या नैतिक निर्णय से जुड़े कार्य।",
            "te": "కళలు, వినోదం, ప్రసూతి వైద్యం, న్యాయం, క్రమశిక్షణ లేదా నైతిక నిర్ణయాలతో కూడిన పని.",
        },
    },
    "Krittika": {
        "deity": "Agni",
        "symbol": "razor/flame",
        "ruling_planet": "Sun",
        "gana": "Rakshasa",
        "traits": {
            "en": "Sharp, honest and purifying; cut through illusion and get things done with courage.",
            "hi": "तीक्ष्ण, ईमानदार और शुद्ध करने वाले; भ्रम को काटकर साहस से कार्य पूर्ण करते हैं।",
            "te": "పదునైన, నిజాయితీ, శుద్ధి చేసే స్వభావం; భ్రమను తొలగించి ధైర్యంగా పనులు పూర్తి చేస్తారు.",
        },
        "career": {
            "en": "Leadership, teaching, cooking, military, surgery and critical or editorial work.",
            "hi": "नेतृत्व, शिक्षण, पाककला, सेना, शल्यचिकित्सा और समीक्षात्मक कार्य।",
            "te": "నాయకత్వం, బోధన, వంట, సైన్యం, శస్త్రచికిత్స, విమర్శనాత్మక పని.",
        },
    },
    "Rohini": {
        "deity": "Brahma (Prajapati)",
        "symbol": "cart/chariot",
        "ruling_planet": "Moon",
        "gana": "Manushya",
        "traits": {
            "en": "Charming, artistic and abundant; nurture growth, beauty and material comfort.",
            "hi": "आकर्षक, कलात्मक और समृद्ध; वृद्धि, सौंदर्य और भौतिक सुख का पोषण करते हैं।",
            "te": "ఆకర్షణీయం, కళాత్మకం, సమృద్ధి కలవారు; ఎదుగుదల, సౌందర్యం, భౌతిక సుఖాన్ని పెంపొందిస్తారు.",
        },
        "career": {
            "en": "Agriculture, fashion, arts, food, finance and any beauty- or comfort-related trade.",
            "hi": "कृषि, फैशन, कला, भोजन, वित्त और सौंदर्य या सुख से जुड़े व्यवसाय।",
            "te": "వ్యవసాయం, ఫ్యాషన్, కళలు, ఆహారం, ఆర్థికం, సౌందర్య లేదా సౌకర్య సంబంధ వృత్తులు.",
        },
    },
    "Mrigashira": {
        "deity": "Soma (Chandra)",
        "symbol": "deer's head",
        "ruling_planet": "Mars",
        "gana": "Deva",
        "traits": {
            "en": "Curious, gentle seekers; forever searching, exploring and gathering knowledge.",
            "hi": "जिज्ञासु, कोमल खोजी; निरंतर अन्वेषण करते और ज्ञान एकत्र करते हैं।",
            "te": "కుతూహలం, సున్నితమైన అన్వేషకులు; నిరంతరం వెతుకుతూ, పరిశోధిస్తూ జ్ఞానం సేకరిస్తారు.",
        },
        "career": {
            "en": "Research, writing, travel, real estate, textiles and exploratory or field work.",
            "hi": "अनुसंधान, लेखन, यात्रा, अचल संपत्ति, वस्त्र और क्षेत्रीय कार्य।",
            "te": "పరిశోధన, రచన, ప్రయాణం, స్థిరాస్తి, వస్త్రాలు, క్షేత్ర పని.",
        },
    },
    "Ardra": {
        "deity": "Rudra",
        "symbol": "teardrop/diamond",
        "ruling_planet": "Rahu",
        "gana": "Manushya",
        "traits": {
            "en": "Intense and transformative; clear away the old like a storm and renew through effort.",
            "hi": "प्रबल और परिवर्तनकारी; तूफ़ान की तरह पुराने को हटाकर प्रयास से नवीनीकरण करते हैं।",
            "te": "తీవ్రత, పరివర్తన కలవారు; తుఫానులా పాతదాన్ని తొలగించి కృషితో పునరుద్ధరిస్తారు.",
        },
        "career": {
            "en": "Science, engineering, research, digital tech and work that solves hard problems.",
            "hi": "विज्ञान, अभियांत्रिकी, अनुसंधान, डिजिटल तकनीक और कठिन समस्याओं का समाधान।",
            "te": "సైన్స్, ఇంజనీరింగ్, పరిశోధన, డిజిటల్ టెక్నాలజీ, కఠిన సమస్యలను పరిష్కరించే పని.",
        },
    },
    "Punarvasu": {
        "deity": "Aditi",
        "symbol": "bow/quiver",
        "ruling_planet": "Jupiter",
        "gana": "Deva",
        "traits": {
            "en": "Optimistic, wise and resilient; return, renew and share generosity and hope.",
            "hi": "आशावादी, विवेकी और लचीले; लौटकर, नवीनीकरण करके उदारता और आशा बाँटते हैं।",
            "te": "ఆశావాదం, వివేకం, పునరుజ్జీవన శక్తి; తిరిగి వచ్చి, ఉదారత, ఆశను పంచుతారు.",
        },
        "career": {
            "en": "Teaching, philosophy, counselling, publishing and spiritual or humanitarian work.",
            "hi": "शिक्षण, दर्शन, परामर्श, प्रकाशन और आध्यात्मिक या मानवीय कार्य।",
            "te": "బోధన, తత్వశాస్త్రం, సలహా, ప్రచురణ, ఆధ్యాత్మిక లేదా మానవతా పని.",
        },
    },
    "Pushya": {
        "deity": "Brihaspati",
        "symbol": "cow's udder/flower",
        "ruling_planet": "Saturn",
        "gana": "Deva",
        "traits": {
            "en": "Nourishing, dutiful and steady; considered among the most auspicious, they support and protect others.",
            "hi": "पोषक, कर्तव्यनिष्ठ और स्थिर; अत्यंत शुभ माने जाते हैं, दूसरों का सहयोग और रक्षा करते हैं।",
            "te": "పోషణ, కర్తవ్యనిష్ఠ, స్థిరత్వం; అత్యంత శుభప్రదంగా భావిస్తారు, ఇతరులకు మద్దతు, రక్షణ ఇస్తారు.",
        },
        "career": {
            "en": "Teaching, priesthood, public service, nutrition, care-giving and administration.",
            "hi": "शिक्षण, पौरोहित्य, लोक-सेवा, पोषण, देखभाल और प्रशासन।",
            "te": "బోధన, పౌరోహిత్యం, ప్రజా సేవ, పోషణ, సంరక్షణ, పరిపాలన.",
        },
    },
    "Ashlesha": {
        "deity": "Nagas (serpent deities)",
        "symbol": "coiled serpent",
        "ruling_planet": "Mercury",
        "gana": "Rakshasa",
        "traits": {
            "en": "Insightful, magnetic and shrewd; penetrate secrets and influence others with subtle intelligence.",
            "hi": "अंतर्दृष्टिपूर्ण, आकर्षक और चतुर; रहस्यों को भेदते और सूक्ष्म बुद्धि से प्रभावित करते हैं।",
            "te": "అంతర్దృష్టి, ఆకర్షణ, చాకచక్యం; రహస్యాలను చేధిస్తూ సూక్ష్మ బుద్ధితో ప్రభావితం చేస్తారు.",
        },
        "career": {
            "en": "Psychology, research, medicine, politics, occult studies and negotiation.",
            "hi": "मनोविज्ञान, अनुसंधान, चिकित्सा, राजनीति, गूढ़ विद्या और मध्यस्थता।",
            "te": "మనస్తత్వశాస్త్రం, పరిశోధన, వైద్యం, రాజకీయం, గూఢ విద్య, మధ్యవర్తిత్వం.",
        },
    },
    "Magha": {
        "deity": "Pitris (ancestors)",
        "symbol": "royal throne",
        "ruling_planet": "Ketu",
        "gana": "Rakshasa",
        "traits": {
            "en": "Dignified and traditional; honour ancestry and lead with authority and generosity.",
            "hi": "गरिमामय और परंपरावादी; पूर्वजों का सम्मान करते और अधिकार व उदारता से नेतृत्व करते हैं।",
            "te": "గౌరవప్రదం, సంప్రదాయబద్ధం; పూర్వీకులను గౌరవిస్తూ అధికారం, ఉదారతతో నాయకత్వం వహిస్తారు.",
        },
        "career": {
            "en": "Leadership, administration, government, heritage work and ceremonial roles.",
            "hi": "नेतृत्व, प्रशासन, सरकार, विरासत-कार्य और आनुष्ठानिक भूमिकाएँ।",
            "te": "నాయకత్వం, పరిపాలన, ప్రభుత్వం, వారసత్వ పని, ఆచార విధులు.",
        },
    },
    "Purva Phalguni": {
        "deity": "Bhaga",
        "symbol": "front legs of a bed/hammock",
        "ruling_planet": "Venus",
        "gana": "Manushya",
        "traits": {
            "en": "Warm, creative and pleasure-loving; enjoy rest, romance and generous celebration.",
            "hi": "गर्मजोश, रचनात्मक और सुखप्रिय; विश्राम, प्रेम और उदार उत्सव का आनंद लेते हैं।",
            "te": "ఆప్యాయత, సృజనాత్మకత, ఆనందప్రియత్వం; విశ్రాంతి, ప్రేమ, ఉదార వేడుకలను ఆస్వాదిస్తారు.",
        },
        "career": {
            "en": "Arts, entertainment, hospitality, luxury goods and creative self-expression.",
            "hi": "कला, मनोरंजन, आतिथ्य, विलासिता-वस्तु और रचनात्मक अभिव्यक्ति।",
            "te": "కళలు, వినోదం, ఆతిథ్యం, విలాస వస్తువులు, సృజనాత్మక వ్యక్తీకరణ.",
        },
    },
    "Uttara Phalguni": {
        "deity": "Aryaman",
        "symbol": "back legs of a bed",
        "ruling_planet": "Sun",
        "gana": "Manushya",
        "traits": {
            "en": "Reliable, kind and principled; build lasting friendships, contracts and generous partnerships.",
            "hi": "विश्वसनीय, दयालु और सिद्धांतवादी; स्थायी मित्रता, अनुबंध और उदार साझेदारी बनाते हैं।",
            "te": "నమ్మకం, దయ, సూత్రబద్ధత; శాశ్వత స్నేహాలు, ఒప్పందాలు, ఉదార భాగస్వామ్యాలు నిర్మిస్తారు.",
        },
        "career": {
            "en": "Social service, management, contracts, marriage counselling and charitable work.",
            "hi": "समाज-सेवा, प्रबंधन, अनुबंध, विवाह-परामर्श और परोपकारी कार्य।",
            "te": "సామాజిక సేవ, నిర్వహణ, ఒప్పందాలు, వివాహ సలహా, దాతృత్వ పని.",
        },
    },
    "Hasta": {
        "deity": "Savitar (Surya)",
        "symbol": "hand/palm",
        "ruling_planet": "Moon",
        "gana": "Deva",
        "traits": {
            "en": "Skilful, clever and hardworking; achieve goals through craft, dexterity and wit.",
            "hi": "कुशल, चतुर और परिश्रमी; शिल्प, हस्तकौशल और बुद्धि से लक्ष्य प्राप्त करते हैं।",
            "te": "నైపుణ్యం, తెలివి, కష్టపడే తత్వం; చేతిపని, నేర్పు, బుద్ధితో లక్ష్యాలు సాధిస్తారు.",
        },
        "career": {
            "en": "Craftsmanship, healing, trade, writing, handiwork and detailed skilled labour.",
            "hi": "शिल्पकला, उपचार, व्यापार, लेखन, हस्तकला और कुशल श्रम।",
            "te": "చేతిపని, వైద్యం, వాణిజ్యం, రచన, హస్తకళ, నైపుణ్య శ్రమ.",
        },
    },
    "Chitra": {
        "deity": "Tvashtar (Vishwakarma)",
        "symbol": "bright jewel/pearl",
        "ruling_planet": "Mars",
        "gana": "Rakshasa",
        "traits": {
            "en": "Artistic, charismatic and design-minded; create beauty and structure with an eye for form.",
            "hi": "कलात्मक, तेजस्वी और रचना-प्रवीण; रूप की समझ से सौंदर्य और संरचना गढ़ते हैं।",
            "te": "కళాత్మకం, ఆకర్షణ, రూపకల్పన నైపుణ్యం; రూపంపై దృష్టితో సౌందర్యం, నిర్మాణం సృష్టిస్తారు.",
        },
        "career": {
            "en": "Architecture, design, engineering, arts, jewellery and creative production.",
            "hi": "वास्तुकला, डिज़ाइन, अभियांत्रिकी, कला, आभूषण और रचनात्मक निर्माण।",
            "te": "వాస్తుశిల్పం, డిజైన్, ఇంజనీరింగ్, కళలు, ఆభరణాలు, సృజనాత్మక నిర్మాణం.",
        },
    },
    "Swati": {
        "deity": "Vayu",
        "symbol": "young sprout in the wind/coral",
        "ruling_planet": "Rahu",
        "gana": "Deva",
        "traits": {
            "en": "Independent, adaptable and diplomatic; value freedom and move flexibly like the wind.",
            "hi": "स्वतंत्र, अनुकूलनशील और कूटनीतिक; स्वतंत्रता को महत्व देते और वायु-सा लचीले ढंग से चलते हैं।",
            "te": "స్వతంత్రం, అనుకూలత, దౌత్యం; స్వేచ్ఛకు విలువనిస్తూ గాలిలా వంగుతూ కదులుతారు.",
        },
        "career": {
            "en": "Business, trade, diplomacy, law, aviation and independent entrepreneurship.",
            "hi": "व्यापार, वाणिज्य, कूटनीति, विधि, विमानन और स्वतंत्र उद्यमिता।",
            "te": "వ్యాపారం, వాణిజ్యం, దౌత్యం, న్యాయం, విమానయానం, స్వతంత్ర వ్యవస్థాపన.",
        },
    },
    "Vishakha": {
        "deity": "Indra-Agni",
        "symbol": "triumphal archway/potter's wheel",
        "ruling_planet": "Jupiter",
        "gana": "Rakshasa",
        "traits": {
            "en": "Goal-focused and determined; pursue ambitions single-mindedly until they triumph.",
            "hi": "लक्ष्य-केंद्रित और दृढ़; एकाग्रचित्त होकर महत्वाकांक्षाओं का पीछा करते और विजय पाते हैं।",
            "te": "లక్ష్యంపై దృష్టి, దృఢత్వం; ఏకాగ్రతతో ఆశయాలను వెంబడిస్తూ విజయం సాధిస్తారు.",
        },
        "career": {
            "en": "Politics, business, research, competitive fields and goal-driven leadership.",
            "hi": "राजनीति, व्यापार, अनुसंधान, प्रतिस्पर्धी क्षेत्र और लक्ष्य-प्रेरित नेतृत्व।",
            "te": "రాజకీయం, వ్యాపారం, పరిశోధన, పోటీ రంగాలు, లక్ష్యాధారిత నాయకత్వం.",
        },
    },
    "Anuradha": {
        "deity": "Mitra",
        "symbol": "lotus/triumphal gateway",
        "ruling_planet": "Saturn",
        "gana": "Deva",
        "traits": {
            "en": "Friendly, devoted and cooperative; build success through friendship, loyalty and teamwork.",
            "hi": "मित्रवत, समर्पित और सहयोगी; मित्रता, निष्ठा और टीमवर्क से सफलता पाते हैं।",
            "te": "స్నేహశీలం, అంకితభావం, సహకారం; స్నేహం, విధేయత, జట్టుకృషితో విజయం సాధిస్తారు.",
        },
        "career": {
            "en": "Organisation, group work, foreign relations, counselling and devotional pursuits.",
            "hi": "संगठन, समूह-कार्य, विदेश-संबंध, परामर्श और भक्ति-कार्य।",
            "te": "సంస్థ నిర్వహణ, జట్టు పని, విదేశీ సంబంధాలు, సలహా, భక్తి కార్యాలు.",
        },
    },
    "Jyeshtha": {
        "deity": "Indra",
        "symbol": "circular amulet/earring/umbrella",
        "ruling_planet": "Mercury",
        "gana": "Rakshasa",
        "traits": {
            "en": "Responsible, protective and capable; carry seniority and shoulder duty for others.",
            "hi": "उत्तरदायी, संरक्षक और सक्षम; वरिष्ठता निभाते और दूसरों के लिए कर्तव्य वहन करते हैं।",
            "te": "బాధ్యత, రక్షణ, సామర్థ్యం; సీనియారిటీని నిర్వహిస్తూ ఇతరుల కోసం కర్తవ్యం భరిస్తారు.",
        },
        "career": {
            "en": "Management, administration, military, protective services and senior roles.",
            "hi": "प्रबंधन, प्रशासन, सेना, सुरक्षा-सेवाएँ और वरिष्ठ भूमिकाएँ।",
            "te": "నిర్వహణ, పరిపాలన, సైన్యం, రక్షణ సేవలు, సీనియర్ పదవులు.",
        },
    },
    "Mula": {
        "deity": "Nirriti",
        "symbol": "tied bunch of roots",
        "ruling_planet": "Ketu",
        "gana": "Rakshasa",
        "traits": {
            "en": "Investigative and truth-seeking; dig to the root of matters and pursue deep understanding.",
            "hi": "अन्वेषी और सत्य-खोजी; मूल तक जाकर गहन समझ का अनुसरण करते हैं।",
            "te": "పరిశోధన, సత్యాన్వేషణ; విషయాల మూలం వరకు తవ్వి లోతైన అవగాహన కోసం ప్రయత్నిస్తారు.",
        },
        "career": {
            "en": "Research, philosophy, medicine, spirituality and investigation of hidden causes.",
            "hi": "अनुसंधान, दर्शन, चिकित्सा, आध्यात्म और छिपे कारणों की जाँच।",
            "te": "పరిశోధన, తత్వశాస్త్రం, వైద్యం, ఆధ్యాత్మికత, దాగిన కారణాల అన్వేషణ.",
        },
    },
    "Purva Ashadha": {
        "deity": "Apas (water deities)",
        "symbol": "hand fan/winnowing basket",
        "ruling_planet": "Venus",
        "gana": "Manushya",
        "traits": {
            "en": "Confident, persuasive and idealistic; inspire others and hold to convictions with optimism.",
            "hi": "आत्मविश्वासी, प्रभावशाली और आदर्शवादी; आशा के साथ दूसरों को प्रेरित करते और विश्वास पर अडिग रहते हैं।",
            "te": "ఆత్మవిశ్వాసం, ప్రభావం, ఆదర్శవాదం; ఆశతో ఇతరులను ప్రేరేపిస్తూ నమ్మకాలపై నిలుస్తారు.",
        },
        "career": {
            "en": "Debate, law, politics, teaching, shipping and inspirational leadership.",
            "hi": "वाद-विवाद, विधि, राजनीति, शिक्षण, नौवहन और प्रेरक नेतृत्व।",
            "te": "వాదన, న్యాయం, రాజకీయం, బోధన, నౌకాయానం, ప్రేరణాత్మక నాయకత్వం.",
        },
    },
    "Uttara Ashadha": {
        "deity": "Vishvadevas",
        "symbol": "elephant tusk/planks of a bed",
        "ruling_planet": "Sun",
        "gana": "Manushya",
        "traits": {
            "en": "Ethical, patient and enduring; achieve lasting, well-earned success through integrity.",
            "hi": "नैतिक, धैर्यवान और सहनशील; सत्यनिष्ठा से स्थायी और अर्जित सफलता पाते हैं।",
            "te": "నైతికత, ఓర్పు, సహనం; నిజాయితీతో శాశ్వతమైన, సార్థకమైన విజయం సాధిస్తారు.",
        },
        "career": {
            "en": "Leadership, government, law, social reform and long-term institution building.",
            "hi": "नेतृत्व, सरकार, विधि, समाज-सुधार और दीर्घकालिक संस्था-निर्माण।",
            "te": "నాయకత్వం, ప్రభుత్వం, న్యాయం, సామాజిక సంస్కరణ, దీర్ఘకాల సంస్థ నిర్మాణం.",
        },
    },
    "Shravana": {
        "deity": "Vishnu",
        "symbol": "ear/three footprints",
        "ruling_planet": "Moon",
        "gana": "Deva",
        "traits": {
            "en": "Attentive listeners and learners; gather wisdom, connect people and value knowledge.",
            "hi": "ध्यानपूर्वक सुनने और सीखने वाले; ज्ञान बटोरते, लोगों को जोड़ते और विद्या को महत्व देते हैं।",
            "te": "శ్రద్ధగా వినేవారు, నేర్చుకునేవారు; జ్ఞానం సేకరిస్తూ, ప్రజలను కలుపుతూ విద్యకు విలువనిస్తారు.",
        },
        "career": {
            "en": "Teaching, media, communication, counselling, music and knowledge fields.",
            "hi": "शिक्षण, मीडिया, संचार, परामर्श, संगीत और ज्ञान-क्षेत्र।",
            "te": "బోధన, మీడియా, సంభాషణ, సలహా, సంగీతం, జ్ఞాన రంగాలు.",
        },
    },
    "Dhanishta": {
        "deity": "Vasus",
        "symbol": "drum/flute",
        "ruling_planet": "Mars",
        "gana": "Rakshasa",
        "traits": {
            "en": "Rhythmic, prosperous and lively; combine wealth, music and group energy with confidence.",
            "hi": "लयबद्ध, समृद्ध और जीवंत; धन, संगीत और सामूहिक ऊर्जा को आत्मविश्वास से जोड़ते हैं।",
            "te": "లయ, సమృద్ధి, ఉత్సాహం; సంపద, సంగీతం, సామూహిక శక్తిని ఆత్మవిశ్వాసంతో కలుపుతారు.",
        },
        "career": {
            "en": "Music, performing arts, finance, real estate and team-based ventures.",
            "hi": "संगीत, प्रदर्शन-कला, वित्त, अचल संपत्ति और सामूहिक उद्यम।",
            "te": "సంగీతం, ప్రదర్శన కళలు, ఆర్థికం, స్థిరాస్తి, జట్టు వ్యాపారాలు.",
        },
    },
    "Shatabhisha": {
        "deity": "Varuna",
        "symbol": "empty circle/hundred healers",
        "ruling_planet": "Rahu",
        "gana": "Rakshasa",
        "traits": {
            "en": "Independent, private and investigative; heal, research and see through to hidden truths.",
            "hi": "स्वतंत्र, एकांतप्रिय और अन्वेषी; उपचार, अनुसंधान और छिपे सत्य को देखने में निपुण।",
            "te": "స్వతంత్రం, ఏకాంతప్రియత్వం, పరిశోధన; వైద్యం, పరిశోధన, దాగిన సత్యాలను గ్రహించడం.",
        },
        "career": {
            "en": "Medicine, healing, research, technology, astrology and mystical sciences.",
            "hi": "चिकित्सा, उपचार, अनुसंधान, प्रौद्योगिकी, ज्योतिष और रहस्य-विद्या।",
            "te": "వైద్యం, చికిత్స, పరిశోధన, సాంకేతికత, జ్యోతిషం, రహస్య శాస్త్రాలు.",
        },
    },
    "Purva Bhadrapada": {
        "deity": "Aja Ekapada",
        "symbol": "sword/front legs of a funeral cot",
        "ruling_planet": "Jupiter",
        "gana": "Manushya",
        "traits": {
            "en": "Idealistic and intense; hold strong convictions and pursue transformation with passion.",
            "hi": "आदर्शवादी और प्रबल; दृढ़ विश्वास रखते और उत्साह से परिवर्तन का अनुसरण करते हैं।",
            "te": "ఆదర్శవాదం, తీవ్రత; బలమైన నమ్మకాలతో ఉత్సాహంగా పరివర్తనను వెంబడిస్తారు.",
        },
        "career": {
            "en": "Philosophy, research, occult studies, priesthood and reformative work.",
            "hi": "दर्शन, अनुसंधान, गूढ़ विद्या, पौरोहित्य और सुधारात्मक कार्य।",
            "te": "తత్వశాస్త్రం, పరిశోధన, గూఢ విద్య, పౌరోహిత్యం, సంస్కరణ పని.",
        },
    },
    "Uttara Bhadrapada": {
        "deity": "Ahir Budhnya",
        "symbol": "back legs of a funeral cot/twins",
        "ruling_planet": "Saturn",
        "gana": "Manushya",
        "traits": {
            "en": "Calm, deep and wise; offer steady counsel and quiet spiritual strength.",
            "hi": "शांत, गहन और विवेकी; स्थिर परामर्श और मौन आध्यात्मिक शक्ति प्रदान करते हैं।",
            "te": "శాంతం, లోతు, వివేకం; స్థిరమైన సలహా, నిశ్శబ్ద ఆధ్యాత్మిక శక్తిని అందిస్తారు.",
        },
        "career": {
            "en": "Counselling, philosophy, charity, writing and contemplative or advisory roles.",
            "hi": "परामर्श, दर्शन, दान, लेखन और चिंतनशील या सलाहकार भूमिकाएँ।",
            "te": "సలహా, తత్వశాస్త్రం, దానం, రచన, ధ్యానాత్మక లేదా సలహా పాత్రలు.",
        },
    },
    "Revati": {
        "deity": "Pushan",
        "symbol": "fish/drum",
        "ruling_planet": "Mercury",
        "gana": "Deva",
        "traits": {
            "en": "Gentle, compassionate and protective; nourish, guide and help others reach safe completion.",
            "hi": "कोमल, करुणामय और संरक्षक; दूसरों का पोषण, मार्गदर्शन और सुरक्षित पूर्णता में सहायता करते हैं।",
            "te": "సున్నితం, కరుణ, రక్షణ; ఇతరులను పోషిస్తూ, మార్గనిర్దేశం చేస్తూ సురక్షిత గమ్యానికి చేరుస్తారు.",
        },
        "career": {
            "en": "Care-giving, teaching, travel guidance, arts and spiritual or charitable service.",
            "hi": "देखभाल, शिक्षण, यात्रा-मार्गदर्शन, कला और आध्यात्मिक या परोपकारी सेवा।",
            "te": "సంరక్షణ, బోధన, ప్రయాణ మార్గదర్శనం, కళలు, ఆధ్యాత్మిక లేదా దాతృత్వ సేవ.",
        },
    },
}

# ---------------------------------------------------------------------------
# 12 Rashis (zodiac signs)
# ---------------------------------------------------------------------------
# lord: sign ruler; element: Fire/Earth/Air/Water (tattva);
# quality: Movable (Chara), Fixed (Sthira), Dual (Dwiswabhava)

RASHI_KB = {
    "Mesha": {
        "lord": "Mars",
        "element": "Fire",
        "quality": "Movable",
        "traits": {
            "en": "Bold, energetic and pioneering; act first, lead and thrive on new challenges.",
            "hi": "साहसी, ऊर्जावान और अग्रणी; पहल करते, नेतृत्व करते और नई चुनौतियों में फलते-फूलते हैं।",
            "te": "ధైర్యం, శక్తి, ముందడుగు; మొదట చర్య తీసుకుంటూ, నాయకత్వం వహిస్తూ కొత్త సవాళ్లలో రాణిస్తారు.",
        },
    },
    "Vrishabha": {
        "lord": "Venus",
        "element": "Earth",
        "quality": "Fixed",
        "traits": {
            "en": "Patient, steady and sensual; value stability, comfort, beauty and material security.",
            "hi": "धैर्यवान, स्थिर और सुखप्रिय; स्थिरता, सुख, सौंदर्य और भौतिक सुरक्षा को महत्व देते हैं।",
            "te": "ఓర్పు, స్థిరత్వం, ఇంద్రియ ఆనందం; స్థిరత్వం, సౌకర్యం, సౌందర్యం, భద్రతకు విలువనిస్తారు.",
        },
    },
    "Mithuna": {
        "lord": "Mercury",
        "element": "Air",
        "quality": "Dual",
        "traits": {
            "en": "Curious, communicative and versatile; love ideas, learning and lively exchange.",
            "hi": "जिज्ञासु, संवादप्रिय और बहुमुखी; विचार, अध्ययन और सजीव संवाद पसंद करते हैं।",
            "te": "కుతూహలం, సంభాషణ, బహుముఖ ప్రజ్ఞ; ఆలోచనలు, నేర్చుకోవడం, ఉత్సాహభరిత సంభాషణ ఇష్టపడతారు.",
        },
    },
    "Karka": {
        "lord": "Moon",
        "element": "Water",
        "quality": "Movable",
        "traits": {
            "en": "Nurturing, emotional and protective; deeply attached to home, family and roots.",
            "hi": "पोषक, भावुक और संरक्षक; घर, परिवार और जड़ों से गहराई से जुड़े रहते हैं।",
            "te": "పోషణ, భావోద్వేగం, రక్షణ; ఇల్లు, కుటుంబం, మూలాలతో లోతుగా అనుబంధం కలిగి ఉంటారు.",
        },
    },
    "Simha": {
        "lord": "Sun",
        "element": "Fire",
        "quality": "Fixed",
        "traits": {
            "en": "Confident, generous and dignified; natural leaders who shine and inspire loyalty.",
            "hi": "आत्मविश्वासी, उदार और गरिमामय; स्वाभाविक नेता जो चमकते और निष्ठा जगाते हैं।",
            "te": "ఆత్మవిశ్వాసం, ఉదారత, గౌరవం; సహజ నాయకులు, ప్రకాశిస్తూ విధేయతను ప్రేరేపిస్తారు.",
        },
    },
    "Kanya": {
        "lord": "Mercury",
        "element": "Earth",
        "quality": "Dual",
        "traits": {
            "en": "Analytical, precise and service-minded; excel at detail, method and practical care.",
            "hi": "विश्लेषणात्मक, सटीक और सेवाभावी; विवरण, विधि और व्यावहारिक देखभाल में निपुण।",
            "te": "విశ్లేషణ, ఖచ్చితత్వం, సేవాభావం; వివరాలు, పద్ధతి, ఆచరణాత్మక సంరక్షణలో నిపుణులు.",
        },
    },
    "Tula": {
        "lord": "Venus",
        "element": "Air",
        "quality": "Movable",
        "traits": {
            "en": "Balanced, fair and sociable; seek harmony, partnership and aesthetic justice.",
            "hi": "संतुलित, न्यायप्रिय और मिलनसार; सामंजस्य, साझेदारी और सौंदर्यात्मक न्याय चाहते हैं।",
            "te": "సమతుల్యత, న్యాయం, స్నేహశీలత; సామరస్యం, భాగస్వామ్యం, సౌందర్యాత్మక న్యాయాన్ని కోరుకుంటారు.",
        },
    },
    "Vrischika": {
        "lord": "Mars",
        "element": "Water",
        "quality": "Fixed",
        "traits": {
            "en": "Intense, secretive and transformative; probe deeply and regenerate through change.",
            "hi": "प्रबल, रहस्यमय और परिवर्तनकारी; गहराई से खोज करते और परिवर्तन से नवजीवन पाते हैं।",
            "te": "తీవ్రత, రహస్యం, పరివర్తన; లోతుగా పరిశోధిస్తూ మార్పు ద్వారా పునరుజ్జీవం పొందుతారు.",
        },
    },
    "Dhanu": {
        "lord": "Jupiter",
        "element": "Fire",
        "quality": "Dual",
        "traits": {
            "en": "Optimistic, philosophical and free; love travel, truth, teaching and higher meaning.",
            "hi": "आशावादी, दार्शनिक और स्वतंत्र; यात्रा, सत्य, शिक्षण और उच्च अर्थ से प्रेम करते हैं।",
            "te": "ఆశావాదం, తత్వం, స్వేచ్ఛ; ప్రయాణం, సత్యం, బోధన, ఉన్నత అర్థాన్ని ప్రేమిస్తారు.",
        },
    },
    "Makara": {
        "lord": "Saturn",
        "element": "Earth",
        "quality": "Movable",
        "traits": {
            "en": "Disciplined, ambitious and patient; build lasting success through steady, responsible effort.",
            "hi": "अनुशासित, महत्वाकांक्षी और धैर्यवान; स्थिर, उत्तरदायी प्रयास से स्थायी सफलता बनाते हैं।",
            "te": "క్రమశిక్షణ, ఆశయం, ఓర్పు; స్థిరమైన, బాధ్యతాయుత కృషితో శాశ్వత విజయం నిర్మిస్తారు.",
        },
    },
    "Kumbha": {
        "lord": "Saturn",
        "element": "Air",
        "quality": "Fixed",
        "traits": {
            "en": "Innovative, humanitarian and independent; think ahead and value community and ideas.",
            "hi": "नवाचारी, मानवतावादी और स्वतंत्र; आगे की सोचते और समुदाय व विचारों को महत्व देते हैं।",
            "te": "నవకల్పన, మానవత్వం, స్వతంత్రత; ముందుచూపుతో సమాజం, ఆలోచనలకు విలువనిస్తారు.",
        },
    },
    "Meena": {
        "lord": "Jupiter",
        "element": "Water",
        "quality": "Dual",
        "traits": {
            "en": "Compassionate, imaginative and spiritual; intuitive dreamers drawn to art and the divine.",
            "hi": "करुणामय, कल्पनाशील और आध्यात्मिक; अंतर्ज्ञानी स्वप्नदर्शी जो कला और दिव्यता की ओर आकर्षित होते हैं।",
            "te": "కరుణ, ఊహాశక్తి, ఆధ్యాత్మికత; అంతర్జ్ఞానం కల కలలుకనేవారు, కళ, దైవత్వం వైపు ఆకర్షితులవుతారు.",
        },
    },
}

# ---------------------------------------------------------------------------
# 9 Grahas (planets, incl. lunar nodes Rahu/Ketu)
# ---------------------------------------------------------------------------
# karaka: primary natural significations (BPHS karakatva)
# significations: broader themes; remedies: traditional, non-fear-based practices

GRAHA_KB = {
    "Sun": {
        "karaka": "soul, father, authority",
        "significations": {
            "en": "Vitality, self, ego, willpower, leadership, government and paternal influence.",
            "hi": "जीवनशक्ति, आत्मा, अहंकार, इच्छाशक्ति, नेतृत्व, सरकार और पितृ-प्रभाव।",
            "te": "ప్రాణశక్తి, ఆత్మ, అహం, సంకల్పశక్తి, నాయకత్వం, ప్రభుత్వం, తండ్రి ప్రభావం.",
        },
        "remedies": {
            "en": "Offer water to the rising Sun (Surya Arghya), chant the Aditya Hridayam and practise honesty and discipline.",
            "hi": "उगते सूर्य को अर्घ्य दें, आदित्य हृदय का पाठ करें और सत्य व अनुशासन का पालन करें।",
            "te": "ఉదయించే సూర్యునికి అర్ఘ్యం ఇవ్వండి, ఆదిత్య హృదయం పఠించండి, నిజాయితీ, క్రమశిక్షణ పాటించండి.",
        },
    },
    "Moon": {
        "karaka": "mind, mother, emotions",
        "significations": {
            "en": "Emotions, mind, nurturing, memory, the public, water and maternal influence.",
            "hi": "भावनाएँ, मन, पोषण, स्मृति, जनता, जल और मातृ-प्रभाव।",
            "te": "భావోద్వేగాలు, మనసు, పోషణ, జ్ఞాపకశక్తి, ప్రజలు, నీరు, తల్లి ప్రభావం.",
        },
        "remedies": {
            "en": "Respect and care for the mother, chant to Chandra or Shiva and keep a calm, regular routine.",
            "hi": "माता का आदर व देखभाल करें, चंद्र या शिव का जप करें और शांत, नियमित दिनचर्या रखें।",
            "te": "తల్లిని గౌరవించి సంరక్షించండి, చంద్ర లేదా శివ జపం చేయండి, ప్రశాంత, క్రమమైన దినచర్య పాటించండి.",
        },
    },
    "Mars": {
        "karaka": "energy, siblings, courage",
        "significations": {
            "en": "Drive, courage, action, competition, land, brothers and physical strength.",
            "hi": "उत्साह, साहस, क्रिया, प्रतिस्पर्धा, भूमि, भाई और शारीरिक बल।",
            "te": "శక్తి, ధైర్యం, చర్య, పోటీ, భూమి, సోదరులు, శారీరక బలం.",
        },
        "remedies": {
            "en": "Channel energy into exercise or service, chant the Hanuman Chalisa and practise patience.",
            "hi": "ऊर्जा को व्यायाम या सेवा में लगाएँ, हनुमान चालीसा का पाठ करें और धैर्य रखें।",
            "te": "శక్తిని వ్యాయామం లేదా సేవలో వినియోగించండి, హనుమాన్ చాలీసా పఠించండి, ఓర్పు పాటించండి.",
        },
    },
    "Mercury": {
        "karaka": "intellect, communication, speech",
        "significations": {
            "en": "Intelligence, speech, learning, commerce, writing, logic and adaptability.",
            "hi": "बुद्धि, वाणी, अध्ययन, वाणिज्य, लेखन, तर्क और अनुकूलनशीलता।",
            "te": "బుద్ధి, వాక్కు, విద్య, వాణిజ్యం, రచన, తర్కం, అనుకూలత.",
        },
        "remedies": {
            "en": "Study, engage in honest communication, chant to Vishnu or Budha and support education.",
            "hi": "अध्ययन करें, सत्य संवाद करें, विष्णु या बुध का जप करें और शिक्षा का सहयोग करें।",
            "te": "అధ్యయనం చేయండి, నిజాయితీగా మాట్లాడండి, విష్ణు లేదా బుధ జపం చేయండి, విద్యకు మద్దతివ్వండి.",
        },
    },
    "Jupiter": {
        "karaka": "wisdom, children, wealth (guru)",
        "significations": {
            "en": "Wisdom, knowledge, dharma, teachers, children, prosperity and good fortune.",
            "hi": "ज्ञान, विद्या, धर्म, गुरु, संतान, समृद्धि और सौभाग्य।",
            "te": "జ్ఞానం, విద్య, ధర్మం, గురువులు, సంతానం, సమృద్ధి, అదృష్టం.",
        },
        "remedies": {
            "en": "Study scripture, respect teachers and elders, chant to Brihaspati and give to education or charity.",
            "hi": "शास्त्र-अध्ययन करें, गुरु व बड़ों का आदर करें, बृहस्पति का जप करें और शिक्षा या दान में दें।",
            "te": "శాస్త్ర అధ్యయనం చేయండి, గురువులను, పెద్దలను గౌరవించండి, బృహస్పతి జపం చేయండి, విద్య లేదా దానం చేయండి.",
        },
    },
    "Venus": {
        "karaka": "love, spouse, luxury",
        "significations": {
            "en": "Love, relationships, beauty, art, comfort, vehicles and refined pleasures.",
            "hi": "प्रेम, संबंध, सौंदर्य, कला, सुख, वाहन और परिष्कृत आनंद।",
            "te": "ప్రేమ, సంబంధాలు, సౌందర్యం, కళ, సౌకర్యం, వాహనాలు, శుద్ధ ఆనందాలు.",
        },
        "remedies": {
            "en": "Cultivate art and beauty, treat partners with respect, chant to Shukra and value harmony.",
            "hi": "कला व सौंदर्य को अपनाएँ, साथी का सम्मान करें, शुक्र का जप करें और सामंजस्य को महत्व दें।",
            "te": "కళ, సౌందర్యాన్ని పెంపొందించండి, భాగస్వాములను గౌరవించండి, శుక్ర జపం చేయండి, సామరస్యానికి విలువనివ్వండి.",
        },
    },
    "Saturn": {
        "karaka": "discipline, longevity, karma",
        "significations": {
            "en": "Discipline, hard work, patience, responsibility, longevity, service and lessons of time.",
            "hi": "अनुशासन, कठिन परिश्रम, धैर्य, उत्तरदायित्व, आयु, सेवा और समय के पाठ।",
            "te": "క్రమశిక్షణ, కష్టపడే తత్వం, ఓర్పు, బాధ్యత, ఆయుష్షు, సేవ, కాల పాఠాలు.",
        },
        "remedies": {
            "en": "Serve the elderly and needy, work diligently, chant to Shani or Hanuman and honour commitments.",
            "hi": "बुजुर्गों व जरूरतमंदों की सेवा करें, परिश्रम करें, शनि या हनुमान का जप करें और वचन निभाएँ।",
            "te": "వృద్ధులకు, అవసరమైనవారికి సేవ చేయండి, శ్రద్ధగా పని చేయండి, శని లేదా హనుమాన్ జపం చేయండి, మాట నిలబెట్టుకోండి.",
        },
    },
    "Rahu": {
        "karaka": "worldly desire, foreign, ambition",
        "significations": {
            "en": "Ambition, obsession, innovation, foreign lands, technology and unconventional paths.",
            "hi": "महत्वाकांक्षा, आसक्ति, नवाचार, विदेश, प्रौद्योगिकी और अपरंपरागत मार्ग।",
            "te": "ఆశయం, తీవ్రాసక్తి, నవకల్పన, విదేశాలు, సాంకేతికత, అసాధారణ మార్గాలు.",
        },
        "remedies": {
            "en": "Stay grounded, avoid shortcuts, chant to Durga and practise clarity and moderation.",
            "hi": "स्थिर रहें, शॉर्टकट से बचें, दुर्गा का जप करें और स्पष्टता व संयम रखें।",
            "te": "నేలపై నిలబడండి, అడ్డదారులు వద్దు, దుర్గా జపం చేయండి, స్పష్టత, మితత్వం పాటించండి.",
        },
    },
    "Ketu": {
        "karaka": "spirituality, moksha, detachment",
        "significations": {
            "en": "Detachment, liberation, intuition, past-life skills, research and spiritual insight.",
            "hi": "वैराग्य, मोक्ष, अंतर्ज्ञान, पूर्वजन्म-कौशल, अनुसंधान और आध्यात्मिक अंतर्दृष्टि।",
            "te": "వైరాగ్యం, మోక్షం, అంతర్జ్ఞానం, పూర్వజన్మ నైపుణ్యాలు, పరిశోధన, ఆధ్యాత్మిక దృష్టి.",
        },
        "remedies": {
            "en": "Practise meditation and simplicity, chant to Ganesha and pursue inner, non-material goals.",
            "hi": "ध्यान व सादगी अपनाएँ, गणेश का जप करें और आंतरिक, अभौतिक लक्ष्यों का अनुसरण करें।",
            "te": "ధ్యానం, సరళత పాటించండి, గణేశ జపం చేయండి, అంతర్గత, అభౌతిక లక్ష్యాలను అనుసరించండి.",
        },
    },
}

# ---------------------------------------------------------------------------
# 12 Bhavas (houses)
# ---------------------------------------------------------------------------
# name: classical Sanskrit house name; themes: core significations of the bhava

BHAVA_KB = {
    1: {
        "name": "Tanu",
        "themes": {
            "en": "Self, body, appearance, personality, vitality and the overall life direction.",
            "hi": "स्वयं, शरीर, रूप, व्यक्तित्व, जीवनशक्ति और जीवन की समग्र दिशा।",
            "te": "స్వయం, శరీరం, రూపం, వ్యక్తిత్వం, ప్రాణశక్తి, జీవిత దిశ.",
        },
    },
    2: {
        "name": "Dhana",
        "themes": {
            "en": "Wealth, family, speech, food, early upbringing and accumulated resources.",
            "hi": "धन, परिवार, वाणी, भोजन, प्रारंभिक परवरिश और संचित संसाधन।",
            "te": "సంపద, కుటుంబం, వాక్కు, ఆహారం, బాల్య పెంపకం, కూడబెట్టిన వనరులు.",
        },
    },
    3: {
        "name": "Sahaja",
        "themes": {
            "en": "Siblings, courage, effort, communication, short journeys and skills.",
            "hi": "भाई-बहन, साहस, प्रयास, संचार, छोटी यात्राएँ और कौशल।",
            "te": "సోదరులు, ధైర్యం, కృషి, సంభాషణ, చిన్న ప్రయాణాలు, నైపుణ్యాలు.",
        },
    },
    4: {
        "name": "Bandhu (Sukha)",
        "themes": {
            "en": "Home, mother, happiness, property, land, vehicles and inner comfort.",
            "hi": "घर, माता, सुख, संपत्ति, भूमि, वाहन और आंतरिक शांति।",
            "te": "ఇల్లు, తల్లి, సుఖం, ఆస్తి, భూమి, వాహనాలు, అంతర్గత శాంతి.",
        },
    },
    5: {
        "name": "Putra",
        "themes": {
            "en": "Children, creativity, intelligence, romance, past-life merit and speculation.",
            "hi": "संतान, रचनात्मकता, बुद्धि, प्रेम, पूर्वजन्म-पुण्य और सट्टा।",
            "te": "సంతానం, సృజనాత్మకత, బుద్ధి, ప్రేమ, పూర్వజన్మ పుణ్యం, ఊహాగానాలు.",
        },
    },
    6: {
        "name": "Ari (Ripu)",
        "themes": {
            "en": "Health challenges, enemies, debts, daily work, service and overcoming obstacles.",
            "hi": "स्वास्थ्य-चुनौतियाँ, शत्रु, ऋण, दैनिक कार्य, सेवा और बाधाओं पर विजय।",
            "te": "ఆరోగ్య సవాళ్లు, శత్రువులు, రుణాలు, రోజువారీ పని, సేవ, అడ్డంకులను అధిగమించడం.",
        },
    },
    7: {
        "name": "Yuvati (Kalatra)",
        "themes": {
            "en": "Marriage, spouse, partnerships, business alliances and one-to-one relationships.",
            "hi": "विवाह, जीवनसाथी, साझेदारी, व्यापारिक गठबंधन और आमने-सामने के संबंध।",
            "te": "వివాహం, జీవిత భాగస్వామి, భాగస్వామ్యాలు, వ్యాపార పొత్తులు, వ్యక్తిగత సంబంధాలు.",
        },
    },
    8: {
        "name": "Randhra (Ayu)",
        "themes": {
            "en": "Longevity, transformation, inheritance, hidden matters, research and deep change.",
            "hi": "आयु, परिवर्तन, विरासत, गुप्त विषय, अनुसंधान और गहन परिवर्तन।",
            "te": "ఆయుష్షు, పరివర్తన, వారసత్వం, రహస్య విషయాలు, పరిశోధన, లోతైన మార్పు.",
        },
    },
    9: {
        "name": "Dharma (Bhagya)",
        "themes": {
            "en": "Fortune, dharma, higher wisdom, guru, father, pilgrimage and long journeys.",
            "hi": "भाग्य, धर्म, उच्च ज्ञान, गुरु, पिता, तीर्थ और लंबी यात्राएँ।",
            "te": "అదృష్టం, ధర్మం, ఉన్నత జ్ఞానం, గురువు, తండ్రి, తీర్థయాత్ర, దూర ప్రయాణాలు.",
        },
    },
    10: {
        "name": "Karma",
        "themes": {
            "en": "Career, status, reputation, authority, public life and worldly achievement.",
            "hi": "करियर, प्रतिष्ठा, यश, अधिकार, सार्वजनिक जीवन और सांसारिक उपलब्धि।",
            "te": "వృత్తి, హోదా, కీర్తి, అధికారం, ప్రజా జీవితం, లౌకిక సాధన.",
        },
    },
    11: {
        "name": "Labha",
        "themes": {
            "en": "Gains, income, aspirations, friends, networks and fulfilment of desires.",
            "hi": "लाभ, आय, आकांक्षाएँ, मित्र, संपर्क और इच्छाओं की पूर्ति।",
            "te": "లాభాలు, ఆదాయం, ఆకాంక్షలు, స్నేహితులు, నెట్‌వర్క్‌లు, కోరికల నెరవేర్పు.",
        },
    },
    12: {
        "name": "Vyaya",
        "themes": {
            "en": "Expenditure, loss, foreign lands, solitude, spirituality and liberation (moksha).",
            "hi": "व्यय, हानि, विदेश, एकांत, आध्यात्म और मोक्ष।",
            "te": "ఖర్చు, నష్టం, విదేశాలు, ఏకాంతం, ఆధ్యాత్మికత, మోక్షం.",
        },
    },
}

# ---------------------------------------------------------------------------
# Vimsottari Mahadasha general effects (per dasha lord)
# ---------------------------------------------------------------------------
# General, non-fear-based tendencies of each planetary period. Actual results
# depend on the planet's strength, dignity, house and aspects in the chart.

DASHA_KB = {
    "Sun": {
        "effect": {
            "en": "A 6-year period favouring authority, recognition, self-confidence and dealings with government or father; a time to lead with integrity.",
            "hi": "6-वर्ष की अवधि जो अधिकार, मान्यता, आत्मविश्वास और सरकार या पिता से संबंध के अनुकूल है; सत्यनिष्ठा से नेतृत्व का समय।",
            "te": "6 సంవత్సరాల కాలం; అధికారం, గుర్తింపు, ఆత్మవిశ్వాసం, ప్రభుత్వం లేదా తండ్రితో వ్యవహారాలకు అనుకూలం; నిజాయితీతో నాయకత్వం వహించే సమయం.",
        },
    },
    "Moon": {
        "effect": {
            "en": "A 10-year period emphasising emotions, home, mother, public life and mental well-being; nurturing and relationships come to the fore.",
            "hi": "10-वर्ष की अवधि जो भावनाओं, घर, माता, सार्वजनिक जीवन और मानसिक कल्याण पर बल देती है; पोषण और संबंध प्रमुख होते हैं।",
            "te": "10 సంవత్సరాల కాలం; భావోద్వేగాలు, ఇల్లు, తల్లి, ప్రజా జీవితం, మానసిక శ్రేయస్సుపై దృష్టి; పోషణ, సంబంధాలు ప్రధానమవుతాయి.",
        },
    },
    "Mars": {
        "effect": {
            "en": "A 7-year period of energy, courage, initiative and action; good for property and competition when channelled with patience.",
            "hi": "7-वर्ष की अवधि जो ऊर्जा, साहस, पहल और क्रिया की है; धैर्य से संचालित होने पर संपत्ति और प्रतिस्पर्धा के लिए शुभ।",
            "te": "7 సంవత్సరాల కాలం; శక్తి, ధైర్యం, చొరవ, చర్య; ఓర్పుతో వినియోగిస్తే ఆస్తి, పోటీకి అనుకూలం.",
        },
    },
    "Mercury": {
        "effect": {
            "en": "A 17-year period favouring intellect, learning, communication, commerce and skilful work; strong for study and business.",
            "hi": "17-वर्ष की अवधि जो बुद्धि, अध्ययन, संचार, वाणिज्य और कुशल कार्य के अनुकूल है; अध्ययन और व्यापार के लिए प्रबल।",
            "te": "17 సంవత్సరాల కాలం; బుద్ధి, విద్య, సంభాషణ, వాణిజ్యం, నైపుణ్య పనికి అనుకూలం; అధ్యయనం, వ్యాపారానికి బలం.",
        },
    },
    "Jupiter": {
        "effect": {
            "en": "A 16-year period of wisdom, growth, prosperity, learning and good fortune; supportive of children, teaching and dharma.",
            "hi": "16-वर्ष की अवधि जो ज्ञान, वृद्धि, समृद्धि, विद्या और सौभाग्य की है; संतान, शिक्षण और धर्म के लिए सहायक।",
            "te": "16 సంవత్సరాల కాలం; జ్ఞానం, ఎదుగుదల, సమృద్ధి, విద్య, అదృష్టం; సంతానం, బోధన, ధర్మానికి మద్దతు.",
        },
    },
    "Venus": {
        "effect": {
            "en": "A 20-year period, the longest, favouring love, comfort, art, relationships and material enjoyment; harmony and creativity flourish.",
            "hi": "20-वर्ष की सबसे लंबी अवधि जो प्रेम, सुख, कला, संबंध और भौतिक आनंद के अनुकूल है; सामंजस्य और रचनात्मकता फलती है।",
            "te": "20 సంవత్సరాల అత్యంత దీర్ఘకాలం; ప్రేమ, సౌకర్యం, కళ, సంబంధాలు, భౌతిక ఆనందానికి అనుకూలం; సామరస్యం, సృజనాత్మకత వర్ధిల్లుతాయి.",
        },
    },
    "Saturn": {
        "effect": {
            "en": "A 19-year period of discipline, hard work, patience and maturity; rewards steady effort and responsibility over time.",
            "hi": "19-वर्ष की अवधि जो अनुशासन, कठिन परिश्रम, धैर्य और परिपक्वता की है; समय के साथ स्थिर प्रयास और उत्तरदायित्व को फल देती है।",
            "te": "19 సంవత్సరాల కాలం; క్రమశిక్షణ, కష్టపడే తత్వం, ఓర్పు, పరిపక్వత; కాలక్రమేణా స్థిర కృషి, బాధ్యతకు ఫలితమిస్తుంది.",
        },
    },
    "Rahu": {
        "effect": {
            "en": "An 18-year period of ambition, change, foreign connections and unconventional growth; brings sudden gains when balanced with clarity.",
            "hi": "18-वर्ष की अवधि जो महत्वाकांक्षा, परिवर्तन, विदेश-संबंध और अपरंपरागत वृद्धि की है; स्पष्टता के संतुलन से आकस्मिक लाभ लाती है।",
            "te": "18 సంవత్సరాల కాలం; ఆశయం, మార్పు, విదేశీ సంబంధాలు, అసాధారణ ఎదుగుదల; స్పష్టతతో సమతుల్యం చేస్తే ఆకస్మిక లాభాలు.",
        },
    },
    "Ketu": {
        "effect": {
            "en": "A 7-year period of detachment, introspection, spirituality and research; supports inner growth and letting go of the non-essential.",
            "hi": "7-वर्ष की अवधि जो वैराग्य, आत्मनिरीक्षण, आध्यात्म और अनुसंधान की है; आंतरिक विकास और अनावश्यक को त्यागने में सहायक।",
            "te": "7 సంవత్సరాల కాలం; వైరాగ్యం, ఆత్మపరిశీలన, ఆధ్యాత్మికత, పరిశోధన; అంతర్గత ఎదుగుదల, అనవసరమైనదాన్ని వదిలివేయడానికి మద్దతు.",
        },
    },
}

# ---------------------------------------------------------------------------
# Sources actually consulted (see docs/SOURCES.md for detail and confidence)
# ---------------------------------------------------------------------------
SOURCES = [
    "Brihat Parashara Hora Shastra (BPHS)",
    "Phaladeepika (Mantreswara)",
    "Saravali (Kalyana Varma)",
    "Brihat Jataka (Varahamihira)",
    "AstroSage (astrosage.com)",
    "Drik Panchang (drikpanchang.com)",
    "Prokerala (prokerala.com)",
    "Wikipedia (Nakshatra, Rashi and Navagraha articles)",
]
