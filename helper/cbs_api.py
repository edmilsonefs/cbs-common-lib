from xml.etree import ElementTree
import re, time, os
import urllib2

class CBSAPI(object):
    server = ''
    base_url = ''
    request_url = ''
    headers = {}

    ###################################################################################################################
    ###################################################################################################################
    # If you want to rerun a test that failed on BitBar then copy the xml OR the dict from the logging
    # (the test steps in the bitbar UI) and past it here.  To get around issues that you might get from that
    # copy/paste, be sure to paste as shown in examples below.
    # Note: api_xml is a STRING and show_dict_array is an ARRAY of DICTS.
    #
    # api_xml = """<?xml version='1.0' encoding='UTF-8'?>....</rss>"""
    # show_dict_array = [{'air_date': '9/25/16', ... 'show_title': 'NCIS: Los Angeles'}]
    ###################################################################################################################
    ###################################################################################################################
    api_xml = """"""
    show_dict_array = []
    ###################################################################################################################
    ###################################################################################################################

    def login(self):
        pass

    def logout(self):
        try:
            # Put logout code here. surround in try/except so that a failed API logout does not invalidate our test
            pass
        except Exception:
            pass

    def get(self, url):
        # base_url set at top.  We split out base_url and url in expectation of future API endpoints on the same server
        request_url = self.base_url + url

        request = urllib2.Request(request_url, headers=self.headers)
        return urllib2.urlopen(request).read()

    def get_xml_from_api(self):
        if not self.api_xml:
            request_url = self.get_request_url()
            self.api_xml = self.get(url=request_url)

        return self.api_xml

    def get_request_url(self):
        if not self.request_url:
            # CBS publishes episodes each day at 2pm and 11pm Pacific Standard Time, so we
            #   offset GMT (also known as UTC) -> PST
            # We do this so we can tell what day it is in PST.  For example, if we execute this script at 11pm PST,
            # in GMT it will already be the next day, and testDroid servers run on GMT (Greenwich Mean Time)

            # testDroid servers run on GMT (also known as UTC) so we temporarily change to Pacific time to see if
            #   daylight savings is active.  tm_isdst == 1 when daylight savings time is active
            #   when daylight savings time is active, GMT -> PST is 7 hours, when NOT active, it is 8 hours.
            os.environ['TZ'] = 'US/Pacific'
            dst = time.localtime().tm_isdst
            os.environ['TZ'] = 'GMT'
            offset = (8 - dst) * 3600   # offset GMT -> PST
            offset += 24 * 3600         # offset by 1 day.  We'll pull from "this time yesterday"
            struct_time = time.localtime(time.mktime(time.localtime()) - offset)

            # format: "2016-12-30"
            year = struct_time.tm_year
            mon = str.rjust(str(struct_time.tm_mon), 2, '0')
            day = str.rjust(str(struct_time.tm_mday), 2, '0')
            hour = str.rjust(str(struct_time.tm_hour), 2, '0')
            # format: "QA-Automation?byPubDate=2016-10-13T15:00:00Z~"
            self.request_url = "QA-Automation?byPubDate=%s-%s-%sT%s:00:00Z~" % (year, mon, day, hour)

        return self.request_url

    def get_daily_shows(self):
        """
        :return: an array of dicts of shows we should see of the form
        show_category
        show_title
        episode_title
        air_date
        season
        episode
        mid_roll      # in seconds, where the first mid-roll ad should fire
        """

        if not self.show_dict_array:
            # If we use the requests package, we have to encode due to possible Spanish characters
            # response = self.get_xml_from_api().text.encode('utf-8')
            response = self.get_xml_from_api()

            node_root = ElementTree.fromstring(response)
            node_channel = list(node_root)[0]
            node_items = list(node_channel)

            # only keep nodes we care about
            node_items = filter(lambda(x): x.tag == 'item', node_items)

            self.show_dict_array = []
            test_count = 0
            for node_item in node_items:
                test_count += 1
                if test_count > 20:
                    break
                show_dict = {}

                # node_item.find('title').text looks like:
                # 'The Late Late Show - 8/4/2016 (Hugh Grant, Bryce Dallas Howard, Local Natives)'
                # We just want:
                # 'The Late Late Show'
                # so we'll use SeriesTitle

                show_dict['show_title'] = node_item.find('{http://xml.cbs.com/field}SeriesTitle').text

                # exception for news shows: get episode_title from <title> instead of <label>
                if show_dict['show_title'] in ['CBS Evening News', '60 Minutes', '48 Hours']:
                    show_dict['episode_title'] = node_item.find('title').text
                else:
                    # title can look like a few things:
                    #   'The Young and The Restless - 8/3/2016'
                    #   We just want:
                    #   '8/3/2016'
                    temp_ep_title = node_item.find('{http://xml.cbs.com/field}Label').text
                    if '(SAP) - ' in temp_ep_title:
                        temp_ep_title = temp_ep_title[len('(SAP) - '):]
                    show_dict['episode_title'] = temp_ep_title

                # PrimaryCategoryName looks like:
                #   'Late Night/Late Late Show/Full Episodes'
                #   But we just want:
                #   'Late Night'
                # For the following
                #   'Specials', 'Primetime', and 'Primetime Episodes'
                #   We want:
                #   'Primetime Episodes'
                cat = node_item.find('{http://xml.cbs.com/field}PrimaryCategoryName').text
                try:
                    show_dict['show_category'] = cat[0:cat.index('/')]
                except ValueError:
                    # some bad shows have no '/' so just take the whole thing
                    show_dict['show_category'] = cat

                if show_dict['show_category'] in ['Specials', 'Primetime']:
                    show_dict['show_category'] = 'Primetime Episodes'

                if show_dict['show_category'] in ['Daytime']:
                    show_dict['show_category'] = 'Daytime Episodes'

                # pubDate looks like:
                # 'Thu, 04 Aug 2016 22:30:00 GMT'
                # We just want:
                # '8/4/2016'
                air_date = node_item.find('pubDate').text
                struct_time = time.strptime(air_date, "%a, %d %b %Y %H:%M:%S %Z")

                # The app is based on Eastern Standard Time, so we need to offset GMT (also known as UTC) -> EST
                # testDroid servers run on GMT so we temporarily change to Pacific time to see if
                #   daylight savings is active.  tm_isdst == 1 when daylight savings time is active
                #   when daylight savings time is active, GMT -> PST is 4 hours, when NOT active, it is 5 hours.
                os.environ['TZ'] = 'US/Eastern'
                dst = time.localtime().tm_isdst
                os.environ['TZ'] = 'GMT'
                offset = (5 - dst) * 3600
                struct_time = time.localtime(time.mktime(struct_time) - offset)

                year = time.strftime("%y", struct_time)
                month = time.strftime("%m", struct_time).lstrip('0')
                day = time.strftime("%d", struct_time).lstrip('0')
                show_dict['air_date'] = "%s/%s/%s" % (month, day, year)

                # There are several chapters, with start times (in seconds).  We want to go just past the first mid-roll,
                # so we'll get the start time of the second chapter and add a couple minutes just to be safe
                # This will be an int, not string
                chapters = node_item.findall('{http://xml.theplatform.com/media/data/Media}chapter')
                if chapters:
                    chapter_2_items = chapters[1].items()
                    for item in chapter_2_items:
                        if item[0] == 'startTime':
                            start_time = item[1]
                            show_dict['mid_roll'] = int(start_time) + 120
                            break
                else:
                    # If mid_roll > total video length, we'll just skip to 90% of the total video length
                    show_dict['mid_roll'] = 99999

                # EpisodeNumber and SeasonNumber are good
                # Both are strings
                if node_item.find('{http://xml.cbs.com/field}EpisodeNumber') is not None:
                    show_dict['episode_number'] = node_item.find('{http://xml.cbs.com/field}EpisodeNumber').text
                else:
                    show_dict['episode_number'] = None

                if node_item.find('{http://xml.cbs.com/field}SeasonNumber') is not None:
                    show_dict['season_number'] = node_item.find('{http://xml.cbs.com/field}SeasonNumber').text
                else:
                    show_dict['season_number'] = None

                self.show_dict_array.append(show_dict)

            # hack - filter out some shows
            filter_list = ['The Bold and the Beautiful (En Espanol)', 'Face The Nation', 'CBS Fall Preview 2016',
                           'Sunday Morning', 'CBSN', 'CBS Evening News']
            self.show_dict_array = filter(lambda x: x['show_title'] not in filter_list, self.show_dict_array)

        return self.show_dict_array

