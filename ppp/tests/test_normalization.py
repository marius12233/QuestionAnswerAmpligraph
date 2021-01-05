import json

from ppp_questionparsing_grammatical import computeTree, simplify, DependenciesTree,\
    QuotationHandler, normalFormProduction, GrammaticalError, NamedEntityMerging, PrepositionMerging
import data

from unittest import TestCase

class StandardTripleTests(TestCase):

    def testAndnormalFormProduction(self):
        tree = computeTree(data.give_chief())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": [
        {
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "chief"
            },
            "object": {
                "type": "missing"
            },
            "predicate": {
                "list": [
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ],
                "type": "list"
            }
        },
        {
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "prime minister"
            },
            "object": {
                "type": "missing"
            },
            "predicate": {
                "list": [
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ],
                "type": "list"
            }
        }
    ],
    "type": "intersection"
})

    def testSuperlativenormalFormProduction(self):
        tree = computeTree(data.give_opera())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": [
        {
            "list": {
                "predicate": {
                    "value": "default",
                    "type": "resource"
                },
                "list": {
                    "value": "Gilbert",
                    "type": "resource"
                },
                "type": "sort"
            },
            "index": 0,
            "type": "nth"
        },
        {
            "list": {
                "predicate": {
                    "value": "default",
                    "type": "resource"
                },
                "list": {
                    "value": "Sullivan opera",
                    "type": "resource"
                },
                "type": "sort"
            },
            "index": 0,
            "type": "nth"
        }
    ],
    "type": "intersection"
})

    def testnormalFormProduction1(self):
        tree = computeTree(data.give_president_of_USA())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "object": {
        "type": "missing"
    },
    "subject": {
        "type": "resource",
        "value": "United States"
    },
    "predicate": {
        "type": "resource",
        "value": "president"
    },
    "type": "triple"
})

    def testnormalFormProduction2(self):
        handler = QuotationHandler('foo')
        sentence = 'Who wrote "Lucy in the Sky with Diamonds" and "Let It Be"?'
        nonAmbiguousSentence = handler.pull(sentence)
        result=data.give_LSD_LIB()
        tree=computeTree(result)
        handler.push(tree)
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": [
        {
            "inverse-predicate": {
                "list": [
                    {
                        "value": "author",
                        "type": "resource"
                    },
                    {
                        "value": "writer",
                        "type": "resource"
                    }
                ],
                "type": "list"
            },
            "subject": {
                "type": "missing"
            },
            "object": {
                "value": "Lucy in the Sky with Diamonds",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "list": [
                    {
                        "value": "written",
                        "type": "resource"
                    },
                    {
                        "value": "literary works",
                        "type": "resource"
                    },
                    {
                        "value": "bibliography",
                        "type": "resource"
                    },
                    {
                        "value": "notable work",
                        "type": "resource"
                    }
                ],
                "type": "list"
            }
        },
        {
            "inverse-predicate": {
                "list": [
                    {
                        "value": "author",
                        "type": "resource"
                    },
                    {
                        "value": "writer",
                        "type": "resource"
                    }
                ],
                "type": "list"
            },
            "subject": {
                "type": "missing"
            },
            "object": {
                "value": "Let It Be",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "list": [
                    {
                        "value": "written",
                        "type": "resource"
                    },
                    {
                        "value": "literary works",
                        "type": "resource"
                    },
                    {
                        "value": "bibliography",
                        "type": "resource"
                    },
                    {
                        "value": "notable work",
                        "type": "resource"
                    }
                ],
                "type": "list"
            }
        }
    ],
    "type": "intersection"
})

    def testnormalFormProduction3(self):
        tree = computeTree(data.give_obama_president_usa())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "type": "intersection",
    "list": [
        {
            "predicate": {
                "type": "list",
                "list": [
                    {
                        "type": "resource",
                        "value": "been"
                    },
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ]
            },
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "Obama"
            },
            "inverse-predicate": {
                "type": "resource",
                "value": "identity"
            },
            "object": {
                "type": "missing"
            }
        },
        {
            "predicate": {
                "type": "list",
                "list": [
                    {
                        "type": "resource",
                        "value": "been"
                    },
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ]
            },
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "United States president"
            },
            "inverse-predicate": {
                "type": "resource",
                "value": "identity"
            },
            "object": {
                "type": "missing"
            }
        }
    ]
})

    def testnormalFormProductionR8(self):
        tree = computeTree(data.mistake())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "type": "triple",
    "subject": {
        "type": "resource",
        "value": "mistake"
    },
    "object": {
        "type": "missing"
    },
    "predicate": {
        "type": "list",
        "list": [
            {
                "type": "resource",
                "value": "place"
            },
            {
                "type": "resource",
                "value": "location"
            },
            {
                "type": "resource",
                "value": "residence"
            },
            {
                "type": "resource",
                "value": "country"
            },
            {
                "type": "resource",
                "value": "city"
            },
            {
                "type": "resource",
                "value": "town"
            },
            {
                "type": "resource",
                "value": "state"
            },
            {
                "type": "resource",
                "value": "locality"
            }
        ]
    }
})


    def testnormalFormProductionSuperl(self):
        tree = computeTree(data.tanzania())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": {
        "list": {
            "object": {
                "type": "missing"
            },
            "predicate": {
                "value": "mountain",
                "type": "resource"
            },
            "subject": {
                "value": "Tanzania",
                "type": "resource"
            },
            "type": "triple"
        },
        "predicate": {
                    "value" : "height",
                    "type"  : "resource"
                },
        "type": "sort"
    },
    "index": -1,
    "type": "nth"
})

    def testnormalFormProductionSuperl2(self):
        tree = computeTree(data.car())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": {
        "list": {
            "subject": {
                "value": "world",
                "type": "resource"
            },
            "predicate": {
                "value": "car",
                "type": "resource"
            },
            "object": {
                "type": "missing"
            },
            "type": "triple"
        },
        "predicate": {
                    "value" : "cost",
                    "type"  : "resource"
                },
        "type": "sort"
    },
    "index": -1,
    "type": "nth"
})

    def testCop(self):
        tree = computeTree(data.black())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        self.assertRaises(GrammaticalError, lambda: simplify(tree))

    def testExists(self):
        tree = computeTree(data.king_england())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": {
        "predicate": {
            "type": "resource",
            "value": "king"
        },
        "subject": {
            "type": "resource",
            "value": "England"
        },
        "type": "triple",
        "object": {
            "type": "missing"
        }
    },
    "type": "exists"
})

    def testSemiQuestionWord1(self):
        tree = computeTree(data.roald())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "subject": {
        "value": "Roald Dahl",
        "type": "resource"
    },
    "type": "triple",
    "predicate": {
        "value": "book",
        "type": "resource"
    },
    "object": {
        "type": "missing"
    }
})

    def testSemiQuestionWord3(self):
        tree = computeTree(data.list_president2())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "type": "triple",
    "object": {
        "type": "missing"
    },
    "predicate": {
        "type": "resource",
        "value": "president"
    },
    "subject": {
        "type": "resource",
        "value": "France"
    }
})

    def testSemiQuestionWord4(self):
        tree = computeTree(data.capital1())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "predicate": {
        "type": "resource",
        "value": "capital"
    },
    "type": "triple",
    "subject": {
        "type": "resource",
        "value": "France"
    },
    "object": {
        "type": "missing"
    }
})

    def testSemiQuestionWord5(self):
        tree = computeTree(data.capital2())
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "predicate": {
        "type": "resource",
        "value": "capital"
    },
    "type": "triple",
    "subject": {
        "type": "resource",
        "value": "France"
    },
    "object": {
        "type": "missing"
    }
})
