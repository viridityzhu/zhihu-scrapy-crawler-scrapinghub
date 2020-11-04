# -*- coding: utf-8 -*-
import pymysql
import logging
import redis
from zhihu_crawl.items import UseranswerItem, TopicfollowerItem, TopicdiscussionItem, UserfollowerItem, UserfollowingItem, UserinformationItem, UserquestionItem, QuestionanswerItem
from zhihu_crawl.settings import DATABASE_HOST, DATABASE_USER, DATABASE_PASS, REDIS_HOST, REDIS_PARAMS, REDIS_PORT


class ZhihuCrawlPipeline(object):
    # the final pipeline

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        DATABASE_NAME = settings.get('DATABASE_NAME')
        return cls(DATABASE_NAME)

    def __init__(self, DATABASE_NAME):
        # 连接redis
        self.r = redis.StrictRedis(
            host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PARAMS['password'])
        # 连接MySQL数据库
        self.conn = pymysql.connect(
            host=DATABASE_HOST,  # 远程登录主机的ip地址
            port=10041,  # mysql服务器的端口
            user=DATABASE_USER,  # mysql的用户
            passwd=DATABASE_PASS,  # 密码
            db=DATABASE_NAME,  # 需要的数据库名称
            use_unicode=True, charset="utf8"
        )
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, TopicfollowerItem):
            try:
                self.curr.execute("""insert into topicfollower values(%s,%s,%s,%s,%s,%s,%s)""", (
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['articles_count'],
                    item['follower_count'],
                    item['gender']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followers?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followees?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/questions?include=data%5B*%5D.created%2Ctopics%2Cdetail%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/answers?include=data%5B*%5D.is_normal,admin_closed_comment,reward_info,is_sticky,comment_count,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question.detail,topics,answer_count,follower_count,excerpt,detail,question_type,title,id,created,updated_time,relevant_info,excerpt,label_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, TopicdiscussionItem):
            try:
                self.curr.execute("""insert into topicdiscussion values(%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['answer_id'],
                    item['content'],
                    item['voteup_count'],
                    item['comment_count'],
                    item['question_id'],
                    item['title'],
                    item['url_token'],
                    item['name'],
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followers?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followees?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/questions?include=data%5B*%5D.created%2Ctopics%2Cdetail%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/answers?include=data%5B*%5D.is_normal,admin_closed_comment,reward_info,is_sticky,comment_count,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question.detail,topics,answer_count,follower_count,excerpt,detail,question_type,title,id,created,updated_time,relevant_info,excerpt,label_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, UserfollowerItem):
            try:
                self.curr.execute("""insert into userfollower values(%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['whose_follower'],
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['articles_count'],
                    item['follower_count'],
                    item['gender']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/questions?include=data%5B*%5D.created%2Ctopics%2Cdetail%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/answers?include=data%5B*%5D.is_normal,admin_closed_comment,reward_info,is_sticky,comment_count,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question.detail,topics,answer_count,follower_count,excerpt,detail,question_type,title,id,created,updated_time,relevant_info,excerpt,label_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, UserfollowingItem):
            try:
                self.curr.execute("""insert into userfollowing values(%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['followed_by_who'],
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['articles_count'],
                    item['follower_count'],
                    item['gender']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/questions?include=data%5B*%5D.created%2Ctopics%2Cdetail%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/answers?include=data%5B*%5D.is_normal,admin_closed_comment,reward_info,is_sticky,comment_count,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question.detail,topics,answer_count,follower_count,excerpt,detail,question_type,title,id,created,updated_time,relevant_info,excerpt,label_info,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized&limit=20&offset=0')
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, UserinformationItem):
            try:
                self.curr.execute("""insert into userinformation values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['question_count'],
                    item['commercial_question_count'],
                    item['articles_count'],
                    item['columns_count'],
                    item['follower_count'],
                    item['following_count'],
                    item['favorite_count'],
                    item['favorited_count'],
                    item['pins_count'],
                    item['logs_count'],
                    item['voteup_count'],
                    item['thanked_count'],
                    item['hosted_live_count'],
                    item['participated_live_count'],
                    item['following_columns_count'],
                    item['following_topic_count'],
                    item['following_question_count'],
                    item['following_favlists_count'],
                    item['gender'],
                    item['description'],
                    item['is_active'],
                    item['is_advertiser'],
                    item['allow_message'],
                    item['business'],
                    item['location'],
                    item['job'],
                    item['company'],
                    item['school'],
                    item['major']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, UserquestionItem):
            try:
                self.curr.execute("""insert into userquestion values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['title'],
                    item['question_id'],
                    item['detail'],
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['gender'],
                    item['answer_count'],
                    item['url'],
                    item['follower_count'],
                    item['created'],
                    item['updated_time'],
                    item['topics']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/questions/' + item['question_id'] + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion.topics%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&platform=desktop&sort_by=default&offset=0')
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, UseranswerItem):
            try:
                self.curr.execute("""insert into useranswer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['answer_id'],
                    item['content'],
                    item['voteup_count'],
                    item['comment_count'],
                    item['is_copyable'],
                    item['question_id'],
                    item['title'],
                    item['detail'],
                    item['answer_count'],
                    item['follower_count'],
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['gender'],
                    item['created_time'],
                    item['updated_time'],
                    item['question_created_time'],
                    item['question_updated_time'],
                    item['topics']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, QuestionanswerItem):
            try:
                self.curr.execute("""insert into questionanswer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['answer_id'],
                    item['content'],
                    item['voteup_count'],
                    item['comment_count'],
                    item['is_copyable'],
                    item['question_id'],
                    item['title'],
                    item['detail'],
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['gender'],
                    item['created_time'],
                    item['updated_time'],
                    item['question_created_time'],
                    item['question_updated_time'],
                    item['topics']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            return item


class ZhihuCrawlNoQAPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        DATABASE_NAME = settings.get('DATABASE_NAME')
        return cls(DATABASE_NAME)

    def __init__(self, DATABASE_NAME):
        # 连接redis
        self.r = redis.StrictRedis(
            host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PARAMS['password'])
        # 连接MySQL数据库
        self.conn = pymysql.connect(
            host=DATABASE_HOST,  # 远程登录主机的ip地址
            port=10041,  # mysql服务器的端口
            user=DATABASE_USER,  # mysql的用户
            passwd=DATABASE_PASS,  # 密码
            db=DATABASE_NAME,  # 需要的数据库名称
            use_unicode=True, charset="utf8"
        )
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, TopicfollowerItem):
            try:
                self.curr.execute("""insert into topicfollower values(%s,%s,%s,%s,%s,%s,%s)""", (
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['articles_count'],
                    item['follower_count'],
                    item['gender']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followers?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followees?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            return item
        elif isinstance(item, TopicdiscussionItem):
            try:
                self.curr.execute("""insert into topicdiscussion values(%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['answer_id'],
                    item['content'],
                    item['voteup_count'],
                    item['comment_count'],
                    item['question_id'],
                    item['title'],
                    item['url_token'],
                    item['name'],
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followers?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/'
                             + item['url_token'] + '/followees?include=data%5B%2A%5D.follower_count%2Canswer_count%2Carticles_count&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)

            return item
        elif isinstance(item, UserfollowerItem):
            try:
                self.curr.execute("""insert into userfollower values(%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['whose_follower'],
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['articles_count'],
                    item['follower_count'],
                    item['gender']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)

            return item
        elif isinstance(item, UserfollowingItem):
            try:
                self.curr.execute("""insert into userfollowing values(%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['followed_by_who'],
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['articles_count'],
                    item['follower_count'],
                    item['gender']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            # push new urls into redis
            try:
                self.r.lpush('zhihu:urls', 'https://www.zhihu.com/api/v4/members/' + item['url_token'] +
                             '?include=data%5B%2A%5D.locations,employments,gender,educations,business,voteup_count,thanked_count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,is_active,sina_weibo_url,sina_weibo_name,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics&limit=10&offset=0')
            except Exception as e:
                logging.warning(e)

            return item
        elif isinstance(item, UserinformationItem):
            try:
                self.curr.execute("""insert into userinformation values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    item['url_token'],
                    item['name'],
                    item['headline'],
                    item['answer_count'],
                    item['question_count'],
                    item['commercial_question_count'],
                    item['articles_count'],
                    item['columns_count'],
                    item['follower_count'],
                    item['following_count'],
                    item['favorite_count'],
                    item['favorited_count'],
                    item['pins_count'],
                    item['logs_count'],
                    item['voteup_count'],
                    item['thanked_count'],
                    item['hosted_live_count'],
                    item['participated_live_count'],
                    item['following_columns_count'],
                    item['following_topic_count'],
                    item['following_question_count'],
                    item['following_favlists_count'],
                    item['gender'],
                    item['description'],
                    item['is_active'],
                    item['is_advertiser'],
                    item['allow_message'],
                    item['business'],
                    item['location'],
                    item['job'],
                    item['company'],
                    item['school'],
                    item['major']
                ))
                self.conn.commit()
            except Exception as e:
                logging.warning(e)
            return item
