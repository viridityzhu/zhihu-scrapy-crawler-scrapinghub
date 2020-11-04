# -*- coding: utf-8 -*-
import scrapy
from zhihu_crawl.items import UseranswerItem, TopicfollowerItem, TopicdiscussionItem, UserfollowerItem, UserfollowingItem, UserinformationItem, UserquestionItem, QuestionanswerItem
import json
from scrapy_redis.spiders import RedisSpider
import re


class ZhihuSpider(RedisSpider):
    # spider values
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    redis_key = 'zhihu:urls'
    custom_settings = {
        'ITEM_PIPELINES': {
            'zhihu_crawl.pipelines.ZhihuCrawlPipeline': 300
        }
    }
    # self values
    # topics = ['19873682', '19598929']
    # topic_id = ''
    # offset = [0, 0, 0, 0, 0, 0, 0]

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(ZhihuSpider, cls).from_crawler(
    #         crawler, *args, **kwargs)
    #     TOPIC = crawler.settings.getint('TOPIC')
    #     # print('topiccccccccccccccccc:' + str(TOPIC))
    #     spider.topic_id = spider.topics[TOPIC - 1]
    #     return spider

    def stringify(self, theItem):
        return str(theItem) if isinstance(theItem, int) else theItem.encode('utf-8', 'ignore').decode('utf-8')

    def parse(self, response):

        # 1: ********************topic follower********************
        if re.match(r'https://www\.zhihu\.com/api/v4/topics/\d+?/followers.+', response.url):
            json_data = json.loads(response.body)['data']
            topicId = response.url.split('/')[6]
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
        # 6: ********************userQuestion********************
        elif re.match(r'https://www\.zhihu\.com/api/v4/members/.+?/questions\?.+', response.url):
            json_data = json.loads(response.body)['data']
            # ----------获取user的提问以及其他信息---------
            for i in json_data:
                item = UserquestionItem()
                for field in item.fields:
                    if field == 'url_token':
                        item[field] = response.url.split('/')[6]
                    elif field == 'question_id':
                        item[field] = self.stringify(i.get('id'))
                    elif field == 'topics':
                        topic_list = []
                        for topic_data in i.get('topics'):
                            topic_dict = {}
                            topic_dict['name'] = topic_data.get('name')
                            topic_dict['id'] = topic_data.get('id')
                            topic_list.append(topic_dict)
                        item[field] = str(topic_list)
                    elif field in i.keys():
                        item[field] = self.stringify(i.get(field))
                    else:
                        item[field] = i.get('author').get(field)
                yield item

            # -------------判断翻页------------------
            # isEnd表明是否已加载到最后一页
            isEnd = json.loads(response.body)['paging']['is_end']
            # 不到最后一页就翻页
            if not isEnd:
                # self.offset[4] += 20
                yield scrapy.Request('https://www.zhihu.com/api/v4/members/'
                                     + response.url.split('/')[6] + '/questions?include=data%5B*%5D.created%2Ctopics%2Cdetail%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&limit=20&offset=' + str(int(response.url.split('=')[-1]) + 20), callback=self.parse)
            # else:
            #     self.logger.info('isEnd:' + str(isEnd))
        # 7: ********************userAnswer********************
        elif re.match(r'https://www\.zhihu\.com/api/v4/members/.+?/answers\?.+', response.url):
            json_data = json.loads(response.body)['data']
            # ----------获取user的回答以及其他信息---------
            for i in json_data:
                item = UseranswerItem()
                for field in item.fields:
                    if field == 'answer_id':
                        item[field] = self.stringify(i.get('id'))
                    elif field in i.keys():
                        item[field] = self.stringify(i.get(field))
                    else:
                        j = i.get('question')
                        if field == 'question_id':
                            item[field] = self.stringify(j.get('id'))
                        elif field == 'question_created_time':
                            item[field] = self.stringify(j.get('created'))
                        elif field == 'question_updated_time':
                            item[field] = self.stringify(j.get('updated_time'))
                        elif field == 'topics':
                            topic_list = []
                            for topic_data in j.get('topics'):
                                topic_dict = {}
                                topic_dict['name'] = topic_data.get('name')
                                topic_dict['id'] = topic_data.get('id')
                                topic_list.append(topic_dict)
                            item[field] = str(topic_list)
                        elif field in j.keys():
                            item[field] = j.get(field)
                        else:
                            k = i.get('author')
                            item[field] = k.get(field)
                yield item

            # -------------判断翻页------------------
            # isEnd表明是否已加载到最后一页
            isEnd = json.loads(response.body)['paging']['is_end']
            # 不到最后一页就翻页
            if not isEnd:
                # self.offset[5] += 20
                yield scrapy.Request('https://www.zhihu.com/api/v4/members/'
                                     + response.url.split('/')[6] + '/answers?include=data%5B*%5D.is_normal,admin_closed_comment,reward_info,is_sticky,comment_count,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question.detail,topics,answer_count,follower_count,excerpt,detail,question_type,title,id,created,updated_time,relevant_info,excerpt,label_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized&limit=20&offset=' + str(int(response.url.split('=')[-1]) + 20), callback=self.parse)
            # else:
            #     self.logger.info('isEnd:' + str(isEnd))
        # 8: ********************questionAnswer********************
        elif re.match(r'https://www\.zhihu\.com/api/v4/questions/\d+?/answers\?.+', response.url):
            json_data = json.loads(response.body)['data']
            # ----------获取user的回答以及其他信息---------
            for i in json_data:
                item = QuestionanswerItem()
                for field in item.fields:
                    if field == 'answer_id':
                        item[field] = self.stringify(i.get('id'))
                    elif field in i.keys():
                        item[field] = self.stringify(i.get(field))
                    else:
                        j = i.get('question')
                        if field == 'question_id':
                            item[field] = self.stringify(j.get('id'))
                        elif field == 'topics':
                            topic_list = []
                            for topic_data in j.get('topics'):
                                topic_dict = {}
                                topic_dict['name'] = topic_data.get('name')
                                topic_dict['id'] = topic_data.get('id')
                                topic_list.append(topic_dict)
                            item[field] = str(topic_list)
                        elif field == 'question_created_time':
                            item[field] = self.stringify(j.get('created'))
                        elif field == 'question_updated_time':
                            item[field] = self.stringify(j.get('updated_time'))
                        elif field in j.keys():
                            item[field] = j.get(field)
                        else:
                            k = i.get('author')
                            item[field] = k.get(field)
                yield item

            # -------------判断翻页------------------
            # isEnd表明是否已加载到最后一页
            isEnd = json.loads(response.body)['paging']['is_end']
            # 不到最后一页就翻页
            if not isEnd:
                # self.offset[6] += 20
                yield scrapy.Request('https://www.zhihu.com/api/v4/questions/' + response.url.split('/')[6] + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion.topics%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&platform=desktop&sort_by=default&offset=' + str(int(response.url.split('=')[-1]) + 5), callback=self.parse)
            # else:
            #     self.logger.info('isEnd:' + str(isEnd))
