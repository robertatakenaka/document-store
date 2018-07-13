import unittest
from copy import deepcopy

from multiverse import domain

SAMPLE_MANIFEST = {
    "id": "0034-8910-rsp-48-2-0275",
    "versions": [
        {
            "data": "/rawfiles/7ca9f9b2687cb/0034-8910-rsp-48-2-0275.xml",
            "assets": {
                "0034-8910-rsp-48-2-0275-gf01.gif": [
                    "/rawfiles/8e644999a8fa4/0034-8910-rsp-48-2-0275-gf01.gif",
                    "/rawfiles/bf139b9aa3066/0034-8910-rsp-48-2-0275-gf01.gif",
                ]
            },
        },
        {
            "data": "/rawfiles/2d3ad9c6bc656/0034-8910-rsp-48-2-0275.xml",
            "assets": {
                "0034-8910-rsp-48-2-0275-gf01.gif": [
                    "/rawfiles/bf139b9aa3066/0034-8910-rsp-48-2-0275-gf01.gif"
                ]
            },
        },
    ],
}


class ArticleTests(unittest.TestCase):
    def make_one(self):
        _manifest = deepcopy(SAMPLE_MANIFEST)
        return domain.Article(manifest=_manifest)

    def test_manifest_is_generated_on_init(self):
        article = domain.Article(doc_id="0034-8910-rsp-48-2-0275")
        self.assertTrue(isinstance(article.manifest, dict))

    def test_manifest_as_arg_on_init(self):
        existing_manifest = {"id": "0034-8910-rsp-48-2-0275", "versions": []}
        article = domain.Article(manifest=existing_manifest)
        self.assertEqual(existing_manifest, article.manifest)

    def test_manifest_with_unknown_schema_is_allowed(self):
        existing_manifest = {"versions": []}
        article = domain.Article(manifest=existing_manifest)
        self.assertEqual(existing_manifest, article.manifest)

    def test_missing_doc_id_return_empty_string(self):
        existing_manifest = {"versions": []}
        article = domain.Article(manifest=existing_manifest)
        self.assertEqual(article.doc_id(), "")

    def test_doc_id(self):
        article = domain.Article(doc_id="0034-8910-rsp-48-2-0275")
        self.assertEqual(article.doc_id(), "0034-8910-rsp-48-2-0275")

    def test_new_version_of_data(self):
        article = self.make_one()
        self.assertEqual(len(article.manifest["versions"]), 2)

        article.new_version(
            "/rawfiles/5e3ad9c6cd6b8/0034-8910-rsp-48-2-0275.xml",
            assets_getter=lambda data_url, timeout: (None, []),
        )
        self.assertEqual(len(article.manifest["versions"]), 3)

    def test_get_latest_version(self):
        article = self.make_one()
        latest = article.version()
        self.assertEqual(
            latest["data"], "/rawfiles/2d3ad9c6bc656/0034-8910-rsp-48-2-0275.xml"
        )

    def test_get_oldest_version(self):
        article = self.make_one()
        oldest = article.version(0)
        self.assertEqual(
            oldest["data"], "/rawfiles/7ca9f9b2687cb/0034-8910-rsp-48-2-0275.xml"
        )

    def test_version_only_shows_newest_assets(self):
        article = self.make_one()
        oldest = article.version(0)
        expected = {
            "data": "/rawfiles/7ca9f9b2687cb/0034-8910-rsp-48-2-0275.xml",
            "assets": {
                "0034-8910-rsp-48-2-0275-gf01.gif": "/rawfiles/bf139b9aa3066/0034-8910-rsp-48-2-0275-gf01.gif"
            },
        }
        self.assertEqual(oldest, expected)