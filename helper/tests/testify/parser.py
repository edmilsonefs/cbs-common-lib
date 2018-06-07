import unittest

from helper.testify import parser


class ParserTest(unittest.TestCase):
    mock_response = '{"AA Secure Omniture": [[{"status": "Fail", "required": "cbsicbsapp", "Name": "c. ' \
                    'sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], [{"status": "Fail", ' \
                    '"required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": ' \
                    '"Fail", "required": "/livetv/check availability", "Name": "pageName", "value": "CBS 4.8.5 (' \
                    '1648548)"}], [{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
                    '"value": "front_door"}, {"status": "Fail", "required": "/livetv/check availability", "Name": "c. ' \
                    'screenName", "value": "/"}, {"status": "Fail", "required": "livetv|upsell|check availability", ' \
                    '"Name": "c. siteHier", "value": "splash"}, {"status": "Fail", "required": "cbsicbsapp", ' \
                    '"Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": ' \
                    '"/livetv/check availability", "Name": "pageName", "value": "/"}], [{"status": "Fail", ' \
                    '"required": "livetv_available", "Name": "c. pageType", "value": "front_door"}, {"status": ' \
                    '"Fail", "required": "/livetv/check availability", "Name": "c. screenName", "value": "/"}, ' \
                    '{"status": "Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", ' \
                    '"value": "splash"}, {"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
                    '"value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], [{"status": "Fail", "required": ' \
                    '"livetv_available", "Name": "c. pageType", "value": "menu"}, {"status": "Fail", "required": ' \
                    '"/livetv/check availability", "Name": "c. screenName", "value": "/menu/home"}, {"status": ' \
                    '"Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", ' \
                    '"value": "menu|home"}, {"status": "Fail", "required": "cbsicbsapp", "Name": "c. ' \
                    'sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], [{"status": "Fail", ' \
                    '"required": "livetv_available", "Name": "c. pageType", "value": "front_door"}, {"status": ' \
                    '"Fail", "required": "/livetv/check availability", "Name": "c. screenName", "value": "/"}, ' \
                    '{"status": "Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", ' \
                    '"value": "home"}, {"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
                    '"value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "pageName", "value": "/"}], [{"status": "Fail", "required": "livetv_available", ' \
                    '"Name": "c. pageType", "value": "front_door"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "c. screenName", "value": "/"}, {"status": "Fail", "required": ' \
                    '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "home"}, {"status": "Fail", ' \
                    '"required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": ' \
                    '"Fail", "required": "/livetv/check availability", "Name": "pageName", "value": "/"}], ' \
                    '[{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", "value": "menu"}, ' \
                    '{"status": "Fail", "required": "/livetv/check availability", "Name": "c. screenName", ' \
                    '"value": "/menu/"}, {"status": "Fail", "required": "livetv|upsell|check availability", ' \
                    '"Name": "c. siteHier", "value": "menu|"}, {"status": "Fail", "required": "cbsicbsapp", ' \
                    '"Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": ' \
                    '"/livetv/check availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], [{"status": ' \
                    '"Fail", "required": "livetv_available", "Name": "c. pageType", "value": "settings"}, {"status": ' \
                    '"Fail", "required": "/livetv/check availability", "Name": "c. screenName", ' \
                    '"value": "/settings/"}, {"status": "Fail", "required": "livetv|upsell|check availability", ' \
                    '"Name": "c. siteHier", "value": "other|other|settings|home"}, {"status": "Fail", "required": ' \
                    '"cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", ' \
                    '"required": "/livetv/check availability", "Name": "pageName", "value": "/settings/"}], ' \
                    '[{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", "value": "settings"}, ' \
                    '{"status": "Fail", "required": "/livetv/check availability", "Name": "c. screenName", ' \
                    '"value": "/settings/"}, {"status": "Fail", "required": "livetv|upsell|check availability", ' \
                    '"Name": "c. siteHier", "value": "other|other|settings|home"}, {"status": "Fail", "required": ' \
                    '"cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", ' \
                    '"required": "/livetv/check availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], ' \
                    '[{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
                    '"value": "svod_upsell"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "c. screenName", "value": "/all access/upsell"}, {"status": "Fail", "required": ' \
                    '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "all access|upsell"}, ' \
                    '{"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
                    '"value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "pageName", "value": "/all access/upsell"}], [{"status": "Fail", "required": ' \
                    '"livetv_available", "Name": "c. pageType", "value": "front_door"}, {"status": "Fail", ' \
                    '"required": "/livetv/check availability", "Name": "c. screenName", "value": "/"}, {"status": ' \
                    '"Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", "value": "home"}, ' \
                    '{"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
                    '"value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "pageName", "value": "/"}], [{"status": "Fail", "required": "livetv_available", ' \
                    '"Name": "c. pageType", "value": "menu"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "c. screenName", "value": "/menu/"}, {"status": "Fail", "required": ' \
                    '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "menu|"}, {"status": "Fail", ' \
                    '"required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": ' \
                    '"Fail", "required": "/livetv/check availability", "Name": "pageName", "value": "CBS 4.8.5 (' \
                    '1648548)"}], [{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
                    '"value": "accounts_login"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "c. screenName", "value": "/accounts/login"}, {"status": "Fail", "required": ' \
                    '"livetv|upsell|check availability", "Name": "c. siteHier", "value": ' \
                    '"other|other|accounts|login"}, {"status": "Fail", "required": "cbsicbsapp", "Name": "c. ' \
                    'sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "pageName", "value": "/accounts/login"}], [{"status": "Fail", "required": ' \
                    '"livetv_available", "Name": "c. pageType", "value": "accounts_login"}, {"status": "Fail", ' \
                    '"required": "/livetv/check availability", "Name": "c. screenName", "value": "/login"}, ' \
                    '{"status": "Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", ' \
                    '"value": "other|other|accounts|login"}, {"status": "Fail", "required": "cbsicbsapp", "Name": "c. ' \
                    'sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], [{"status": "Fail", ' \
                    '"required": "livetv_available", "Name": "c. pageType", "value": "front_door"}, {"status": ' \
                    '"Fail", "required": "/livetv/check availability", "Name": "c. screenName", "value": "/"}, ' \
                    '{"status": "Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", ' \
                    '"value": "home"}, {"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
                    '"value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "pageName", "value": "/"}], [{"status": "Fail", "required": "livetv_available", ' \
                    '"Name": "c. pageType", "value": "menu"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "c. screenName", "value": "/menu/live tv"}, {"status": "Fail", ' \
                    '"required": "livetv|upsell|check availability", "Name": "c. siteHier", "value": "menu|live tv"}, ' \
                    '{"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
                    '"value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], [{"status": "Fail", "required": ' \
                    '"livetv_available", "Name": "c. pageType", "value": "menu"}, {"status": "Fail", "required": ' \
                    '"/livetv/check availability", "Name": "c. screenName", "value": "/menu/live tv"}, {"status": ' \
                    '"Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", ' \
                    '"value": "menu|live tv"}, {"status": "Fail", "required": "cbsicbsapp", "Name": "c. ' \
                    'sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": "/livetv/check ' \
                    'availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], [{"status": "Fail", ' \
                    '"required": "livetv_available", "Name": "c. pageType", "value": "livetv_availability"}, ' \
                    '{"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
                    '"value": "cnetcbscomsite"}], [{"status": "Fail", "required": "livetv_available", "Name": "c. ' \
                    'pageType", "value": "livetv"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "c. screenName", "value": "/livetv/"}, {"status": "Fail", "required": ' \
                    '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "livetv"}, {"status": ' \
                    '"Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, ' \
                    '{"status": "Fail", "required": "/livetv/check availability", "Name": "pageName", ' \
                    '"value": "/livetv/"}], [{"status": "Fail", "required": "livetv_available", "Name": "c. ' \
                    'pageType", "value": "livetv"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "c. screenName", "value": "/livetv/"}, {"status": "Fail", "required": ' \
                    '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "livetv"}, {"status": ' \
                    '"Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, ' \
                    '{"status": "Fail", "required": "/livetv/check availability", "Name": "pageName", ' \
                    '"value": "/livetv/"}], [{"status": "Fail", "required": "livetv_available", "Name": "c. ' \
                    'pageType", "value": "livetv"}, {"status": "Fail", "required": "/livetv/check availability", ' \
                    '"Name": "c. screenName", "value": "/livetv/"}, {"status": "Fail", "required": ' \
                    '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "livetv"}, {"status": ' \
                    '"Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, ' \
                    '{"status": "Fail", "required": "/livetv/check availability", "Name": "pageName", "value": "CBS ' \
                    '4.8.5 (1648548)"}], [{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
                    '"value": "livetv"}, {"status": "Fail", "required": "/livetv/check availability", "Name": "c. ' \
                    'screenName", "value": "/livetv/"}, {"status": "Fail", "required": "livetv|upsell|check ' \
                    'availability", "Name": "c. siteHier", "value": "livetv"}, {"status": "Fail", "required": ' \
                    '"cbsicbsapp", "Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", ' \
                    '"required": "/livetv/check availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}], ' \
                    '[{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", "value": "livetv"}, ' \
                    '{"status": "Fail", "required": "/livetv/check availability", "Name": "c. screenName", ' \
                    '"value": "/livetv/"}, {"status": "Fail", "required": "livetv|upsell|check availability", ' \
                    '"Name": "c. siteHier", "value": "livetv"}, {"status": "Fail", "required": "cbsicbsapp", ' \
                    '"Name": "c. sitePrimaryRsid", "value": "cnetcbscomsite"}, {"status": "Fail", "required": ' \
                    '"/livetv/check availability", "Name": "pageName", "value": "CBS 4.8.5 (1648548)"}]]} '
    
    actual = 'set([\'{"status": "Fail", "required": "/livetv/check availability", "Name": "pageName", "value": "CBS ' \
             '4.8.5 (1648548)"}\', \'{"status": "Fail", "required": "livetv|upsell|check availability", "Name": "c. ' \
             'siteHier", "value": "splash"}\', \'{"status": "Fail", "required": "livetv|upsell|check availability", ' \
             '"Name": "c. siteHier", "value": "menu|home"}\', \'{"status": "Fail", "required": "/livetv/check ' \
             'availability", "Name": "c. screenName", "value": "/livetv/"}\', \'{"status": "Fail", "required": ' \
             '"livetv_available", "Name": "c. pageType", "value": "settings"}\', \'{"status": "Fail", "required": ' \
             '"/livetv/check availability", "Name": "pageName", "value": "/accounts/login"}\', \'{"status": "Fail", ' \
             '"required": "livetv|upsell|check availability", "Name": "c. siteHier", "value": "menu|live tv"}\', ' \
             '\'{"status": "Fail", "required": "/livetv/check availability", "Name": "c. screenName", "value": "/all ' \
             'access/upsell"}\', \'{"status": "Fail", "required": "/livetv/check availability", "Name": "pageName", ' \
             '"value": "/settings/"}\', \'{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
             '"value": "menu"}\', \'{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
             '"value": "svod_upsell"}\', \'{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
             '"value": "front_door"}\', \'{"status": "Fail", "required": "livetv_available", "Name": "c. pageType", ' \
             '"value": "livetv_availability"}\', \'{"status": "Fail", "required": "livetv_available", "Name": "c. ' \
             'pageType", "value": "livetv"}\', \'{"status": "Fail", "required": "livetv|upsell|check availability", ' \
             '"Name": "c. siteHier", "value": "all access|upsell"}\', \'{"status": "Fail", "required": "/livetv/check ' \
             'availability", "Name": "pageName", "value": "/livetv/"}\', \'{"status": "Fail", "required": ' \
             '"livetv_available", "Name": "c. pageType", "value": "accounts_login"}\', \'{"status": "Fail", ' \
             '"required": "livetv|upsell|check availability", "Name": "c. siteHier", "value": "menu|"}\', ' \
             '\'{"status": "Fail", "required": "/livetv/check availability", "Name": "c. screenName", ' \
             '"value": "/settings/"}\', \'{"status": "Fail", "required": "/livetv/check availability", "Name": "c. ' \
             'screenName", "value": "/menu/"}\', \'{"status": "Fail", "required": "/livetv/check availability", ' \
             '"Name": "c. screenName", "value": "/accounts/login"}\', \'{"status": "Fail", "required": ' \
             '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "other|other|settings|home"}\', ' \
             '\'{"status": "Fail", "required": "/livetv/check availability", "Name": "pageName", "value": "/"}\', ' \
             '\'{"status": "Fail", "required": "/livetv/check availability", "Name": "c. screenName", ' \
             '"value": "/login"}\', \'{"status": "Fail", "required": "cbsicbsapp", "Name": "c. sitePrimaryRsid", ' \
             '"value": "cnetcbscomsite"}\', \'{"status": "Fail", "required": "/livetv/check availability", ' \
             '"Name": "c. screenName", "value": "/menu/home"}\', \'{"status": "Fail", "required": "/livetv/check ' \
             'availability", "Name": "pageName", "value": "/all access/upsell"}\', \'{"status": "Fail", "required": ' \
             '"/livetv/check availability", "Name": "c. screenName", "value": "/menu/live tv"}\', \'{"status": ' \
             '"Fail", "required": "livetv|upsell|check availability", "Name": "c. siteHier", ' \
             '"value": "other|other|accounts|login"}\', \'{"status": "Fail", "required": "/livetv/check ' \
             'availability", "Name": "c. screenName", "value": "/"}\', \'{"status": "Fail", "required": ' \
             '"livetv|upsell|check availability", "Name": "c. siteHier", "value": "livetv"}\', \'{"status": "Fail", ' \
             '"required": "livetv|upsell|check availability", "Name": "c. siteHier", "value": "home"}\']) '

    def test_parser(self):
        expected = parser.parse_response_to_set(self.mock_response)
        self.assertEquals(self.actual, str(expected))


if __name__ == '__main__':
    unittest.main()
