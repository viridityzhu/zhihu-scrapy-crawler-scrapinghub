# -*- coding: utf-8 -*-
import scrapy
from zhihu_crawl.items import TopicfollowerItem, TopicdiscussionItem, UserfollowerItem, UserfollowingItem, UserinformationItem
import json
from scrapy_redis.spiders import RedisSpider
import re


class ZhihuNoQASpider(RedisSpider):
    # spider values
    name = 'zhihunoqa'
    allowed_domains = ['zhihu.com']
    redis_key = 'zhihu:urls'
    custom_settings = {
        'ITEM_PIPELINES': {
            'zhihu_crawl.pipelines.ZhihuCrawlNoQAPipeline': 300
        }
    }
    # self values
    # 19598929
    # offset = [0, 0, 0, 0, 0, 0, 0]

    # def __init__(self, settings, *args, **kwargs):
    #     super(ZhihuNoQASpider, self).__init__(*args, **kwargs)
    #     print(settings.get('TOPIC'))

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(ZhihuNoQASpider, cls).from_crawler(
    #         crawler, *args, **kwargs)
    #     TOPIC = crawler.settings.getint('TOPIC')
    #     # print('topiccccccccccccccccc:' + str(TOPIC))
    #     spider.topic_id = spider.topics[TOPIC - 1]
    #     return spider

    def stringify(self, theItem):
        return str(theItem) if isinstance(theItem, int) else theItem.encode('utf-8', 'ignore').decode('utf-8')

    def parse(self, response):
        # print('topicccccccccccccccccID:' + self.topic_id)
        # 1: ********************topic follower********************
        if re.match(r'https://www\.zhihu\.com/api/v4/topics/\d+?/followers.+', response.url):
            json_data = json.loads(response.body)['data']
            topicId = response.url.split('/')[6]
            # print('topic id:::::::::::::' + str(topicId))
            # ----------获取话题follower的url以及其他信息---------
            for i in json_data:
                item = TopicfollowerItem()
                for field in item.fields:
                    if field in i.keys():
                        item[field] = self.stringify(i.get(field))
                yield item
            # -------------判断翻页------------------
            # isEnd表明是否已加载到最后一页
            isEnd = json.loads(response.body)['paging']['is_end']
            # 不到最后一页就翻页
            if not isEnd:
                # self.offset[0] += 20
                yield scrapy.Request('https://www.zhihu.com/api/v4/topics/' + topicId + '/followers?include=data%5B*%5D.gender%2Canswer_count%2Carticles_count%2Cfollower_count%2Cis_following%2Cis_followed&limit=20&offset=' + str(int(response.url.split('=')[-1]) + 20), callback=self.parse)
            # else:
            #     self.logger.info('isEnd:' + str(isEnd))
        # 2: ********************topicDiscussion********************
        elif re.match(r'https://www\.zhihu\.com/api/v4/topics/\d+?/feeds/essence.+', response.url):
            json_data = json.loads(response.body)['data']
            topicId = response.url.split('/')[6]
            # print('topic id:::::::::::::' + str(topicId))
            for i in json_data:
                i = dict(i['target'])
                # ----------获取话题discussion的信息---------
                if i.get('type') == 'answer':
                    item = TopicdiscussionItem()
                    for field in item.fields:
                        if field in i.keys():
                            item[field] = self.stringify(i.get(field))
                        elif field == 'answer_id':
                            item[field] = self.stringify(i.get('id'))
                        elif field == 'content':
                            item[field] = i.get('excerpt')
                        else:
                            j = i.get('question')
                            if field == 'question_id':
                                item[field] = self.stringify(j.get('id'))
                            elif field in j.keys():
                                item[field] = j.get(field)
                            else:
                                k = i.get('author')
                                item[field] = k.get(field)
                    yield item
                else:
                    self.logger.info(
                        'type is not answer, it is:' + i.get('type'))
            # -------------判断翻页------------------
            # isEnd表明是否已加载到最后一页
            isEnd = json.loads(response.body)['paging']['is_end']
            # 不到最后一页就翻页
            if not isEnd:
                # self.offset[1] += 20
                yield scrapy.Request('https://www.zhihu.com/api/v4/topics/' + topicId + '/feeds/essence?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&offset='
                                     + str(int(response.url.split('=')[-1]) + 10), callback=self.parse)
            # else:
            #     self.logger.info('isEnd:' + str(isEnd))
        # 3: ********************userFollower********************
        elif re.match(r'https://www\.zhihu\.com/api/v4/members/.+?/followers.+', response.url):
            json_data = json.loads(response.body)['data']
            whose_follower = response.url.split('/')[6]
            # ----------获取话题follower的url以及其他信息---------
            for i in json_data:
                item = UserfollowerItem()
                item['whose_follower'] = whose_follower
                for field in item.fields:
                    if field == 'whose_follower':
                        continue
                    if field in i.keys():
                        item[field] = self.stringify(i.get(field))
                yield item

            # -------------判断翻页------------------
            # isEnd表明是否已加载到最后一页
            isEnd = json.loads(response.body)['paging']['is_end']
            # 不到最后一页就翻页
            if not isEnd:
                # self.offset[2] += 20
                yield scrapy.Request('https://www.zhihu.com/api/v4/members/'
                                     + whose_follower + '/followers?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=' + str(int(response.url.split('=')[-1]) + 10), callback=self.parse)
            # else:
            #     self.logger.info('isEnd:' + str(isEnd))
        # 4: ********************userFollowing********************
        elif re.match(r'https://www\.zhihu\.com/api/v4/members/.+?/followees.+', response.url):
            json_data = json.loads(response.body)['data']
            followed_by_who = response.url.split('/')[6]
            # ----------获取话题follower的url以及其他信息---------
            for i in json_data:
                item = UserfollowingItem()
                item['followed_by_who'] = followed_by_who
                for field in item.fields:
                    if field == 'followed_by_who':
                        continue
                    if field in i.keys():
                        item[field] = self.stringify(i.get(field))
                yield item

            # -------------判断翻页------------------
            # isEnd表明是否已加载到最后一页
            isEnd = json.loads(response.body)['paging']['is_end']
            # 不到最后一页就翻页
            if not isEnd:
                # self.offset[3] += 20
                yield scrapy.Request('https://www.zhihu.com/api/v4/members/'
                                     + followed_by_who + '/followees?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=' + str(int(response.url.split('=')[-1]) + 10), callback=self.parse)
            # else:
            #     self.logger.info('isEnd:' + str(isEnd))
        # 5: ********************userInformation********************
        elif re.match(r'https://www\.zhihu\.com/api/v4/members/.+?\?include=data%5B%2A%5D\.locations.+', response.url):
            json_data = json.loads(response.body)
            # ----------获取话题follower的url以及其他信息---------
            item = UserinformationItem()
            for field in item.fields:
                if field == 'business':
                    try:
                        item[field] = json_data.get('business')['name']
                    except Exception as e:
                        item[field] = ''
                elif field in json_data.keys():
                    item[field] = json_data.get(field)
                elif field == 'location':
                    try:
                        item[field] = json_data.get('locations')[0].get('name')
                    except Exception as e:
                        item['location'] = ''
                elif field == 'job':
                    try:
                        item[field] = json_data.get('employments')[
                            0].get('job').get('name')
                    except Exception as e:
                        item[field] = ''
                        print('not get job')
                        print(e)
                elif field == 'company':
                    try:
                        item[field] = json_data.get('employments')[
                            0].get('company').get('name')
                    except Exception as e:
                        item[field] = ''
                elif field == 'school':
                    try:
                        item[field] = json_data.get('educations')[
                            0].get('school').get('name')
                    except Exception as e:
                        item[field] = ''
                elif field == 'major':
                    try:
                        item[field] = json_data.get('educations')[
                            0].get('major').get('name')
                    except Exception as e:
                        item[field] = ''
            yield item
        else:
            pass
